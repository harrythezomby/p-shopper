from ._anvil_designer import formSettingsTemplate
from anvil import *
import anvil.server

class formSettings(formSettingsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def btnColourThemeDefault_click(self, **event_args):
        anvil.server.call('set_user_theme', 'default-theme')
        get_open_form().apply_theme('default-theme')

    def btnColourThemeDark_click(self, **event_args):
        anvil.server.call('set_user_theme', 'dark-theme')
        get_open_form().apply_theme('dark-theme')

