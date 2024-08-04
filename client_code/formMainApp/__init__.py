from ._anvil_designer import formMainAppTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .formThemes import formThemes
from .formCheckItem import formCheckItem

class formMainApp(formMainAppTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Setting the event handler to refresh the data grid so other forms can refresh it
        self.set_event_handler('x-refresh-data', self.refresh_data_grid)

        # Setting the headers of the data grid
        self.data = []
        self.headers = {
            'item_name': self.linkItemName,
            'quantity': self.linkQuantity,
            'category_id': self.linkCategory,
            'brand': self.linkBrand,
            'store': self.linkStore,
            'aisle': self.linkAisle
        }

        # Setting default sort
        self.current_sort_column = 'item_name'
        self.current_sort_reverse = False

        # Calling init functions
        self.apply_user_theme()  # Apply the user's theme on startup
      
        self.populate_lists_dropdown()
        self.update_expiry_warning()
        self.update_list_title()
        
        # Refresh data grid after initial population
        self.refresh_data_grid()


    """Setting up (grabbing data from database, etc)"""
    # Populates the list selector dropdown with all the logged in user's lists
    def populate_lists_dropdown(self):
        user = anvil.users.get_user()
        lists = anvil.server.call('get_all_lists', user) # Gets all the current users lists
        self.ddListSelector.items = [(l['list_name'], l['list_id']) for l in lists if l['list_name']]
        if lists:
            self.ddListSelector.selected_value = lists[0]['list_id']
            self.refresh_data_grid()  # Ensure the data grid is refreshed on initial load
        else:
            self.ddListSelector.selected_value = None
            self.data = []
            self.apply_filter_and_sort()
            self.lblIsEmpty.text = "The currently selected list is empty."
            self.lblIsEmpty.visible = True

    # Populates the category selector dropdown with all the logged in user's categories
    def populate_category_dropdown(self):
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user) # Gets all the current users categories

        # Adding the ability to create and remove categories to the dropdown
        self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories] + [("New Category", "New Category"), ("Remove Category", "Remove Category")]
        selected_list_id = self.ddListSelector.selected_value
        if selected_list_id:
            categories = anvil.server.call('get_categories_for_list', selected_list_id)
            self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]

    def update_list_title(self):
        selected_list_id = self.ddListSelector.selected_value
        if selected_list_id:
            list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
            self.lblListTitle.text = list_name

  
    """Category interaction"""
    def ddNewItemCategory_change(self, **event_args):
        selected_value = self.ddNewItemCategory.selected_value
        if selected_value == "New Category":
            self.add_new_category()
        elif selected_value == "Remove Category":
            self.remove_category()
        else:
            pass
    
    def add_new_category(self):
        content = TextBox()

        # New category popup
        result = alert("Enter name for the new category:", buttons=[("OK", "ok")], content=content, title="Create New Category", large=True)
        if result == "ok":
            new_category_name = content.text.strip().title()
            
            # Input validation: only allow English alphabetic characters and spaces
            if not new_category_name.isalpha() and not all(char.isalpha() or char.isspace() for char in new_category_name):
                alert("Invalid input. Please enter only English alphabetic characters and spaces.")
                content.text = ""  # Clear the input field
                self.revert_category_selection()
                return
    
            # Check for blank input
            if not new_category_name:
                alert("Category name cannot be blank.")
                content.text = ""  # Clear the input field
                self.revert_category_selection()
                return
            
            # Call the server function to create a new category
            success = anvil.server.call('create_new_category', new_category_name)
            if success:
                self.populate_category_dropdown()
                alert("New category created successfully.")
            else:
                alert("Category creation failed.")
        self.revert_category_selection()
        
    def remove_category(self):
        content = TextBox()

        # Remove category popup
        result = alert("Enter name of the category to remove:", buttons=[("OK", "ok")], content=content, title="Remove Category", large=True)
        if result == "ok":
            category_name = content.text.strip().title()
    
            # Input validation: only allow English alphabetic characters and spaces
            if not category_name.isalpha() and not all(char.isalpha() or char.isspace() for char in category_name):
                alert("Invalid input. Please enter only English alphabetic characters and spaces.")
                content.text = ""  # Clear the input field
                self.revert_category_selection()
                return
    
            # Check for blank input
            if not category_name:
                alert("Category name cannot be blank.")
                content.text = ""  # Clear the input field
                self.revert_category_selection()
                return
    
            # Call the server function to remove the category
            success, message = anvil.server.call('remove_category', category_name)
            if success:
                self.populate_category_dropdown()
                alert("Category removed successfully.")
            else:
                alert(message)
        self.revert_category_selection()
    
    def revert_category_selection(self):
        if self.ddNewItemCategory.items:
            self.ddNewItemCategory.selected_value = self.ddNewItemCategory.items[0][1]

  
    """Searching and filtering"""
    def filter(self, **event_args):
        self.apply_filter_and_sort()

    def search(self, **event_args):
        self.apply_filter_and_sort(search_query=self.tbSearchList.text) # Search with the query in the search box

    # Updates the expiry warning on the bottom of the screen (shows items expiring for the current user in the next 2 days)
    def update_expiry_warning(self):
        expiring_soon_items = anvil.server.call('get_items_expiring_soon')
        if expiring_soon_items:
            self.lblExpiryWarning.text = f"The following item(s) are expiring soon: {', '.join(expiring_soon_items)}"
            self.lblExpiryWarning.visible = True
        else:
            self.lblExpiryWarning.visible = False # If there aren't any items expiring soon, hide the label

    # Refreshes the data grid of the current list, in case changes have been made (i.e., new or modified items, checked off items, deleted items, etc)
    def refresh_data_grid(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        if selected_list_id:
            self.data = anvil.server.call('get_all_items', selected_list_id)
            self.apply_filter_and_sort(search_query=self.tbSearchList.text)
            self.populate_category_dropdown()
            self.update_empty_label()
        else:
            self.data = []
            self.apply_filter_and_sort()
            self.populate_category_dropdown()
            self.update_empty_label()

    # Displays an empty list label if the currently selected list is empty
    def update_empty_label(self):
        if not self.data:
            self.lblIsEmpty.text = "The currently selected list is empty."
            self.lblIsEmpty.visible = True
        else:
            self.lblIsEmpty.visible = False

    # Sorting by columns within the list
    def sort_by_column(self, column):
        if self.current_sort_column == column:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_column = column
            self.current_sort_reverse = False

        self.apply_filter_and_sort()

    # Sorting data within the list
    """Python's built-in sorted() function is used, which uses Timsort. Timsort is a hybrid sorting algorithm derived from merge sort and insertion sort. It is highly efficient for real-world data and is stable, meaning that it preserves the order of equal elements."""
    def sort_data(self, data):
        try:
            # Check if the current sort column is 'category_id'
            if self.current_sort_column == 'category_id':
                # Sort the data based on the 'category_name' within 'category_id'
                sorted_data = sorted(
                    data,
                    key=lambda x: x[self.current_sort_column]['category_name'].lower() if x[self.current_sort_column] else "",
                    reverse=self.current_sort_reverse  # Determine sort order (ascending/descending)
                )
            else:
                # Sort the data based on the value of the current sort column
                sorted_data = sorted(
                    data,
                    key=lambda x: str(x[self.current_sort_column]).lower() if x[self.current_sort_column] else "",
                    reverse=self.current_sort_reverse  # Determine sort order (ascending/descending)
                )
            return sorted_data  # Return the sorted data
        except Exception as e:
            # Handle any exceptions that may occur during sorting
            print(f"Error during sorting: {e}")
            return data  # Return the original data if an error occurs

    # Applies the category filter, as well as sorts the list in one go
    def apply_filter_and_sort(self, search_query=None):
        selected_category = self.ddCategorySelector.selected_value
        if selected_category:
            filtered_data = [item for item in self.data if item['category_id']['category_id'] == selected_category]
        else:
            filtered_data = self.data
    
        if search_query:
            filtered_data = [item for item in filtered_data if search_query.lower() in item['item_name'].lower()]
    
        sorted_data = self.sort_data(filtered_data)
        self.repeatListItems.items = sorted_data
    
        self.update_empty_label()  # Update the empty label after filtering and sorting
    
        for key, link in self.headers.items():
            if key == self.current_sort_column:
                link.icon = 'fa:caret-up' if self.current_sort_reverse else 'fa:caret-down'
            else:
                link.icon = None

    """The following links are the list headers which can be sorted by"""
    def linkItemName_click(self, **event_args):
        self.sort_by_column('item_name')

    def linkQuantity_click(self, **event_args):
        self.sort_by_column('quantity')

    def linkCategory_click(self, **event_args):
        self.sort_by_column('category_id')

    def linkBrand_click(self, **event_args):
        self.sort_by_column('brand')

    def linkStore_click(self, **event_args):
        self.sort_by_column('store')

    def linkAisle_click(self, **event_args):
        self.sort_by_column('aisle')

  
    """Other buttons"""
    # Move to the graphs and reports module/section of P-Shopper
    def btnReports_click(self, **event_args):
        open_form('formGraphsReports')

    def btnThemes_click(self, **event_args):
        # Display the theme selector form as a popup
        alert(content=formThemes(), large=True, buttons=[], title="Themes")

    def btnLogout_click(self, **event_args):
        # Logout of P-Shopper as the currently logged in user
        anvil.users.logout()
        open_form('formLogin')

  
    """Item Interaction"""
    def check_off_item(self, item_id, list_id, **event_args):
      content = formCheckItem(item_id=item_id, list_id=list_id, parent_form=self)
      alert(content=content, large=True, buttons=[], title="Check Off Item")

    def btnCreateItem_click(self, **event_args):
        # Sanitize and validate item name
        item_name = self.tbNewItemName.text.strip().title()
        if not all(c.isalnum() or c.isspace() for c in item_name) or self.tbNewItemName.text == "":
            alert("Item name can only contain English alphanumeric characters and spaces, and cannot be blank.")
            self.tbNewItemName.text = ""
            return
        
        # Validate and set quantity
        quantity_text = str(self.tbNewItemQuantity.text)
        if quantity_text is None:
            quantity_text = ""
            quantity = 1
        quantity_text = quantity_text.strip()
        if not quantity_text:
            quantity = 1
        else:
            try:
                quantity = int(quantity_text)
                if quantity <= 0:
                    alert("Quantity must be a positive integer.")
                    self.tbNewItemQuantity.text = ""
                    return
            except ValueError:
                alert("Quantity must be a positive integer.")
                self.tbNewItemQuantity.text = ""
                return
        
        # Sanitize and validate brand
        brand = self.tbNewItemBrand.text.strip().title() if self.tbNewItemBrand.text else "None"
        # Allow letters, numbers, and specific symbols for Australian businesses
        if not all(c.isalnum() or c in " .&-_" for c in brand):
            alert("Brand can only contain letters, numbers, and the symbols .&-_")
            self.tbNewItemBrand.text = ""
            return
        
        # Sanitize and validate store
        store = self.tbNewItemStore.text.strip().title() if self.tbNewItemStore.text else "None"
        if not all(c.isalnum() or c in " .&-_" for c in store):
            alert("Store can only contain letters, numbers, and the symbols .&-_")
            self.tbNewItemStore.text = ""
            return
        
        # Sanitize and validate aisle
        aisle = self.tbNewItemAisle.text.strip().title() if self.tbNewItemAisle.text else "None"
        if not all(c.isalnum() or c.isspace() for c in aisle):
            alert("Aisle can only contain English alphanumeric characters and spaces.")
            self.tbNewItemAisle.text = ""
            return
        
        # Get selected category ID and list ID
        category_id = self.ddNewItemCategory.selected_value
        list_id = self.ddListSelector.selected_value
    
        # Add item to the database
        anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle, list_id)
        alert("Item added successfully.")
        
        # Refresh the data grid and clear input fields
        self.refresh_data_grid()
        self.tbNewItemName.text = ""
        self.tbNewItemQuantity.text = ""
        self.tbNewItemBrand.text = ""
        self.tbNewItemStore.text = ""
        self.tbNewItemAisle.text = ""

  
    """List Interaction"""
    # When the list selector is changed
    def ddListSelector_change(self, **event_args):
      self.refresh_data_grid()
      self.update_list_title()

    def btnDeleteList_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        if not selected_list_id:
            alert("No list selected to delete.")
            return
    
        # Get the name of the selected list for the confirmation alert
        selected_list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
    
        confirm_delete = confirm(f"Are you sure you want to delete the list '{selected_list_name}'? This action cannot be undone.")
        if confirm_delete:
            success, message = anvil.server.call('delete_list', selected_list_id)
            if success:
                alert(f"List '{selected_list_name}' and its items have been deleted successfully.")
                self.populate_lists_dropdown()
                self.update_list_title()
                self.refresh_data_grid()
            else:
                alert(message)

    def btnNewList_click(self, **event_args):
        # Create a TextBox for user input
        content = TextBox()
        # Display an alert dialog to enter the name for the new list
        result = alert("Enter name for the new list:", buttons=[("OK", "ok")], content=content, title="Create New List")
        
        # Check if the user clicked "OK"
        if result == "ok":
            # Get the entered name, strip leading/trailing spaces, and capitalize the first letter of each word
            new_name = content.text.strip().title()
            
            # Validate the entered name: it should only contain alphanumeric characters, spaces, and apostrophes
            if not new_name or not new_name.replace("'", "").replace(" ", "").isalnum():
                # Show an alert if the name is invalid
                alert("List name can only contain English alphanumeric characters, spaces, and apostrophes. Please try again.")
                return
            
            # If a valid name is entered
            if new_name:
                # Get the current user
                user = anvil.users.get_user()
                # Call the server function to create a new list with the entered name and user info
                anvil.server.call('create_new_list', new_name, user)
                # Update the dropdown with the new list
                self.populate_lists_dropdown()
                # Update the list title (assumes this function does something related to the new list)
                self.update_list_title()

    def btnRenameList_click(self, **event_args):
        # Get the ID of the selected list from the dropdown
        selected_list_id = self.ddListSelector.selected_value
        # Find the current name of the selected list
        current_list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
        
        # Create a TextBox with the current list name for user input
        content = TextBox(text=current_list_name)
        # Display an alert dialog to enter a new name for the list
        result = alert("Enter new name for the list:", buttons=[("OK", "ok")], content=content, title="Rename List")
        
        # Check if the user clicked "OK"
        if result == "ok":
            # Get the entered name, strip leading/trailing spaces, and capitalize the first letter of each word
            new_name = content.text.strip().title()
            
            # Validate the entered name: it should only contain alphanumeric characters, spaces, and apostrophes
            if not new_name or not new_name.replace("'", "").replace(" ", "").isalnum():
                # Show an alert if the name is invalid
                alert("List name can only contain English alphanumeric characters, spaces, and apostrophes. Please try again.")
                return
            
            # If a valid name is entered
            if new_name:
                # Call the server function to rename the selected list with the new name
                anvil.server.call('rename_list', selected_list_id, new_name)
                # Update the dropdown with the renamed list
                self.populate_lists_dropdown()
                # Update the list title (assumes this function does something related to the renamed list)
                self.update_list_title()


    """Exporting"""
    # Exporting the active list to csv
    def btnExport_click(self, **event_args):
          selected_list_id = self.ddListSelector.selected_value
          csv_file = anvil.server.call('export_items_to_csv', selected_list_id)
          download(csv_file)


    """Theming"""
    # Function to pull the user's currently saved theme and apply it at init
    def apply_user_theme(self):
        theme = anvil.server.call('get_user_theme')
        self.apply_theme(theme)

    # Function to change CSS class which is active to select theme
    def apply_theme(self, theme_name):
        js_code = f"""
        document.body.className = '';
        document.body.classList.add('{theme_name}');
        """
        self.call_js(js_code)

    # Function to inject js
    def call_js(self, js_code):
        anvil.js.window.eval(js_code)
