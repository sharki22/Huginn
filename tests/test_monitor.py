from unittest.mock import MagicMock, patch

import psutil

from huginn.monitor import KilledProcess, ProcessMonitor
from huginn.config import AI_PROCESS_NAMES, AI_PROCESS_CMDLINE


class TestKilledProcess:
    def test_is_frozen(self):
        p = KilledProcess("ollama", 123, "ollama serve")
        assert p.name == "ollama"
        assert p.pid == 123
        assert p.cmdline == "ollama serve"

    def test_is_immutable(self):
        p = KilledProcess("ollama", 123, "ollama serve")
        try:
            p.name = "other"
            assert False, "Should be frozen"
        except AttributeError:
            pass


class TestIsAiProcess:
    def setup_method(self):
        self.monitor = ProcessMonitor()

    def test_matches_by_name(self):
        for name in AI_PROCESS_NAMES:
            assert self.monitor._is_ai_process(name, "") is True

    def test_matches_by_cmdline(self):
        for cmd in AI_PROCESS_CMDLINE:
            assert self.monitor._is_ai_process("python3", cmd) is True

    def test_no_match(self):
        assert self.monitor._is_ai_process("bash", "bash -l") is False
        assert self.monitor._is_ai_process("firefox", "firefox --new-window") is False

    def test_partial_name_match(self):
        assert self.monitor._is_ai_process("my-ollama-server", "") is True
        assert self.monitor._is_ai_process("comfyui-launcher", "") is True


class TestGetProcInfo:
    def setup_method(self):
        self.monitor = ProcessMonitor()

    def test_returns_name_and_cmdline(self):
        proc = MagicMock()
        proc.name.return_value = "python3"
        proc.cmdline.return_value = ["python3", "test.py"]
        result = self.monitor._get_proc_info(proc)
        assert result == ("python3", "python3 test.py")

    def test_returns_none_on_nosuchprocess(self):
        proc = MagicMock()
        proc.name.side_effect = psutil.NoSuchProcess(1)
        assert self.monitor._get_proc_info(proc) is None

    def test_returns_none_on_access_denied(self):
        proc = MagicMock()
        proc.name.side_effect = psutil.AccessDenied(1)
        assert self.monitor._get_proc_info(proc) is None

    def test_lowercases_output(self):
        proc = MagicMock()
        proc.name.return_value = "OLLAMA"
        proc.cmdline.return_value = ["OLLAMA", "SERVE"]
        result = self.monitor._get_proc_info(proc)
        assert result == ("ollama", "ollama serve")


class TestScanAndKill:
    def setup_method(self):
        self.monitor = ProcessMonitor()

    @patch("huginn.monitor.psutil.process_iter")
    def test_kills_ai_process(self, mock_iter):
        proc = MagicMock()
        proc.name.return_value = "ollama"
        proc.pid = 1234
        proc.cmdline.return_value = ["ollama", "serve"]
        mock_iter.return_value = [proc]

        killed = self.monitor.scan_and_kill()
        assert len(killed) == 1
        assert killed[0].name == "ollama"
        assert killed[0].pid == 1234
        proc.terminate.assert_called_once()

    @patch("huginn.monitor.psutil.process_iter")
    def test_skips_non_ai_process(self, mock_iter):
        proc = MagicMock()
        proc.name.return_value = "firefox"
        proc.pid = 5678
        proc.cmdline.return_value = ["firefox"]
        mock_iter.return_value = [proc]

        killed = self.monitor.scan_and_kill()
        assert len(killed) == 0
        proc.terminate.assert_not_called()

    @patch("huginn.monitor.psutil.process_iter")
    def test_increments_total_killed(self, mock_iter):
        proc = MagicMock()
        proc.name.return_value = "llama.cpp"
        proc.pid = 100
        proc.cmdline.return_value = ["llama.cpp"]
        mock_iter.return_value = [proc]

        self.monitor.scan_and_kill()
        assert self.monitor.total_killed == 1

    @patch("huginn.monitor.psutil.process_iter")
    def test_calls_kill_on_timeout(self, mock_iter):
        proc = MagicMock()
        proc.name.return_value = "comfyui"
        proc.pid = 200
        proc.cmdline.return_value = ["comfyui"]
        proc.wait.side_effect = psutil.TimeoutExpired(3)
        mock_iter.return_value = [proc]

        self.monitor.scan_and_kill()
        proc.kill.assert_called_once()

    @patch("huginn.monitor.psutil.process_iter")
    def test_handles_nosuchprocess_during_kill(self, mock_iter):
        proc = MagicMock()
        proc.name.return_value = "ollama"
        proc.pid = 300
        proc.cmdline.return_value = ["ollama"]
        proc.terminate.side_effect = psutil.NoSuchProcess(300)
        mock_iter.return_value = [proc]

        killed = self.monitor.scan_and_kill()
        assert len(killed) == 0


class TestNotify:
    @patch("huginn.monitor.subprocess.run")
    def test_sends_notification(self, mock_run):
        processes = [KilledProcess("ollama", 123, "ollama serve")]
        ProcessMonitor.notify(processes)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "notify-send" in args
        assert "ollama" in args[-1]

    @patch("huginn.monitor.subprocess.run")
    def test_empty_list_does_nothing(self, mock_run):
        ProcessMonitor.notify([])
        mock_run.assert_not_called()

    @patch("huginn.monitor.subprocess.run", side_effect=FileNotFoundError)
    def test_handles_missing_notify_send(self, _):
        processes = [KilledProcess("ollama", 123, "ollama serve")]
        ProcessMonitor.notify(processes)
