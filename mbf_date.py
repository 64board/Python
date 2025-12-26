#!/usr/bin/env python3

"""
mbf_date: A small command-line tool that prints dates based on simple rules.

It can output:
  • the current date
  • the previous date
  • the next date

Optionally, it can treat Saturday and Sunday as non-business days, so:
  • previous business date skips weekends backward
  • next business date skips weekends forward

You can also specify the output format using Python strftime patterns.

janeiros@mbfcc.com
"""

import sys
import argparse
from datetime import date, timedelta

PROGRAM_VERSION = "2025.11.30"


class MBFDate:
    def __init__(self, business_dates: bool, date_format: str = "%Y%m%d"):
        self.format = date_format
        self.today = date.today()

        dow = self.today.weekday()  # Monday=0 ... Sunday=6

        # -------------------------------
        # PREVIOUS DATE LOGIC
        # -------------------------------
        if business_dates:
            if dow == 0:      # Monday → Friday
                subtract_days = -3
            elif dow == 6:    # Sunday → Friday
                subtract_days = -2
            elif dow == 5:    # Saturday → Friday
                subtract_days = -1
            else:
                subtract_days = -1
        else:
            subtract_days = -1

        self.previous_date = self.today + timedelta(days=subtract_days)

        # -------------------------------
        # NEXT DATE LOGIC
        # -------------------------------
        if business_dates:
            if dow == 4:      # Friday → Monday
                add_days = 3
            elif dow == 5:    # Saturday → Monday
                add_days = 2
            elif dow == 6:    # Sunday → Monday
                add_days = 1
            else:
                add_days = 1
        else:
            add_days = 1

        self.next_date = self.today + timedelta(days=add_days)

    def get_current_date(self):
        return self.today.strftime(self.format)

    def get_previous_date(self):
        return self.previous_date.strftime(self.format)

    def get_next_date(self):
        return self.next_date.strftime(self.format)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mbf_date",
        description="Print current, previous or next date (optionally using business-day logic).",
        add_help=True,
    )

    # --------------------------
    # Version option
    # --------------------------
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"mbf_date {PROGRAM_VERSION}",
        help="Show program version and exit.",
    )

    parser.add_argument(
        "-b", "--business",
        action="store_true",
        help="Use business dates (skip weekends for previous/next).",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c", "--current",
        action="store_true",
        help="Print current date (default).",
    )
    group.add_argument(
        "-p", "--previous",
        action="store_true",
        help="Print previous date.",
    )
    group.add_argument(
        "-n", "--next",
        action="store_true",
        help="Print next date.",
    )

    parser.add_argument(
        "-f", "--format",
        dest="date_format",
        default="%Y%m%d",
        help="Date format (Python strftime, default: %(default)s).",
    )

    parser.add_argument(
        "-?",
        action="help",
        help=argparse.SUPPRESS,
    )

    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    business_dates = args.business
    date_format = args.date_format

    d = MBFDate(business_dates, date_format)

    if args.current:
        out = d.get_current_date()
    elif args.previous:
        out = d.get_previous_date()
    elif args.next:
        out = d.get_next_date()
    else:
        out = d.get_current_date()

    sys.stdout.write(out)


if __name__ == "__main__":
    main()
