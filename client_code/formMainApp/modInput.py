import anvil.server
from anvil import alert, TextBox

class modInput:
    def __init__(self, main_app):
        self.main_app = main_app

    def btnCreateItem_click(self, **event_args):
        item_name = self.main_app.tbNewItemName.text
        category_id = self.main_app.ddNewItemCategory.selected_value
        list_id = self.main_app.ddListSelector.selected_value
    
        quantity = self.main_app.tbNewItemQuantity.text or 1
        brand = self.main_app.tbNewItemBrand.text or "None"
        store = self.main_app.tbNewItemStore.text or "None"
        aisle = self.main_app.tbNewItemAisle.text or "None"
    
        anvil.server.call('add_item', item_name, quantity, category_id, brand, store, aisle, list_id)
        alert("Item added successfully.")
        self.main_app.refresh_data_grid()
    
        self.main_app.tbNewItemName.text = ""
        self.main_app.tbNewItemQuantity.text = ""
        self.main_app.tbNewItemBrand.text = ""
        self.main_app.tbNewItemStore.text = ""
        self.main_app.tbNewItemAisle.text = ""

    def ddNewItemCategory_change(self, **event_args):
        selected_value = self.main_app.ddNewItemCategory.selected_value
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
                    self.main_app.populate_category_dropdown()
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
                    self.main_app.populate_category_dropdown()
                    alert("Category removed successfully.")
                else:
                    alert(message)
        self.revert_category_selection()
    
    def revert_category_selection(self):
        if self.main_app.ddNewItemCategory.items:
            self.main_app.ddNewItemCategory.selected_value = self.main_app.ddNewItemCategory.items[0][1]
