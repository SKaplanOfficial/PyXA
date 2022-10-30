""".. versionadded:: 0.1.0

Control Flow using JXA-like syntax.
"""

from datetime import timedelta

from PyXA import XABaseScriptable

class XAFlowApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Flow.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def start(self) -> str:
        """Starts or resumes the current session.

        :return: The name of the current session
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.start()

    def stop(self) -> str:
        """Stops the current session.

        :return: The name of the stopped session
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.stop()

    def skip(self) -> str:
        """Skips the current session.

        :return: The name of the next pending session.
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.skip()

    def previous(self) -> str:
        """Reloads the current or previous session.

        :return: The name of the next pending session
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.previous()

    def reset(self) -> str:
        """Resets the session progress.

        :return: The name of the next pending session
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.reset()

    def show(self) -> str:
        """Shows the Flow app window.

        :return: The name of the current session
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.show()

    def hide(self) -> str:
        """Hides the Flow app window.

        :return: The name of the current session
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.hide()

    def get_phase(self) -> str:
        """Gets the current phase (e.g. Flow or Break)

        :return: The name of the current session
        :rtype: str

        .. versionadded:: 0.1.0
        """
        return self.xa_scel.getPhase()

    def get_time(self) -> timedelta:
        """Gets the remaining time of the current session.

        :return: The remaining time of the current session
        :rtype: timedelta

        .. versionadded:: 0.1.0
        """
        time_strs = self.xa_scel.getTime().split(":")
        return timedelta(minutes=int(time_strs[0]), seconds=int(time_strs[1]))