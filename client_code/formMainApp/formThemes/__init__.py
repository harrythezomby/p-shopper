from ._anvil_designer import formThemesTemplate
from anvil import *
import anvil.server
import anvil.users

class formThemes(formThemesTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def btnColourThemePrincess_click(self, **event_args):
        anvil.server.call('set_user_theme', 'princess-theme')
        get_open_form().apply_theme('princess-theme')

    def btnColourThemeSakura_click(self, **event_args):
        anvil.server.call('set_user_theme', 'sakura-theme')
        get_open_form().apply_theme('sakura-theme')

    def btnColourThemePlainish_click(self, **event_args):
        anvil.server.call('set_user_theme', 'plainish-theme')
        get_open_form().apply_theme('plainish-theme')

    def btnColourThemeDefault_click(self, **event_args):
        anvil.server.call('set_user_theme', 'default-theme')
        get_open_form().apply_theme('default-theme')

    def btnColourThemeDark_click(self, **event_args):
        anvil.server.call('set_user_theme', 'dark-theme')
        get_open_form().apply_theme('dark-theme')

    def btnConfirm_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Command to close the form with this button
      self.raise_event("x-close-alert", value=42)

