from ._anvil_designer import formMainAppTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .formInitiateShare import formInitiateShare
from .formSettings import formSettings
from .formCheckItem import formCheckItem

class formMainApp(formMainAppTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.set_event_handler('x-refresh-data', self.refresh_data_grid)
        
        # Initialize data and headers
        self.data = []
        self.headers = {
            'item_name': self.linkItemName,
            'quantity': self.linkQuantity,
            'category_id': self.linkCategory,
            'brand': self.linkBrand,
            'store': self.linkStore,
            'aisle': self.linkAisle
        }
        
        # Set default sorting to item_name in ascending order
        self.current_sort_column = 'item_name'
        self.current_sort_reverse = False  # Start with ascending

        self.populate_lists_dropdown()
        
        # Populate the category dropdown
        categories = anvil.server.call('get_all_categories')
        self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]
        self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories] + [("New Category", "new"), ("Remove Category", "remove")]

        # Perform initial filter to show all items
        self.filter()

        self.update_expiry_warning()

        self.refresh_data_grid()

    def populate_lists_dropdown(self):
        lists = anvil.server.call('get_all_lists')
        self.ddListSelector.items = [(l['list_name'], l['list_id']) for l in lists if l['list_name']]
        if lists:
            max_list_id = max(l['list_id'] for l in lists)
            self.ddListSelector.selected_value = max_list_id
            self.refresh_data_grid()
        else:
            self.ddListSelector.selected_value = None
            self.data = []  # Clear the data if there are no lists
            self.apply_filter_and_sort()

    def ddListSelector_change(self, **event_args):
        self.refresh_data_grid()

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
            self.apply_filter_and_sort(search_query=self.tbSearchList.text)  # Ensure the search term is applied
    
            # Update the category filter dropdown based on the current list's categories
            categories = anvil.server.call('get_categories_for_list', selected_list_id)
            self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]
            
            # Update the list title
            list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
            self.lblListTitle.text = list_name
        else:
            self.data = []
            self.apply_filter_and_sort()
            self.ddCategorySelector.items = [('All Categories', None)]  # Reset categories when no list is selected
            self.lblListTitle.text = "No List Selected"

    def btnCreateItem_click(self, **event_args):
        """This method is called when the button is clicked"""
        item_name = self.tbNewItemName.text
        category_id = self.ddNewItemCategory.selected_value
        list_id = self.ddListSelector.selected_value
    
        # If quantity is blank, assume 1
        if self.tbNewItemQuantity.text == 0 or None:
            quantity = 1
        else:
            quantity = self.tbNewItemQuantity.text
    
        none = "None"  # Assuming blank/N/A value, can be changed to whatever here easily
    
        # If brand is empty assume no brand
        if self.tbNewItemBrand.text == "" or None:
            brand = none
        else:
            brand = self.tbNewItemBrand.text
    
        # If store is empty assume no store
        if self.tbNewItemStore.text == "" or None:
            store = none
        else:
            store = self.tbNewItemStore.text
    
        # If aisle is empty assume no aisle
        if self.tbNewItemAisle.text == "" or None:
            aisle = none
        else:
            aisle = self.tbNewItemAisle.text
    
        anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle, list_id)
        alert("Item added successfully.")
        self.refresh_data_grid()
    
        # Clear input fields
        self.tbNewItemName.text = ""
        self.tbNewItemQuantity.text = ""
        self.tbNewItemBrand.text = ""
        self.tbNewItemStore.text = ""
        self.tbNewItemAisle.text = ""

    def sort_by_column(self, column):
        if self.current_sort_column == column:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_column = column
            self.current_sort_reverse = False

        self.apply_filter_and_sort()

    def sort_data(self, data):
        if self.current_sort_column == 'category_id':
            sorted_data = sorted(
                data,
                key=lambda x: x[self.current_sort_column]['category_name'].lower(),
                reverse=self.current_sort_reverse
            )
        else:
            sorted_data = sorted(
                data,
                key=lambda x: str(x[self.current_sort_column]).lower(),
                reverse=self.current_sort_reverse
            )
        return sorted_data

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

    def btnShare_click(self, **event_args):
        alert(content=formInitiateShare(), large=False, buttons=[], title="Initiate Share")

    def btnReports_click(self, **event_args):
        open_form('formGraphsReports')

    def btnSettings_click(self, **event_args):
        alert(content=formSettings(), large=False, buttons=[], title="Settings")

    def btnRenameList_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        current_list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]  # Get the current list name
        content = TextBox(text=current_list_name)  # Set the default value to the current list name
        result = alert("Enter new name for the list:", buttons=[("OK", "ok")], content=content, title="Rename List")
        if result == "ok":
            new_name = content.text
            if new_name:
                anvil.server.call('rename_list', selected_list_id, new_name)
                self.populate_lists_dropdown()
  
    def btnNewList_click(self, **event_args):
        content = TextBox()
        result = alert("Enter name for the new list:", buttons=[("OK", "ok")], content=content, title="Create New List")
        if result == "ok":
            new_name = content.text
            if new_name:
                anvil.server.call('create_new_list', new_name)
                self.populate_lists_dropdown()

    def btnExport_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        csv_file = anvil.server.call('export_items_to_csv', selected_list_id)
        download(csv_file)

    def check_off_item(self, list_item_id, **event_args):
        content = formCheckItem(list_item_id, parent_form=self)
        alert(content=content, large=True, buttons=[], title="Check Off Item")

    def ddNewItemCategory_change(self, **event_args):
        selected_value = self.ddNewItemCategory.selected_value
        if selected_value == "new":
            self.create_new_category()
        elif selected_value == "remove":
            self.remove_category()
        else:
            self.ddNewItemCategory.selected_value = selected_value  # Ensure it stays on the selected category

    def create_new_category(self):
        content = TextBox()
        result = alert("Enter name for the new category:", buttons=[("OK", "ok")], content=content, title="Create New Category")
        if result == "ok":
            new_category_name = content.text.title()  # Capitalize the category name
            if new_category_name:
                anvil.server.call('create_new_category', new_category_name)
                # Refresh the category dropdowns
                categories = anvil.server.call('get_all_categories')
                self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories] + [("New Category", "new"), ("Remove Category", "remove")]
                self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]
                # Reset dropdown to first category
                self.ddNewItemCategory.selected_value = categories[0]['category_id'] if categories else None
            else:
                # Reset dropdown to first category
                self.ddNewItemCategory.selected_value = self.ddNewItemCategory.items[0][1]
        else:
            # Reset dropdown to first category
            self.ddNewItemCategory.selected_value = self.ddNewItemCategory.items[0][1]

    def remove_category(self):
        content = TextBox()
        result = alert("Enter name of the category to remove:", buttons=[("OK", "ok")], content=content, title="Remove Category")
        if result == "ok":
            category_name_to_remove = content.text.title()  # Capitalize the category name
            if category_name_to_remove:
                response = anvil.server.call('remove_category', category_name_to_remove)
                alert(response)
                # Refresh the category dropdowns
                categories = anvil.server.call('get_all_categories')
                self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories] + [("New Category", "new"), ("Remove Category", "remove")]
                self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]
                # Reset dropdown to first category
                self.ddNewItemCategory.selected_value = categories[0]['category_id'] if categories else None
            else:
                # Reset dropdown to first category
                self.ddNewItemCategory.selected_value = self.ddNewItemCategory.items[0][1]
        else:
            # Reset dropdown to first category
            self.ddNewItemCategory.selected_value = self.ddNewItemCategory.items[0][1]
