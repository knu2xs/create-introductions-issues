# Logging

Logging utilities including an ArcPy logging handler and logger configuration function.

As a best practice, it is recommended to set up logging for your application using the
[`get_logger`][create_introductions_issues.utils.get_logger] function. This ensures logging 
is properly routed to the console, logfile and ArcPy messaging as appropriate. For example, 
in each module of your application, you should set up a logger like this:

``` python
from create_introductions_issues.utils import get_logger

logger = get_logger(__name__, level='DEBUG', add_stream_handler=False)
```

This ensures logging is consistent across your application and can be easily managed. Then, when
you create a script in the scripts diretory, you can configure the root logger as needed for that
script's execution context.

``` python
import datetime
from pathlib import Path

from create_introductions_issues.utils import get_logger

# get the path to a directory to store logfiles - assuming script is in scripts directory
script_pth = Path(__file__)
dir_prj = script_pth.parent.parent
dir_logs = dir_prj / 'data' / 'logs'

# ensure the log directory exists
if not dir_logs.exists():
    dir_logs.mkdir(parents=True)

# get the name of the scritp without the .py extension
script_name = script_pth.stem

if __name__ == "__main__":

    # define the logfile path with a timestamp - enables unique logfile per execution
    logfile_path = dir_logs / f'{script_name}_{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}.log'

    # ommitting the name uses the root logger - messages from package loggers will bubble up into the root logger
    logger = get_logger(level='INFO', add_stream_handler=True, logfile_path=logfile_path)

    # from here on out, use the logger to log messages
    logger.debug('This is a debug message, which will not be shown since the log level is set to INFO.')
    logger.info('This is an informational message, which will be shown in both the console and logfile.')
    logger.warning('This is a warning message, indicating a potential issue.')
    logger.error('This is an error message, indicating a failure in a specific operation.')
    logger.critical('This is a critical message, indicating a severe failure that may stop the program.')
```