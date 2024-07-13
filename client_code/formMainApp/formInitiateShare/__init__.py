from ._anvil_designer import formInitiateShareTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class formInitiateShare(formInitiateShareTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btnOkay_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Command to close the form with this button
    self.raise_event("x-close-alert", value=42)
