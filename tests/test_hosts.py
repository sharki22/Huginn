import pytest

from ai_blocker.hosts import HostsBlocker
from ai_blocker.config import AI_DOMAINS, HOSTS_MARKER


@pytest.fixture
def hosts_file(tmp_path):
    return tmp_path / "hosts"


@pytest.fixture
def blocker(hosts_file, monkeypatch):
    hosts_file.write_text("127.0.0.1 localhost\n")
    monkeypatch.setattr("ai_blocker.hosts.HOSTS_PATH", hosts_file)
    return HostsBlocker()


@pytest.fixture
def blocker_with_block(hosts_file, monkeypatch):
    block = f"{HOSTS_MARKER}\n127.0.0.1 chatgpt.com\n{HOSTS_MARKER}\n"
    hosts_file.write_text(f"127.0.0.1 localhost\n{block}")
    monkeypatch.setattr("ai_blocker.hosts.HOSTS_PATH", hosts_file)
    return HostsBlocker()


class TestBuildBlock:
    def test_contains_marker(self, blocker):
        block = blocker._build_block()
        assert HOSTS_MARKER in block

    def test_contains_all_domains(self, blocker):
        block = blocker._build_block()
        for domain in AI_DOMAINS:
            assert f"127.0.0.1 {domain}" in block

    def test_marker_wraps_content(self, blocker):
        block = blocker._build_block()
        lines = block.strip().split("\n")
        assert lines[0] == HOSTS_MARKER
        assert lines[-1] == HOSTS_MARKER


class TestBlock:
    def test_returns_count(self, blocker):
        count = blocker.block()
        assert count == len(AI_DOMAINS)

    def test_writes_to_hosts(self, blocker, hosts_file):
        blocker.block()
        content = hosts_file.read_text()
        assert HOSTS_MARKER in content

    def test_preserves_existing_content(self, blocker, hosts_file):
        blocker.block()
        content = hosts_file.read_text()
        assert "127.0.0.1 localhost" in content

    def test_idempotent(self, blocker, hosts_file):
        blocker.block()
        blocker.block()
        content = hosts_file.read_text()
        assert content.count(HOSTS_MARKER) == 2

    def test_empty_hosts_returns_zero(self, tmp_path, monkeypatch):
        hosts_file = tmp_path / "hosts"
        hosts_file.write_text("")
        monkeypatch.setattr("ai_blocker.hosts.HOSTS_PATH", hosts_file)
        b = HostsBlocker()
        assert b.block() == 0


class TestUnblock:
    def test_removes_block(self, blocker_with_block, hosts_file):
        assert blocker_with_block.unblock() is True
        assert HOSTS_MARKER not in hosts_file.read_text()

    def test_preserves_other_content(self, blocker_with_block, hosts_file):
        blocker_with_block.unblock()
        content = hosts_file.read_text()
        assert "127.0.0.1 localhost" in content

    def test_returns_false_when_no_block(self, blocker):
        assert blocker.unblock() is False

    def test_resets_count(self, blocker_with_block):
        blocker_with_block.unblock()
        assert blocker_with_block.blocked_count == 0


class TestReadPermissionError:
    def test_read_returns_empty(self, tmp_path, monkeypatch):
        hosts_file = tmp_path / "hosts"
        monkeypatch.setattr("ai_blocker.hosts.HOSTS_PATH", hosts_file)

        original_read_text = type(hosts_file).read_text

        def fail_read(self):
            raise PermissionError()

        monkeypatch.setattr(type(hosts_file), "read_text", fail_read)
        b = HostsBlocker()
        assert b._read() == ""
