from ._anvil_designer import formSettingsTemplate
from anvil import *
import anvil.server

class formSettings(formSettingsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def btnColourThemeDefault_click(self, **event_args):
        self.set_theme("default-theme")

    def btnColourThemeDark_click(self, **event_args):
        self.set_theme("dark-theme")

    def set_theme(self, theme_name):
        user = anvil.users.get_user()
        if user:
            anvil.server.call('set_user_theme', user, theme_name)
        self.apply_theme(theme_name)

    def apply_theme(self, theme_name):
        js_code = f"""
        document.body.className = '';
        document.body.classList.add('{theme_name}');
        """
        self.call_js(js_code)

    def call_js(self, js_code):
        anvil.js.window.eval(js_code)

