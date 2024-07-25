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

This setup ensures that you can quickly start using P-Shopper with a predefined structure, making it easier to understand and manage your shopping lists and items.





# Categories
## User-Oriented Write-Up

### Managing Categories in P-Shopper

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

3. **Automatic Category Selection**:
    - After adding or removing a category, the dropdown will automatically reset to a default category to ensure smooth operation.

## Developer-Oriented Write-Up

### Managing Categories in P-Shopper

In P-Shopper, categories are managed through a combination of user interactions and database operations. Here’s an in-depth look at how it works:

1. **Adding a New Category**:
    - When a user selects "New Category" from the category dropdown, a prompt is displayed asking for the new category name.
    - The category name is capitalized correctly before being added to the `tblCategories` table.
    - The `category_id` for the new entry is incremented based on the highest existing `category_id`.

2. **Removing a Category**:
    - Upon selecting "Remove Category," users are prompted to enter the category name they wish to delete.
    - The system checks if the category exists in the `tblCategories` table.
    - It then verifies whether the category is in use by querying the `tblItems` and `tblLongTermHistory` tables.
    - If the category is not in use, it is deleted from the `tblCategories` table, and the user receives a confirmation.
    - If the category is in use, the user is informed that it cannot be deleted.

3. **Automatic Category Selection**:
    - After adding or removing a category, the category dropdown is reset to ensure it does not stay on the "New Category" or "Remove Category" options.
    - This is handled by resetting the dropdown to a default category, either the first category or the most recently used one.

These functionalities ensure that categories are managed efficiently and that the user experience remains smooth and intuitive.
