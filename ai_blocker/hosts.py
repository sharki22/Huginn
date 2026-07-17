import logging

from ai_blocker.config import AI_DOMAINS, HOSTS_MARKER, HOSTS_PATH

logger = logging.getLogger(__name__)


class HostsBlocker:
    def __init__(self) -> None:
        self.blocked_count: int = 0

    def _read(self) -> str:
        try:
            return HOSTS_PATH.read_text()
        except PermissionError:
            logger.error("No permission to read /etc/hosts. Run with sudo.")
            return ""
        except FileNotFoundError:
            return ""

    def _write(self, content: str) -> None:
        try:
            HOSTS_PATH.write_text(content)
        except PermissionError:
            logger.error("No permission to write /etc/hosts. Run with sudo.")

    def _build_block(self) -> str:
        lines = "\n".join(f"127.0.0.1 {d}" for d in AI_DOMAINS)
        return f"{HOSTS_MARKER}\n{lines}\n{HOSTS_MARKER}\n"

    def block(self) -> int:
        content = self._read()
        if not content:
            return 0

        block = self._build_block()

        if HOSTS_MARKER in content:
            start = content.index(HOSTS_MARKER)
            second = content.index(HOSTS_MARKER, start + 1)
            end = content.index("\n", second) + 1
            content = content[:start] + block + content[end:]
        else:
            content = content.rstrip("\n") + "\n" + block

        self._write(content)
        self.blocked_count = len(AI_DOMAINS)
        logger.info("Blocked %d AI domains", self.blocked_count)
        return self.blocked_count

    def unblock(self) -> bool:
        content = self._read()
        if HOSTS_MARKER not in content:
            return False

        result, skip = [], False
        for line in content.splitlines(keepends=True):
            if HOSTS_MARKER in line:
                skip = not skip
                continue
            if not skip:
                result.append(line)

        self._write("".join(result))
        self.blocked_count = 0
        logger.info("Hosts unblocked")
        return True
