import logging
import sys

from huginn.app import HuginnApp


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )
    logging.getLogger(__name__).info("Starting Huginn")
    HuginnApp().run()


if __name__ == "__main__":
    main()
