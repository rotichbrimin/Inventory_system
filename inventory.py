import json

def load_data():
    try:
        with open("/storage/emulated/0/items.json", "r") as file:
            return json.load(file)
    except:
        return []
        
def save_data(items):
    with open("/storage/emulated/0/items.json", "w") as file:
        json.dump(items, file)

def add_item(items):
    while True:
        try:
            new_id = int(input("Enter item ID :"))
            
            exists=False
            for item in items:  
                if item ["id"] == new_id:
                    exists=True
                    break
            if exists:
                print(f"The ID {new_id} already exists! Try again.")
            else:
                break
        except ValueError:
            print("Enter a valid ID !")
                
    name=input(f"Enter name of the item of id {new_id}:")
    
    while True:
        try:
            quantity =int(input(f"Enter quantity(s) for {name} :"))
            if quantity>0:
                break
            else:
                print("Quantity must be more than 0 !")
        except ValueError:
            print("Enter a valid quantity !")
    while True:
        try:
            price=float(input(f"Enter price for each {name} :"))
            if price >0:
                break
            else:
                print("Price must be more than 0 !")
        except ValueError:
            print("Enter a valid price :")
    return{
        "id":new_id,
        "name": name,
        "price":price,
        "quantity":quantity
            }

def view_items(items):
    if not items:
        print("No item has been saved !")
        return
    print("\n===ITEMS AVAILABLE ===")
    for item in items:
        print(f"ID: {item['id']} | Name: {item['name']} | Stock: {item['quantity']} | Price: {item['price']:.2f}")

def delete_item(items):
    try:
        search_id = int(input("Enter item ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return

    for i, item in enumerate(items):
        if item["id"] == search_id:
            print(f"Item ID {item['id']} - {item['name']} deleted successfully!")
            del items[i]
            save_data(items)
            return

    print("Item not found!")

def update_items(items):
    if not items:
        print("No items available to update!")
        return

    try:
        search_id = int(input("Enter product ID to update: "))
    except ValueError:
        print("Invalid ID!")
        return

    for item in items:
        if item["id"] == search_id:
            print(f"Found: {item['name']}")

            print("1. Update Price")
            print("2. Update Quantity")

            choice = input("Choose option: ").strip()

            if choice == "1":
                while True:
                    try:
                        new_price = float(input("Enter new price: "))
                        if new_price > 0:
                            item["price"] = new_price
                            save_data(items)
                            print("Price updated successfully!")
                            return
                        else:
                            print("Price must be more than 0!")
                    except ValueError:
                        print("Enter a valid price!")

            elif choice == "2":
                while True:
                    try:
                        new_quantity = int(input("Enter new quantity: "))
                        if new_quantity >= 0:
                            item["quantity"] = new_quantity
                            save_data(items)
                            print("Quantity updated successfully!")
                            return
                        else:
                            print("Quantity cannot be negative!")
                    except ValueError:
                        print("Enter a valid quantity!")

            else:
                print("Invalid option!")
                return

    print("Item not found!")
    
def sell_item(items):
    if not items:
        print("No items available!")
        return

    while True:
        try:
            search_id = int(input("Enter product ID to sell: "))
        except ValueError:
            print("Invalid ID!")
            continue

        for item in items:
            if item["id"] == search_id:
                print(f"Product: {item['name']}")
                print(f"Available stock: {item['quantity']}")

                while True:
                    try:
                        qty = int(input("Enter quantity to sell: "))
                        if qty <= 0:
                            print("Quantity must be more than 0!")
                            continue
                        break
                    except ValueError:
                        print("Invalid quantity!")

                if qty > item["quantity"]:
                    print("Not enough stock! Try again !")
                    continue

                total = qty * item["price"]
                item["quantity"] -= qty
                save_data(items)

                print(f"Sold {qty} {item['name']}")
                print(f"Total price: {total:.2f}")
                print(f"Remaining stock: {item['quantity']}")
                return

        print("Item not found. Try again.")

def low_stock(items):
    if not items:
        print("No items available !")
        return
    found = False
    for item in items:
        if item["quantity"] <5:
            print(f"Name: {item['name']} | Stock: {item['quantity']} is running low")
            found =True
    if not found:
        print("All items have enough stock")
def search_item(items):
    if not items:
        print("No items available!")
        return
    while True:
        query = input("Enter item name or ID to search: ").strip().lower()

        found = False

        for item in items:
            if query == str(item["id"]) or query in item["name"].lower():
                print(f"ID: {item['id']} | Name: {item['name']} | Stock: {item['quantity']} | Price: {item['price']:.2f}")
                found = True
                break
        if not found:
            print("No matching item found. Try again !")
        again=input("Do you want to search another item? :").strip().lower()
        if again in ["no", "n"]:
            break
        
        
items = load_data()
while True:
    print("===SELLER'S MENU===")
    print("1. Add a new item")
    print("2. View available items.")
    print("3. Update available item :")
    print("4. Delete item.")
    print("5. Sell Item :")
    print("6. View low stock :")
    print("7. Search Item :")
    print("8. Exit:")
    
    while True:
        try:
            choice = int(input("Enter your option: "))
            break
        except ValueError:
            print("Enter a valid number!")
    if choice ==1:
        while True:
            items.append(add_item(items))
            save_data(items)
            again=input("Add another item? yes/no :").strip().lower()
            if again in ["no", "n"]:
                view_items(items)
                break
    elif choice==2:
            view_items(items)
    elif choice == 3:
        if not items:
            print("No items available to update!")
        else:
            while True:
                update_items(items)
                again = input("Do you want to update another item? yes/no :").strip().lower()
                if again in ["no", "n"]:
                    view_items(items)
                    break
    elif choice ==4:
        if items:
            while True:
                delete_item(items)
                again=input("Delete another item?yes/no :").strip().lower()
                if again in ["no", "n"]:
                    view_items(items)
                    break
        else:
            print("No item to delete!")
    elif choice == 5:
        sell_item(items)
        view_items(items)
    elif choice == 6:
        print("\n===LOW STOCK ITEMS ===")
        low_stock(items)
    elif choice ==7:
        search_item(items)
    elif choice == 8:
        print("Exiting program")
        break
    else:
        print("Invalid option")
        
            