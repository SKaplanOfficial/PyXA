from typing import Any, Union

import AppKit


class XAProtocol():
    """A meta-class for protocols that other classes can adhere to.
    """


class XAShowable(XAProtocol):
    """A protocol for classes that can be shown via a :func:`show` method.

    .. versionchanged:: 0.0.8
       Moved from XABase into XAProtocols

    .. versionadded:: 0.0.1
    """

    def show(self) -> 'XAShowable':
        """Shows the object.

        Child classes of XAShowable should redefine this method as necessary.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAShowable

        .. versionadded:: 0.0.1
        """
        self.xa_elem.show()
        return self


class XASelectable(XAProtocol):
    """A protocol for classes that can be selected via a :func:`select` method.
    
    .. versionchanged:: 0.0.8
       Moved from XABase into XAProtocols

    .. versionadded:: 0.0.1
    """
    def select(self) -> 'XASelectable':
        """Selects the object This may open a new window, depending on which kind of object and application it acts on.

        Child classes of XASelectable should redefine this method as necessary.

        :return: A reference to the PyXA object that called this method.
        :rtype: XASelectable

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()
        return self


class XADeletable(XAProtocol):
    """A protocol for classes that can be deleted via a :func:`delete` method.
    
    .. versionchanged:: 0.0.8
       Moved from XABase into XAProtocols

    .. versionadded:: 0.0.1
    """
    def delete(self):
        """Deletes the object.

        Child classes of XADeletable should redefine this method as necessary.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAShowable

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem.delete()


class XAPrintable(XAProtocol):
    """A protocol for classes that can be printed.

    .. versionadded:: 0.0.8
    """
    def print(self, print_properties: Union[dict, None] = None, show_dialog: bool = True) -> 'XAPrintable':
        """Prints the object.

        Child classes of XAPrintable should override this method as necessary.

        :param show_dialog: Whether to show the print dialog, defaults to True
        :type show_dialog: bool, optional
        :param print_properties: Properties to set for printing, defaults to None
        :type print_properties: Union[dict, None], optional
        :return: A reference to the PyXA object that called this method.
        :rtype: XACanPrintPath

        .. versionadded:: 0.0.8
        """
        if print_properties is None:
            print_properties = {}
        self.xa_elem.printWithProperties_printDialog_(self.xa_elem, show_dialog, print_properties)
        return self


class XACloseable(XAProtocol):
    def close(self, save: 'XACloseable.SaveOption' = None, location: Union[str, None] = None):
        """Closes the object.

        Child classes of XACloseable should override this method as necessary.

        .. versionadded:: 0.0.8
        """
        if save is None:
            save = 1852776480
        else:
            save = save.value
        self.xa_elem.closeSaving_savingIn_(save, AppKit.NSURL.alloc().initFileURLWithPath_(location))


class XAClipboardCodable(XAProtocol):
    """A protocol for classes that can be copied to the clipboard.

    .. versionadded:: 0.0.8
    """
    def get_clipboard_representation(self) -> Any:
        """Gets a clipboard-codable representation of the object.

        This method should be overriden where reasonable in child classes of XAClipboardCodable.

        :return: The clipboard-codable form of the content
        :rtype: Any
        """
        return str(self)


class XACanOpenPath(XAProtocol):
    """A protocol for classes that can open an item at a given path (either in its default application or in an application whose PyXA object extends this class).

    .. versionchanged:: 0.0.8
       Moved from XABase into XAProtocols

    .. versionadded:: 0.0.1
    """
    def open(self, target: str) -> Any:
        """Opens the file/website at the given filepath/URL.

        Child classes of XACanOpenPath should redefine this method as necessary.

        :param target: The path to a file or the URL to a website to open.
        :type target: str
        :return: A reference to the opened document or element, or None if no document/element was created or it cannot be found
        :rtype: Any

        .. versionadded:: 0.0.1
        """
        target = AppKit.NSURL.alloc().initFileURLWithPath_(target)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([target], self.xa_elem.bundleIdentifier(), 0, None, None)


class XACanPrintPath(XAProtocol):
    """A protocol for classes that can print a file at a given path (either in its default application or in an application whose PyXA object extends this class).

    .. versionchanged:: 0.0.8
       Moved from XABase into XAProtocols

    .. versionadded:: 0.0.1
    """
    def print(self, target: str) -> 'XACanPrintPath':
        """Prints the file/website at the given filepath/URL.

        Child classes of XACanPrintPath should redefine this method as necessary.

        :param target: The path to a file or the URL to a website to print.
        :type target: str
        :return: A reference to the PyXA object that called this method.
        :rtype: XACanPrintPath

        .. versionadded:: 0.0.1
        """
        if target.startswith("/"):
            target = AppKit.NSURL.alloc().initFileURLWithPath_(target)
        else:
            target = AppKit.NSURL.alloc().initWithString_(target)
        self.xa_elem.print_(target)
        return self