from ._anvil_designer import formLoginTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class formLogin(formLoginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.handle_login()

    def handle_login(self):
        url_hash = anvil.get_url_hash()
        share_url = url_hash.get('share_url') if url_hash else None

        if share_url:
            open_form('formMainApp', share_url=share_url)
        else:
            user = anvil.users.login_with_form()
            if user:
                if not anvil.server.call('user_has_lists', user):
                    anvil.server.call('create_default_list', user)
                open_form('formMainApp')
            else:
                alert("Login failed. Please try again.")

    def btnOpen_click(self, **event_args):
        user = anvil.users.login_with_form()
        if user:
            if not anvil.server.call('user_has_lists', user):
                anvil.server.call('create_default_list', user)
            open_form('formMainApp')
        else:
            alert("Login failed. Please try again.")
