""".. versionadded:: 0.0.6

Control the macOS Stocks application using JXA-like syntax.
"""

from curses import nonl
from typing import List, Literal, Union
from AppKit import NSPredicate, NSMutableArray

from PyXA import XABase
from PyXA import XABaseScriptable

class XAStocksApplication(XABase.XAApplication):
    """A class for managing and interacting with Stocks.app.

    .. seealso:: :class:`XAStocksSavedStock`

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.sidebar_showing: bool #: Whether the sidebar is currently showing

    @property
    def sidebar_showing(self) -> bool:
        sidebar = self.front_window().xa_elem.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].groups()[1]
        return sidebar.get() is not None

    def show_symbol(self, ticker: str) -> 'XAStocksApplication':
        """Displays the page for the specified ticker symbol.

        :param ticker: The ticker symbol for the desired stock
        :type ticker: str
        :return: A reference to the application object
        :rtype: XAStocksApplication

        .. versionadded:: 0.0.6
        """
        XABase.XAURL("stocks://?symbol=" + ticker).open()

    def go_back(self) -> 'XAStocksApplication':
        """Clicks the 'back' button (from a new article when viewed in the Stocks app).

        :return: A reference to the application object
        :rtype: XAStocksApplication

        .. versionadded:: 0.0.6
        """
        self.front_window().toolbars()[0].buttons()[0].actions()[0].perform()
        return self

    def show_business_news(self) -> 'XAStocksApplication':
        """Shows the 'Business News' tab in the front stock window.

        :return: A reference to the application object
        :rtype: XAStocksApplication

        .. versionadded:: 0.0.6
        """
        self.front_window().groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(1).groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(0).groups().at(1).groups().at(0).groups().at(0).groups().at(1).groups().at(0).ui_elements().at(2).buttons().at(0).actions()[0].perform()

    def new_tab(self):
        """Opens a new tab.

        .. versionadded:: 0.0.6
        """
        predicate = NSPredicate.predicateWithFormat_("name == %@", "AXPress")
        press_action = self.front_window().xa_elem.tabGroups()[0].buttons()[0].actions().filteredArrayUsingPredicate_(predicate)[0]
        press_action.perform()

    def saved_stocks(self) -> 'XAStocksSavedStockList':
        """Gets a list of stocks.

        :return: The list of stocks
        :rtype: XAStocksStockList

        .. versionadded:: 0.0.6
        """
        stock_element_list = self.front_window().xa_elem.groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[0].groups()[1].groups()[0].groups()[0].groups()[1].groups()[0].groups()

        stocks = []
        def add_stock(element, index, stop):
            nonlocal stocks
            groups = element.groups()
            if len(groups) == 1:
                stocks.append(groups[0].UIElements()[0])

        stock_element_list.enumerateObjectsUsingBlock_(add_stock)

        return self._new_element(NSMutableArray.alloc().initWithArray_(stocks), XAStocksSavedStockList)




class XAStocksSavedStockList(XABase.XAList):
    """A wrapper around a list of stocks.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAStocksSavedStock, filter)

    def properties(self) -> List[str]:
        return self.xa_elem.arrayByApplyingSelector_("properties")

    def name(self) -> List[str]:
        return [x.name for x in self]

    def symbol(self) -> List[str]:
        return [x.symbol for x in self]

    def price(self) -> List[str]:
        return [x.price for x in self]

    def change(self) -> List[str]:
        return [x.change for x in self]

    def selected(self) -> List[str]:
        ls = self.xa_elem.arrayByApplyingSelector_("selected")
        return [x.get() for x in ls]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.object_description()) + ">"

class XAStocksSavedStock(XABase.XAObject):
    """A class for interacting with stocks in Stocks.app.

    .. versionadded:: 0.0.6
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.properties: dict #: All properties of the stock
        self.name: str #: The name of the stock (The company name)
        self.symbol: str #: The symbol for the stock
        self.price: float #: The current price of the stock
        self.change: str #: The percentage or point change of the stock in the current trading session
        self.selected: bool #: Whether the stock is the currently selected stock

    @property
    def properties(self) -> dict:
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        reversed = self.xa_elem.objectDescription().get()[::-1]
        return reversed[reversed.index(",") + 1:][::-1]

    @property
    def symbol(self) -> str:
        return self.xa_elem.objectDescription().get().split(", ")[-1]

    @property
    def price(self) -> float:
        value = self.xa_elem.value().get()
        value = value.replace("selected, ", "")
        return float(value.split(", ")[0].replace(",", ""))

    @property
    def change(self) -> str:
        value = self.xa_elem.value().get()
        return value.split(", ")[-1]

    @property
    def selected(self) -> bool:
        return self.xa_elem.selected().get()

    def show(self):
        """Shows the stock's tab in the front stock window.

        .. versionadded:: 0.0.6
        """
        self.xa_elem.actions()[0].perform()