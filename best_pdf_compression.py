#!/usr/bin/env python3

import argparse
import logging
import os
import os.path
import shutil
import subprocess
import sys


CMDS = [
    ('images', ['--use-image-optimizer=pingo9,rbrito,jbig2', '--use-multivalent=no', '--do-optimize-images=yes', '--do-fast-bilevel-images=yes'], '.pso'),
    ('multivalent', ['--use-image-optimizer=pingo9,rbrito,jbig2', '--use-multivalent=yes', '--do-optimize-images=no', '--do-fast-bilevel-images=yes'], '.psom'),
    ('final', ['--use-image-optimizer=pingo9,rbrito,jbig2', '--use-multivalent=no', '--do-optimize-images=no', '--do-fast-bilevel-images=yes'], '.pso')
]


# Some auxiliary functions to avoid dealing with exceptions
def unconditional_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass


def unconditional_move(src, dst):
    logging.info('    **** Moving %s to %s.', src, dst)
    try:
        shutil.move(src, dst)
    except shutil.Error as e:
        logging.warning('    **** Exception: %s.', e)


def unconditional_stat(filename):
    try:
        file_size = os.stat(filename).st_size
    except FileNotFoundError:
        logging.error('    **** File %s not found.', filename)
        sys.exit(1)

    return file_size


def unconditional_unlink(filename):
    logging.info('    **** Removing %s.', filename)
    try:
        os.unlink(filename)
    except FileNotFoundError:
        pass


# The main function of the program
def main(args):
    orig_name = args.filename
    orig_size = unconditional_stat(orig_name)

    orig_pair = (orig_name, orig_size)

    sizes = [(orig_name, orig_size)]

    cmd_prefix = '~/Downloads/pdfsizeopt/pdfsizeopt'
    cmd_prefix = os.path.expanduser(cmd_prefix)

    file_name = args.filename

    for _, opts, extra_ext in CMDS:
        full_command = [cmd_prefix]
        full_command.extend(opts)
        full_command.append(file_name)

        file_name, ext = os.path.splitext(file_name)
        new_file_name = file_name + extra_ext + ext

        logging.debug('    **** Executing command: %s', full_command)
        ret = subprocess.run(full_command)

        print('\n\n')

        # Don't even bother with commands that didn't execute; also,
        # subsequent commands depend on previous phases
        if ret.returncode != 0:
            break

        file_size = unconditional_stat(new_file_name)

        sizes.append((new_file_name, file_size))

        file_name = new_file_name

    sorted_list = sorted(sizes, key=lambda x: x[1])
    logging.debug('    **** sorted list: %s.', sorted_list)

    orig_position = sorted_list.index(orig_pair)

    logging.debug('    **** position of original file: %d.', orig_position)
    logging.debug('    **** original tuple: %s.', orig_pair)
    logging.debug('    **** best option: %s.', sorted_list[0])

    # Definitely remove the files that are bigger than the original (BUT NOT
    # THE ORIGINAL).
    for file_name, _ in sorted_list[orig_position + 1:]:
        unconditional_unlink(file_name)

    candidates, list_of_removed = sorted_list[:orig_position], sorted_list[orig_position + 1:]

    logging.debug('    **** List of removed: %s.', list_of_removed)
    logging.debug('    **** List of candidates: %s.', candidates)

    # comparepdf --verbose=0 --compare=appearance in.pdf out.pdf
    cmd = ['comparepdf', '--verbose=2', '--compare=appearance', orig_name]

    for candidate_name, _ in candidates:
        logging.debug('    **** Comparing original %s with %s.', orig_name, candidate_name)
        full_command = cmd[:]
        full_command.append(candidate_name)

        logging.debug('    **** Command line to execute: %s.', full_command)

        ret = subprocess.run(full_command)

        if ret.returncode == 0:
            # success !
            unconditional_mkdir('done')
            unconditional_mkdir('orig')

            unconditional_move(candidate_name, 'done')
            unconditional_move(orig_name, 'orig')

            break

        elif ret.returncode in [1, 2]:
            # some error that the manpage of comparepdf doesn't specify what it is
            pass
        else:
            # some difference found
            unconditional_mkdir('not-optimized')
            unconditional_move(candidate_name, 'not-optimized')

    for candidate_name, _ in candidates:
        unconditional_unlink(candidate_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select "best" optimized version of a PDF file')

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
