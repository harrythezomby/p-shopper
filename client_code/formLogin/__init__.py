# Imports
from ._anvil_designer import formLoginTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

class formLogin(formLoginTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Apply default theme CSS
        self.apply_default_theme()

    # Apply the default theme on startup, the css is in here as a workaround, since I couldn't get it to import straight from default-theme.css - potential optimisation for the future
    def apply_default_theme(self):
        css_code = """
        <style>
        /* General Styles for Markdown */
        body.default-theme {
            background: linear-gradient(to right, #d6e3ff, #e2d1ff);
            color: #333;
            font-family: 'Roboto', sans-serif;
        }

        /* Headings */
        h1 {
            font-size: 2.5em;
            color: #4e79a7;
            border-bottom: 2px solid #4e79a7;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        h2 {
            font-size: 2em;
            color: #4e79a7;
            border-bottom: 1px solid #4e79a7;
            padding-bottom: 8px;
            margin-bottom: 16px;
        }

        h3 {
            font-size: 1.75em;
            color: #4e79a7;
            margin-bottom: 12px;
        }

        /* Paragraphs */
        p {
            font-size: 1em;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        /* Bold Text */
        strong {
            color: #9e79a7;
            font-weight: bold;
        }

        /* Bullet Points */
        ul {
            list-style-type: disc;
            margin: 20px 0;
            padding-left: 40px;
        }

        ul li {
            margin-bottom: 10px;
        }

        /* Numbered Lists */
        ol {
            list-style-type: decimal;
            margin: 20px 0;
            padding-left: 40px;
        }

        ol li {
            margin-bottom: 10px;
        }

        /* Links */
        a {
            color: #4e79a7;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        /* Blockquotes */
        blockquote {
            border-left: 5px solid #4e79a7;
            margin: 20px 0;
            padding-left: 20px;
            color: #666;
            font-style: italic;
        }

        /* Code Blocks */
        pre {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }

        code {
            background: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }

        th {
            background-color: #4e79a7;
            color: white;
        }

        td {
            background-color: #fff;
        }

        /* Alerts */
        .alert {
            background: linear-gradient(to right, #d6e3ff, #e2d1ff);
            color: #333;
            border-radius: 5px;
            padding: 20px;
            border: 1px solid #4e79a7;
        }

        /* Buttons */
        .button, .btn {
            background: linear-gradient(to right, #4e79a7, #9e79a7);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }

        .button:hover, .btn:hover {
            background: linear-gradient(to right, #3a5a8b, #7a5a8b);
        }
        </style>
        """
        js_code = f"""
        document.head.insertAdjacentHTML('beforeend', `{css_code}`);
        document.body.className = '';
        document.body.classList.add('default-theme');
        """
        self.call_js(js_code)

    # The login button functionality
    def btnOpen_click(self, **event_args):
        """This method is called when the button is clicked"""
        user = anvil.users.login_with_form()
        if user:
            if not anvil.server.call('user_has_lists', user): # Check if the user has lists
                anvil.server.call('create_default_list', user) # If not, make the default list
            self.remove_default_theme()  # Removes the default theme class upon login
            open_form('formMainApp')
        else:
            alert("Login failed. Please try again.")

    # Removes the default theme upon logging in incase the user has a different theme selected
    def remove_default_theme(self):
        js_code = """
        document.body.classList.remove('default-theme');
        """
        anvil.js.window.eval(js_code)

    # Function used to inject js
    def call_js(self, js_code):
        anvil.js.window.eval(js_code)

    # Button to go to the github repo for the project
    def btnGithub_click(self, **event_args):
      """This method is called when the button is clicked"""
      anvil.js.window.open("https://github.com/harrythezomby/p-shopper", "_blank")



