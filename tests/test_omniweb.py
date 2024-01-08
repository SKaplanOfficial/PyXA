import PyXA
import time
import unittest

import ScriptingBridge

from PyXA.apps.OmniWeb import *

class TestOmniweb(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("OmniWeb")

    def test_omniweb_application_type(self):
        app2 = PyXA.Omniweb()
        self.assertEqual(self.app, app2)
        self.assertIsInstance(self.app, XAOmniWebApplication)

    def test_omniweb_application_attributes(self):
        self.assertEqual(self.app.name, "OmniWeb")
        self.assertIsInstance(self.app.version, str)
        self.assertIsInstance(self.app.frontmost, bool)

        self.assertIsInstance(self.app.active_workspace, XAOmniWebWorkspace)
        self.assertIsInstance(self.app.favorites, XAOmniWebBookmark)
        self.assertIsInstance(self.app.full_version, str)
        self.assertIsInstance(self.app.personal_bookmarks, XAOmniWebBookmarksDocument)

        self.assertIsInstance(self.app.documents(), PyXA.XABase.XAList)
        self.assertIsInstance(self.app.windows(), PyXA.XABase.XAList)
        self.assertIsInstance(self.app.browsers(), PyXA.XABase.XAList)
        self.assertIsInstance(self.app.workspaces(), PyXA.XABase.XAList)
        self.assertIsInstance(self.app.bookmarks_documents(), PyXA.XABase.XAList)

        self.assertIsInstance(self.app.documents(), XAOmniWebDocumentList)
        self.assertIsInstance(self.app.windows(), PyXA.XABaseScriptable.XASBWindowList)
        self.assertIsInstance(self.app.browsers(), XAOmniWebBrowserList)
        self.assertIsInstance(self.app.workspaces(), XAOmniWebWorkspaceList)
        self.assertIsInstance(self.app.bookmarks_documents(), XAOmniWebBookmarksDocumentList)

    def test_omniweb_application_methods(self):
        window_ids = self.app.list_windows()
        self.assertIsInstance(window_ids, list)
        self.assertIsInstance(window_ids[0], int)

        window_info = self.app.get_window_info()
        self.assertIsInstance(window_info, list)
        self.assertIsInstance(window_info[0], str)
        self.assertIsInstance(window_info[1], str)

        self.app.activate()
        self.app.open("http://www.google.com")
        self.assertEqual(self.app.browsers()[0].address, PyXA.XABase.XAURL("http://www.google.com/"))

    def test_omniweb_bookmark(self):
        bookmark = self.app.favorites
        self.assertIsInstance(bookmark, XAOmniWebBookmark)
        self.assertIsInstance(bookmark.bookmarks(), XAOmniWebBookmarkList)

        self.assertIsInstance(bookmark.address, PyXA.XABase.XAURL)
        self.assertIsInstance(bookmark.check_interval, int)
        self.assertIsInstance(bookmark.is_new, bool)
        self.assertIsInstance(bookmark.is_reachable, bool)
        self.assertTrue(isinstance(bookmark.last_checked_date, datetime) or bookmark.last_checked_date is None)
        self.assertIsInstance(bookmark.name, PyXA.XABase.XAText)
        self.assertTrue(isinstance(bookmark.note, PyXA.XABase.XAText) or bookmark.note is None)

        bookmark = self.app.bookmarks_documents()[0].bookmarks()[0]

        self.assertIsInstance(bookmark.address, PyXA.XABase.XAURL)
        self.assertIsInstance(bookmark.check_interval, int)
        self.assertIsInstance(bookmark.is_new, bool)
        self.assertIsInstance(bookmark.is_reachable, bool)
        self.assertTrue(isinstance(bookmark.last_checked_date, datetime) or bookmark.last_checked_date is None)
        self.assertIsInstance(bookmark.name, PyXA.XABase.XAText)
        self.assertTrue(isinstance(bookmark.note, PyXA.XABase.XAText) or bookmark.note is None)

    def test_omniweb_bookmarks_document(self):
        bookmarks_document = self.app.bookmarks_documents()[0]
        self.assertIsInstance(bookmarks_document, XAOmniWebBookmarksDocument)

        self.assertIsInstance(bookmarks_document.bookmarks(), XAOmniWebBookmarkList)
        self.assertIsInstance(bookmarks_document.address, PyXA.XABase.XAURL)
        self.assertIsInstance(bookmarks_document.is_read_only, bool)

    def test_omniweb_browser(self):
        browser = self.app.browsers()[0]
        self.assertIsInstance(browser, XAOmniWebBrowser)

        self.assertIsInstance(browser.active_tab, XAOmniWebTab)
        self.assertIsInstance(browser.address, PyXA.XABase.XAURL)
        self.assertIsInstance(browser.has_favorites, bool)
        self.assertIsInstance(browser.has_tabs, bool)
        self.assertIsInstance(browser.has_toolbar, bool)
        self.assertIsInstance(browser.is_busy, bool)
        self.assertIsInstance(browser.shows_address, bool)

        self.assertIsInstance(browser.tabs(), XAOmniWebTabList)

    def test_omniweb_tab(self):
        tab = self.app.browsers()[0].tabs()[0]
        self.assertIsInstance(tab, XAOmniWebTab)

        self.assertIsInstance(tab.address, PyXA.XABase.XAURL)
        self.assertIsInstance(tab.is_busy, bool)
        self.assertIsInstance(tab.title, PyXA.XABase.XAText)
        # Source is not currently working even in Script Editor
        # self.assertIsInstance(tab.source, PyXA.XABase.XAText)

    def test_omniweb_workspace(self):
        workspace = self.app.workspaces()[0]
        self.assertIsInstance(workspace, XAOmniWebWorkspace)

        self.assertIsInstance(workspace.name, PyXA.XABase.XAText)
        self.assertIsInstance(workspace.autosaves, bool)

        self.assertIsInstance(workspace.browsers(), XAOmniWebBrowserList)
