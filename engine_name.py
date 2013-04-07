#!/usr/bin/env python
# -*- coding: utf-8 -*-
from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
from lxml import etree

import lxml.html.soupparser

import logging


class engine_name(object):
    url = 'http://psychocydd.co.uk'
    name = 'RockBox'

    supported_categories = {'all': '0', 'movies': '6', 'music': '1'}

    @staticmethod
    def bytes_from_string(s):
        """
        We assume that there is a space between the numbers and the units.
        """
        sz = s.split()
        return int(float(sz[0]) * (1024 ** ' BKMG'.index(sz[1][0])))


    def __init__(self):
        logging.error('Class created.')

    # def download_torrent(self, info):
    #     # Providing this function is optional. It can however be interesting
    #     # to provide your own torrent download implementation in case the
    #     # search engine in question does not allow traditional downloads
    #     # (for example, cookie-based download).
    #     print(download_file(info))

    # DO NOT CHANGE the name and parameters of this function This
    # function will be the one called by nova2.py
    def search(self, what, cat='all'):
        """
        Method called by nova2.

        `what` is the already scaped search string, while `cat` restricts in
        which category the search should be performed.

        For each parsed line of the result, we put it in a dictionary and
        pass it to the prettyPrint function.
        """
        logging.error('Searching for %s.', what)

        data = retrieve_url('http://psychocydd.co.uk/torrents.php?search=%s' % what)

        logging.error('Data retrieved.')
        with open('searchresult.html', 'w') as f:
            f.write(data)

        logging.error('Creating tree.')

        #htmlparser = etree.HTMLParser()
        #tree = etree.fromstring(data, htmlparser)
        tree = lxml.html.soupparser.fromstring(data)
        table = tree.xpath('/html/body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr')

        logging.error('Tree created.')

        # Relevant <tr>s have length 12.
        for row in table:
            if len(row) == 12:
                logging.error('Found relevant row.')

                info = {
                    'name': row[1][0].text,
                    'link': row[4][0].get('href'),
                    'size': bytes_from_string(row[6].text),
                    'seeds': int(row[7][0].text),
                    'leech': int(row[8][0].text),
                    'engine_url': self.url,
                    }
                prettyPrinter(info)
