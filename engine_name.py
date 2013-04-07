from novaprinter import prettyPrinter
from helpers import retrieve_url

class engine_name(object):
  url = 'http://psychocydd.co.uk'
  name = 'RockBox'

  supported_categories = {
    'all': '0',
    'movies': '6',
    'music': '1',
    }

  def __init__(self):
    # some initialization
    pass

  def download_torrent(self, info):
    # Providing this function is optional. It can however be interesting to provide
    # your own torrent download implementation in case the search engine in question
    # does not allow traditional downloads (for example, cookie-based download).
    print download_file(info)

  # DO NOT CHANGE the name and parameters of this function
  # This function will be the one called by nova2.py
  def search(self, what, cat='all'):
    # what is a string with the search tokens, already escaped (e.g. "Ubuntu+Linux")
    # cat is the name of a search category in ('all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books')
    #
    # Here you can do what you want to get the result from the
    # search engine website.
    # everytime you parse a result line, store it in a dictionary
    # and call the prettyPrint(your_dict) function
    pass
