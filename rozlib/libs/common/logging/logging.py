import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# from libs.common.logging.logging_tee_output import TeeErr, TeeOut

def make_timestamp_str():
    timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    return timestamp

def setup_logging(
        logs_output_dir: Path,
        write_print_to_log=False
):
    print(f"Setting up logging in {logs_output_dir}")
    if not os.path.exists(logs_output_dir):
        os.mkdir(logs_output_dir)

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    timestamp = make_timestamp_str()
    logging.basicConfig(
        level=logging.DEBUG,
        format=
            '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d \n %(message)s',
        handlers=[
            logging.FileHandler(logs_output_dir / f"{timestamp}.log"),     # Log to file
            # use stdout so that it doesn't log red
            logging.StreamHandler(sys.stdout)             # Log to console
        ]
    )

    # if write_print_to_log:
    #     TeeErr()
    #     TeeOut()
