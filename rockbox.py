#VERSION: 1.0
#AUTHORS: Rogerio Brito (rbrito@ime.usp.br)
from bs4 import BeautifulSoup

from novaprinter import prettyPrinter
from helpers import retrieve_url

class rockbox(object):
    url = 'http://psychocydd.co.uk'
    name = 'RockBox'

    supported_categories = {'all': '0', 'movies': '6', 'music': '1'}

    def __init__(self):
        pass

    def search(self, what, cat='all'):
        """
        Method called by nova2.

        `what` is the already scaped search string, while `cat` restricts in
        which category the search should be performed.

        For each parsed line of the result, we put it in a dictionary and
        pass it to the prettyPrint function.
        """
        data = retrieve_url('http://psychocydd.co.uk/torrents.php?search=%s' % what)

        soup = BeautifulSoup(data)
        res = soup.find_all('table', attrs={'width': '100%', 'class': 'lista'})
        rows = res[5].find_all('tr')  # by inspection, we want res[5]

        for row in rows[2:]:  # by inspection, we want rows[2:]
            cells = row.find_all('td')

            # Columns of interest
            info = {
                'name': cells[1].a.text,
                'link': self.url + '/' + cells[4].a['href'],
                'size': cells[6].text,
                'seeds': cells[7].text,
                'leech': cells[8].text,
                'engine_url': self.url,
                }
            prettyPrinter(info)
