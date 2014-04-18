from email.utils import mktime_tz, parsedate_tz
import datetime
import re
import time
from urlparse import urlparse

from .xml_model import XmlListModel, XmlRole
from .._listmodel import Role, Row


class RssModel(XmlListModel):
    class RssRow(Row):
        link = XmlRole('link/text()')
        text = XmlRole('description/text()')
        title = XmlRole('title/text()')

        @XmlRole
        def domain(self, val):
            domain = urlparse(self.link).netloc
            domain = re.sub(r'^www\.', '', domain)
            return domain

        @XmlRole('pubDate/text()')
        def pub_date(self, value):
            timestamp = mktime_tz(parsedate_tz(value))
            return datetime.datetime.utcfromtimestamp(timestamp)
    
    __rowquery__ = '//item'
    __rowcls__ = RssRow

    title = XmlRole('//channel/title/text()')
    fetch_time = Role(datetime.datetime.utcfromtimestamp(time.time()))
