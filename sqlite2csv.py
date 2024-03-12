from model import DataSaver as ds
import csv


def main():
    base = ds('confirmat.db')
    data = base.get_all()


    with open('products_import.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Product ID', 'Active (0/1)', 'Name *', 'Categories (x,y,z...)', 'Price tax excluded', 'Tax rules ID', 'Wholesale price', 'On sale (0/1)', 'Discount amount', 'Discount percent', 'Discount from (yyyy-mm-dd)', 'Discount to (yyyy-mm-dd)', 'Reference #', 'Supplier reference #', 'Supplier', 'Manufacturer', 'EAN13', 'UPC', 'Ecotax', 'Width', 'Height', 'Depth', 'Weight', 'Delivery time of in-stock products', 'Delivery time of out-of-stock products with allowed orders', 'Quantity', 'Minimal quantity', 'Low stock level', 'Receive a low stock alert by email', 'Visibility', 'Additional shipping cost', 'Unity', 'Unit price', 'Summary', 'Description', 'Tags (x,y,z...)', 'Meta title', 'Meta keywords', 'Meta description', 'URL rewritten', 'Text when in stock', 'Text when backorder allowed', 'Available for order (0 = No, 1 = Yes)', 'Product available date', 'Product creation date', 'Show price (0 = No, 1 = Yes)', 'Image URLs (x,y,z...)', 'Image alt texts (x,y,z...)', 'Delete existing images (0 = No, 1 = Yes)', 'Feature(Name:Value:Position)', 'Available online only (0 = No, 1 = Yes)', 'Condition', 'Customizable (0 = No, 1 = Yes)', 'Uploadable files (0 = No, 1 = Yes)', 'Text fields (0 = No, 1 = Yes)', 'Out of stock action', 'Virtual product', 'File URL', 'Number of allowed downloads', 'Expiration date', 'Number of days', 'ID / Name of shop', 'Advanced stock management', 'Depends On Stock', 'Warehouse', 'Acessories  (x,y,z...)']
        writer = csv.DictWriter(f, delimiter=';',fieldnames=fieldnames)
        writer.writeheader()
        for d in data:
            row = {}
            row['Name *'] = d['name']
            row['Categories (x,y,z...)'] = d['name']
            row['Price tax excluded'] = d['name']
            row['Manufacturer'] = d['manufacturer']
            row['Name *'] = d['name']
            row['Name *'] = d['name']
            writer.writerows(row)

if __name__ == '__main__':
    main()