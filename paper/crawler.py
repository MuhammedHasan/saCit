import urllib2
from bs4 import BeautifulSoup


def cid_to_paperid(cid):
    ''' This function return paperid from cid if exist
        If not it will return None
    '''
    url = 'http://citeseerx.ist.psu.edu/viewdoc/summary?cid=' + str(cid)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
    tags = soup.select('#docMenu ul li a')
    if tags:
        return tags[0]['href'].split('doi=')[1]
