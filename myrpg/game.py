# -*- coding: utf-8 -*-

from myrpg.engines.app import Application

from argparse import ArgumentParser
import json
import six
import sys
import os


def main():
    parser = ArgumentParser(description='MyRPG project launcher')

    parser.add_argument(
        'proj',
        nargs=1,
        help='Path to MyRPG project file',
        required=True
    )

    args = parser.parse_args()

    if not os.path.exists(args.proj):
        six.print_('Cannot find project:', args.proj, file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.proj) as f:
            proj = json.load(f)

    except IOError as err:
        six.print_('Cannot open project:', err, file=sys.stderr)
        sys.exit(1)

    except ValueError as err:
        six.print_('Cannot parse project:', err, file=sys.stderr)
        sys.exit(1)

    os.setenv('B3J0F_CONF_DIR', proj['directory'])

    app = Application()
    app.run()
