import urllib2
from bs4 import BeautifulSoup
from httplib import BadStatusLine


def cid_to_paperid(cid):
    ''' This function return (cid,paperid) from cid if exist
        If not it will return None
    '''
    if cid:
        None
    url = 'http://citeseerx.ist.psu.edu/viewdoc/summary?cid=' + str(cid)
    html = str()
    while True:
        try:
            html = urllib2.urlopen(url).read()
            break
        except urllib2.HTTPError:
            return None
        except BadStatusLine:
            print 'BadStatusLine'
            continue
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.select('#docMenu ul li a')
    if tags:
        return tags[0]['href'].split('doi=')[1]


def cids_to_paperids(cids):
    return [cid_to_paperid(i) for i in cids]
