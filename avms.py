
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import mysql.connector
def connect_to_db():
    try:
        return mysql.connector.connect(
                host="localhost",
                username="root",
                password="",
                database="agrovet"
            )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None

# Function to open the cashier window (from the second code snippet)
def open_cashier_window():
    cashier_window = tk.Toplevel(root)
    cashier_window.title("Cashier Operations")
    cashier_window.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    cashier_window.configure(background='green')
    # Hide the main window
    root.withdraw()

    # Make the main window reappear when the login window is closed
    cashier_window.protocol("WM_DELETE_WINDOW", lambda: [root.deiconify(), cashier_window.destroy()])

    # Function to record a sale and update inventory
    def record_sale():
        # Record the sale
        db = connect_to_db()
        if db is not None:
            try:
                cursor = db.cursor()
                # Check if enough quantity is available
                cursor.execute("SELECT Quantity FROM Inventory WHERE ProductID = %s", (product_id_entry.get(),))
                inventory_quantity = cursor.fetchone()[0]
                if inventory_quantity >= int(quantity_entry.get()):
                    # Proceed with the sale
                    cursor.execute(
                        "INSERT INTO Sales (SalesID, ProductID, ProductName, Quantity_Sold, Price, Date_sold) VALUES (%s, %s, %s, %s, %s, %s)",
                        (sales_id_entry.get(), product_id_entry.get(), product_name_entry.get(), quantity_entry.get(), cost_entry.get(),
                         datetime.get()))
                    cursor.execute("UPDATE Inventory SET Quantity = Quantity - %s WHERE ProductID = %s",
                                   (quantity_entry.get(), product_id_entry.get()))
                    db.commit()
                    messagebox.showinfo("Success", "Sales updated successfully And Inventory updated")
                else:
                    # Not enough quantity, do not proceed with the sale
                    messagebox.showwarning("Warning", "Not enough inventory to complete the sale.")

            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                db.close()

    def check_availability():
        item_name = entry.get().strip()
        if not item_name:
            messagebox.showinfo("Input Error", "Please enter an item name.")
            return

        db = connect_to_db()
        if db is not None:
            try:
                cursor = db.cursor()  # Create a cursor
                query = "SELECT ProductID, product_name, quantity FROM Inventory WHERE product_name = %s"
                cursor.execute(query, (item_name,))
                result = cursor.fetchone()
            except mysql.connector.Error as err:
                messagebox.showerror("Query Error", f"Error: {err}")
            else:
                if result:
                    text_area.delete('1.0', tk.END)
                    text_area.insert(tk.INSERT,
                                     f"Product Id: {result[0]}, Item Name: {result[1]}, Quantity in Stock: {result[2]}")
                else:
                    text_area.delete('1.0', tk.END)
                    text_area.insert(tk.INSERT, "Item not found in the database.")
            finally:
                db.close()

    # Rest of your code...

    def clear_text_area():
        text_area.delete('1.0', tk.END)

    frame_forms = tk.Frame(cashier_window)
    frame_forms.pack(side="top", fill="both", expand=True)
    frame_forms.configure(background='pink')

    entry_label_frame = tk.LabelFrame(frame_forms, text="Search for Product", font="40", bg="green", fg="black",
                                      borderwidth=0, highlightthickness=0)
    entry_label_frame.pack(side="left", fill="x", expand=True, padx=cashier_window.winfo_screenwidth() // 8)
    entry_label = tk.Label(entry_label_frame, text="Enter item name:")
    entry_label.pack(pady=10)
    entry = tk.Entry(entry_label_frame)
    entry.pack(pady=10)
    # Create the check button
    check_button = tk.Button(entry_label_frame, text="Check Availability", command=check_availability)
    check_button.pack(pady=10)
    # Create the clear button
    clear_button = tk.Button(entry_label_frame, text="Clear Results", command=clear_text_area)
    clear_button.pack(pady=10)
    # Create the textarea for displaying results
    text_area = scrolledtext.ScrolledText(entry_label_frame, wrap=tk.WORD, width=30, height=20)
    text_area.pack(pady=10)

    # Sales Section
    sales_frame = tk.LabelFrame(frame_forms, text="Record Sales", font="Helvetica, 20", bg="blue", fg="black",
                                borderwidth=0, highlightthickness=0)
    sales_frame.pack(side="right", fill="x", expand=True, padx=cashier_window.winfo_screenwidth() // 8)

    entry_label = tk.Label(sales_frame, text="Sales ID:")
    entry_label.pack(pady=10)
    sales_id_entry = tk.Entry(sales_frame)
    sales_id_entry.pack(pady=10)
    entry_label=tk.Label(sales_frame, text="Product ID:")
    entry_label.pack(pady=10)
    product_id_entry = tk.Entry(sales_frame)
    product_id_entry.pack(pady=10)
    entry_label = tk.Label(sales_frame, text="Product name:")
    entry_label.pack(pady=10)
    product_name_entry = tk.Entry(sales_frame)
    product_name_entry.pack(pady=10)
    entry_label = tk.Label(sales_frame, text="Quantity sold:")
    entry_label.pack(pady=10)
    quantity_entry = tk.Entry(sales_frame)
    quantity_entry.pack(pady=10)
    entry_label = tk.Label(sales_frame, text="Total cost:")
    entry_label.pack(pady=10)
    cost_entry = tk.Entry(sales_frame)
    cost_entry.pack(pady=10)
    entry_label = tk.Label(sales_frame, text="Date sold:")
    entry_label.pack(pady=10)
    datetime = tk.Entry(sales_frame)
    datetime.pack(pady=10)
    submit_btn = tk.Button(sales_frame, text="Record Sale", command=record_sale)
    submit_btn.pack(padx=4, pady=4)

# Function to open the manager window (from the second code snippet)
# def open_manager_window():
def open_manager_window():
    manager_window = tk.Toplevel(root)
    manager_window.title("Manager")
    manager_window.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    manager_window.configure(background='light blue')
    # Create a menu bar
    menubar = tk.Menu(manager_window)
    manager_window.config(menu=menubar)

    # Create a menu item
    filemenu = tk.Menu(menubar)

    # Add commands to the menu item
    filemenu.add_command(label="Update")
    filemenu.add_command(label="Delete")

    # Add the menu item to the menu bar
    menubar.add_cascade(label="Options", menu=filemenu)

    # Hide the main window
    root.withdraw()

    # Make the main window reappear when the login window is closed
    manager_window.protocol("WM_DELETE_WINDOW", lambda: [root.deiconify(), manager_window.destroy()])

    def insert_inventory():
        db = connect_to_db()
        if db is not None:
            try:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO Inventory (productid, product_name, description, quantity, unit_price) VALUES (%s, %s, %s, %s, %s)",
                    (entry_productid.get(), entry_product_name.get(), entry_description.get(), entry_quantity.get(),entry_unit_price.get()))
                db.commit()
                messagebox.showinfo("Success", "Inventory updated successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                db.close()

    def update_inventory():
        product_id = product_id_entry.get()
        new_quantity = quantity_entry.get()

        # Validate inputs
        if not product_id or not new_quantity.isdigit():
            messagebox.showerror("Error", "Please enter a valid product ID and numeric quantity.")
            return

        db = connect_to_db()
        if db is not None:
            with db:
                cursor = db.cursor()
                try:
                    cursor.execute("UPDATE Inventory SET Quantity = %s WHERE ProductID = %s",
                                   (new_quantity, product_id))
                    db.commit()
                    messagebox.showinfo("Success", "Inventory updated successfully")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    # Function to insert data into the supplier table
    def insert_supplier():
        db = connect_to_db()
        if db is not None:
            try:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO Supplier (supplierid, supplier_name, productid, quantity, date_of_supply, cost) VALUES (%s, %s, %s, %s, %s, %s)",
                    (entry_supplierid.get(), entry_suppliername.get(), entry_productid_supplier.get(),
                     entry_quantity_supplier.get(), entry_dateofsupply.get(), entry_total_cost.get()))
                db.commit()
                messagebox.showinfo("Success", "Supplier added successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                db.close()

    # Frame for inventory and supplier fields
    frame_forms = tk.Frame(manager_window)
    frame_forms.pack(side="top", fill="both", expand=True)
    frame_forms.configure(background='light green')
    # Inventory fields
    inventory_label_frame = tk.LabelFrame(frame_forms, text="Insert New product to Inventory", font="40", bg="green", fg="black",
                                          borderwidth=0, highlightthickness=0)
    inventory_label_frame.pack(side="left", fill="x", expand=True, padx=root.winfo_screenwidth() // 8)
    tk.Label(inventory_label_frame, text="Product ID:").grid(row=0, column=0, pady=14, padx=14)
    entry_productid = tk.Entry(inventory_label_frame)
    entry_productid.grid(row=0, column=1, pady=14, padx=14)
    tk.Label(inventory_label_frame, text="Product Name:").grid(row=1, column=0, pady=14, padx=14)
    entry_product_name = tk.Entry(inventory_label_frame)
    entry_product_name.grid(row=1, column=1, pady=14, padx=14)
    tk.Label(inventory_label_frame, text="Description:").grid(row=2, column=0, pady=14, padx=14)
    entry_description = tk.Entry(inventory_label_frame)
    entry_description.grid(row=2, column=1, pady=14, padx=14)
    tk.Label(inventory_label_frame, text="Quantity:").grid(row=3, column=0, pady=14, padx=14)
    entry_quantity = tk.Entry(inventory_label_frame)
    entry_quantity.grid(row=3, column=1, pady=14, padx=14)
    tk.Label(inventory_label_frame, text="Unit Price:").grid(row=4, column=0, pady=14, padx=14)
    entry_unit_price = tk.Entry(inventory_label_frame)
    entry_unit_price.grid(row=4, column=1, pady=14, padx=14)
    tk.Button(inventory_label_frame, text="Add to Inventory", command=insert_inventory).grid(row=5, columnspan=2,
                                                                                            pady=14, padx=14)
    #Update Inventory
    inventory_frame = tk.LabelFrame(frame_forms, text="Update Product In Stock", font="40", bg="pink", fg="black",
                                          borderwidth=0, highlightthickness=0)
    inventory_frame.pack(side="bottom", fill="x", expand=True, padx=root.winfo_screenwidth() // 8)
    entry_label = tk.Label(inventory_frame, text="Product ID:")
    entry_label.pack(pady=10)
    product_id_entry = tk.Entry(inventory_frame)
    product_id_entry.pack(pady=10)

    entry_label = tk.Label(inventory_frame, text="New Quantity:")
    entry_label.pack(pady=10)
    quantity_entry = tk.Entry(inventory_frame)
    quantity_entry.pack(pady=10)

    update_btn = tk.Button(inventory_frame, text="Update Inventory", command=update_inventory)
    update_btn.pack(padx=10, pady=10)

    # Supplier fields
    supplier_label_frame = tk.LabelFrame(frame_forms, text="Keep record of Supplier", font="40", bg="blue", fg="black", borderwidth=0,
                                         highlightthickness=0)
    supplier_label_frame.pack(side="right", fill="y", expand=True, padx=root.winfo_screenwidth() // 8)
    tk.Label(supplier_label_frame, text="Supplier ID:").grid(row=0, column=0, pady=14, padx=14)
    entry_supplierid = tk.Entry(supplier_label_frame)
    entry_supplierid.grid(row=0, column=1, pady=14, padx=14)
    tk.Label(supplier_label_frame, text="Supplier Name:").grid(row=1, column=0, pady=14, padx=14)
    entry_suppliername = tk.Entry(supplier_label_frame)
    entry_suppliername.grid(row=1, column=1, pady=14, padx=14)
    tk.Label(supplier_label_frame, text="Product ID:").grid(row=2, column=0, pady=14, padx=14)
    entry_productid_supplier = tk.Entry(supplier_label_frame)
    entry_productid_supplier.grid(row=2, column=1, pady=14, padx=14)
    tk.Label(supplier_label_frame, text="Quantity:").grid(row=3, column=0, pady=14, padx=14)
    entry_quantity_supplier = tk.Entry(supplier_label_frame)
    entry_quantity_supplier.grid(row=3, column=1, pady=14, padx=14)
    tk.Label(supplier_label_frame, text="Date of Supply:").grid(row=4, column=0, pady=14, padx=14)
    entry_dateofsupply = tk.Entry(supplier_label_frame)
    entry_dateofsupply.grid(row=4, column=1, pady=14, padx=14)
    tk.Label(supplier_label_frame, text="Total cost:").grid(row=5, column=0, pady=14, padx=14)
    entry_total_cost = tk.Entry(supplier_label_frame)
    entry_total_cost.grid(row=5, column=1, pady=14, padx=14)
    tk.Button(supplier_label_frame, text="Add Supplier", command=insert_supplier).grid(row=6, columnspan=2, pady=14,
                                                                                       padx=14)


# Function to open the login window (from the first code snippet)
def open_login_window(user_type):
    login_window = tk.Toplevel(root)
    login_window.title(f"{user_type} Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=lambda: login(user_type, username_entry.get(), password_entry.get())).pack()

    # Function to handle the login logic
    def login(user_type, user_name, Password):
        db = connect_to_db()
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE user_name = %s AND Password = %s"
        cursor.execute(query, (user_name, Password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", f"{user_type} logged in successfully!")
            # Call the appropriate window function upon successful login
            if user_type == "Cashier":
                open_cashier_window()
            elif user_type == "Manager":
                open_manager_window()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

        db.close()


# Main window setup (from the first code snippet)
root = tk.Tk()
# ... (rest of the main window setup)
root.title("Dashboard")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# To set an image as the background, uncomment the following lines and replace 'path_to_your_image.png' with your image file path
bg_image = tk.PhotoImage(file="/home/lasty/PycharmProjects/AVMS/images/background_image.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
welcome_label = tk.Label(root, text="Agrovet Management System", bg="white", fg="black", font=("Helvetica", 46))
welcome_label.pack(pady=40)

# Load the logo and add it to a Label
logo_image = tk.PhotoImage(file="/home/lasty/PycharmProjects/AVMS/images/logo.png")
logo_label = tk.Label(root, image=logo_image)
logo_label.pack()

frame = tk.Frame(root)
frame.pack(pady=15)

cashier_button = tk.Button(frame, text="Cashier", command=lambda: open_login_window("Cashier"))
cashier_button.pack(side="left", padx=10)

manager_button = tk.Button(frame, text="Manager", command=lambda: open_login_window("Manager"))
manager_button.pack(side="left", padx=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=20)

# Ensure you have a button for the cashier login that calls open_login_window("Cashier")
"""cashier_button = tk.Button(frame, text="Cashier", command=lambda: open_login_window("Cashier"))
cashier_button.pack(side="left", padx=10)"""

# ... (rest of the main window setup)
root.mainloop()
