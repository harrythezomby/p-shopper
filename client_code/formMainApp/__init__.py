from ._anvil_designer import formMainAppTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .formInitiateShare import formInitiateShare
from .formSettings import formSettings

class formMainApp(formMainAppTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

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

        self.refresh_data_grid()

        # Populate the category dropdown
        categories = anvil.server.call('get_all_categories')
        self.ddCategorySelector.items = [('All Categories', None)] + [(r['category_name'], r['category_id']) for r in categories]
        self.ddNewItemCategory.items = [(r['category_name'], r['category_id']) for r in categories]

        # Perform initial filter to show all items
        self.filter()

        self.update_expiry_warning()

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
        self.data = anvil.server.call('get_all_items')
        self.apply_filter_and_sort()  # Apply filter and sort after fetching data

    def btnCreateItem_click(self, **event_args):
        """This method is called when the button is clicked"""
        item_name = self.tbNewItemName.text
        category_id = self.ddNewItemCategory.selected_value

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

        anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle)
        alert("Item added successfully.")
        self.refresh_data_grid()

        # Clearing the previous input fields after the item is added
        self.tbNewItemName.text = ""
        self.tbNewItemQuantity.text = ""
        self.tbNewItemBrand.text = ""
        self.tbNewItemStore.text = ""
        self.tbNewItemAisle.text = ""

    def sort_by_column(self, column):
        # Determine the current sort direction and toggle it
        if self.current_sort_column == column:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_column = column
            self.current_sort_reverse = False  # Start with ascending

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
        # Apply filter
        selected_category = self.ddCategorySelector.selected_value
        if selected_category:
            filtered_data = [item for item in self.data if item['category_id']['category_id'] == selected_category]
        else:
            filtered_data = self.data

        # Apply search filter
        if search_query:
            filtered_data = [item for item in filtered_data if search_query.lower() in item['item_name'].lower()]

        # Apply sorting
        sorted_data = self.sort_data(filtered_data)

        self.repeatListItems.items = sorted_data

        # Update arrow direction
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
        """This method is called when the button is clicked"""
        # Alert to display the form in a popup
        alert(content=formInitiateShare(),  # For now, the edit button will just use the new item form for simplicity, this may be changed later on
              large=False,
              buttons=[],
              title="Initiate Share")

    def btnReports_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('formGraphsReports')

    def btnSettings_click(self, **event_args):
        """This method is called when the button is clicked"""
        alert(content=formSettings(),  # For now, the edit button will just use the new item form for simplicity, this may be changed later on
              large=False,
              buttons=[],
              title="Settings")

    def btnExport_click(self, **event_args):
        """This method is called when the export button is clicked"""
        csv_file = anvil.server.call('export_items_to_csv')
        download(csv_file)

    
