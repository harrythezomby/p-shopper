"""
   ____                    __    
  /  _/_ _  ___  ___  ____/ /____
 _/ //  ' \/ _ \/ _ \/ __/ __(_-<
/___/_/_/_/ .__/\___/_/  \__/___/
         /_/                     
"""
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

"""
   __  ___     _        ___               
  /  |/  /__ _(_)__    / _ \___ ____ ____ 
 / /|_/ / _ `/ / _ \  / ___/ _ `/ _ `/ -_)
/_/  /_/\_,_/_/_//_/ /_/   \_,_/\_, /\__/ 
                               /___/      
"""
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

@anvil.server.callable
def get_items_expiring_soon():
    import datetime

    now = datetime.date.today()
    alert_items = []

    rows = app_tables.tbllongtermhistory.search()
    for row in rows:
        expiry_date = row['expiry_date']
        if expiry_date and now <= expiry_date <= (now + datetime.timedelta(days=2)):
            alert_items.append(row['item_name'])

    return alert_items

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
def export_items_to_csv():
    # Fetch data from tblItems
    rows = app_tables.tblitems.search()

    # Create an in-memory string buffer
    output = io.StringIO()
    writer = csv.writer(output)

    # Write headers (excluding item_id)
    headers = [col for col in app_tables.tblitems.list_columns() if col != 'item_id']
    writer.writerow(headers)

    # Write data rows
    for row in rows:
        row_data = []
        for col in headers:
            cell_value = row.get(col)
            if isinstance(cell_value, dict):  # Handle related tables (e.g., category_id)
                cell_value = ', '.join([f"{k}: {v}" for k, v in cell_value.items()])
            elif isinstance(cell_value, list):  # Handle list fields
                cell_value = ','.join(str(item) for item in cell_value)
            else:
                cell_value = str(cell_value)
            row_data.append(cell_value)
        writer.writerow(row_data)

    # Get CSV data from buffer
    csv_data = output.getvalue()

    # Create a Media object for the CSV file
    media = anvil.BlobMedia("text/csv", csv_data.encode("utf-8"), name="items.csv")

    return media

"""
  _____              __         ____      ___                    __    
 / ___/______ ____  / /  ___   / __/___  / _ \___ ___  ___  ____/ /____
/ (_ / __/ _ `/ _ \/ _ \(_-<   > _/_ _/ / , _/ -_) _ \/ _ \/ __/ __(_-<
\___/_/  \_,_/ .__/_//_/___/  |_____/  /_/|_|\__/ .__/\___/_/  \__/___/
            /_/                                /_/                     
"""
# Functions for the category consumption graph
@anvil.server.callable
def get_all_categories_for_graphs():
    categories = app_tables.tblcategories.search()
    return [{'category_id': cat['category_id'], 'category_name': cat['category_name']} for cat in categories]

@anvil.server.callable
def get_category_consumption_data(category_id, timeframe):
    from dateutil.relativedelta import relativedelta
    import collections

    now = datetime.datetime.now()

    if timeframe == 'week':
        start_date = now - datetime.timedelta(weeks=52)  # Past year
        date_format = "%U"  # Week format
        increment = datetime.timedelta(weeks=1)
    elif timeframe == 'month':
        start_date = now - relativedelta(years=1)  # Past year
        date_format = "%b"  # Month format (e.g., Jan, Feb)
        increment = relativedelta(months=1)
    elif timeframe == 'year':
        start_date = now - relativedelta(years=5)  # Past 5 years
        date_format = "%Y"  # Year format
        increment = relativedelta(years=1)
    else:
        raise ValueError("Invalid timeframe")

    category_row = app_tables.tblcategories.get(category_id=category_id)
    
    rows = app_tables.tbllongtermhistory.search(
        category_id=category_row,
        purchase_date=q.greater_than_or_equal_to(start_date)
    )

    # Aggregate data
    aggregated_data = collections.defaultdict(int)
    for row in rows:
        date_key = row['purchase_date'].strftime(date_format)
        aggregated_data[date_key] += row['quantity']

    # Convert to sorted list of dictionaries
    sorted_data = [{'date': date, 'quantity': quantity} for date, quantity in sorted(aggregated_data.items())]
    return sorted_data

# Functions for the item quantity consumption graph
@anvil.server.callable
def get_all_items_for_graphs():
    items = app_tables.tbllongtermhistory.search()
    unique_items = {item['item_name'] for item in items}
    return [{'item_name': name} for name in unique_items]

