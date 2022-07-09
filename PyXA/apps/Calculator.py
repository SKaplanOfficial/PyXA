""".. versionadded:: 0.0.2

Control the macOS Calculator application using JXA-like syntax.
"""

from PyXA import XABase

class XACalculatorApplication(XABase.XAApplication):
    """A class for managing and interacting with Calculator.app.

    .. versionadded:: 0.0.2
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_btns = None

    def __load_buttons(self):
        """Loads references to primary buttons of the calculator.

        .. versionadded:: 0.0.2
        """
        buttons = self.front_window().groups()[-1].buttons()
        self.xa_btns = {
            "0": buttons[4],
            "1": buttons[5],
            "2": buttons[0],
            "3": buttons[2],
            "4": buttons[10],
            "5": buttons[7],
            "6": buttons[11],
            "7": buttons[15],
            "8": buttons[14],
            "9": buttons[3],
            ".": buttons[9],
            "+": buttons[12],
            "-": buttons[6],
            "*": buttons[8],
            "/": buttons[17],
            "%": buttons[13],
            "~": buttons[18],
            "=": buttons[1],
            "c": buttons[16],
        }

    ## Menu Bar
    # Calculator Menu
    def open_about_panel(self):
        """Opens the "About Calculator" panel. Mimics clicking File->About Calculator.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[1].menus()[0].menu_items()[0].press()

    # File Menu
    def save_tape(self):
        """Opens the "save tape" dialog. Mimics clicking File->Save Tape As...

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[2].menus()[0].menu_items()[2].press()

    def open_page_setup(self):
        """Opens the page setup dialog. Mimics clicking File->Page Setup...

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[2].menus()[0].menu_items()[4].press()

    def print_tape(self):
        """Opens the print tape dialog. Mimics clicking File->Print Tape...

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[2].menus()[0].menu_items()[5].press()

    # Edit Menu
    def copy_value(self):
        """Copies the current value of the calculator result. Mimics clicking Edit->Copy.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[3].menus()[0].menu_items()[4].press()

    # View Menu
    def show_basic_calculator(self):
        """Switches the view to the basic calculator. Mimics clicking View->Basic.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[4].menus()[0].menu_items()[0].press()

    def show_scientific_calculator(self):
        """Switches the view to the scientific calculator. Mimics clicking View->Scientific.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[4].menus()[0].menu_items()[1].press()

    def show_programmer_calculator(self):
        """Switches the view to the programmer calculator. Mimics clicking View->Programmer.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[4].menus()[0].menu_items()[2].press()

    def toggle_thousands_separators(self):
        """Toggles whether comma separators are shown at thousand intervals. Mimics clicking View->Show Thousands Separators.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[4].menus()[0].menu_items()[4].press()

    def toggle_RPN_mode(self):
        """Toggles Reverse Polish Notation. Mimics clicking View->RPN Mode.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[4].menus()[0].menu_items()[6].press()

    # Window Menu
    def show_paper_tape(self):
        """Opens the paper tape window. Mimics clicking Window->Show Paper Tape.

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[7].menus()[0].menu_items()[6].press()

    # Help Menu
    def show_help(self):
        """Opens the Calculator help window. Mimics clicking Help->Calculator Help.add()

        .. versionadded:: 0.0.2
        """
        self.menu_bars()[0].menu_bar_items()[8].menus()[0].menu_items()[1].press()

    # Actions
    def clear_value(self):
        """Clears the current calculator output. Mimics clicking the "C" (clear) button.

        .. versionadded:: 0.0.2
        """
        if self.xa_btns is None:
            self.__load_buttons()
        self.xa_btns["c"].press()

    def input(self, sequence: str):
        """Inputs a sequence of numbers and operations into the calculator by mimicking button clicks.

        This method does not obtain the result of the input. For that, use :func:`current_value`. 
        
        The sequence should be a continuous string (no spaces). The valid characters are numbers `0-9`, `+`, `-`, `*`, `/`, `%`, `~`, `=`, and `c`. Their meanings are as follows:

        - `+`, `-`, `*`, and `/` correspond to their usual operation buttons.
        - `%` designates the percentage button.
        - `~` corresponds to the negation button.
        - `=` represents the equals button.
        - `c` denotes the clear button.

        :param sequence: The sequence of numbers and operations to execute.
        :type sequence: str

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calculator")
        >>> app.input("c2*3.14*5*5=")
        34.54

        .. versionadded:: 0.0.2
        """
        if self.xa_btns is None:
            self.__load_buttons()
        for symbol in sequence:
            self.xa_btns[symbol].press()

    # Misc Methods
    def current_value(self) -> float:
        """Retrieves the current value of the calculator output.

        :return: The calculator's current displayed value
        :rtype: float

        .. versionadded:: 0.0.2
        """
        return float(self.front_window().groups()[0].static_texts()[0].value.get())