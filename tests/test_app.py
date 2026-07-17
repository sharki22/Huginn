from unittest.mock import MagicMock

from PIL import Image

from huginn.app import _icon_image, HuginnApp


class TestIconImage:
    def test_returns_rgba_image(self):
        img = _icon_image()
        assert img.mode == "RGBA"
        assert img.size == (64, 64)

    def test_active_icon_is_red(self):
        img = _icon_image(active=True)
        pixels = img.load()
        center = pixels[32, 32]
        assert center[0] > 200
        assert center[1] < 100
        assert center[2] < 100

    def test_inactive_icon_is_gray(self):
        img = _icon_image(active=False)
        pixels = img.load()
        center = pixels[32, 32]
        assert 80 < center[0] < 120
        assert 80 < center[1] < 120
        assert 80 < center[2] < 120

    def test_both_icons_are_different(self):
        img_a = _icon_image(active=True)
        img_b = _icon_image(active=False)
        px_a = img_a.load()
        px_b = img_b.load()
        assert px_a[32, 32] != px_b[32, 32]

    def test_default_is_inactive(self):
        img = _icon_image()
        pixels = img.load()
        center = pixels[32, 32]
        assert 80 < center[0] < 120


class TestHuginnApp:
    def test_init_creates_components(self):
        app = HuginnApp()
        assert app._monitoring is True
        assert app._stop is not None
        assert app._hosts is not None
        assert app._monitor is not None

    def test_menu_structure(self):
        app = HuginnApp()
        menu = app._menu()
        items = list(menu)
        assert len(items) >= 5

    def test_toggle_changes_state(self):
        app = HuginnApp()
        assert app._monitoring is True
        mock_icon = MagicMock()
        app._toggle(mock_icon, None)
        assert app._monitoring is False
        mock_icon.icon = _icon_image(active=False)
        app._toggle(mock_icon, None)
        assert app._monitoring is True
