# Imports
from ._anvil_designer import formCatConsGraphTemplate
from anvil import *
import anvil.users
import anvil.server
import plotly.graph_objs as go
import datetime

class formCatConsGraph(formCatConsGraphTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set default timeframe
        self.timeframe = 'week'
        self.radioWeek.selected = True

        # Populate the category dropdown
        self.ddCatSelector.items = [(r['category_name'], r['category_id']) for r in anvil.server.call('get_all_categories_for_graphs')]

        # Set default selection
        self.ddCatSelector.selected_value = self.ddCatSelector.items[0][1]

        # Plot the initial graph
        self.plot_graph()

    def plot_graph(self):
        category_id = self.ddCatSelector.selected_value
        timeframe = self.timeframe

        # Get the data from the server
        data = anvil.server.call('get_category_consumption_data', category_id, timeframe)
        
        # Sort data based on the actual date for correct chronological order
        data.sort(key=lambda x: x['date'])

        # Set the x and y data for the graph
        x = [item['date'] for item in data]
        y = [item['quantity'] for item in data]

        # Sets the timeframe behaviour of the graph
        if timeframe == 'week':
            x_labels = [f"Week {label}" for label in x]
            x_axis_title = 'Week'
        elif timeframe == 'month':
            x_labels = x  # Already formatted as month names
            x_axis_title = 'Month'
        elif timeframe == 'year':
            x_labels = [str(int(float(label))) for label in x]  # Ensure no decimal years
            x_axis_title = 'Year'

        # Find the category name
        category_name = next((cat[0] for cat in self.ddCatSelector.items if cat[1] == category_id), "Category")

        # Sets properties of the plotly graph
        self.plotGraphCatCons.data = [go.Bar(x=x_labels, y=y, name='Consumption')]
        self.plotGraphCatCons.layout = go.Layout(
            title=f"{category_name} Consumption",
            xaxis=dict(title=x_axis_title, tickvals=x_labels, ticktext=x_labels),
            yaxis=dict(title='Quantity')
        )

        # Ensure the plot is refreshed
        self.plotGraphCatCons.redraw()

    # Updates the graph when the category is changed
    def ddCatSelector_change(self, **event_args):
        self.plot_graph()

    # Updates the graph when the timeframe is changed
    def radioWeek_change(self, **event_args):
        if self.radioWeek.selected:
            self.timeframe = 'week'
            self.plot_graph()

    def radioMonth_change(self, **event_args):
        if self.radioMonth.selected:
            self.timeframe = 'month'
            self.plot_graph()

    def radioYear_change(self, **event_args):
        if self.radioYear.selected:
            self.timeframe = 'year'
            self.plot_graph()


