__title__ = "create-introductions-issues"
__version__ = "0.9.0"
__author__ = "Joel McCune (https://github.com/knu2xs)"
__license__ = "Apache 2.0"
__copyright__ = "Copyright 2023 by Joel McCune (https://github.com/knu2xs)"

# add specific imports below if you want to organize your code into modules, which is mostly what I do
from . import utils

__all__ = ["utils"]

# configure package-level logging
logger = utils.get_logger("create_introductions_issues", level="DEBUG", add_stream_handler=False)
