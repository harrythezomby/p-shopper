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
        self.populate_category_dropdown()

        # Perform initial filter to show all items
        self.refresh_data_grid()

        self.update_expiry_warning()
        self.update_list_title()

    def populate_lists_dropdown(self):
        user = anvil.users.get_user()
        lists = anvil.server.call('get_all_lists', user)
        self.ddListSelector.items = [(l['list_name'], l['list_id']) for l in lists if l['list_name']]
        if lists:
            self.ddListSelector.selected_value = lists[0]['list_id']
            self.refresh_data_grid()
        else:
            self.ddListSelector.selected_value = None
            self.data = []
            self.apply_filter_and_sort()
            self.lblIsEmpty.text = "The currently selected list is empty."
            self.lblIsEmpty.visible = True

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
            if new_category_name:
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
            if category_name:
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
    
    def populate_category_dropdown(self):
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories] + [("New Category", "New Category"), ("Remove Category", "Remove Category")]

    def ddListSelector_change(self, **event_args):
        self.refresh_data_grid()
        self.update_list_title()

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
          self.populate_category_dropdown()  # Refresh category dropdowns
          if not self.data:
              self.lblIsEmpty.text = "The currently selected list is empty."
              self.lblIsEmpty.visible = True
          else:
              self.lblIsEmpty.visible = False
      else:
          self.data = []
          self.apply_filter_and_sort()
          self.populate_category_dropdown()  # Refresh category dropdowns
          self.lblIsEmpty.text = "No list selected."
          self.lblIsEmpty.visible = True

    def btnCreateItem_click(self, **event_args):
        item_name = self.tbNewItemName.text
        category_id = self.ddNewItemCategory.selected_value
        list_id = self.ddListSelector.selected_value
    
        if self.tbNewItemQuantity.text == 0 or None:
            quantity = 1
        else:
            quantity = self.tbNewItemQuantity.text
    
        none = "None"
    
        if self.tbNewItemBrand.text == "" or None:
            brand = none
        else:
            brand = self.tbNewItemBrand.text
    
        if self.tbNewItemStore.text == "" or None:
            store = none
        else:
            store = self.tbNewItemStore.text
    
        if self.tbNewItemAisle.text == "" or None:
            aisle = none
        else:
            aisle = self.tbNewItemAisle.text
    
        anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle, list_id)
        alert("Item added successfully.")
        self.refresh_data_grid()
    
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
        current_list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
        content = TextBox(text=current_list_name)
        result = alert("Enter new name for the list:", buttons=[("OK", "ok")], content=content, title="Rename List")
        if result == "ok":
            new_name = content.text
            if new_name:
                anvil.server.call('rename_list', selected_list_id, new_name)
                self.populate_lists_dropdown()
                self.update_list_title()
  
    def btnNewList_click(self, **event_args):
        content = TextBox()
        result = alert("Enter name for the new list:", buttons=[("OK", "ok")], content=content, title="Create New List")
        if result == "ok":
            new_name = content.text.strip().title()
            if new_name:
                user = anvil.users.get_user()
                anvil.server.call('create_new_list', new_name, user)
                self.populate_lists_dropdown()

    def btnExport_click(self, **event_args):
        selected_list_id = self.ddListSelector.selected_value
        csv_file = anvil.server.call('export_items_to_csv', selected_list_id)
        download(csv_file)

    def check_off_item(self, item_id, list_id, **event_args):
        content = formCheckItem(item_id=item_id, list_id=list_id, parent_form=self)
        alert(content=content, large=True, buttons=[], title="Check Off Item")

    def update_list_title(self):
        selected_list_id = self.ddListSelector.selected_value
        if selected_list_id:
            list_name = [item[0] for item in self.ddListSelector.items if item[1] == selected_list_id][0]
            self.lblListTitle.text = list_name

    def btnLogout_click(self, **event_args):
        anvil.users.logout()
        open_form('formLogin')

