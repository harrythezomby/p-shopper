import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def getAllItems():
  rows = app_tables.tblitems.search()
  return rows # Not a good practice, since can be a security risk. In a more security oriented situation consider exporting as a different object.

@anvil.server.callable
def get_all_categories():
    return [dict(row) for row in app_tables.tblcategories.search()]

@anvil.server.callable
def search_items(query):
  result = app_tables.tblitems.search()
  if query:
    result = [
      x for x in result
      if query in x['item_name']
      or query in x['brand']
      or query in x['store']
      or query in x['aisle']
    ]
  return result

@anvil.server.callable
def add_item(item_name, quantity, category_id, brand, store, aisle):
    app_tables.tblitems.add_row(
        item_name=item_name,
        quantity=quantity,
        category_id=app_tables.tblcategories.get(category_id=category_id),
        brand=brand,
        store=store,
        aisle=aisle
    )


