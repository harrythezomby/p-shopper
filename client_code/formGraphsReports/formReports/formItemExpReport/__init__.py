# Imports
from ._anvil_designer import formItemExpReportTemplate
from anvil import *
import anvil.users
import anvil.server

class formItemExpReport(formItemExpReportTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set default timeframe
        self.timeframe = 'week'
        self.radioWeek.selected = True

        # Flag to track if alert has been shown
        self.alert_shown = False

        # Generate the initial report
        self.generate_report()

    def generate_report(self):
        # Fetch report data from the server
        future_items, expired_items, alert_items = anvil.server.call('get_expiry_report', self.timeframe)

        # Create report in markdown format
        report_markdown = """
### Item Expiry Report

#### Future Expiry Items
| Item Name | Expiry Date |
| --- | --- |
"""
        for item in future_items:
            report_markdown += f"| {item['item_name']} | {item['expiry_date']} |\n"

        report_markdown += """
#### Recently Expired Items
| Item Name | Expiry Date |
| --- | --- |
"""
        for item in expired_items:
            report_markdown += f"| {item['item_name']} | {item['expiry_date']} |\n"

        # Display the report in the rich text component
        self.textReport.content = report_markdown

        # Show alert if there are items expiring in the next two days and if the alert hasn't been shown yet
        if alert_items and not self.alert_shown:
            alert(f"The following item(s) are expiring in the next two days: {', '.join(alert_items)}")
            self.alert_shown = True  # Set the flag to True after showing the alert

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
        media = anvil.BlobMedia("text/markdown", report_markdown.encode(), name="expiry_report.md")

        # Download the file
        download(media)