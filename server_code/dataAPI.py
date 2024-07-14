import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def getAllItems():
    rows = app_tables.tblitems.search()
    result = []
    
    for row in rows:
        category_row = row['category_id']  # This gets the linked row from tblCategories
        category_name = category_row['category_name'] if category_row else None
        
        item = {
            'item_id': row['item_id'],
            'item_name': row['item_name'],
            'category_id': row['category_id'],
            'category_name': category_name,
            'quantity': row['quantity'],
            'brand': row['brand'],
            'store': row['store'],
            'aisle': row['aisle']
        }
        result.append(item)
    
    return result

