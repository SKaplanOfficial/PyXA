Automator Module
================

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
########
PyXA supports all of Automator's OSA features, including but not limited to creating and executing workflows, managing Automator actions and their settings, and interacting with execution return values. PyXA can create workflows and variables, assign and arrange actions, and modify the attributes thereof. PyXA can also observe the execution of  workflow files, allowing you to use existing automation workflows aongside PyXA and Python in general.

Automator Tutorials
###################
There is currently one tutorial for the Automator module:

.. toctree::
   :maxdepth: 1

   tutorial1

Automator Examples
##################
The examples below provide an overview of the capabilities of the Automator module.

Example 1 - Creating workflows from scratch
*******************************************

The example below creates a workflow that displays a notification, waits five seconds, then starts the screen saver. The process for creating workflows begins with making a new workflow object, adding it to the list of workflows, and saving it to the disk. Without saving here, you may encounter errors as some methods and actions require access to the workflow file. With an empty workflow created, the next step is to add actions, which is most easily done by name. Next, you must retrieve a mutable form of the actions; you can think of the original ones as a template that you've now made a copy of. From there, you can change the value of settings however you desire.

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.Application("Automator")

   # Create and save a new workflow
   new_workflow = app.make("workflow", {"name": "New Workflow"})
   app.workflows().push(new_workflow)
   new_workflow.save()

   # Add actions to the workflow
   action1 = app.automator_actions().by_name("Display Notification")
   action2 = app.automator_actions().by_name("Pause")
   action3 = app.automator_actions().by_name("Start Screen Saver")
   app.add(action1, new_workflow)
   app.add(action2, new_workflow)
   app.add(action3, new_workflow)

   # Obtain actions in mutable form and change their settings
   actions = new_workflow.automator_actions()
   notification_text = actions[0].settings().by_name("title")
   notification_text.set_property("value", "PyXA Notification")

   pause_duration = actions[1].settings().by_name("pauseDuration")
   pause_duration.set_property("value", 5)

   # Run the workflow
   new_workflow.execute()

Example 2 - Running existing workflows
**************************************

In the short example below, we open an existing workflow file, run it, and display the execution's results.

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.Application("Automator")

   app.open("/Users/exampleuser/Downloads/Example.workflow")
   workflow = app.workflows().by_name("Example.workflow")
   workflow.execute()

   print(workflow.execution_result)

Automator Resources
###################
- `Automator User Guide - Apple Support <https://support.apple.com/guide/automator/welcome/mac>`_

For all classes, methods, and inherited members of the Automator module, see the :ref:`Automator Module Reference`.