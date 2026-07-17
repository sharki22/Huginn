import logging
import threading

import pystray
from PIL import Image, ImageDraw

from huginn.config import MONITOR_INTERVAL
from huginn.hosts import HostsBlocker
from huginn.monitor import ProcessMonitor

logger = logging.getLogger(__name__)


def _icon_image(active: bool = False) -> Image.Image:
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = (220, 50, 50, 255) if active else (100, 100, 100, 255)
    draw.rounded_rectangle([4, 4, 60, 60], radius=8, fill=fill)
    draw.text((14, 12), "HI", fill="white")
    draw.text((12, 34), "OFF" if active else "ON", fill="white")
    return img


class HuginnApp:
    def __init__(self) -> None:
        self._hosts = HostsBlocker()
        self._monitor = ProcessMonitor()
        self._monitoring = True
        self._stop = threading.Event()
        self._icon: pystray.Icon | None = None

    def _loop(self) -> None:
        while not self._stop.is_set():
            if self._monitoring:
                killed = self._monitor.scan_and_kill()
                if killed:
                    self._monitor.notify(killed)
                    if self._icon:
                        self._icon.update_menu()
            self._stop.wait(MONITOR_INTERVAL)

    def _toggle(self, icon: pystray.Icon, _: object) -> None:
        self._monitoring = not self._monitoring
        logger.info("Monitoring %s", "enabled" if self._monitoring else "disabled")
        icon.icon = _icon_image(active=self._monitor.total_killed > 0)

    def _reblock(self, _: pystray.Icon, __: object) -> None:
        self._hosts.unblock()
        logger.info("Reblocked %d domains", self._hosts.block())

    def _unblock(self, _: pystray.Icon, __: object) -> None:
        self._hosts.unblock()

    def _quit(self, icon: pystray.Icon, _: object) -> None:
        self._stop.set()
        self._hosts.unblock()
        icon.stop()

    def _menu(self) -> pystray.Menu:
        status = "ON" if self._monitoring else "OFF"
        k = self._monitor.total_killed
        h = self._hosts.blocked_count

        return pystray.Menu(
            pystray.MenuItem(f"Monitoring: {status}", self._toggle, default=True),
            pystray.MenuItem(f"Killed: {k} | Hosts: {h}", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Reblock hosts", self._reblock),
            pystray.MenuItem("Unblock hosts", self._unblock),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )

    def run(self) -> None:
        self._hosts.block()
        logger.info("Blocked %d AI domains", self._hosts.blocked_count)

        self._stop.clear()
        threading.Thread(target=self._loop, daemon=True).start()

        self._icon = pystray.Icon(
            "huginn", icon=_icon_image(), title="Huginn", menu=self._menu()
        )
        self._icon.run()
