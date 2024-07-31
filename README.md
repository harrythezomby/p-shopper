# Welcome to P-Shopper!
![image](https://github.com/user-attachments/assets/258fdd1b-57e3-4469-af37-9bf5b801bdc5)

## Note to Developers:
If testing/playing around with the app in a development environment, such as straight from an Anvil clone link, make sure to follow the standard account creation steps present within the app itself. This is because P-Shopper performs a variety of tasks behind the scenes upon new user accounts being created, which has to do setting up graphs and reports, as well as creating a default list for the new user. If this isn't done, errors _will_ be encountered, so please keep this in mind!

# Creating List Items

P-Shopper provides an intuitive way to add new items to your shopping list:

### Add New Item
![image](https://github.com/user-attachments/assets/56d42af9-779c-4f88-8dfd-668e61d2d86b)

- **Input Fields**:
  - **Item Name**: Enter the name of the item you wish to add. Only English alphanumeric characters are allowed.
  - **Quantity**: Specify the quantity. If left blank, it defaults to 1. Quantity must be a positive integer.
  - **Category**: Select a category from the dropdown. If needed, you can create a new category or remove an existing one.
  - **Brand**: Enter the brand name, which can include letters, numbers, and certain symbols.
  - **Store**: Specify the store name, allowing similar characters as the brand.
  - **Aisle**: Enter the aisle number or identifier, restricted to English alphanumeric characters and capitalized.

### Validation
- **Input Validation**: The app checks inputs for validity. If any input is invalid, an alert will notify you with the specific issue.
- **Sanitization**: All inputs are sanitized by trimming whitespace and capitalizing as needed.

### Add Item
- **Save Item**: Click the "Add Item" button to save the item to your list. The list will update to show the new item.

# Editing List Items
![image](https://github.com/user-attachments/assets/e581437a-4738-4666-9e4d-f2262b09aac8)

![image](https://github.com/user-attachments/assets/084aab19-fee4-450f-8d65-a561d5ef8c52)

P-Shopper allows you to edit the details of your list items:

### Edit Item
- **Initiate Edit**: Click on the edit icon next to the item you want to edit.
- **Edit Fields**: Modify the item's details in the provided fields.
- **Save Changes**: Click the "Save" button to apply the changes. The list will update with the edited details.

### Validation
- **Input Validation**: Similar to adding items, the app ensures that all inputs during editing are valid.
- **Sanitization**: Edited inputs are also sanitized by trimming whitespace and capitalizing as needed.

# Checking Off List Items

When you check off an item, P-Shopper records additional details for future calculations:

### Check Off Item
![image](https://github.com/user-attachments/assets/7ff628d1-304c-42b1-92b7-e5d05c31f7ad)
![image](https://github.com/user-attachments/assets/74810418-f7cb-4180-94aa-879b5915680a)


- **Checkbox**: Each item in your list has a checkbox.
- **Prompt**: Clicking the checkbox will prompt you to enter additional details, such as:
  - **Purchase Date**: The date you purchased the item.
  - **Expiry Date**: The date the item will expire.
  - **Price**: The price you paid for the item.

### Record Details
- **History**: Checked-off items are recorded in the long-term history database, including all relevant details.
- **Calculations**: These details are used for calculations in graphs and reports.

# Deleting List Items
![image](https://github.com/user-attachments/assets/081edd47-4890-4e4a-87d4-808b9f021ef1)


![image](https://github.com/user-attachments/assets/a786ed80-8866-4699-9fe3-1ebe13268544)


P-Shopper provides a straightforward way to delete items from your list:

### Delete Item
- **Initiate Delete**: First, click on the edit icon next to the item you want to delete.
- **Delete Icon**: Then, click the delete icon.
- **Confirmation**: An alert will ask if you are sure you want to delete the item.

### Validation
- **Confirmation Required**: The app ensures you cannot delete an item unless you confirm the action.
- **Remove Item**: Once confirmed, the item is removed from the list and the database. The list updates automatically to reflect the change.


# P-Shopper Input Validation Guide

P-Shopper ensures that all input data is sanitized and validated to maintain data integrity and avoid errors. Here is an explanation of the validation rules applied to different fields when adding or editing items:

## Item Name
- **Sanitization:** The item name is stripped of leading and trailing spaces and converted to title case.
- **Validation:** The item name must only contain English alphanumeric characters. No special characters or symbols are allowed.
- **Error Handling:** If the item name contains invalid characters, an alert will be displayed, and the input field will be cleared.

## Quantity
- **Sanitization:** The quantity is stripped of leading and trailing spaces.
- **Validation:** The quantity must be a positive integer. It cannot be zero, negative, or a floating-point number. It must also not be text of any sort.
- **Error Handling:** If the quantity is invalid, an alert will be displayed, and the input field will be cleared.

## Brand
- **Sanitization:** The brand name is stripped of leading and trailing spaces.
- **Validation:** The brand name can contain letters, numbers, and the symbols `.`, `&`, `-`, and `_`. It should not be empty.
- **Error Handling:** If the brand name contains invalid characters, an alert will be displayed, and the input field will be cleared. If the brand name is left blank, it will default to "None".

## Store
- **Sanitization:** The store name is stripped of leading and trailing spaces.
- **Validation:** The store name can contain letters, numbers, and the symbols `.`, `&`, `-`, and `_`. It should not be empty.
- **Error Handling:** If the store name contains invalid characters, an alert will be displayed, and the input field will be cleared. If the store name is left blank, it will default to "None".

## Aisle
- **Sanitization:** The aisle name is stripped of leading and trailing spaces and converted to uppercase.
- **Validation:** The aisle name must only contain English alphanumeric characters. No special characters or symbols are allowed.
- **Error Handling:** If the aisle name contains invalid characters, an alert will be displayed, and the input field will be cleared. If the aisle name is left blank, it will default to "None".

## Error Handling
If any of the above validation criteria are not met, an alert will inform you of the specific problem that needs to be remedied before proceeding with adding or editing an item.

By following these validation rules, P-Shopper ensures that all data entered into the system is clean, consistent, and reliable.



# Searching, Sorting, and Filtering

P-Shopper offers powerful tools to help you manage your shopping lists efficiently. Here's how you can use searching, sorting, and filtering to your advantage:

### Searching
![image](https://github.com/user-attachments/assets/59d6d178-c6aa-4f8f-b5a1-3faf19a1af1a)

- **Search Bar**: At the top of your shopping list, you'll find a search bar.
- **Functionality**: Simply type in the name of the item you're looking for, and the list will instantly update to show matching items.
- **Real-Time**: The search function works in real-time, filtering the list as you type.

### Sorting
![image](https://github.com/user-attachments/assets/4315542b-dd56-402b-9382-d2d7005f87a6)

- **Data Grid Titles**: Each column in your shopping list has a title that you can click to sort the items.
- **Sortable Columns**: You can sort items by name, quantity, category, brand, store, and aisle.
- **Toggle Sorting**: Clicking a column title will toggle between ascending and descending order, allowing you to quickly find what you need.
- **Indicators**: An arrow icon next to the column title indicates the current sort order (up for ascending, down for descending).

### Filtering by Category
![image](https://github.com/user-attachments/assets/855d637a-fc91-4a87-94ac-1890288d1ef1)


- **Category Filter Dropdown**: Located above your shopping list, this dropdown allows you to filter items by category.
- **Dynamic Categories**: The dropdown only shows categories that are present in the currently selected list, making it easy to find relevant items.
- **Select Category**: Choose a category from the dropdown to instantly filter the list and display only items in that category.
- **Show All**: To reset the filter and show all items, simply select "All Categories" from the dropdown.

# Explanation of the Dummy Item in P-Shopper
When you create a new account in P-Shopper, the system automatically sets up a few initial items to help you get started. Here’s what happens:

## New List and Default Theme

- **New List**: A default list named "New List" is created for you.
- **Default Theme**: The theme of the app is set to the default theme to ensure you have a visually appealing and consistent experience right from the start.

## Initial Category

- **First Category**: A category named "First Category" is created. This helps you organize your items right away.

## Example Item in Long-Term History

- **Example Item**: To help you understand how items are tracked, an example item is added to your long-term history. Here are its details:
  - **Item Name**: Example Item
  - **Category**: First Category
  - **Quantity**: 1
  - **Price**: 1
  - **Purchase Date**: The current date when you created your account
  - **Expiry Date**: The current date when you created your account
 
    

# Managing Lists in P-Shopper
![image](https://github.com/user-attachments/assets/c6a41e33-34ed-4c21-9cb3-10e76a635f5d)

## Creating a New List
![image](https://github.com/user-attachments/assets/6b8440d3-45e8-4836-a939-e4a7a6531d5d)

To create a new list in P-Shopper:

1. **Open the Create List Dialog**: Click the button labeled "New List" in the application.
2. **Enter List Name**: A dialog will appear asking you to enter the name for the new list.
3. **Validation**:
    - The list name must contain only English alphanumeric characters, spaces, and apostrophes.
    - The input is stripped of leading and trailing spaces and capitalized appropriately.
    - If the input is invalid (e.g., contains forbidden characters or is blank), an alert will notify you of the specific issue.
4. **Confirmation**: Upon entering a valid name and confirming, the list will be created and added to your list of shopping lists.

## Renaming a List
![image](https://github.com/user-attachments/assets/2b154da4-f60b-4264-8b66-531573cdb1ca)

To rename an existing list:

1. **Open the Rename List Dialog**: Select the list you want to rename from the dropdown and click the button labeled "Rename List."
2. **Enter New List Name**: A dialog will appear with the current name of the list pre-filled. Enter the new name for the list.
3. **Validation**:
    - The new list name must contain only English alphanumeric characters, spaces, and apostrophes.
    - The input is stripped of leading and trailing spaces and capitalized appropriately.
    - If the input is invalid (e.g., contains forbidden characters or is blank), an alert will notify you of the specific issue.
4. **Confirmation**: Upon entering a valid name and confirming, the list will be renamed and the new name will be reflected in your list of shopping lists.

## Deleting a List
![image](https://github.com/user-attachments/assets/d7b13a8d-dcf8-4a03-b8e6-82b6b3b9cdec)

To delete an existing list:

1. **Open the Delete List Confirmation**: Select the list you want to delete from the dropdown and click the button labeled "Delete List."
2. **Confirmation**: A confirmation dialog will appear, asking if you are sure you want to delete the selected list. The dialog will display the name of the list to be deleted.
3. **Finalization**:
    - If you confirm, the list will be deleted along with all its associated items.
    - **Note**: You cannot delete the last remaining list. An alert will notify you if you attempt to do so.

By following these steps, you can efficiently manage your shopping lists within P-Shopper while ensuring data integrity and proper validation.



# Categories
In P-Shopper, categories help you organize your shopping lists effectively. Here's how you can manage them:

1. **Adding a New Category**:
    - When creating a new item, you can select "New Category" from the dropdown.
    - This will prompt you to enter a name for the new category.
    - After you enter the name, the new category will be added and can be used for any new items you create.

2. **Removing a Category**:
    - You can also select "Remove Category" from the dropdown.
    - Enter the name of the category you wish to remove.
    - If the category is not in use by any items, it will be removed, and you'll receive a confirmation.
    - If the category is in use, you'll be notified that it cannot be deleted.
    - **Note**: If the category you are trying to delete is your last category, you will be informed that the last category cannot be deleted.

3. **Automatic Category Selection**:
    - After adding or removing a category, the dropdown will automatically reset to a default category to ensure smooth operation.

4. **First Category for New Users**:
    - When a new user is created, a default category named "First Category" is automatically added for them.
    - This ensures that new users have a starting point for organizing their items.

# List Exports

P-Shopper allows you to export your shopping lists to a CSV format, making it easy to share and manage your lists outside the app. Here's how it works:

## Exporting Lists
![image](https://github.com/user-attachments/assets/9315fb36-8269-4ce6-b6de-8b0520448d85)
![image](https://github.com/user-attachments/assets/59f3280d-789e-4fc4-980c-bffcfe5120ff)

### How to Export a List
- **Step 1**: Navigate to the list you want to export.
- **Step 2**: Click on the "Export" button.
- **Step 3**: The list will be exported to a CSV file, which can be downloaded to your device.

### CSV Format
- **Content**: The CSV file will include all the items in the selected list along with their details such as item name, category, quantity, brand, store, and aisle.
- **Usage**: This format is compatible with various spreadsheet applications, allowing you to open, edit, and share your list easily.

## Benefits of Exporting Lists

### Sharing
- **Flexibility**: Exported lists can be easily shared via email or other messaging platforms.
- **Collaboration**: Share your shopping list with family or friends, making it easier to coordinate shopping tasks.

### Backup
- **Safety**: Keep a backup of your shopping lists to ensure you don't lose any important data.
- **Access**: Store your exported lists in cloud storage or on your local device for easy access anytime.

### Integration
- **Compatibility**: The CSV format allows integration with other tools and applications, such as inventory management software or budgeting tools.
- **Customization**: Customize the exported list to fit your specific needs using spreadsheet applications.




# Graphs and Reports
![image](https://github.com/user-attachments/assets/606d8162-e416-4a1a-b124-ed54e443842f)


![image](https://github.com/user-attachments/assets/30ef5839-0900-417d-b7d9-59ea6dd80ca2)


![image](https://github.com/user-attachments/assets/cb5ce917-7b8d-4de1-a37f-c8154055d7ef)

P-Shopper offers robust graphing and reporting functionalities to help you analyze your shopping habits and expenditure patterns. Here's a detailed look at the features:

## Graphs

P-Shopper provides four types of graphs to visualize your data:

### 1. Item Price History Graph
- **Description**: This graph shows the price history of items over time.
- **Usage**: Helps you track price changes and identify trends in item pricing.

### 2. Category Consumption Graph
- **Description**: Displays your consumption patterns across different categories.
- **Usage**: Useful for understanding which categories you spend the most on.

### 3. Item Quantity Consumption Graph
- **Description**: Tracks the quantities of items consumed over time.
- **Usage**: Allows you to see how your consumption of specific items changes over time.

### 4. Monthly Spend History Graph
- **Description**: Shows your total spending on items each month.
- **Usage**: Helps you track your monthly expenditure and budget accordingly.

### Exporting Graphs
- **Note**: While P-Shopper does not provide a built-in export functionality for graphs, you can take screenshots of the graphs for your records and presentations.

## Reports
![image](https://github.com/user-attachments/assets/d8aadb90-1d9d-426b-b09a-1d0f089c9f61)


P-Shopper offers three types of reports to provide detailed insights into your shopping data:

### 1. Item Comparison Report
- **Description**: Compares different items based on various criteria such as price, quantity, and purchase frequency.
- **Usage**: Useful for analyzing which items offer the best value or are bought most frequently.

### 2. Item Expiry Report
- **Description**: Lists items nearing their expiry dates.
- **Usage**: Helps you manage inventory and reduce waste by identifying items that need to be consumed soon.

### 3. Weekly Spend Comparison Report
- **Description**: Compares your weekly spending over a selected period.
- **Usage**: Useful for budgeting and understanding your weekly spending patterns.

### Exporting Reports
- **Functionality**: Reports in P-Shopper can be exported directly to CSV format.
- **Usage**: This allows you to easily share and analyze your data using other software such as spreadsheets.

## User Experience

### Easy Navigation
- **Tabs**: Switch between different graphs and reports using the tabs in the Graphs and Reports section.
- **Interactive**: The interface allows you to interact with the graphs and reports, making it easy to drill down into specific data points.

### Real-Time Data
- **Up-to-Date**: Graphs and reports are generated using the most recent data, ensuring that your analysis is always current.

### Customization
- **Filters**: Apply filters to customize the data shown in the graphs and reports, allowing you to focus on the information that matters most to you.

By utilizing the graphs and reports in P-Shopper, you can gain valuable insights into your shopping habits, manage your budget more effectively, and ensure that your pantry is always well-stocked with fresh items.



# Items Expiring Soon
![image](https://github.com/user-attachments/assets/62f8a937-ce25-4ce0-9f9a-0fffd2fd40c2)

At the bottom of the P-Shopper screen, you may notice a message indicating items that are expiring soon. This feature helps you stay on top of your perishable goods and ensures you use them before they go bad.

### How It Works

- **Detection**: The system constantly checks for items in your shopping list that are nearing their expiry date.
- **Criteria**: An item is considered to be expiring soon if its expiry date falls within the next two days.
- **Notification**: When such items are detected, a message appears at the bottom of the screen listing the items that are expiring soon.
- **Visibility**: This message only appears when there are items that meet the criteria. If no items are expiring in the next two days, the message remains hidden, ensuring that your screen remains uncluttered.


# Themes

P-Shopper offers a variety of themes to customize the look and feel of your application. 
They can be selected via the 'Themes' button in the main app like so:
![image](https://github.com/user-attachments/assets/fcd4516e-4eb7-4b8a-af12-3f1879fd37a0)

![image](https://github.com/user-attachments/assets/28bd1edb-d420-442f-878e-4a064da31135)


Here are the available themes and their appearances:

### Default Theme
![image](https://github.com/user-attachments/assets/53eea71a-4f21-43c6-8c26-781638ce1e3e)

- **Appearance**: A modern and colorful theme featuring pastel blue and purple as its main colors. The background is a gradient from light blue to light purple.
- **Font**: 'Roboto', a clean and modern font.
- **Buttons**: Gradient buttons from blue to purple with rounded corners.
- **Dropdowns and Textboxes**: Light purple background with blue borders.
- **Other Elements**: Header and footer have a gradient background, and alerts have a matching gradient.

### Dark Theme
![image](https://github.com/user-attachments/assets/d7989936-b60f-4267-87c9-cfa0b72a4d8e)

- **Appearance**: A dark version of the Default Theme, with shades of dark blue and purple. The background is a gradient from dark blue to dark purple.
- **Font**: 'Roboto', providing a clean and modern look.
- **Buttons**: Gradient buttons from dark blue to dark purple with rounded corners.
- **Dropdowns and Textboxes**: Dark purple background with blue borders.
- **Other Elements**: Header and footer have a gradient background, and alerts have a matching gradient.

### Princess Theme
![image](https://github.com/user-attachments/assets/b57870d0-4435-41c0-aef9-2f4c5ca135f4)

- **Appearance**: A vibrant theme with pink and blue as its main colors. The background is a gradient from pink to blue.
- **Font**: 'Dancing Script', a whimsical and elegant font.
- **Buttons**: Gradient buttons from pink to blue with rounded corners.
- **Dropdowns and Textboxes**: Light pink background with blue borders.
- **Other Elements**: Header and footer have a gradient background, and alerts have a matching gradient.

### Sakura Theme
![image](https://github.com/user-attachments/assets/f9fb062e-c039-4811-a280-4ef00e46279f)

- **Appearance**: A soft and elegant theme with shades of pink and white. The background is a gradient from light pink to white.
- **Font**: 'Sakura Blossom', an elegant and delicate font.
- **Buttons**: Gradient buttons from pink to white with rounded corners.
- **Dropdowns and Textboxes**: Light pink background with white borders.
- **Other Elements**: Header and footer have a gradient background, and alerts have a matching gradient.

### Plainish Theme
![image](https://github.com/user-attachments/assets/a9d6d59a-8c5f-4779-b255-341e981fc616)

- **Appearance**: A minimalist theme with shades of gray and white. The background is a gradient from light gray to white.
- **Font**: 'Helvetica', a clean and simple font.
- **Buttons**: Solid gray buttons with rounded corners.
- **Dropdowns and Textboxes**: Light gray background with white borders.
- **Other Elements**: Header and footer have a gradient background, and alerts have a matching gradient.

Each theme ensures a unique user experience, allowing you to personalize P-Shopper to your liking. You can change the theme in the Settings menu, and your selection will be remembered for your next visit.

# Disclaimer

## Account and Login Requirements

To ensure the full functionality and optimal performance of P-Shopper, users are required to create an account and remain logged in while using the app. Here’s why this is necessary:

### Why an Account is Necessary

1. **Personalized Experience**: By logging in, P-Shopper can provide a personalized experience tailored to your preferences and shopping habits. This includes saving your preferred themes, categories, and lists.

2. **Data Management**: User accounts allow P-Shopper to securely store and manage your data. This ensures that your shopping lists, categories, and item history are saved and can be accessed across multiple sessions and devices.

3. **Automated Functions**: Certain functions, such as category management, list exporting, and item tracking, rely on user-specific data. These functions can only be automated and managed effectively when the user is logged in.

4. **Security and Privacy**: User accounts help ensure that your data is secure and private. Without an account, there is no way to securely associate your data with you, which could lead to data loss or privacy issues.

### Creating an Account

Creating an account is quick and easy. Simply follow the prompts on the login screen to sign up. Once you have an account, you can log in and start using all the features that P-Shopper has to offer.

By ensuring that all users are logged in, P-Shopper can provide a secure, personalized, and fully functional shopping list management experience.


# Deprecated Features

In the development of P-Shopper, certain features were considered but ultimately deprecated. One notable example is the list sharing functionality. Here’s an explanation of this feature and the reasons why it was not implemented:

## List Sharing

### Initial Concept
- **Purpose**: The list sharing feature was intended to allow users to generate a unique URL for their shopping lists. This URL could be shared with others, enabling them to view the list without needing to log in to P-Shopper.
- **Functionality**: Users would be able to click a "Share" button to generate a URL. If sharing was active, users could also opt to unshare the list.

### Implementation Challenges
- **Security Concerns**: Ensuring that shared lists were accessible only to intended recipients while maintaining user data privacy proved complex. Implementing secure, temporary URLs that couldn't be exploited was challenging.
- **User Experience**: Providing a seamless experience where shared lists were easily accessible without compromising the overall app's functionality was difficult. Issues arose in maintaining the app's integrity and user flow when accessing shared lists.
- **Technical Limitations**: Handling URL hashes and ensuring correct list loading without user login required significant changes to the app's core structure. This introduced potential instability and complexity that outweighed the benefits.

### Decision to Deprecate
- **Focus on Core Features**: To maintain a high-quality user experience, the development focus shifted to enhancing the core features of P-Shopper, such as item management, sorting, filtering, and reporting.
- **Security and Privacy**: Prioritizing the security and privacy of user data was paramount. Given the challenges in securely implementing list sharing, it was decided to deprecate this feature to ensure user trust and data protection.
- **Resource Allocation**: The development resources were better allocated to features that directly improved the usability and functionality of the app, rather than maintaining a complex sharing system.

### Future Considerations
- **Possible Revisit**: While list sharing is not currently supported, it may be revisited in the future if a secure and user-friendly implementation can be devised.
- **Alternative Sharing Methods**: Users are encouraged to use the export functionality to share lists. Exporting lists as CSV files provides a simple and secure way to share shopping data without compromising privacy or security.

By focusing on the essential features and ensuring a secure and streamlined user experience, P-Shopper continues to provide effective and reliable shopping list management. The decision to deprecate list sharing reflects a commitment to quality and user satisfaction.
