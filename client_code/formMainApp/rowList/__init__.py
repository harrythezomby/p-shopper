from ._anvil_designer import rowListTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..formCheckItem import formCheckItem

class rowList(rowListTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Populate category dropdown immediately
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddCategory.items = [(r['category_name'], r['category_id']) for r in categories]

    def btnEdit_click(self, **event_args):
        # Populate category dropdown before showing the write view
        user = anvil.users.get_user()
        categories = anvil.server.call('get_all_categories', user)
        self.ddCategory.items = [(r['category_name'], r['category_id']) for r in categories]

        # Set the selected value to the current item's category
        current_category = self.item['category_id']
        if current_category:
            self.ddCategory.selected_value = current_category['category_id']
        
        self.dataRowPanelWriteView.visible = True
        self.dataRowPanelReadView.visible = False

    def btnSaveEdits_click(self, **event_args):
      # Sanitize and validate item name
      item_name = self.tbItemName.text.strip().title()
      if not all(c.isalnum() or c.isspace() for c in item_name):
          alert("Item name can only contain English alphanumeric characters and spaces.")
          self.tbItemName.text = ""
          return
      
      # Validate and set quantity
      quantity_text = self.tbQuantity.text.strip()
      if not quantity_text:
          quantity = 1
      else:
          try:
              quantity = int(quantity_text)
              if quantity <= 0:
                  alert("Quantity must be a positive integer.")
                  self.tbQuantity.text = ""
                  return
          except ValueError:
              alert("Quantity must be an integer.")
              self.tbQuantity.text = ""
              return
      
      # Sanitize and validate brand
      brand = self.tbBrand.text.strip() if self.tbBrand.text else "None"
      # Allow letters, numbers, and specific symbols for Australian businesses
      if not all(c.isalnum() or c in " .&-_" for c in brand):
          alert("Brand can only contain letters, numbers, and the symbols .&-_")
          self.tbBrand.text = ""
          return
      
      # Sanitize and validate store
      store = self.tbStore.text.strip() if self.tbStore.text else "None"
      if not all(c.isalnum() or c in " .&-_" for c in store):
          alert("Store can only contain letters, numbers, and the symbols .&-_")
          self.tbStore.text = ""
          return
      
      # Sanitize and validate aisle
      aisle = self.tbAisle.text.strip().title() if self.tbAisle.text else "None"
      if not all(c.isalnum() or c.isspace() for c in aisle):
          alert("Aisle can only contain English alphanumeric characters and spaces.")
          self.tbAisle.text = ""
          return
      
      # Get selected category ID
      selected_category_id = self.ddCategory.selected_value
      category = anvil.server.call('get_category_by_id', selected_category_id)
  
      # Save the edited item to the database
      anvil.server.call(
          'edit_item',
          item_id=self.item['item_id'],
          item_name=item_name,
          quantity=quantity,
          category_id=category['category_id'],
          brand=brand,
          store=store,
          aisle=aisle
      )
  
      # Update the UI
      self.dataRowPanelReadView.visible = True
      self.dataRowPanelWriteView.visible = False
      self.refresh_data_bindings()
      self.parent.parent.parent.refresh_data_grid()


    def btnDelete_click(self, **event_args):
        item_id = self.item['item_id']
        confirm_delete = confirm("Are you sure you want to delete this item?")
        if confirm_delete:
            anvil.server.call('delete_item', item_id)
            alert("Item deleted successfully.")
            self.raise_event('x-refresh-data')
            self.refresh_data_bindings()
            self.parent.parent.parent.refresh_data_grid()

    def btnCheck_click(self, **event_args):
        item_id = self.item['item_id']
        
        # Call the server function to get the list item row
        list_item_row = anvil.server.call('get_list_item_row', item_id)
        if list_item_row:
            list_item_id = list_item_row['list_item_id']
            content = formCheckItem(item_id=item_id, list_item_id=list_item_id, parent_form=self)
            alert(content=content, large=True, buttons=[], title="Check Off Item")
        else:
            alert("Error: List item not found.")
        self.refresh_data_bindings()
        self.parent.parent.parent.refresh_data_grid()