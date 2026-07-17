import logging
import subprocess
from dataclasses import dataclass

import psutil

from huginn.config import AI_PROCESS_CMDLINE, AI_PROCESS_NAMES

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class KilledProcess:
    name: str
    pid: int
    cmdline: str


class ProcessMonitor:
    def __init__(self) -> None:
        self.total_killed: int = 0

    def _get_proc_info(self, proc: psutil.Process) -> tuple[str, str] | None:
        try:
            return proc.name().lower(), " ".join(proc.cmdline()).lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def _is_ai_process(self, name: str, cmdline: str) -> bool:
        return any(p in name for p in AI_PROCESS_NAMES) or any(
            p in cmdline for p in AI_PROCESS_CMDLINE
        )

    def scan_and_kill(self) -> list[KilledProcess]:
        killed: list[KilledProcess] = []

        for proc in psutil.process_iter():
            info = self._get_proc_info(proc)
            if info is None:
                continue

            name, cmdline = info
            if not self._is_ai_process(name, cmdline):
                continue

            try:
                display_name = proc.name()
                pid = proc.pid
                display_cmdline = " ".join(proc.cmdline())

                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except psutil.TimeoutExpired:
                    proc.kill()

                self.total_killed += 1
                killed.append(KilledProcess(display_name, pid, display_cmdline))
                logger.warning("Killed AI process: %s (PID %d)", display_name, pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.error("Failed to kill process: %s", e)

        return killed

    @staticmethod
    def notify(processes: list[KilledProcess]) -> None:
        if not processes:
            return

        names = ", ".join(f"{p.name} (PID {p.pid})" for p in processes)
        try:
            subprocess.run(
                ["notify-send", "-u", "critical", "Huginn", f"Blocked: {names}"],
                timeout=5,
                check=False,
            )
        except FileNotFoundError:
            logger.warning("notify-send not found")
        except Exception as e:
            logger.error("Notification failed: %s", e)
