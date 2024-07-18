import anvil.server
import anvil
import anvil.tables as tables
from anvil.tables import app_tables

def parse_url_hash(url_hash):
    params = {}
    if url_hash:
        hash_string = url_hash.lstrip('#')
        pairs = hash_string.split('&')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
    return params

def get_list_id_from_url(url_hash):
    params = parse_url_hash(url_hash)
    return params.get('list_id', None)

def get_share_url_from_url(url_hash):
    params = parse_url_hash(url_hash)
    return params.get('share_url', None)

def load_shared_list(share_url):
    shared_list = anvil.server.call('get_shared_list', share_url)
    if shared_list:
        return {'list_name': shared_list['list_name'], 'list_id': shared_list['list_id']}
    return None

def disable_user_interaction(form):
    form.btnNewList.visible = False
    form.btnRenameList.visible = False
    form.btnDeleteList.visible = False
    form.btnExport.visible = False
    form.btnCreateItem.visible = False
    form.tbNewItemName.enabled = False
    form.tbNewItemQuantity.enabled = False
    form.tbNewItemBrand.enabled = False
    form.tbNewItemStore.enabled = False
    form.tbNewItemAisle.enabled = False
    form.ddNewItemCategory.enabled = False
    form.btnSettings.visible = False
    form.btnShare.visible = False

def handle_sharing_logic(form):
    url_hash = anvil.get_url_hash()
    share_url = get_share_url_from_url(url_hash)

    if share_url:
        shared_list = load_shared_list(share_url)
        if shared_list:
            form.ddListSelector.items = [(shared_list['list_name'], shared_list['list_id'])]
            form.ddListSelector.selected_value = shared_list['list_id']
            form.refresh_data_grid()
            disable_user_interaction(form)
        else:
            alert("Invalid or expired share URL.")
            open_form('formLogin')
    else:
        form.populate_lists_dropdown()
        form.update_expiry_warning()
        form.update_list_title()
        form.refresh_data_grid()

def generate_share_url(form):
    selected_list_id = form.ddListSelector.selected_value
    if not selected_list_id:
        alert("No list selected to share.")
        return

    confirm_share = confirm(f"Do you want to share the list '{form.ddListSelector.selected_text}'?")
    if confirm_share:
        share_url = anvil.server.call('generate_share_url', selected_list_id)
        anvil.set_url_hash(f"share_url={share_url}")
        alert(f"List shared successfully. Share URL: {anvil.server.get_app_origin()}#share_url={share_url}")

def unshare_list(form):
    selected_list_id = form.ddListSelector.selected_value
    if not selected_list_id:
        alert("No list selected to unshare.")
        return

    confirm_unshare = confirm(f"Do you want to stop sharing the list '{form.ddListSelector.selected_text}'?")
    if confirm_unshare:
        anvil.server.call('unshare_list', selected_list_id)
        anvil.set_url_hash('')
        alert("List unshared successfully.")

