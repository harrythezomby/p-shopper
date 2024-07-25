import anvil.server

class modTheming:
    def __init__(self, main_app):
        self.main_app = main_app

    def apply_user_theme(self):
        theme = anvil.server.call('get_user_theme')
        self.apply_theme(theme)
    
    def apply_theme(self, theme_name):
        js_code = f"""
        document.body.className = '';
        document.body.classList.add('{theme_name}');
        """
        self.call_js(js_code)

    def call_js(self, js_code):
        anvil.js.window.eval(js_code)
