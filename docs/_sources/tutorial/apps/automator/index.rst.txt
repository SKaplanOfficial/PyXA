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

   tutorials/automator/tutorial1

Automator Examples
##################
The examples below provide an overview of the capabilities of the Automator module.

Example 1 - Creating workflows from scratch
*******************************************

The example below creates a workflow that displays a notification, waits five seconds, then starts the screen saver. The process for creating workflows begins with making a new workflow object, adding it to the list of workflows, and saving it to the disk. Without saving here, you may encounter errors as some methods and actions require access to the workflow file. With an empty workflow created, the next step is to add actions, which is most easily done by name. Next, you must retrieve a mutable form of the actions; you can think of the original ones as a template that you've now made a copy of. From there, you can change the value of settings however you desire.

.. code-block:: python
   :linenos:

   import PyXA
   app = PyXA.application("Automator")

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
   app = PyXA.application("Automator")

   app.open("/Users/exampleuser/Downloads/Example.workflow")
   workflow = app.workflows().by_name("Example.workflow")
   workflow.execute()

   print(workflow.execution_result)

Automator Resources
###################
- `Automator User Guide - Apple Support <https://support.apple.com/guide/automator/welcome/mac>`_

Automator Classes and Methods
#############################
   
Classes
*******

.. autosummary:: PyXA.apps.Automator
   :nosignatures:

    ~PyXA.apps.Automator.XAAutomatorApplication
    ~PyXA.apps.Automator.XAAutomatorDocumentList
    ~PyXA.apps.Automator.XAAutomatorDocument
    ~PyXA.apps.Automator.XAAutomatorActionList
    ~PyXA.apps.Automator.XAAutomatorAction
    ~PyXA.apps.Automator.XAAutomatorRequiredResourceList
    ~PyXA.apps.Automator.XAAutomatorRequiredResource
    ~PyXA.apps.Automator.XAAutomatorSettingList
    ~PyXA.apps.Automator.XAAutomatorSetting
    ~PyXA.apps.Automator.XAAutomatorVariableList
    ~PyXA.apps.Automator.XAAutomatorVariable
    ~PyXA.apps.Automator.XAAutomatorWorkflowList
    ~PyXA.apps.Automator.XAAutomatorWorkflow
    ~PyXA.apps.Automator.XAAutomatorWindow

XAAutomatorApplication Enums
****************************

.. autosummary:: PyXA.apps.Automator.XAAutomatorApplication
   :nosignatures:

   ~PyXA.apps.Automator.XAAutomatorApplication.SaveOption
   ~PyXA.apps.Automator.XAAutomatorApplication.WarningLevel
   ~PyXA.apps.Automator.XAAutomatorApplication.PrintErrorHandling

XAAutomatorApplication Methods
******************************

.. autosummary:: PyXA.apps.Automator.XAAutomatorApplication
   :nosignatures:

   ~PyXA.apps.Automator.XAAutomatorApplication.add
   ~PyXA.apps.Automator.XAAutomatorApplication.documents
   ~PyXA.apps.Automator.XAAutomatorApplication.automator_actions
   ~PyXA.apps.Automator.XAAutomatorApplication.variables
   ~PyXA.apps.Automator.XAAutomatorApplication.workflows
   ~PyXA.apps.Automator.XAAutomatorApplication.make

XAAutomatorDocumentList Methods
*******************************

.. autosummary:: PyXA.apps.Automator.apps.XAAutomatorDocumentList
   :nosignatures:
   
   ~PyXA.apps.Automator.XAAutomatorDocumentList.id
   ~PyXA.apps.Automator.XAAutomatorDocumentList.title
   ~PyXA.apps.Automator.XAAutomatorDocumentList.index
   ~PyXA.apps.Automator.XAAutomatorDocumentList.by_id
   ~PyXA.apps.Automator.XAAutomatorDocumentList.by_title
   ~PyXA.apps.Automator.XAAutomatorDocumentList.by_index

XAAutomatorActionList Methods
*****************************
   
