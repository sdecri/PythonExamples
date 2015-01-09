__author__ = 'simone.decristofaro'

from urllib3 import PoolManager,Timeout

def ping(url):
    """
    Return true if the url answer correctly (HTTP status = 200)

    :param url: url to ping
    :rtype: bool
    """
    http = PoolManager()
    request=None
    try:
        request = http.request('GET',url)
    except:
        return False
    if request and request.status == 200:
        return True
    return False


