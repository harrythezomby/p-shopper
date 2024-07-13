import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def getAllItems():
  rows = app_tables.tblitems.search()
  return rows # Not a good practice, since can be a security risk. In a more security oriented situation consider exporting as a different object.
