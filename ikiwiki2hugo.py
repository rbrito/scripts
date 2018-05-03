#!/usr/bin/python3

import re
import sys

SEPARATOR_LINE = '---\n'

if __name__ == '__main__':

    for filename in sys.argv[1:]:

        with open(filename) as f:
            lines = f.readlines()

        head = {}
        body = []
        tags = []

        for line in lines:
            title_match = re.search(r'\[\[!meta\s*title=(.*)\]\]', line)
            if title_match:
                title = title_match.group(1)
                head['title'] = title
                continue

            date_match = re.search(r'\[\[!meta\s*date=(.*)\]\]', line)
            if date_match:
                date = date_match.group(1)
                head['date'] = date
                continue

            tag_match = re.search(r'\[\[!tag\s*(.*)\]\]', line)
            if tag_match:
                tags.append(tag_match.group(1))
                continue

            toc_match = re.search(r'\[\[!toc\]\]', line)
            if toc_match:
                continue

            body.append(line)


        ### Header
        post = [SEPARATOR_LINE]

        for k, v in head.items():
            post.append('%s: %s\n' % (k, v))

        if tags:
            post.append('tags: [%s]\n' % ', '.join(tags))

        post.append(SEPARATOR_LINE)
        ### Header

        post.extend(body)

        with open('new-%s' % filename, 'w') as f:
            f.write(''.join(post))