@anvil.server.callable
def get_item_consumption_data(item_name, timeframe):
    import datetime
    from dateutil.relativedelta import relativedelta
    import collections

    now = datetime.datetime.now()

    if timeframe == 'week':
        start_date = now - datetime.timedelta(weeks=52)  # Past year
        date_format = "%U"  # Week format
        increment = datetime.timedelta(weeks=1)
    elif timeframe == 'month':
        start_date = now - relativedelta(years=1)  # Past year
        date_format = "%b"  # Month format (e.g., Jan, Feb)
        increment = relativedelta(months=1)
    elif timeframe == 'year':
        start_date = now - relativedelta(years=5)  # Past 5 years
        date_format = "%Y"  # Year format
        increment = relativedelta(years=1)
    else:
        raise ValueError("Invalid timeframe")

    rows = app_tables.tbllongtermhistory.search(
        item_name=item_name,
        purchase_date=q.greater_than_or_equal_to(start_date)
    )

    # Aggregate data
    aggregated_data = collections.defaultdict(int)
    for row in rows:
        date_key = row['purchase_date'].strftime(date_format)
        aggregated_data[date_key] += row['quantity']

    # Convert to sorted list of dictionaries
    sorted_data = [{'date': date, 'quantity': quantity} for date, quantity in sorted(aggregated_data.items())]
    return sorted_data

# Functions for money spent history graph
@anvil.server.callable
def get_money_spent_data(timeframe):
    import datetime
    from dateutil.relativedelta import relativedelta
    import collections

    now = datetime.datetime.now()

    if timeframe == 'week':
        start_date = now - datetime.timedelta(weeks=52)  # Past year
        date_format = "%U"  # Week format
        increment = datetime.timedelta(weeks=1)
    elif timeframe == 'month':
        start_date = now - relativedelta(years=1)  # Past year
        date_format = "%b"  # Month format (e.g., Jan, Feb)
        increment = relativedelta(months=1)
    elif timeframe == 'year':
        start_date = now - relativedelta(years=5)  # Past 5 years
        date_format = "%Y"  # Year format
        increment = relativedelta(years=1)
    else:
        raise ValueError("Invalid timeframe")

    rows = app_tables.tbllongtermhistory.search(
        purchase_date=q.greater_than_or_equal_to(start_date)
    )

    # Aggregate data
    aggregated_data = collections.defaultdict(float)
    for row in rows:
        date_key = row['purchase_date'].strftime(date_format)
        aggregated_data[date_key] += row['price']

    # Convert to sorted list of dictionaries
    sorted_data = [{'date': date, 'amount_spent': amount} for date, amount in sorted(aggregated_data.items())]
    return sorted_data

# Functions for Item price history graph
@anvil.server.callable
def get_item_price_history_data(item_name, timeframe):
    import datetime
    from dateutil.relativedelta import relativedelta
    import collections

    now = datetime.datetime.now()

    if timeframe == 'week':
        start_date = now - datetime.timedelta(weeks=52)  # Past year
        date_format = "%U"  # Week format
    elif timeframe == 'month':
        start_date = now - relativedelta(years=1)  # Past year
        date_format = "%b"  # Month format (e.g., Jan, Feb)
    elif timeframe == 'year':
        start_date = now - relativedelta(years=5)  # Past 5 years
        date_format = "%Y"  # Year format
    else:
        raise ValueError("Invalid timeframe")

    rows = app_tables.tbllongtermhistory.search(
        item_name=item_name,
        purchase_date=q.greater_than_or_equal_to(start_date)
    )

    # Aggregate data
    aggregated_data = collections.defaultdict(list)
    for row in rows:
        date_key = row['purchase_date'].strftime(date_format)
        price_per_quantity = row['price'] / row['quantity']
        aggregated_data[date_key].append(price_per_quantity)

    # Calculate the average price per quantity for each date key
    average_data = {date: sum(prices) / len(prices) for date, prices in aggregated_data.items()}

    # Convert to sorted list of dictionaries
    sorted_data = [{'date': date, 'price': price} for date, price in sorted(average_data.items())]
    return sorted_data

