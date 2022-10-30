Using Appscript to Work With Unsupported Applications
=====================================================

PyXA aims to be have fine-grained documentation on a per-application basis, which greatly limits its ability to interact with applications outside of the ones explicitly mentioned in this documentation. To make up for this limitation, PyXA falls back to `appscript <https://appscript.sourceforge.io>`_ when no PyXA definition exists for an application. This allows you to interact with any AppleScript-compatible application, through appscript, while having access to the additional features of PyXA for an ever-expanding set of applications.

Converting Between Appscript and PyXA Types
-------------------------------------------

