Messages Module Overview
========================

.. contents:: Table of Contents
   :depth: 3
   :local:

PyXA supports all of the OSA features for Messages.app.

Messages Tutorials
##################
There are currently no tutorials for the Messages module.

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

Classes
*******
   
.. autosummary:: PyXA.apps.Messages
   :nosignatures:

   ~PyXA.apps.Messages.XAMessagesApplication
   ~PyXA.apps.Messages.XAMessagesDocumentList
   ~PyXA.apps.Messages.XAMessagesDocument
   ~PyXA.apps.Messages.XAMessagesChatList
   ~PyXA.apps.Messages.XAMessagesChat
   ~PyXA.apps.Messages.XAMessagesFileTransferList
   ~PyXA.apps.Messages.XAMessagesFileTransfer
   ~PyXA.apps.Messages.XAMessagesParticipantList
   ~PyXA.apps.Messages.XAMessagesParticipant
   ~PyXA.apps.Messages.XAMessagesAccountList
   ~PyXA.apps.Messages.XAMessagesAccount
   ~PyXA.apps.Messages.XAMessagesWindow

XAMessagesApplication Enums
***************************
   
.. autosummary:: PyXA.apps.Messages.XAMessagesApplication
   :nosignatures:

   ~PyXA.apps.Messages.XAMessagesApplication.SaveOption
   ~PyXA.apps.Messages.XAMessagesApplication.PrintErrorHandling
   ~PyXA.apps.Messages.XAMessagesApplication.ServiceType
   ~PyXA.apps.Messages.XAMessagesApplication.TransferStatus
   ~PyXA.apps.Messages.XAMessagesApplication.ConnectionStatus

XAMessagesApplication Methods
*****************************
   
.. autosummary:: PyXA.apps.Messages.XAMessagesApplication
   :nosignatures:

   ~PyXA.apps.Messages.XAMessagesApplication.send
   ~PyXA.apps.Messages.XAMessagesApplication.print
   ~PyXA.apps.Messages.XAMessagesApplication.documents
   ~PyXA.apps.Messages.XAMessagesApplication.chats
   ~PyXA.apps.Messages.XAMessagesApplication.participants
   ~PyXA.apps.Messages.XAMessagesApplication.accounts
   ~PyXA.apps.Messages.XAMessagesApplication.file_transfers

XAMessagesDocumentList Methods
******************************
   
.. autosummary:: PyXA.apps.Messages.XAMessagesDocumentList
   :nosignatures:
   
   ~PyXA.apps.Messages.XAMessagesDocumentList.name
   ~PyXA.apps.Messages.XAMessagesDocumentList.modified
   ~PyXA.apps.Messages.XAMessagesDocumentList.file
   ~PyXA.apps.Messages.XAMessagesDocumentList.by_name
   ~PyXA.apps.Messages.XAMessagesDocumentList.by_modified
   ~PyXA.apps.Messages.XAMessagesDocumentList.by_file

XAMessagesChatList Methods
**************************

.. autosummary:: PyXA.apps.Messages.XAMessagesChatList
   :nosignatures:

   ~PyXA.apps.Messages.XAMessagesChatList.id
   ~PyXA.apps.Messages.XAMessagesChatList.name
   ~PyXA.apps.Messages.XAMessagesChatList.account
   ~PyXA.apps.Messages.XAMessagesChatList.participants
   ~PyXA.apps.Messages.XAMessagesChatList.by_id
   ~PyXA.apps.Messages.XAMessagesChatList.by_name
   ~PyXA.apps.Messages.XAMessagesChatList.by_account
   ~PyXA.apps.Messages.XAMessagesChatList.by_participants

XAMessagesChat Methods
**********************

.. autosummary:: PyXA.apps.Messages.XAMessagesChat
   :nosignatures:
   
   ~PyXA.apps.Messages.XAMessagesChat.send
   ~PyXA.apps.Messages.XAMessagesChat.participants

XAMessagesFileTransferList Methods
**********************************

.. autosummary:: PyXA.apps.Messages.XAMessagesFileTransferList
   :nosignatures:

   ~PyXA.apps.Messages.XAMessagesFileTransferList.id
   ~PyXA.apps.Messages.XAMessagesFileTransferList.name
   ~PyXA.apps.Messages.XAMessagesFileTransferList.file_path
   ~PyXA.apps.Messages.XAMessagesFileTransferList.direction
   ~PyXA.apps.Messages.XAMessagesFileTransferList.account
   ~PyXA.apps.Messages.XAMessagesFileTransferList.participant
   ~PyXA.apps.Messages.XAMessagesFileTransferList.file_size
   ~PyXA.apps.Messages.XAMessagesFileTransferList.file_progress
   ~PyXA.apps.Messages.XAMessagesFileTransferList.transfer_status
   ~PyXA.apps.Messages.XAMessagesFileTransferList.started
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_id
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_name
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_file_path
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_direction
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_account
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_participant
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_file_size
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_file_progress
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_transfer_status
   ~PyXA.apps.Messages.XAMessagesFileTransferList.by_started

XAMessagesParticipantList Methods
*********************************

.. autosummary:: PyXA.apps.Messages.XAMessagesParticipantList
   :nosignatures:
   
   ~PyXA.apps.Messages.XAMessagesParticipantList.id
   ~PyXA.apps.Messages.XAMessagesParticipantList.account
   ~PyXA.apps.Messages.XAMessagesParticipantList.name
   ~PyXA.apps.Messages.XAMessagesParticipantList.handle
   ~PyXA.apps.Messages.XAMessagesParticipantList.first_name
   ~PyXA.apps.Messages.XAMessagesParticipantList.last_name
   ~PyXA.apps.Messages.XAMessagesParticipantList.full_name
   ~PyXA.apps.Messages.XAMessagesParticipantList.by_id
   ~PyXA.apps.Messages.XAMessagesParticipantList.by_account
   ~PyXA.apps.Messages.XAMessagesParticipantList.by_name
   ~PyXA.apps.Messages.XAMessagesParticipantList.by_handle
   ~PyXA.apps.Messages.XAMessagesParticipantList.by_first_name
   ~PyXA.apps.Messages.XAMessagesParticipantList.by_last_name
   ~PyXA.apps.Messages.XAMessagesParticipantList.by_full_name

XAMessagesAccountList Methods
*****************************

.. autosummary:: PyXA.apps.Messages.XAMessagesAccountList
   :nosignatures:
   
   ~PyXA.apps.Messages.XAMessagesAccountList.id
   ~PyXA.apps.Messages.XAMessagesAccountList.object_description
   ~PyXA.apps.Messages.XAMessagesAccountList.enabled
   ~PyXA.apps.Messages.XAMessagesAccountList.connection_status
   ~PyXA.apps.Messages.XAMessagesAccountList.service_type
   ~PyXA.apps.Messages.XAMessagesAccountList.by_id
   ~PyXA.apps.Messages.XAMessagesAccountList.by_object_description
   ~PyXA.apps.Messages.XAMessagesAccountList.by_enabled
   ~PyXA.apps.Messages.XAMessagesAccountList.by_connection_status
   ~PyXA.apps.Messages.XAMessagesAccountList.by_service_type

XAMessagesAccount Methods
*************************

.. autosummary:: PyXA.apps.Messages.XAMessagesAccount
   :nosignatures:
   
   ~PyXA.apps.Messages.XAMessagesAccount.chats
   ~PyXA.apps.Messages.XAMessagesAccount.participants

For all classes, methods, and inherited members on one page, see the :ref:`Messages Module Reference`