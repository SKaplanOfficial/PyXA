Project Overview
================

What is PyXA?
#############

Python for Automation, or PyXA for short, is a wrapper around several macOS frameworks that enables AppleScript- and JXA-like control over macOS applications from within Python. PyXA's objects and methods are based on applications' scripting dictionaries and coupled with additional automation features supported by Apple's macOS APIs. 

PyXA was created with the goals of:

    1. Simplifying the way automation tasks can be accomplished via Python
    2. Introducing new features to macOS application scripting by simplifying complex procedures into simple, declarative methods
    3. Disambiguating the capabilities of application scripting on macOS by providing easy-to-follow documentation throughout the entire project

PyXA fills a gap where currently available frameworks ultimately fall short: it aims to be easy to learn for users accustomed to Python (or users who _must_ use Python). To that end, the package's documentation contains numerous examples of how to use just about every method, and additional examples are provided covering specific use cases. PyXA's code also serves as a source of examples for how to use `PyObjC <https://pyobjc.readthedocs.io/en/latest/>`_ to interact with various macOS frameworks.

Is PyXA for Me?
###############

PyXA is not intended to replace AppleScript or even to cover 100% of AppleScript's capabilities. Instead, PyXA is meant to provide general convenience in accomplishing AppleScript and other automation tasks via Python, for the most commonly used applications. If you need a complete Apple Event bridge, or if you find that PyXA cannot handle your particular use case, consider using `appscript <https://appscript.sourceforge.io>`_ or one of its derivatives. If you just need something that works in most circumstances, that has abundant examples for you to reference, and supports some additional automation features (such as opening Maps to a specific address), then PyXA might be a good fit for you.

