from ._anvil_designer import formLoginTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class formLogin(formLoginTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

    def btnOpen_click(self, **event_args):
        """This method is called when the button is clicked"""
        user = anvil.users.login_with_form()
        if user:
            if not anvil.server.call('user_has_lists', user):
                anvil.server.call('create_default_list', user)
            open_form('formMainApp')
        else:
            alert("Login failed. Please try again.")
