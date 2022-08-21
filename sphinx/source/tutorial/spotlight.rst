Searching Spotlight
===================
The :class:`XABase.XASpotlight` class allows you to search Spotlight and obtain :class:`XABase.XAPath` references to files. With this, you can easily locate and open files with particular names, containing particular content, or modified on a particular date. The examples below show how to carry out such tasks.

Simple Searches
---------------
To perform a simple term-based file search, instantiate a :class:`XABase.XASpotlight` object and provide a search term as an argument, as seen in the code below. This will instruct PyXA to prepare a new Spotlight search, but it won't begin the search until you actually attempt to access the results. When you provide a string, integer, or float as a search term, PyXA searches for files where the term appears in their display name, file system name, or text content. The search can take some time depending on how many items match the search, but usually completes within a second. The results of a search are given as a list of :class:`XABase.XAPath` objects.

    >>> import PyXA
    >>> search = PyXA.XASpotlight("Example")
    >>> print(search.results)
    [<<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Documents/ExampleFile1.txt>, <<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Documents/ExampleFile2.pdf>, ...]

The more specific your query is, the less time the search will take. The easiest way to increase the specificity is to provide a longer search string, as in the following example:

    import PyXA
    search = PyXA.XASpotlight("This is a test")
    print(len(search.results))
    10

Alternatively, you can supply multiple arguments to check for multiple terms. Doing this instructs PyXA to search for files where all of the supplied terms are found in the name or content of the file. For example, a text file named "test.txt" containing the text "This is awesome" would appear in the first search below but not the second. In the first search, we are looking for files where "this" appears in the filename or content, "is" appears in the filename or content, "a" appears in the filename or content, and "test" appears in the filename or content. Our example file has "test" in its name, and "this", "is", and "a" all appear in its content, thus the file would appear in the search results. For the second search, we are looking for files where "This is" appears in the filename or content and "a test" appears in the filename or content. Our example file does not match that condition, thus it would not appear in the search results.

    >>> import PyXA
    >>> search = PyXA.XASpotlight("This", "is", "a", "test")
    >>> print(len(search.results))
    40022

    >>> import PyXA
    >>> search = PyXA.XASpotlight("This is", "a test")
    >>> print(len(search.results))
    49

Note that the first search above returned over 800 times more results than the second and thus takes noticeably longer to finish. Just as before, providing longer search strings increases the specificity of the query, helping Spotlight to more quickly narrow down the search results. When providing multiple arguments, you can also increase specificity by simply providing more arguments, as highlighted by the two code snippets below:

    >>> search = PyXA.XASpotlight("This", "is", "a", "test", "avocado")
    >>> print(len(search.results))
    15

    >>> search = PyXA.XASpotlight("This", "is", "a", "test", "avocado", "quack")
    >>> print(len(search.results))
    2

If you find that searches are taking too long, you can increase the specificity of your search query in any of the following ways:
- Use terms less likely to appear in many files
- Use longer strings, combining multiple words in one argument
- Use multiple search terms, providing multiple words as separate arguments
- Combining all of the above methods


Search by Date
--------------
PyXA also provides a mechanism to search Spotlight by date. To perform a simple date-based search, instantiate a :class:`XABase.XASpotlight` object and pass a :class:`datetime` object as an argument. This instructs PyXA to search for files created, added, or modified within the surrounding 24-hour period (plus or minus 12 hours from the supplied datetime).

    >>> import PyXA
    >>> from datetime import datetime
    >>> search = PyXA.XASpotlight(datetime.now())
    >>> print(search.results)
    [<<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Documents/>, <<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Documents/GitHub/>, ...]

To search for files created, added, or modified within a specific time range, you can supply two datetime objects as arguments, as seen in the example below:

    >>> import PyXA
    >>> from datetime import date, datetime, time
    >>> date1 = datetime.combine(date(2022, 5, 17), time(0, 0, 0))
    >>> date2 = datetime.combine(date(2022, 5, 18), time(0, 0, 0))
    >>> search = PyXA.XASpotlight(date1, date2)
    >>> print(search.results)
    [<<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Downloads/>, <<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Downloads/Example.txt>, ...]

You can also combined these two date-based search methods with term-based ones by adding additional arguments. The date(s) must always come before the term(s). All previously noted strategies for increasing query specificity still apply. The two code snippets below showcase this in action.

    >>> import PyXA
    >>> search = PyXA.XASpotlight(datetime.now(), "This", "is", "a", "test")
    >>> print(len(search.results))
    42

    >>> import PyXA
    >>> search = PyXA.XASpotlight(datetime.now() - timedelta(minutes=5), datetime.now(), "This is a test")
    >>> print(len(search.results))
    2


Search by Predicate
-------------------
PyXA allows you to supply your own predicate to filter search results by. You can supply the predicate as either a raw string or as an :class:`XABase.XAPredicate` object. For the former, use Apple's documentation on `File Metadata Query Expression Syntax`_ as a reference. The following examples show how to use both strategies.

    >>> import PyXA
    >>> search = PyXA.XASpotlight()
    >>> search.predicate = "kMDItemDisplayName == 'Example.txt'"
    >>> search.run()
    >>> print(search.results)
    [<<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Downloads/Example.txt>]

    >>> import PyXA
    >>> search = PyXA.XASpotlight()
    >>> predicate = PyXA.XAPredicate()
    >>> predicate.add_eq_condition("kMDItemDisplayName", "Example.txt")
    >>> search.predicate = predicate
    >>> search.run()
    >>> print(len(search.results))
    [<<class 'PyXA.XABase.XAPath'>file:///Users/exampleUser/Downloads/Example.txt>]

.. _File Metadata Query Expression Syntax: https://developer.apple.com/library/archive/documentation/Carbon/Conceptual/SpotlightQuery/Concepts/QueryFormat.html#//apple_ref/doc/uid/TP40001849