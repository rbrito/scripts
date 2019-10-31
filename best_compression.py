#!/usr/bin/env python3

import logging
import os
import os.path
import subprocess
import sys


if len(sys.argv) <= 1:
    sys.exit(1)

cmds = [('gzip', 'gz'), ('bzip2', 'bz2'), ('xz', 'xz')]

file_name = sys.argv[1]

file_size = os.stat(file_name).st_size
sizes = [(file_name, file_size)]

for cmd, ext in cmds:
    full_command = [cmd, '-9k', file_name]
    logging.warning('    **** Executing command: <%s>', full_command)
    subprocess.run(full_command)
    new_file_name = file_name + '.' + ext

    file_size = os.stat(new_file_name).st_size
    logging.warning('    **** Resulting file size: <%s>.', file_size)
    sizes.append((new_file_name, file_size))

sorted_list = sorted(sizes, key=lambda x: x[1])
logging.warning('    **** sorted list: %s.', sorted_list)
logging.warning('    **** best option: %s.', str(sorted_list[1]))

for file_name, _ in sorted_list[1:]:
    logging.warning('    *** Removing: <%s>.', file_name)
    os.unlink(file_name)