.. autosummary:: PyXA.apps.Automator.XAAutomatorActionList
   :nosignatures:

   ~PyXA.apps.Automator.XAAutomatorActionList.bundle_id
   ~PyXA.apps.Automator.XAAutomatorActionList.category
   ~PyXA.apps.Automator.XAAutomatorActionList.comment
   ~PyXA.apps.Automator.XAAutomatorActionList.enabled
   ~PyXA.apps.Automator.XAAutomatorActionList.execution_error_message
   ~PyXA.apps.Automator.XAAutomatorActionList.execution_error_number
   ~PyXA.apps.Automator.XAAutomatorActionList.execution_result
   ~PyXA.apps.Automator.XAAutomatorActionList.icon_name
   ~PyXA.apps.Automator.XAAutomatorActionList.ignores_input
   ~PyXA.apps.Automator.XAAutomatorActionList.index
   ~PyXA.apps.Automator.XAAutomatorActionList.input_types
   ~PyXA.apps.Automator.XAAutomatorActionList.keywords
   ~PyXA.apps.Automator.XAAutomatorActionList.name
   ~PyXA.apps.Automator.XAAutomatorActionList.output_types
   ~PyXA.apps.Automator.XAAutomatorActionList.parent_workflow
   ~PyXA.apps.Automator.XAAutomatorActionList.path
   ~PyXA.apps.Automator.XAAutomatorActionList.show_action_when_run
   ~PyXA.apps.Automator.XAAutomatorActionList.target_application
   ~PyXA.apps.Automator.XAAutomatorActionList.version
   ~PyXA.apps.Automator.XAAutomatorActionList.warning_action
   ~PyXA.apps.Automator.XAAutomatorActionList.warning_level
   ~PyXA.apps.Automator.XAAutomatorActionList.warning_message
   ~PyXA.apps.Automator.XAAutomatorActionList.by_bundle_id
   ~PyXA.apps.Automator.XAAutomatorActionList.by_category
   ~PyXA.apps.Automator.XAAutomatorActionList.by_comment
   ~PyXA.apps.Automator.XAAutomatorActionList.by_enabled
   ~PyXA.apps.Automator.XAAutomatorActionList.by_execution_error_message
   ~PyXA.apps.Automator.XAAutomatorActionList.by_execution_error_number
   ~PyXA.apps.Automator.XAAutomatorActionList.by_execution_result
   ~PyXA.apps.Automator.XAAutomatorActionList.by_icon_name
   ~PyXA.apps.Automator.XAAutomatorActionList.by_id
   ~PyXA.apps.Automator.XAAutomatorActionList.by_ignores_input
   ~PyXA.apps.Automator.XAAutomatorActionList.by_input_types
   ~PyXA.apps.Automator.XAAutomatorActionList.by_keywords
   ~PyXA.apps.Automator.XAAutomatorActionList.by_name
   ~PyXA.apps.Automator.XAAutomatorActionList.by_output_types
   ~PyXA.apps.Automator.XAAutomatorActionList.by_parent_workflow
   ~PyXA.apps.Automator.XAAutomatorActionList.by_path
   ~PyXA.apps.Automator.XAAutomatorActionList.by_show_action_when_run
   ~PyXA.apps.Automator.XAAutomatorActionList.by_target_application
   ~PyXA.apps.Automator.XAAutomatorActionList.by_version
   ~PyXA.apps.Automator.XAAutomatorActionList.by_warning_action
   ~PyXA.apps.Automator.XAAutomatorActionList.by_warning_level
   ~PyXA.apps.Automator.XAAutomatorActionList.by_warning_message

XAAutomatorAction Methods
*************************
   
.. autosummary:: PyXA.apps.Automator.XAAutomatorAction
   :nosignatures:

   ~PyXA.apps.Automator.XAAutomatorAction.required_resources
   ~PyXA.apps.Automator.XAAutomatorAction.settings

XAAutomatorRequiredResourceList Methods
***************************************

.. autosummary:: PyXA.apps.Automator.XAAutomatorRequiredResourceList
   :nosignatures:

   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.kind
   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.name
   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.resource
   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.version
   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.by_kind
   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.by_name
   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.by_resource
   ~PyXA.apps.Automator.XAAutomatorRequiredResourceList.by_version

XAAutomatorSettingList Methods
******************************

.. autosummary:: PyXA.apps.Automator.XAAutomatorSettingList
   :nosignatures:
   
   ~PyXA.apps.Automator.XAAutomatorSettingList.default_value
   ~PyXA.apps.Automator.XAAutomatorSettingList.name
   ~PyXA.apps.Automator.XAAutomatorSettingList.value
   ~PyXA.apps.Automator.XAAutomatorSettingList.by_default_value
   ~PyXA.apps.Automator.XAAutomatorSettingList.by_name
   ~PyXA.apps.Automator.XAAutomatorSettingList.by_value

XAAutomatorVariableList Methods
*******************************

.. autosummary:: PyXA.apps.Automator.XAAutomatorVariableList
   :nosignatures:
   
   ~PyXA.apps.Automator.XAAutomatorVariableList.name
   ~PyXA.apps.Automator.XAAutomatorVariableList.settable
   ~PyXA.apps.Automator.XAAutomatorVariableList.value
   ~PyXA.apps.Automator.XAAutomatorVariableList.by_name
   ~PyXA.apps.Automator.XAAutomatorVariableList.by_settable
   ~PyXA.apps.Automator.XAAutomatorVariableList.by_value

XAAutomatorWorkflowList Methods
*******************************

.. autosummary:: PyXA.apps.Automator.XAAutomatorWorkflowList
   :nosignatures:
   
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.current_action
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.execution_error_message
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.execution_error_number
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.execution_id
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.execution_result
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.name
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.by_current_action
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.by_execution_error_message
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.by_execution_error_number
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.by_execution_id
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.by_execution_result
   ~PyXA.apps.Automator.XAAutomatorWorkflowList.by_name

XAAutomatorWorkflow Methods
***************************

.. autosummary:: PyXA.apps.Automator.XAAutomatorWorkflow
   :nosignatures:
   
   ~PyXA.apps.Automator.XAAutomatorWorkflow.automator_actions
   ~PyXA.apps.Automator.XAAutomatorWorkflow.execute
   ~PyXA.apps.Automator.XAAutomatorWorkflow.variables
   ~PyXA.apps.Automator.XAAutomatorWorkflow.delete
   ~PyXA.apps.Automator.XAAutomatorWorkflow.save

For all classes, methods, and inherited members on one page, see the :ref:`Automator Module Reference`