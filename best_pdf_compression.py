#!/usr/bin/env python3

import argparse
import logging
import os
import os.path
import subprocess
import shutil

CMDS = [
    ('images', ['--use-image-optimizer=pingo9,rbrito,jbig2', '--use-multivalent=no', '--do-optimize-images=yes', '--do-fast-bilevel-images=yes'], '.pso'),
    ('multivalent', ['--use-image-optimizer=pingo9,rbrito,jbig2', '--use-multivalent=yes', '--do-optimize-images=no', '--do-fast-bilevel-images=yes'], '.psom'),
    ('final', ['--use-image-optimizer=pingo9,rbrito,jbig2', '--use-multivalent=no', '--do-optimize-images=no', '--do-fast-bilevel-images=yes'], '.pso')
]


def main(args):
    orig_name = args.filename

    file_size = os.stat(orig_name).st_size

    orig_pair = (orig_name, file_size)

    sizes = [(orig_name, file_size)]

    cmd_prefix = '~/Downloads/pdfsizeopt/pdfsizeopt'
    cmd_prefix = os.path.expanduser(cmd_prefix)

    file_name = args.filename

    for phase, opts, extra_ext in CMDS:
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

        file_size = os.stat(new_file_name).st_size

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
    for file_name, _ in sorted_list[orig_position+1:]:
        logging.debug('    **** Removing: %s.', file_name)
        os.unlink(file_name)

    candidates, list_of_removed = sorted_list[:orig_position], sorted_list[orig_position+1:]

    logging.debug('    **** List of removed: %s.', list_of_removed)
    logging.debug('    **** List of candidates: %s.', candidates)

    # comparepdf --verbose=0 --compare=appearance in.pdf out.pdf
    cmd = ['comparepdf', '--verbose=2', '--compare=appearance', orig_name]

    for candidate_name, candidate_size in candidates:

        logging.debug('    **** Comparing original %s with %s.', orig_name, candidate_name)
        full_command = cmd[:]
        full_command.append(candidate_name)

        logging.debug('    **** Command line to execute: %s.', full_command)

        ret = subprocess.run(full_command)

        if ret.returncode == 0:
            # success !
            try:
                os.mkdir('done')
                os.mkdir('orig')
            except FileExistsError:
                pass

            logging.debug('    **** Moving %s to %s.', candidate_name, 'done')
            try:
                shutil.move(candidate_name, 'done')
            except shutil.Error as e:
                logging.warn('    **** Exception: %s.', e)
            
            logging.debug('    **** Moving %s to %s.', orig_name, 'orig')
            try:
                shutil.move(orig_name, 'orig')
            except shutil.Error as e:
                logging.warn('    **** Exception: %s.', e)

            break
        
        elif ret.returncode in [1, 2]:
            # some error that the manpage of comparepdf doesn't specify what it is
            pass
        else:
            # some difference found
            try:
                os.mkdir('not-optimized')
            except FileExistsError:
                pass

            logging.debug('    **** Moving %s to %s.', candidate_name, 'not-optimized')

            try:
                shutil.move(candidate_name, 'not-optimized')
            except shutil.Error as e:
                logging.warn('    **** Exception: %s.', e)


    for candidate_name, _ in candidates:
        try:
            os.unlink(candidate_name)
        except FileNotFoundError:
            pass



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
