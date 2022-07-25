Messages Module
===============

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
########
PyXA supports all of Automator's OSA features, including but not limited to creating and executing workflows, managing Automator actions and their settings, and interacting with execution return values. PyXA can create workflows and variables, assign and arrange actions, and modify the attributes thereof. PyXA can also observe the execution of  workflow files, allowing you to use existing automation workflows aongside PyXA and Python in general.

Messages Tutorials
##################
There are currently no tutorials for the Automator module.

Messages Examples
#################
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

Messages Resources
##################
- `Messages User Guide - Apple Support <https://support.apple.com/guide/messages/welcome/mac`_

Messages Classes and Methods
############################
.. toctree::
   :maxdepth: 1
   :caption: Classes

   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication
   ../api/apps/messages/XAMessagesDocumentList/PyXA.apps.Messages.XAMessagesDocumentList
   ../api/apps/messages/XAMessagesDocument/PyXA.apps.Messages.XAMessagesDocument
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList
   ../api/apps/messages/XAMessagesChat/PyXA.apps.Messages.XAMessagesChat
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList
   ../api/apps/messages/XAMessagesFileTransfer/PyXA.apps.Messages.XAMessagesFileTransfer
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList
   ../api/apps/messages/XAMessagesParticipant/PyXA.apps.Messages.XAMessagesParticipant
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList
   ../api/apps/messages/XAMessagesAccount/PyXA.apps.Messages.XAMessagesAccount
   ../api/apps/messages/XAMessagesWindow/PyXA.apps.Messages.XAMessagesWindow

.. toctree::
   :maxdepth: 1
   :caption: Methods

   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.send
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.print
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.documents
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.chats
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.participants
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.accounts
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.file_transfers

.. toctree::
   :maxdepth: 1
   
   ../api/apps/messages/XAMessagesDocumentList/PyXA.apps.Messages.XAMessagesDocumentList.name
   ../api/apps/messages/XAMessagesDocumentList/PyXA.apps.Messages.XAMessagesDocumentList.modified
   ../api/apps/messages/XAMessagesDocumentList/PyXA.apps.Messages.XAMessagesDocumentList.file
   ../api/apps/messages/XAMessagesDocumentList/PyXA.apps.Messages.XAMessagesDocumentList.by_name
   ../api/apps/messages/XAMessagesDocumentList/PyXA.apps.Messages.XAMessagesDocumentList.by_modified
   ../api/apps/messages/XAMessagesDocumentList/PyXA.apps.Messages.XAMessagesDocumentList.by_file

.. toctree::
   :maxdepth: 1

   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.id
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.name
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.account
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.participants
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.by_id
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.by_name
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.by_account
   ../api/apps/messages/XAMessagesChatList/PyXA.apps.Messages.XAMessagesChatList.by_participants

.. toctree::
   :maxdepth: 1
   
   ../api/apps/messages/XAMessagesChat/PyXA.apps.Messages.XAMessagesChat.send
   ../api/apps/messages/XAMessagesChat/PyXA.apps.Messages.XAMessagesChat.participants

.. toctree::
   :maxdepth: 1

   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.id
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.name
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.file_path
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.direction
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.account
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.participant
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.file_size
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.file_progress
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.transfer_status
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.started
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_id
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_name
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_file_path
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_direction
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_account
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_participant
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_file_size
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_file_progress
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_transfer_status
   ../api/apps/messages/XAMessagesFileTransferList/PyXA.apps.Messages.XAMessagesFileTransferList.by_started

.. toctree::
   :maxdepth: 1
   
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.id
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.account
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.name
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.handle
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.first_name
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.last_name
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.full_name
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.by_id
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.by_account
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.by_name
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.by_handle
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.by_first_name
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.by_last_name
   ../api/apps/messages/XAMessagesParticipantList/PyXA.apps.Messages.XAMessagesParticipantList.by_full_name

.. toctree::
   :maxdepth: 1
   
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.id
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.object_description
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.enabled
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.connection_status
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.service_type
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.by_id
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.by_object_description
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.by_enabled
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.by_connection_status
   ../api/apps/messages/XAMessagesAccountList/PyXA.apps.Messages.XAMessagesAccountList.by_service_type

.. toctree::
   :maxdepth: 1
   
   ../api/apps/messages/XAMessagesAccount/PyXA.apps.Messages.XAMessagesAccount.chats
   ../api/apps/messages/XAMessagesAccount/PyXA.apps.Messages.XAMessagesAccount.participants

.. toctree::
   :maxdepth: 1
   :caption: Enums

   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.SaveOption
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.PrintErrorHandling
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.ServiceType
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.TransferStatus
   ../api/apps/messages/XAMessagesApplication/PyXA.apps.Messages.XAMessagesApplication.ConnectionStatus

For all classes, methods, and inherited members on one page, see the :ref:`Complete Messages API`