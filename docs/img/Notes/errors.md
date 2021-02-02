Crashing randomly - catch & restart?
---------
####### SNPedia import for rs25531
Traceback (most recent call last):
  File "SNPedia/DataScraper.py", line 265, in <module>
    dfCrawl = SNPCrawl(rsids=rsid)
  File "SNPedia/DataScraper.py", line 45, in __init__
    self.initcrawl(rsids)
  File "SNPedia/DataScraper.py", line 54, in initcrawl
    self.grabTable(rsid) # imports
  File "SNPedia/DataScraper.py", line 81, in grabTable
    response = urllib.request.urlopen(url)
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/urllib/request.py", line 222, in urlopen
    return opener.open(url, data, timeout)
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/urllib/request.py", line 525, in open
    response = self._open(req, data)
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/urllib/request.py", line 543, in _open
    '_open', req)
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/urllib/request.py", line 503, in _call_chain
    result = func(*args)
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/urllib/request.py", line 1360, in https_open
    context=self._context, check_hostname=self._check_hostname)
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/urllib/request.py", line 1320, in do_open
    r = h.getresponse()
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/http/client.py", line 1321, in getresponse
    response.begin()
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/http/client.py", line 296, in begin
    version, status, reason = self._read_status()
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/http/client.py", line 265, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response