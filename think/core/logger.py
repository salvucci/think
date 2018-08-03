import logging


def get_think_logger(name="think", formats="%(time)12.3f      %(source)-16s      %(message)s", level=logging.DEBUG):
        """Returns a new logger."""
        logging.basicConfig(format=formats, level=level)
        return logging.getLogger(name)