# Functions for item comparison report
@anvil.server.callable
def get_item_comparison_report_data(timeframe):
    import datetime
    from dateutil.relativedelta import relativedelta
    import collections

    now = datetime.datetime.now()

    if timeframe == 'week':
        start_date = now - datetime.timedelta(weeks=1)  # Past week
    elif timeframe == 'month':
        start_date = now - relativedelta(months=1)  # Past month
    elif timeframe == 'year':
        start_date = now - relativedelta(years=1)  # Past year
    else:
        raise ValueError("Invalid timeframe")

    rows = app_tables.tbllongtermhistory.search(
        purchase_date=q.greater_than_or_equal_to(start_date)
    )

    # Initialize counters and aggregators
    item_count = collections.Counter()
    category_count = collections.Counter()
    date_count = collections.Counter()
    total_quantity = 0
    total_spending = 0

    for row in rows:
        item_count[row['item_name']] += row['quantity']
        category_count[row['category_id']['category_name']] += row['quantity']
        date_key = row['purchase_date'].strftime("%Y-%m-%d")
        date_count[date_key] += row['quantity']
        total_quantity += row['quantity']
        total_spending += row['price']

    # Find the most bought item, date, and category
    most_bought_item = item_count.most_common(1)[0] if item_count else ("N/A", 0)
    most_bought_date = date_count.most_common(1)[0] if date_count else ("N/A", 0)
    most_bought_category = category_count.most_common(1)[0] if category_count else ("N/A", 0)

    # Prepare the report data
    report_data = {
        'most_bought_item': most_bought_item,
        'most_bought_date': most_bought_date,
        'most_bought_category': most_bought_category,
        'total_quantity': total_quantity,
        'total_spending': total_spending,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': now.strftime("%Y-%m-%d")
    }

    return report_data

# Functions for weekly spending report
@anvil.server.callable
def get_weekly_spending_report():
    import datetime
    from dateutil.relativedelta import relativedelta
    import collections

    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(weeks=52)  # Past year

    rows = app_tables.tbllongtermhistory.search(
        purchase_date=q.greater_than_or_equal_to(start_date)
    )

    # Initialize weekly spending dictionary
    weekly_spending = collections.defaultdict(float)
    week_dates = {}

    for row in rows:
        week_key = row['purchase_date'].strftime("%Y-%U")
        week_start = row['purchase_date'] - datetime.timedelta(days=row['purchase_date'].weekday())
        week_end = week_start + datetime.timedelta(days=6)
        week_dates[week_key] = (week_start.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d"))
        weekly_spending[week_key] += row['price']

    # Convert to sorted list of tuples
    sorted_spending = sorted(weekly_spending.items())

    # Calculate increases and decreases
    spending_changes = []
    for i in range(1, len(sorted_spending)):
        current_week = sorted_spending[i]
        previous_week = sorted_spending[i - 1]
        change = current_week[1] - previous_week[1]
        percent_change = (change / previous_week[1]) * 100 if previous_week[1] != 0 else 0
        week_range = week_dates[current_week[0]]
        spending_changes.append((current_week[0], current_week[1], change, percent_change, week_range))

    return spending_changes

# Expiry Report
@anvil.server.callable
def get_expiry_report(timeframe):
    import datetime
    from dateutil.relativedelta import relativedelta

    now = datetime.date.today()

    if timeframe == 'week':
        future_end_date = now + datetime.timedelta(weeks=1)
        expired_start_date = now - datetime.timedelta(weeks=1)
    elif timeframe == 'month':
        future_end_date = now + relativedelta(months=1)
        expired_start_date = now - relativedelta(months=1)
    elif timeframe == 'year':
        future_end_date = now + relativedelta(years=1)
        expired_start_date = now - relativedelta(years=1)
    else:
        raise ValueError("Invalid timeframe")

    future_items = []
    expired_items = []
    alert_items = []

    rows = app_tables.tbllongtermhistory.search()
    for row in rows:
        expiry_date = row['expiry_date']
        if expiry_date:
            if now <= expiry_date <= future_end_date:
                future_items.append({
                    'item_name': row['item_name'],
                    'expiry_date': expiry_date.strftime("%Y-%m-%d")
                })
                if (expiry_date - now).days <= 2:
                    alert_items.append(row['item_name'])
            elif expired_start_date <= expiry_date < now:
                expired_items.append({
                    'item_name': row['item_name'],
                    'expiry_date': expiry_date.strftime("%Y-%m-%d")
                })

    return future_items, expired_items, alert_items


