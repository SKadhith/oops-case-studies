import json
import os
import random
from tabulate import tabulate

DATA_FILE = r"D:\ADHI\data.json"

class FileManager:
    @staticmethod
    def ensure_directory():
        directory = os.path.dirname(DATA_FILE)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def ensure_file_exists():
        FileManager.ensure_directory()
        if not os.path.exists(DATA_FILE):
            default_data = {"users": {}, "products": {}, "cart": {}}
            with open(DATA_FILE, "w") as f:
                json.dump(default_data, f, indent=4)

    @staticmethod
    def load_data():
        FileManager.ensure_file_exists()
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

class User:
    def __init__(self, name="", email="", password=""):
        self.name = name
        self.email = email
        self.__password = password  

    def check_password(self, password):
        return self.__password == password

    def login(self):
        data = FileManager.load_data()
        if self.email in data["users"] and data["users"][self.email]["password"] == self.__password:
            print("Login Successful!✅")
            return True
        print("Invalid Credentials❌")
        return False

    def register(self):
        data = FileManager.load_data()
 
        while not self.name.strip():
            self.name = input("Enter Name: ").strip()
            if not self.name:
                print("⚠ Name is required!")
 
        while not self.email.strip():
            self.email = input("Enter Email: ").strip()
            if not self.email:
                print("⚠ Email is required!")
            elif self.email in data["users"]:
                print("⚠ Email already registered! Try another.")
                return  # Stop registration if the email already exists
        
        while True:
            password = input("Enter Password: ").strip()
            if not password:
                print("⚠ Password is required!")
                continue  

        self.__password = password
        data["users"][self.email] = {"name": self.name, "password": self.__password}
        FileManager.save_data(data)
        print("🎉 Registered Successfully!")

class Admin(User):
    ADMIN_EMAIL = "admin@gmail.com"
    ADMIN_PASSWORD = "admin"

    def __init__(self, email, password):
        super().__init__("Admin", email, password)

    def login(self):
        if self.email == Admin.ADMIN_EMAIL and self.check_password(Admin.ADMIN_PASSWORD):
            print("Admin Login Successful!✅")
            return True
        print("Invalid Admin Credentials❌")
        return False

class ProductManager:
    @staticmethod
    def generate_product_id():
        return "P" + str(random.randint(1000, 9999))

    @staticmethod
    def add_product():
        data = FileManager.load_data()
        name = input("Enter Product Name: ")
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        product_id = ProductManager.generate_product_id()
        data["products"][product_id] = {"name": name, "price": price, "quantity": quantity}
        FileManager.save_data(data)
        print("Product Added Successfully!✅")
        
    @staticmethod
    def edit_product():
        data = FileManager.load_data()
        pid = input("Enter Product ID to Edit: ")
        if pid in data["products"]:
            name = input("Enter New Name: ") or data["products"][pid]["name"]
            price = input("Enter New Price: ") or data["products"][pid]["price"]
            quantity = input("Enter New Quantity: ") or data["products"][pid]["quantity"]
            data["products"][pid] = {"name": name, "price": float(price), "quantity": int(quantity)}
            FileManager.save_data(data)
            print("Product Updated Successfully!✅")
        else:
            print("Product Not Found!❌")

    @staticmethod
    def delete_product():
        data = FileManager.load_data()
        pid = input("Enter Product ID to Delete: ")
        if pid in data["products"]:
            del data["products"][pid]
            FileManager.save_data(data)
            print("Product Deleted Successfully!🗑")
        else:
            print("Product Not Found!❌")

    @staticmethod
    def view_products():
        data = FileManager.load_data()
        if data["products"]:
            table = [[pid, details["name"], f"₹{details['price']}", details["quantity"]] for pid, details in data["products"].items()]
            print("\nAvailable Products:")
            print(tabulate(table, headers=["Product ID", "Name", "Price", "Stock"], tablefmt="fancy_grid"))
        else:
            print("No products available❌")

    @staticmethod
    def search_product():
        data = FileManager.load_data()
        search = input("➤Enter Product Name: ").lower()
        found_products = [[pid, details["name"], f"₹{details['price']}", details["quantity"]] for pid, details in data["products"].items() if search in details["name"].lower()]
        
        if found_products:
            print("\nSearch Results:")
            print(tabulate(found_products, headers=["Product ID", "Name", "Price", "Stock"], tablefmt="fancy_grid"))
        else:
            print("Product Not Found❌")

