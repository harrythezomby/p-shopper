import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

categories = {item['category_name'] for item in anvil.server.call('get_categories_simple')}
categories = sorted(list(categories))
