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

Calculator Tutorials
####################
There are currently no tutorials for working with the Calculator application.

Calculator Examples
###################
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

For all classes, methods, and inherited members of the Calculator module, see the :ref:`Calculator Module Reference`.