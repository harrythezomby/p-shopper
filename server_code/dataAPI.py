import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_all_items():
  rows = app_tables.tblitems.search()
  return rows # Not a good practice, since can be a security risk. In a more security oriented situation consider exporting as a different object.

@anvil.server.callable
def get_all_categories():
    return [dict(row) for row in app_tables.tblcategories.search()]

# Simple version of category getter used for editting a list category dropdown
@anvil.server.callable
def get_categories_simple():
  return app_tables.tblcategories.search(tables.order_by("category_id", ascending=False))

@anvil.server.callable
def get_category_by_name(category_name):
    return app_tables.tblcategories.get(category_name=category_name)

# Search function for a list
@anvil.server.callable
def search_items(query):
    result = app_tables.tblitems.search()
    if query:
        query = query.lower() # Everything is transformed into lower case to allow for case insensitive searching
        result = [
            x for x in result
            if query in x['item_name'].lower()
            or query in x['brand'].lower()
            or query in x['store'].lower()
            or query in x['aisle'].lower()
        ]
    return result

@anvil.server.callable
def filter_items(selected_category):
    if selected_category is not None:
        category_row = app_tables.tblcategories.get(category_id=selected_category)
        result = app_tables.tblitems.search(category_id=category_row)
    else:
        result = app_tables.tblitems.search()
    return result

@anvil.server.callable
def add_item(item_name, quantity, category_id, brand, store, aisle):
    # Get the last item_id and increment by 1
    items = list(app_tables.tblitems.search(tables.order_by("item_id", ascending=False)))
    if items:
        last_item = items[0]
        new_item_id = last_item['item_id'] + 1
    else:
        new_item_id = 1  # Start at 1 if the table is empty
    
    # Add the new item
    app_tables.tblitems.add_row(
        item_id=new_item_id,
        item_name=item_name,
        quantity=quantity,
        category_id=app_tables.tblcategories.get(category_id=category_id),
        brand=brand,
        store=store,
        aisle=aisle
    )

@anvil.server.callable
def edit_item(item_id, item_name, quantity, category_id, brand, store, aisle):
    item = app_tables.tblitems.get(item_id=item_id)
    if item:
        category = app_tables.tblcategories.get(category_id=category_id)
        item.update(
            item_name=item_name,
            quantity=quantity,
            category_id=category,
            brand=brand,
            store=store,
            aisle=aisle
        )

@anvil.server.callable
def delete_item(item):
    item.delete()

"""
  _______           __     ____  ______  __             _    
 / ___/ /  ___ ____/ /__  / __ \/ _/ _/ / /  ___  ___ _(_)___
/ /__/ _ \/ -_) __/  '_/ / /_/ / _/ _/ / /__/ _ \/ _ `/ / __/
\___/_//_/\__/\__/_/\_\  \____/_//_/  /____/\___/\_, /_/\__/ 
                                                /___/        
"""
@anvil.server.callable
def get_item_details(item_id):
    item = app_tables.tblitems.get(item_id=item_id)
    return item

@anvil.server.callable
def check_off_item(item_id, purchase_date, expiry_date, price):
    item = app_tables.tblitems.get(item_id=item_id)
    
    if not item:
        raise Exception("Item not found")

    # Increment long_term_id
    last_entry = app_tables.tbllongtermhistory.search(tables.order_by('long_term_id', ascending=False), limit=1)
    if last_entry:
        next_id = last_entry[0]['long_term_id'] + 1
    else:
        next_id = 1

    app_tables.tbllongtermhistory.add_row(
        long_term_id=next_id,
        item_id=item['item_id'],
        price=price,
        purchase_date=purchase_date,
        expiry_date=expiry_date,
        category_id=item['category_id'],
        quantity=item['quantity']
    )

    # Delete item from tblItems
    item.delete()



