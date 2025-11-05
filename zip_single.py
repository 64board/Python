#!/usr/bin/env python3

"""
    Creates a zip file using the basename of the original file.
    janeiros@mbfcc.com
    2025.11.05
"""

import sys
import os
import zipfile
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging(verbose: bool, log_file: str):
    """
    Configure console + daily rotating file logging.
    Keeps last 7 daily logs (log_file.YYYY-MM-DD).
    """
    logger = logging.getLogger()
    logger.handlers = []            # avoid duplicate handlers if re-run
    logger.setLevel(logging.DEBUG)  # let handlers filter

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO if verbose else logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(ch)

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Daily rotation at local midnight, keep 7 files
    fh = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=False,  # rotate by local time
    )

    fh.setLevel(logging.INFO)  # file gets INFO+
    
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    logger.addHandler(fh)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Zip a single file using its base name."
    )
    parser.add_argument("file", help="File to zip")
    parser.add_argument(
        "-o", "--outdir",
        help="Output directory for the ZIP (default: same as input file)",
        default=None,
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Enable verbose console logging",
        action="store_true",
    )
    parser.add_argument(
        "--log-file",
        help="Path to log file (default: <outdir>\\zip_single.log)",
        default=None,
    )
    args = parser.parse_args()

    input_path = args.file

    if not os.path.isfile(input_path):
        print(f"Error: '{input_path}' is not a file.")
        sys.exit(1)

    src_dir = os.path.dirname(os.path.abspath(input_path))

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # Resolve outdir
    outdir = args.outdir if args.outdir else src_dir

    if not os.path.isdir(outdir):
        # create it early so logging can write there if default log path is used
        os.makedirs(outdir, exist_ok=True)

    # Default log file sits in outdir unless overridden
    log_file = args.log_file if args.log_file else os.path.join(outdir, "zip_single.log")
    setup_logging(args.verbose, log_file)

    logging.info(f"Input file: {input_path}")
    logging.info(f"Output directory: {outdir}")
    logging.info(f"Log file: {log_file}")

    # Zip filename based on original filename.
    zip_file: str = base_name + '.zip'
    zip_path: str = os.path.join(outdir, zip_file)
    logging.info(f"ZIP path: {zip_path}")

    try:

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            arcname = os.path.basename(input_path)
            z.write(input_path, arcname=arcname)
            logging.info(f"Added '{input_path}' as '{arcname}'")
            logging.info(f"Created: {zip_path}")

    except Exception as e:
        logging.exception(f"Failed to create ZIP: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
