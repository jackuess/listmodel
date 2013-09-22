List Model
============
List Model is a Python library for building iterators for various list sources (XML documents, Text documents, JSON objects etc.) in a unified manner. Inspiration was taken from [Qt QML:s](http://en.wikipedia.org/wiki/QML) [XmlListModel](http://qt-project.org/doc/qt-4.8/qml-xmllistmodel.html).

Usage
-----
Below is a simple example of how one could define a model for RSS feeds.
```python
from email.utils import mktime_tz, parsedate_tz
import datetime
import re
import time
from urlparse import urlparse

import listmodel


class RssModel(listmodel.XmlListModel):
    class RssRow(listmodel.Row):
        link = listmodel.XmlRole('link/text()')
        text = listmodel.XmlRole('description/text()')
        title = listmodel.XmlRole('title/text()')

        @listmodel.XmlRole
        def domain(self, val):
            domain = urlparse(self.link).netloc
            domain = re.sub(r'^www\.', '', domain)
            return domain

        @listmodel.XmlRole('pubDate/text()')
        def pub_date(self, value):
            timestamp = mktime_tz(parsedate_tz(value))
            return datetime.datetime.utcfromtimestamp(timestamp)
    
    query = '//item'
    rowhandler = RssRow

    title = listmodel.XmlRole('//channel/title/text()')
    fetch_time = listmodel.Role(
        datetime.datetime.utcfromtimestamp(time.time()))
```

The `RssModel` can then be used like this:
```python
>>> VSKFotboll_nu = RssModel('http://vskfotboll.nu/rss')
>>> VSKFotboll_nu
<RssModel (fetch_time=datetime.datetime(2013, 9, 22, 15, 21, 27, 370357), title='VSK Fotboll')>
>>> for row in VSKFotboll_nu.iter():
...     row
<RssRow (title=u'Tv\xe5 klassm\xe5l grusade Gr\xf6nvitts hopp', text=u'Njogu Demba Nyr\xe9n. Anfallaren var klinisk n\xe4r han s\xe4nkte VSK Fotboll i kv\xe4ll.\nHans tv\xe5 m\xe5l innebar att Dalkurd gick segra
nde ur striden p\xe5 Swedbank Park.', domain='vskfotboll.nu', link='http://www.vskfotboll.nu/index.php?fot=nyh&newsno=3719', pub_date=datetime.datetime(2013, 9, 15, 21, 59, 34))>
<RssRow (title=u'LIVE: VSK Fotboll\x96Dalkurd FF', text=u'S\xe5 h\xe4r f\xf6ljer du kv\xe4llens match mot Dalkurd FF.', domain='vskfotboll.nu', link='http://www.vskfotboll.nu/index.php?fot=nyh&newsno=3718', pub_
date=datetime.datetime(2013, 9, 15, 14, 51, 3))>
[More rows]
```
