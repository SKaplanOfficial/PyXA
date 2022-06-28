""".. versionadded:: 0.0.2

Control the macOS Dictionary application using JXA-like syntax.
"""

from CoreServices import DCSCopyTextDefinition

from PyXA import XABase

class XADictionaryApplication(XABase.XAApplication):
    """A class for managing and interacting with Dictionary.app.

    .. seealso:: :class:`XADictionaryDefinition`

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)

    def define(self, word: str) -> str:
        """Gets the definition of a word in raw text form.

        :param word: The word to define
        :type word: str
        :return: The definition of the word
        :rtype: str

        .. versionadded:: 0.0.2
        """
        definition = DCSCopyTextDefinition(None, word, (0, len(word)))
        return definition

    ### UI Interaction
    ## Menu Bar
    # Dictionary Menu
    def open_about_panel(self):
        """Opens the "About Dictionary" panel. Mimics clicking File->About Dictionary.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(1).menu(0).menu_item(0).press()

    def open_preferences(self):
        """Opens the preferences window for the Dictionary application. Mimics clicking File->Preferences...

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(1).menu(0).menu_item(2).press()

    # File Menu
    def new_window(self):
        """Opens a new Dictionary window.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(2).menu(0).menu_item(0).press()

    def new_tab(self):
        """Opens a new Dictionary tab.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(2).menu(0).menu_item(1).press()

    def open_dictionaries_folder(self):
        """Opens the folder containing custom/downloaded dictionaries.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(2).menu(0).menu_item(-3).press()

    def print(self):
        """Opens the dictionary app's print dialog.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(2).menu(0).menu_item(-1).press()

    # Edit Menu
    def paste(self):
        """Pastes the current contents of the clipboard into the selected item, if there is one.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(3).menu(0).menu_item(5).press()

    def start_dictation(self):
        """Begins dictation to fill the selected item, if there is one.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(3).menu(0).menu_item(-2).press()

    # Go Menu
    def go_back(self):
        """Goes to the previous page/definition.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(4).menu(0).menu_item(0).press()

    def go_forward(self):
        """Goes to the next page/definition.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(4).menu(0).menu_item(1).press()

    def view_front_back_matter(self):
        """Displays the front/back matter of the selected dictionary.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(4).menu(0).menu_item(3).press()

    # Window Menu
    def fullscreen(self):
        """Toggles fullscreen for the current Dictionary window.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(6).menu(0).menu_item(9).press()

    # Help Menu
    def show_help(self):
        """Displays the help window for Dictionary.app.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(7).menu(0).menu_item(-1).press()

    ## Window
    def switch_to_all(self):
        """Switches to searching all installed dictionaries.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(5).menu(0).menu_item(0).press()

    def switch_to_new_oxford(self):
        """Switches to searching the New Oxford American Dictionary.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(5).menu(0).menu_item(2).press()

    def switch_to_oxford_thesaurus(self):
        """Switches to searching the Oxford American Writer's Thesaurus.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(5).menu(0).menu_item(3).press()

    def switch_to_apple_dictionary(self):
        """Switches to searching the Apple Dictionary.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(5).menu(0).menu_item(4).press()

    def switch_to_wikipedia(self):
        """Switches to searching Wikipedia.

        .. versionadded:: 0.0.2
        """
        self.menu_bar(0).menu_bar_item(5).menu(0).menu_item(5).press()

    def search(self, term: str):
        """Searches the currently selected dictionary.

        :param term: The term to search
        :type term: str

        .. versionadded:: 0.0.2
        """
        if hasattr(self.window(0).toolbar(0).group(2).text_field(0), "value"):
            # Search from empty
            self.window(0).toolbar(0).group(2).text_field(0).set_property("value", term)
        else:
            # Search from searched word
            self.window(0).toolbar(0).group(0).text_field(0).set_property("value", "")
            print("hi")
            self.window(0).toolbar(0).group(2).text_field(0).set_property("value", term)

    def search_all(self, term: str):
        """Searches the provided term in all dictionaries

        :param term: The term to search
        :type term: str

        .. versionadded:: 0.0.2
        """
        self.switch_to_all()
        self.search(term)

    def search_new_oxford(self, term: str):
        """Searches the provided term in the New Oxford American Dictionary

        :param term: The term to search
        :type term: str

        .. versionadded:: 0.0.2
        """
        self.switch_to_new_oxford()
        self.search(term)

    def search_oxford_thesaurus(self, term: str):
        """Searches the provided term in the Oxford American Writer's Thesaurus

        :param term: The term to search
        :type term: str

        .. versionadded:: 0.0.2
        """
        self.switch_to_oxford_thesaurus()
        self.search(term)

    def search_apple_dictionary(self, term: str):
        """Searches the provided term in the Apple Dictionary

        :param term: The term to search
        :type term: str

        .. versionadded:: 0.0.2
        """
        self.switch_to_apple_dictionary()
        self.search(term)

    def search_wikipedia(self, term: str):
        """Searches the provided term in Wikipedia

        :param term: The term to search
        :type term: str

        .. versionadded:: 0.0.2
        """
        self.switch_to_wikipedia()
        self.search(term)