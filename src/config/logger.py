import logging

# Create Logger
logger = logging.getLogger("Bloksupplychain Script Logger")
logger.setLevel(level=logging.DEBUG)


def config_logger(file_path: str = "./logs.txt ", to_file=False, to_console=True):
    # Create file handler
    if to_file:
        file_handler = logging.FileHandler(filename=file_path)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        logger.addHandler(file_handler)

    if to_console:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        logger.addHandler(console_handler)
