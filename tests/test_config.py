from pathlib import Path

from ai_blocker.config import (
    AI_DOMAINS,
    AI_PROCESS_CMDLINE,
    AI_PROCESS_NAMES,
    HOSTS_MARKER,
    HOSTS_PATH,
    MONITOR_INTERVAL,
)


class TestHostsConfig:
    def test_hosts_path_is_etc(self):
        assert HOSTS_PATH == Path("/etc/hosts")

    def test_marker_format(self):
        assert HOSTS_MARKER.startswith("# ===")
        assert HOSTS_MARKER.endswith("===")

    def test_interval_is_positive(self):
        assert MONITOR_INTERVAL > 0


class TestDomains:
    def test_no_duplicates(self):
        assert len(AI_DOMAINS) == len(set(AI_DOMAINS))

    def test_all_are_strings(self):
        assert all(isinstance(d, str) for d in AI_DOMAINS)

    def test_all_have_dots(self):
        assert all("." in d for d in AI_DOMAINS)

    def test_known_domains_present(self):
        assert "chatgpt.com" in AI_DOMAINS
        assert "claude.ai" in AI_DOMAINS
        assert "gemini.google.com" in AI_DOMAINS
        assert "deepseek.com" in AI_DOMAINS

    def test_is_tuple(self):
        assert type(AI_DOMAINS) is tuple


class TestProcessNames:
    def test_no_duplicates(self):
        assert len(AI_PROCESS_NAMES) == len(set(AI_PROCESS_NAMES))

    def test_all_are_strings(self):
        assert all(isinstance(p, str) for p in AI_PROCESS_NAMES)

    def test_known_processes_present(self):
        assert "ollama" in AI_PROCESS_NAMES
        assert "llama.cpp" in AI_PROCESS_NAMES
        assert "comfyui" in AI_PROCESS_NAMES
        assert "lmstudio" in AI_PROCESS_NAMES

    def test_is_tuple(self):
        assert type(AI_PROCESS_NAMES) is tuple


class TestProcessCmdline:
    def test_no_duplicates(self):
        assert len(AI_PROCESS_CMDLINE) == len(set(AI_PROCESS_CMDLINE))

    def test_all_are_strings(self):
        assert all(isinstance(p, str) for p in AI_PROCESS_CMDLINE)

    def test_is_tuple(self):
        assert type(AI_PROCESS_CMDLINE) is tuple

    def test_overlaps_with_names_are_intentional(self):
        common = set(AI_PROCESS_CMDLINE) & set(AI_PROCESS_NAMES)
        assert len(common) > 0


class TestConsistency:
    def test_domains_count(self):
        assert len(AI_DOMAINS) >= 40

    def test_process_names_count(self):
        assert len(AI_PROCESS_NAMES) >= 25

    def test_process_cmdline_count(self):
        assert len(AI_PROCESS_CMDLINE) >= 10
