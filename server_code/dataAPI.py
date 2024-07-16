import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# For exports
import io
import csv
import anvil.media

# For graphs and reports
import datetime

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
    last_entry = list(app_tables.tbllongtermhistory.search(tables.order_by('long_term_id', ascending=False)))[:1]
    next_id = last_entry[0]['long_term_id'] + 1 if last_entry else 1

    app_tables.tbllongtermhistory.add_row(
        long_term_id=next_id,
        item_name=item['item_name'],  # Store the item name instead of item ID
        price=price,
        purchase_date=purchase_date,
        expiry_date=expiry_date,
        category_id=item['category_id'],
        quantity=item['quantity']
    )

    # Delete item from tblItems
    item.delete()

"""
   __   _     __    ____                    __ 
  / /  (_)__ / /_  / __/_ __ ___  ___  ____/ /_
 / /__/ (_-</ __/ / _/ \ \ // _ \/ _ \/ __/ __/
/____/_/___/\__/ /___//_\_\/ .__/\___/_/  \__/ 
                          /_/                  
"""


@anvil.server.callable
def export_items_to_txt():
    # Fetch data from tblItems
    rows = app_tables.tblitems.search()
    
    # Create an in-memory string buffer
    output = io.StringIO()
    
    # Write headers (excluding item_id)
    headers = [col for col in app_tables.tblitems.list_columns() if col != 'item_id']
    output.write('\t'.join(headers) + '\n')
    
    # Write data rows
    for row in rows:
        row_data = []
        for col in headers:
            if isinstance(row[col], dict):  # Handle related tables (e.g., category_id)
                if 'category_name' in row[col]:
                    row_data.append(row[col]['category_name'])
                else:
                    row_data.append(str(row[col]))
            elif isinstance(row[col], list):  # Handle list fields
                row_data.append(','.join(str(item) for item in row[col]))
            else:
                row_data.append(str(row[col]))
        output.write('\t'.join(row_data) + '\n')
    
    # Get text data from buffer
    text_data = output.getvalue()
    
    # Create a Media object for the text file
    media = anvil.BlobMedia("text/plain", text_data.encode("utf-8"), name="items.txt")
    
    return media

"""
  _____              __         ____      ___                    __    
 / ___/______ ____  / /  ___   / __/___  / _ \___ ___  ___  ____/ /____
/ (_ / __/ _ `/ _ \/ _ \(_-<   > _/_ _/ / , _/ -_) _ \/ _ \/ __/ __(_-<
\___/_/  \_,_/ .__/_//_/___/  |_____/  /_/|_|\__/ .__/\___/_/  \__/___/
            /_/                                /_/                     
"""
@anvil.server.callable
def get_all_categories_for_graphs():
    categories = app_tables.tblcategories.search()
    return [{'category_id': cat['category_id'], 'category_name': cat['category_name']} for cat in categories]

@anvil.server.callable
def get_category_consumption_data(category_id, timeframe):
    from dateutil.relativedelta import relativedelta
    
    now = datetime.datetime.now()

    if timeframe == 'week':
        start_date = now - datetime.timedelta(weeks=1)
    elif timeframe == 'month':
        start_date = now - relativedelta(months=1)
    elif timeframe == 'year':
        start_date = now - relativedelta(years=1)
    else:
        raise ValueError("Invalid timeframe")

    category_row = app_tables.tblcategories.get(category_id=category_id)
    
    rows = app_tables.tbllongtermhistory.search(
        category_id=category_row,
        purchase_date=q.greater_than_or_equal_to(start_date)
    )

    data = []
    for row in rows:
        data.append({'date': row['purchase_date'], 'quantity': row['quantity']})

    data.sort(key=lambda x: x['date'])
    return data




