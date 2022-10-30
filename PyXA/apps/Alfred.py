""".. versionadded:: 0.0.8

Control Alfred using JXA-like syntax.
"""

from PyXA import XABaseScriptable

class XAAlfredApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Alfred.app.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    def search(self, query: str):
        """Shows Alfred with the given search query

        :param query: The term(s) to search
        :type query: str

        .. versionadded:: 0.0.8
        """
        self.xa_scel.search_(query)

    def action(self, items: list[str]):
        """Shows Alfred actions for the given file/folder/item.

        :param items: A list of item paths
        :type items: list[str]

        .. versionadded:: 0.0.8
        """
        self.xa_scel.action_asType_(items, None)

    def run_workflow(self, workflow: str, trigger: str, argument: str):
        """Runs the given workflow with the specified trigger and argument.

        :param workflow: The workflow to run
        :type workflow: str
        :param trigger: The trigger to run the workflow with
        :type trigger: str
        :param argument: The argument to pass alongside the trigger
        :type argument: str

        .. versionadded:: 0.0.8
        """
        self.xa_scel.runTrigger_inWorkflow_withArgument_(trigger, workflow, argument)

    def reload_workflow(self, workflow_uid: str):
        """Reloads the workflow with the given UID or Bundle ID

        :param workflow: The UID or Bundle ID of the workflow to reload
        :type workflow: str

        .. versionadded:: 0.0.8
        """
        self.xa_scel.reloadWorkflow_(workflow_uid)

    def set_configuration(self, variable_name: str, value: str, workflow: str, exportable: bool = False):
        """Sets the workflow configuration variable with the given name.

        :param variable_name: The configuration variable to set
        :type variable_name: str
        :param value: The value to assign to the configuration variable
        :type value: str
        :param workflow: The bundle ID of the workflow to make the change in
        :type workflow: str
        :param exportable: Whether the variable is fine for export (whether the Don't Export box is unchecked), defaults to False
        :type exportable: bool, optional

        .. versionadded:: 0.0.8
        """
        self.xa_scel.setConfiguration_toValue_inWorkflow_exportable_(variable_name, value, workflow, exportable)

    def remove_configuration(self, variable_name: str, workflow: str):
        """Removes the workflow configuration variable with the given name.

        :param variable_name: The configuration variable to remove
        :type variable_name: str
        :param workflow: The bundle ID of the workflow to make the change in
        :type workflow: str

        .. versionadded:: 0.0.8
        """
        self.xa_scel.removeConfiguration_inWorkflow_(variable_name, workflow)

    def set_theme(self, theme_name: str):
        """Sets the Alfred theme to the given theme name.

        :param theme_name: The name of the desired theme
        :type theme_name: str

        .. versionadded:: 0.0.8
        """
        self.xa_scel.setTheme_(theme_name)