#!/usr/bin/env python3

import argparse
import logging
import os
import os.path
import shutil
import subprocess
import sys

COMPRESS_OPT = '--use-image-optimizer=pingo9,rbrito,jbig2'


CMD = os.path.expanduser('~/Downloads/pdfsizeopt/pdfsizeopt')
CMDS = [
    (['qpdf', '--stream-data=uncompress', '--compress-streams=n', '--decode-level=specialized'], '.unc'),
    ([CMD, COMPRESS_OPT, '--do-fast-bilevel-images=yes', '--use-multivalent=no', '--do-optimize-images=yes'], '.pso'),
    ([CMD, COMPRESS_OPT, '--do-fast-bilevel-images=yes', '--use-multivalent=yes', '--do-optimize-images=no'], '.psom'),
    ([CMD, COMPRESS_OPT, '--do-fast-bilevel-images=yes', '--use-multivalent=no', '--do-optimize-images=no'], '.pso')
]
TMPDIR = '/tmp/rbrito'


# Some auxiliary functions to avoid dealing with exceptions
def unconditional_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass


def unconditional_move(src, dst):
    logging.debug('    **** Moving %s to %s.', src, dst)
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
    logging.debug('    **** Removing %s.', filename)
    try:
        os.unlink(filename)
    except FileNotFoundError:
        pass


def compare_pdfs(original, candidate):
    cmd = ['comparepdf', '--verbose=2', '--compare=appearance', original, candidate]
    logging.debug('    **** Comparing original %s with %s.', original, candidate)
    logging.debug('    **** Command line to execute: %s.', cmd)

    return subprocess.run(cmd)


def new_name(in_filename, extra_ext):
    filename, ext = os.path.splitext(in_filename)
    return filename + extra_ext + ext


def process_pdf(cmd, in_filename, out_filename):
    full_cmd = cmd.copy()
    full_cmd.append(in_filename)
    full_cmd.append(out_filename)

    logging.debug('    **** Executing command: %s', full_cmd)

    return subprocess.run(full_cmd)


def generate_candidates(orig_name, full_generation=False):
    '''
    Generate various compressed versions of orig_name.

    Given a PDF file orig_name, we try many strategies (some "chained" on
    top of each other) to further compress the original file. We return a
    list with pairs of the generated names and their sizes.

    If full_generation is True, then the file is also uncompressed to be
    compressed also, to try more strategies.
    '''
    orig_pair = (orig_name, unconditional_stat(orig_name))
    sizes = [orig_pair]
    filename = orig_name

    cmds = CMDS if full_generation else CMDS[1:]

    for cmd, extra_ext in cmds:
        new_filename = new_name(filename, extra_ext)

        ret = process_pdf(cmd, filename, new_filename)
        print('\n')

        # Don't even bother with commands that didn't execute; also,
        # subsequent commands depend on previous phases.  But there's an
        # exception: qpdf exits with code 3 if a warning (not an error) is
        # issued.
        if (cmd[0] == 'qpdf' and ret.returncode not in (0, 3)
            or (cmd[0] != 'qpdf' and ret.returncode != 0)):
            break

        new_size = unconditional_stat(new_filename)

        sizes.append((new_filename, new_size))

        filename = new_filename

    return sizes


# The main function of the program
def main(args):
    # FIXME: Way too much repetition
    orig_name = args.filename
    orig_pair = (orig_name, unconditional_stat(orig_name))

    sizes = generate_candidates(orig_name, full_generation=args.decompress)

    sorted_list = sorted(sizes, key=lambda x: x[1])
    logging.debug('    **** sorted list: %s.', sorted_list)

    # Definitely remove the files that are bigger than the original (BUT NOT
    # THE ORIGINAL).
    orig_position = sorted_list.index(orig_pair)

    candidates = sorted_list[:orig_position]
    list_to_remove = sorted_list[orig_position + 1:]

    logging.debug('    **** List to remove: %s.', list_to_remove)
    logging.debug('    **** List of candidates: %s.', candidates)

    for filename, _ in list_to_remove:
        unconditional_unlink(filename)

    basedir, _ = os.path.split(orig_name)

    optimized = False  # if we got a smaller file than the original one

    for candidate, _ in candidates:
        ret = compare_pdfs(orig_name, candidate)

        if ret.returncode == 0:
            # Success !
            done_dir = os.path.join(basedir, 'done')
            orig_dir = os.path.join(basedir, 'orig')
            unconditional_mkdir(done_dir)
            unconditional_mkdir(orig_dir)

            unconditional_move(candidate, done_dir)
            unconditional_move(orig_name, orig_dir)

            optimized = True
            # We clean up the remaining/unused candidates now
            break

        elif ret.returncode in [1, 2]:
            # some error that the manpage of comparepdf doesn't specify what it is
            pass
        else:
            # Some difference found; keep files for further inspection
            keeper_dir = os.path.join(basedir, 'to-inspect-manually')
            unconditional_mkdir(keeper_dir)
            unconditional_move(candidate, keeper_dir)

    if optimized is False:
        # The best option was the original file (this includes the
        # possibility of an error with pdfsizeopt)...
        done_dir = os.path.join(basedir, 'done')
        unconditional_mkdir(done_dir)
        unconditional_move(orig_name, done_dir)
        logging.warning("    **** Couldn't optimize %s further.", orig_name)

    # Check the relationship of optimized == False/True vs. the remaining
    # of candidates
    for candidate, _ in candidates:
        unconditional_unlink(candidate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select "best" optimized version of a PDF file')

    parser.add_argument('--decompress', action='store_true', default=False,
                        help='decompress the input PDF before further processing')
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

    # try:
    #     os.mkdir(TMPDIR, mode=0o700)
    # except FileExistsError:
    #     pass
    # # FIXME: Cleanup the TMP DIR if we fail somehow
    # os.environ['TMPDIR'] = TMPDIR

    main(args)
