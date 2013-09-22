List Model
============
List Model is a Python library for building iterators for various list sources (XML documents, Text documents, JSON objects etc.) in a unified manner. Inspiration was taken from [Qt QML:s](http://en.wikipedia.org/wiki/QML) [XmlListModel](http://qt-project.org/doc/qt-4.8/qml-xmllistmodel.html).

Usage
-----
```python
>>> from listmodel import Row, XmlListModel, XmlRole
>>> xml = '''<bookshelf>
...     <name>My Bookshelf</name>
...     <content>
...         <book>
...             <name>1984</name>
...             <author>George Orwell</author>
...             <isbn>978-0-452-28423-4</isbn>
...         </book>
...         <book>
...             <name>The man in the high castle</name>
...             <author>Philip K. Dick</author>
...             <isbn>0679740678</isbn>
...         </book>
...     </content>
... </bookshelf>
... '''
>>> class BookshelfModel(XmlListModel):
...     class Book(Row):
...         name = XmlRole('name/text()')
...         author = XmlRole('author/text()')
...
...         # XmlRole can also be used to decorate functions
...         @XmlRole('isbn/text()')
...         def sources(self, value):
...             return 'http://en.wikipedia.org/wiki/Special:BookSources/%s' % value
...
...     __rowquery__ = '//content/book'
...     __rowcls__ = Book
...
...     name = XmlRole('/bookshelf/name/text()')
...     random = XmlRole('/hookshelf/name/text()')  # This will not be found and hence given the value None
...
>>> my_shelf = BookshelfModel(xml)  # The first argument to an XmlListModel can be eihter a URL or a string containing XML
>>> my_shelf
<BookshelfModel (name='My Bookshelf', random=None)>
>>> for book in my_shelf:
...     book
... 
<Book (sources='http://en.wikipedia.org/wiki/Special:BookSources/978-0-452-28423-4', name='1984', author='George Orwell')>
<Book (sources='http://en.wikipedia.org/wiki/Special:BookSources/0679740678', name='The man in the high castle', author='Philip K. Dick')>
```
