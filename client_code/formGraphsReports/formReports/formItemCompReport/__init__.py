# Imports
from ._anvil_designer import formItemCompReportTemplate
from anvil import *
import anvil.users
import anvil.server

class formItemCompReport(formItemCompReportTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set default timeframe
        self.timeframe = 'week'
        self.radioWeek.selected = True

        # Generate the initial report
        self.generate_report()

    def generate_report(self):
        timeframe = self.timeframe

        # Fetch report data from the server
        report_data = anvil.server.call('get_item_comparison_report_data', timeframe)

        # Extract data
        most_bought_item = report_data['most_bought_item']
        most_bought_date = report_data['most_bought_date']
        most_bought_category = report_data['most_bought_category']
        total_quantity = report_data['total_quantity']
        total_spending = report_data['total_spending']
        start_date = report_data['start_date']
        end_date = report_data['end_date']

        # Create report in markdown format
        report_markdown = f"""
### Item Comparison Report

**Timeframe**: {timeframe.capitalize()}

**Date Range**: {start_date} to {end_date}

**Most Bought Item**: {most_bought_item[0]} ({most_bought_item[1]} units)

**Most Bought Date**: {most_bought_date[0]} ({most_bought_date[1]} units)

**Most Bought Category**: {most_bought_category[0]} ({most_bought_category[1]} units)

**Total Quantity of Items Bought**: {total_quantity} units

**Total Spending**: ${total_spending:.2f}
"""

        # Display the report in the rich text component
        self.textReport.content = report_markdown

    # Timeframe selectors
    def radioWeek_change(self, **event_args):
        if self.radioWeek.selected:
            self.timeframe = 'week'
            self.generate_report()

    def radioMonth_change(self, **event_args):
        if self.radioMonth.selected:
            self.timeframe = 'month'
            self.generate_report()

    def radioYear_change(self, **event_args):
        if self.radioYear.selected:
            self.timeframe = 'year'
            self.generate_report()

    # Exporting the report
    def btnExport_click(self, **event_args):
        # Generate report markdown
        report_markdown = self.textReport.content
        
        # Create a BlobMedia object for the markdown file
        media = anvil.BlobMedia("text/markdown", report_markdown.encode(), name="item_comparison_report.md")
        
        # Download the file
        download(media)
