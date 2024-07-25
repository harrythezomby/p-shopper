from ._anvil_designer import formMainAppTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .formInitiateShare import formInitiateShare
from .formThemes import formThemes
from .formCheckItem import formCheckItem

class formMainApp(formMainAppTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.set_event_handler('x-refresh-data', self.refresh_data_grid)
        
        self.data = []
        self.headers = {
            'item_name': self.linkItemName,
            'quantity': self.linkQuantity,
            'category_id': self.linkCategory,
            'brand': self.linkBrand,
            'store': self.linkStore,
            'aisle': self.linkAisle
        }
        
        self.current_sort_column = 'item_name'
        self.current_sort_reverse = False

        self.apply_user_theme()  # Apply the user's theme on startup
      
        self.populate_lists_dropdown()
        self.update_expiry_warning()
        self.update_list_title()
        
        # Refresh data grid after initial population
        self.refresh_data_grid()


    """Setting up (grabbing data from database, etc)"""
    def populate_lists_dropdown(self):
        user = anvil.users.get_user()
        lists = anvil.server.call('get_all_lists', user)
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

    def populate_category_dropdown(self):
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories] + [("New Category", "New Category"), ("Remove Category", "Remove Category")]
        selected_list_id = self.ddListSelector.selected_value
        if selected_list_id:
            categories = anvil.server.call('get_categories_for_list', selected_list_id)
            self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]



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
        self.apply_filter_and_sort(search_query=self.tbSearchList.text)

    def update_expiry_warning(self):
        expiring_soon_items = anvil.server.call('get_items_expiring_soon')
        if expiring_soon_items:
            self.lblExpiryWarning.text = f"The following item(s) are expiring soon: {', '.join(expiring_soon_items)}"
            self.lblExpiryWarning.visible = True
        else:
            self.lblExpiryWarning.visible = False

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

    def update_empty_label(self):
        if not self.data:
            self.lblIsEmpty.text = "The currently selected list is empty."
            self.lblIsEmpty.visible = True
        else:
            self.lblIsEmpty.visible = False
  
    

    def sort_by_column(self, column):
        if self.current_sort_column == column:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_column = column
            self.current_sort_reverse = False

        self.apply_filter_and_sort()

    def sort_data(self, data):
        try:
            if self.current_sort_column == 'category_id':
                sorted_data = sorted(
                    data,
                    key=lambda x: x[self.current_sort_column]['category_name'].lower() if x[self.current_sort_column] else "",
                    reverse=self.current_sort_reverse
                )
            else:
                sorted_data = sorted(
                    data,
                    key=lambda x: str(x[self.current_sort_column]).lower() if x[self.current_sort_column] else "",
                    reverse=self.current_sort_reverse
                )
            return sorted_data
        except Exception as e:
            # Handle any exceptions that may occur during sorting
            print(f"Error during sorting: {e}")
            return data

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
    def btnReports_click(self, **event_args):
        open_form('formGraphsReports')

    def btnThemes_click(self, **event_args):
        alert(content=formThemes(), large=True, buttons=[], title="Themes")

    def btnLogout_click(self, **event_args):
        anvil.users.logout()
        open_form('formLogin')
  
    

    

    

    def update_list_title(self):
        selected_list_id = self.ddListSelector.selected_value
        if selected_list_id:
            list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
            self.lblListTitle.text = list_name

    


  
    """Item Interaction"""
    def check_off_item(self, item_id, list_id, **event_args):
      content = formCheckItem(item_id=item_id, list_id=list_id, parent_form=self)
      alert(content=content, large=True, buttons=[], title="Check Off Item")

    def btnCreateItem_click(self, **event_args):
        # Sanitize and validate item name
        item_name = self.tbNewItemName.text.strip().title()
        if not item_name.isalnum():
            alert("Item name can only contain English alphanumeric characters.")
            self.tbNewItemName.text = ""
            return
        
        # Validate and set quantity
        try:
            quantity = int(self.tbNewItemQuantity.text)
            if quantity <= 0:
                alert("Quantity must be a positive integer.")
                self.tbNewItemQuantity.text = ""
                return
        except ValueError:
            quantity = 1
        
        # Sanitize and validate brand
        brand = self.tbNewItemBrand.text.strip()
        # Allow letters, numbers, and specific symbols for Australian businesses
        if not all(c.isalnum() or c in " .&-_" for c in brand):
            alert("Brand can only contain letters, numbers, and the symbols .&-_")
            self.tbNewItemBrand.text = ""
            return
        if brand == "":
            brand = "None"
        
        # Sanitize and validate store
        store = self.tbNewItemStore.text.strip()
        if not all(c.isalnum() or c in " .&-_" for c in store):
            alert("Store can only contain letters, numbers, and the symbols .&-_")
            self.tbNewItemStore.text = ""
            return
        if store == "":
            store = "None"
        
        # Sanitize and validate aisle
        aisle = self.tbNewItemAisle.text.strip().upper()
        if not aisle.isalnum():
            alert("Aisle can only contain English alphanumeric characters.")
            self.tbNewItemAisle.text = ""
            return
        if aisle == "":
            aisle = "None"
        
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
                self.prepare.populate_lists_dropdown()
                self.prepare.update_list_title()
                self.prepare.refresh_data_grid()
            else:
                alert(message)

    def btnNewList_click(self, **event_args):
        content = TextBox()
        result = alert("Enter name for the new list:", buttons=[("OK", "ok")], content=content, title="Create New List")
        if result == "ok":
            new_name = content.text.strip().title()
            if not new_name or not new_name.replace("'", "").replace(" ", "").isalnum():
                alert("List name can only contain English alphanumeric characters, spaces, and apostrophes. Please try again.")
                return
            if new_name:
                user = anvil.users.get_user()
                anvil.server.call('create_new_list', new_name, user)
                self.populate_lists_dropdown()
                self.update_list_title()

    def btnRenameList_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        current_list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
        content = TextBox(text=current_list_name)
        result = alert("Enter new name for the list:", buttons=[("OK", "ok")], content=content, title="Rename List")
        if result == "ok":
            new_name = content.text.strip().title()
            if not new_name or not new_name.replace("'", "").replace(" ", "").isalnum():
                alert("List name can only contain English alphanumeric characters, spaces, and apostrophes. Please try again.")
                return
            if new_name:
                anvil.server.call('rename_list', selected_list_id, new_name)
                self.populate_lists_dropdown()
                self.update_list_title()


    """Exporting"""
    def btnExport_click(self, **event_args):
          selected_list_id = self.ddListSelector.selected_value
          csv_file = anvil.server.call('export_items_to_csv', selected_list_id)
          download(csv_file)


    """Theming"""
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