class CartManager:
    @staticmethod
    def add_to_cart(user_email):
        data = FileManager.load_data()
        pid = input("➤Enter Product ID: ")
        if pid in data["products"] and data["products"][pid]["quantity"] > 0:
            data["cart"].setdefault(user_email, []).append(pid)
            FileManager.save_data(data)
            print("Product Added to Cart!✅")
        else:
            print("Invalid Product or Out of Stock❌")

    @staticmethod
    def view_cart(user_email):
        data = FileManager.load_data()
        cart = data["cart"].get(user_email, [])
        if cart:
            cart_items = [[pid, data["products"][pid]["name"], f"₹{data['products'][pid]['price']}"] for pid in cart]
            print("\nCart:")
            print(tabulate(cart_items, headers=["Product ID", "Name", "Price"], tablefmt="fancy_grid"))
            total = sum(data["products"][pid]["price"] for pid in cart)
            print(f"Total: ₹{total}")
        else:
            print("Cart is Empty🗑")

    @staticmethod
    def checkout(user_email):
        data = FileManager.load_data()
        cart = data["cart"].get(user_email, [])
        if not cart:
            print("Cart is Empty🗑")
            return

        print("Choose Payment Option: 1. Credit Card 2. Paytm")
        payment = input("✅Enter Choice: ")
        if payment in ["1", "2"]:
            for pid in cart:
                data["products"][pid]["quantity"] -= 1
            data["cart"][user_email] = []
            FileManager.save_data(data)
            print("Purchase Successful!🛒")
        else:
            print("Invalid Payment Method✖️")

class AdminManager:
    @staticmethod
    def view_users():
        data = FileManager.load_data()
        if data["users"]:
            table = [[email, details["name"]] for email, details in data["users"].items()]
            print(tabulate(table, headers=["Email", "Name"], tablefmt="fancy_grid"))
        else:
            print("No users found✖️")

def main():
    while True:
        print("\nWelcome to E-Commerce!😄")
        print("1. Login ↪ 2. Register 👤 3. Admin Login 👨🏻‍💻 4. Exit 🏃🚪")
        choice = input("Enter choice: ")

        if choice == "1":
            email = input("👤Enter Email: ")
            password = input("🔑Enter Password: ")
            user = User("", email, password)
            if user.login():
                while True:
                    print("\nUser Panel: [1] View Products 📤[2] Search Product 🔎[3] Add to Cart ✅[4] View Cart 🛒[5] Checkout 📦[6] Logout⍈")
                    choice = input("✅️Enter choice: ")
                    if choice == "1":
                        ProductManager.view_products()
                    elif choice == "2":
                        ProductManager.search_product()
                    elif choice == "3":
                        CartManager.add_to_cart(email)
                    elif choice == "4":
                        CartManager.view_cart(email)
                    elif choice == "5":
                        CartManager.checkout(email)
                    elif choice == "6":
                        break
                    else:
                        print("Invalid choice!✖️")
        elif choice == "2":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            user = User(name, email, "")
            user.register()
        elif choice == "3":
            email = input("👤Enter Admin Email: ")
            password = input("🔑Enter Admin Password: ")
            admin = Admin(email, password)
            if admin.login():
                while True:
                    print("\nAdmin Panel: [1] Add Product ➕[2] Edit Product ✏️[3] Delete Product ❌[4] View Products 📤[5] View Users 👥[6] Logout⍈")
                    choice = input("✅️Enter choice: ")
                    if choice == "1":
                        ProductManager.add_product()
                    elif choice == "2":
                        ProductManager.edit_product()
                    elif choice == "3":
                        ProductManager.delete_product()
                    elif choice == "4":
                        ProductManager.view_products()
                    elif choice == "5":
                        AdminManager.view_users()
                    elif choice == "6":
                        break
        elif choice == "4":
            break

if __name__ == "__main__":
    main()
