Calculator Module Overview
==========================

.. contents:: Table of Contents
   :depth: 3
   :local:

PyXA enables limited scripting functionalities in Calculator.app, despite no official scripting support for it. Currently, the calculator's scripting functionalities are entirely supported by UI scripting, however additional features are planned for future development work.

Using :func:`XACalculatorApplication.input`, you can command the Calculator to execute a sequence of button clicks. The sequence must be a continuous string (no spaces). The valid characters are numbers `0-9`, `+`, `-`, `*`, `/`, `%`, `~`, `=`, and `c`. Their meanings are as follows:

   - `+`, `-`, `*`, and `/` correspond to their usual operation buttons.
   - `%` designates the percentage button.
   - `~` corresponds to the negation button.
   - `=` represents the equals button.
   - `c` denotes the clear button.

Tutorials
#########
There are currently no tutorials for working with the Calculator application.

Examples
########
The examples below provide an overview of the capabilities of the Calculator module. They do not provide any output.
.. For more in-depth examples that show output and provide more detailed explanations, refer to the previous section (:ref:`Tutorials`).

Example 1 - Performing Operations in Calculator.app
***************************************************

This example uses :func:`XACalculatorApplication.input` to calculate the result of an expression, then retrieves the result using :func:`XACalculatorApplication.current_value`.

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.application("Calculator")
   app.input("3.14159265*2*3*5*5*5=")
   x = app.current_value()
   print(x)

Calculator Resources
####################
- `Calculator User Guide - Apple Support <https://support.apple.com/guide/calculator/welcome/mac>`_

Calculator Classes and Methods
##############################

Classes
*******
   
.. autosummary:: PyXA.apps.Calculator
   :nosignatures:

   ~PyXA.apps.Calculator.XACalculatorApplication

XACalculatorApplication Methods
*******************************

.. autosummary:: PyXA.apps.Calculator.XACalculatorApplication
   :nosignatures:

   ~PyXA.apps.Calculator.XACalculatorApplication.open_about_panel
   ~PyXA.apps.Calculator.XACalculatorApplication.save_tape
   ~PyXA.apps.Calculator.XACalculatorApplication.open_page_setup
   ~PyXA.apps.Calculator.XACalculatorApplication.print_tape
   ~PyXA.apps.Calculator.XACalculatorApplication.copy_value
   ~PyXA.apps.Calculator.XACalculatorApplication.show_basic_calculator
   ~PyXA.apps.Calculator.XACalculatorApplication.show_scientific_calculator
   ~PyXA.apps.Calculator.XACalculatorApplication.show_programmer_calculator
   ~PyXA.apps.Calculator.XACalculatorApplication.toggle_thousands_separators
   ~PyXA.apps.Calculator.XACalculatorApplication.toggle_RPN_mode
   ~PyXA.apps.Calculator.XACalculatorApplication.show_paper_tape
   ~PyXA.apps.Calculator.XACalculatorApplication.show_help
   ~PyXA.apps.Calculator.XACalculatorApplication.clear_value
   ~PyXA.apps.Calculator.XACalculatorApplication.input
   ~PyXA.apps.Calculator.XACalculatorApplication.current_value

For all classes, methods, and inherited members on one page, see the :ref:`Calculator Module Reference`