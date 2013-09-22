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
    
    __query__ = '//item'
    __rowcls__ = RssRow

    title = listmodel.XmlRole('//channel/title/text()')
    fetch_time = listmodel.Role(
        datetime.datetime.utcfromtimestamp(time.time()))
