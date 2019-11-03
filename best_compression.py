#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys

CMDS = [('gzip', 'gz'), ('bzip2', 'bz2'), ('xz', 'xz')]


def main(args):
    file_name = args.filename

    file_size = os.stat(file_name).st_size

    sizes = [(file_name, file_size)]

    for cmd, ext in CMDS:
        full_command = [cmd]

        if cmd == 'gzip':
            full_command.extend(['-9k', '-n'])
        elif cmd == 'bzip2':
            full_command.extend(['-9k'])
        elif cmd == 'xz':
            full_command.extend(['-ek'])
        else:
            logging.error('    *** command %s not recognized.', cmd)
            sys.exit(1)

        full_command.append(file_name)

        logging.debug('    **** Executing command: %s', full_command)
        subprocess.run(full_command)

        new_file_name = file_name + '.' + ext
        file_size = os.stat(new_file_name).st_size

        sizes.append((new_file_name, file_size))

    sorted_list = sorted(sizes, key=lambda x: x[1])
    logging.debug('    **** sorted list: %s.', sorted_list)
    logging.debug('    **** best option: %s.', str(sorted_list[0]))

    for file_name, _ in sorted_list[1:]:
        logging.info('    *** Removing: %s.', file_name)
        os.unlink(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select "best" compression of a file')

    parser.add_argument('--verbose', action='store_true', default=False,
                        help='generate verbose output')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='generate very verbose output')
    parser.add_argument('--quiet', action='store_true', default=False,
                        help='generate only error messages')
    parser.add_argument('filename',
                        help='name of the file to compress')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.WARN)
    elif args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    main(args)
