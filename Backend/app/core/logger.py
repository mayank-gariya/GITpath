import logging

# Create logger
logger = logging.getLogger("gitpath")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

logger.propagate = False