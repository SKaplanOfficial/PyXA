Tips and Tricks
===============

1. Know when and when not to chain commands. You might be tempted to use a batch operation such as `PyXA.Application("Notes").notes().plaintext()` to obtain the text of each note, but then you will _only_ have the unicode text, not references to the note objects. If you're going to need the note objects, you should store a reference to the list of notes in a separate variable, then run batch operations via that reference. On the other hand, you should make use of PyXA's command chaining where reasonable to improve the overall clarity of your code and maintain its syntactic similarity to JXA.

2. Use :class:`~PyXA.XABase.XAList` and its child classes whenever dealing with lists of PyXA objects. Bulk methods on :class:`~PyXA.XABase.XAList` objects are often significantly faster (sometimes over 56x faster) than using non-bulk methods and regular iteration over a list.