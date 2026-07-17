import logging
import sys

from ai_blocker.app import AIBlockerApp


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )
    logging.getLogger(__name__).info("Starting AI Blocker")
    AIBlockerApp().run()


if __name__ == "__main__":
    main()
