# tests/web/utils/alert_handler.py
from typing import Callable, Optional


class AlertHandler:
    def __init__(self, page):
        self.page = page

    def accept_next(self):
        """
        Sets up a listener to automatically accept the next dialog that appears.
        Useful for simple success messages or confirmations.
        """
        self.page.once("dialog", lambda dialog: dialog.accept())

    def dismiss_next(self):
        """
        Sets up a listener to automatically dismiss (cancel) the next dialog.
        """
        self.page.once("dialog", lambda dialog: dialog.dismiss())

    def get_text_and_accept(self, trigger_action: Callable) -> str:
        """
        Sets up a listener, executes the trigger action (like clicking a button),
        captures the dialog message, accepts the dialog, and returns the message.

        Args:
            trigger_action: A function/lambda that triggers the alert (e.g., lambda: self.page.click(btn))

        Returns:
            str: The text content of the alert.
        """
        dialog_message = []

        def handle_dialog(dialog):
            dialog_message.append(dialog.message)
            dialog.accept()

        # 1. Set listener
        self.page.once("dialog", handle_dialog)

        # 2. Trigger the action that causes the alert
        trigger_action()

        # 3. Return captured text
        return dialog_message[0] if dialog_message else ""