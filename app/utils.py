# -*- coding: utf-8 -*-
import sys

import csdmpy as cp

# This is a very simple function for logging messages in a Terminal in near-realtime
# from a web application


def slogger(origin, message):
    """Log a message in the Terminal
    Args:
        str: The origin of the message, e.g. the name of a function
        str: The message itself, e.g. 'Query the database'
    Returns:
        None
    """
    ORIGIN = origin.upper()
    print(f"\033[94m[SLOG] \u001b[36m|  \033[1m\u001b[33m{ORIGIN} \u001b[0m{message}")
    sys.stdout.flush()


def load_csdm(content):
    """Load a JSON file. Return a list with members
    - Success: True if file is read correctly,
    - Data: File content is success, otherwise an empty string,
    - message: An error message when JSON file load fails, else an empty string.
    """
    content = str(content, encoding="UTF-8")
    try:
        data = cp.loads(content)
        return True, data, ""
    except Exception as e:
        return False, "", e
