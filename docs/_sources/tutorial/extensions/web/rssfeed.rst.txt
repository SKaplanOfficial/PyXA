Reading RSS Feeds
=================

PyXA provides straightforward RSS reading capabilities through the :class:`~PyXA.extensions.XAWeb.RSSFeed` class. In combination with the associated :class:`~PyXA.extensions.XAWeb.RSSItem` and :class:`~PyXA.extensions.XAWeb.RSSItemContent` classes, the :class:`~PyXA.extensions.XAWeb.RSSFeed` class handles the details of parsing RSS feeds and makes their information accessible via object attributes and methods. These classes also automatically converts complex types, such as URLs and images, into their PyXA representations.

To create a new RSS reader, instantiate an :class:`~PyXA.extensions.XAWeb.RSSFeed` object and provide an RSS feed endpoint (i.e. URL) as an argument. You can then view the retrieved RSS items via the :func:`~PyXA.extensions.XAWeb.RSSFeed.items` method. The example below obtains the top 10 songs on iTunes, at the of time of writing, from Apple's public RSS feed.

.. code-block:: Python

    import PyXA
    reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
    print(reader.items())
    # <<class 'PyXA.extensions.XAWeb.RSSItemList'>['Hold Me Closer - Elton John & Britney Spears', 'Only Ever Wanted - Timcast', "I Ain't Worried - OneRepublic", 'wait in the truck - HARDY & Lainey Wilson', 'Bring Me to Life - Evanescence', 'Running Up That Hill (A Deal with God) - Kate Bush', 'Beer With My Friends - Kenny Chesney & Old Dominion', 'American Pie (Full Length Version) - Don Mclean', 'She Had Me At Heads Carolina - Cole Swindell', 'You Proof - Morgan Wallen']>

As you can see, the :func:`~PyXA.extensions.XAWeb.RSSFeed.items` method returns an :class:`~PyXA.extensions.XAWeb.RSSItemList` object, an instance of :class:`~PyXA.XABase.XAList` -- meaning that 1) the list supports bulk actions via method calls, and 2) the items are not fully evaluated until retrieved from the list by index. The latter is not significant when working with small amounts of items as in the example above, but it saves significant time when working with very large lists. The ability to perform bulk actions is present regardless of list size. The example below shows some of the bulk methods available for the :class:`~PyXA.extensions.XAWeb.RSSItemList` class.

.. code-block:: Python

    import PyXA
    reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
    items = reader.items()
    print(items)
    print(items.title())
    print(items.link())
    print(items.shuffle())

    # <<class 'PyXA.extensions.XAWeb.RSSItemList'>['Hold Me Closer - Elton John & Britney Spears', 'Only Ever Wanted - Timcast', "I Ain't Worried - OneRepublic", 'Bring Me to Life - Evanescence', 'wait in the truck - HARDY & Lainey Wilson', 'Running Up That Hill (A Deal with God) - Kate Bush', 'Beer With My Friends - Kenny Chesney & Old Dominion', 'American Pie (Full Length Version) - Don Mclean', 'She Had Me At Heads Carolina - Cole Swindell', "Summer of '69 - Bryan Adams"]>

    # ['Hold Me Closer - Elton John & Britney Spears', 'Only Ever Wanted - Timcast', "I Ain't Worried - OneRepublic", 'Bring Me to Life - Evanescence', 'wait in the truck - HARDY & Lainey Wilson', 'Running Up That Hill (A Deal with God) - Kate Bush', 'Beer With My Friends - Kenny Chesney & Old Dominion', 'American Pie (Full Length Version) - Don Mclean', 'She Had Me At Heads Carolina - Cole Swindell', "Summer of '69 - Bryan Adams"]

    # [<<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>, <<class 'PyXA.XABase.XAURL'>>]

    # <<class 'PyXA.extensions.XAWeb.RSSItemList'>['Bring Me to Life - Evanescence', 'American Pie (Full Length Version) - Don Mclean', "I Ain't Worried - OneRepublic", 'Running Up That Hill (A Deal with God) - Kate Bush', 'Only Ever Wanted - Timcast', 'Beer With My Friends - Kenny Chesney & Old Dominion', 'wait in the truck - HARDY & Lainey Wilson', 'Hold Me Closer - Elton John & Britney Spears', "Summer of '69 - Bryan Adams", 'She Had Me At Heads Carolina - Cole Swindell']>

The combination of :class:`~PyXA.XABase.XAList` objects and automatic conversion to PyXA-wrapped objects allows for highly streamlined code. For example, to open each image contained in the `description` element of each RSS item in preview, you can use bulk operations first to get the description of each item, then to get the images of each description, and finally to show each image.

.. code-block:: Python

    import PyXA
    reader = PyXA.RSSFeed("https://www.nhc.noaa.gov/gtwo.xml")
    descriptions = reader.items().description()
    descriptions.images().show_in_preview()

You could, of course, condense this further by taking full advantage of PyXA's support for chaining method calls:

.. code-block:: Python

    import PyXA
    PyXA.RSSFeed("https://www.nhc.noaa.gov/gtwo.xml").items().description().images().show_in_preview()

In this case, the sacrifice to readability is not too extreme, but you can decide which form suites your tastes.

The previous example utilized the :func:`~PyXA.extensions.XAWeb.RSSItemContentList.images` method to obtain a list of :class:`~PyXA.XABase.XAImage` objects. Another useful method is the :func:`~PyXA.extensions.XAWeb.RSSItemContentList.links` method, which obtains a list of :class:`~PyXA.XABase.XAURL` objects. Both of these methods work on lists of item content as well as on individual items. An example of using the :func:`~PyXA.extensions.XAWeb.RSSItemContentList.links` method is shown below. The example also showcases how you can use interweave an RSS reader with other aspects of PyXA, in this case using the :class:`~PyXA.XABase.XASound` class to listen to m4a files stored at a web URL.

.. code-block:: Python

    import PyXA
    reader = PyXA.RSSFeed("http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/topsongs/limit=10/xml")
    links = reader.items().links()
    m4as = filter(lambda x: "m4a" in x.url, links)

    for index, song in enumerate(m4as):
        print("Now playing: " + reader.items()[index].title)
        sound = PyXA.XASound(song)
        sound.play()
        sleep(sound.duration)
