import sqlite3
from datetime import datetime
from prettytable import PrettyTable

def main():
    print("🎯 Running Expense Tracker!")

    database = "expense_tracker.db"

    # Initialize the database
    initialize_db(database)

    while True:
        print("1. Add an expense")
        print("2. Summarize expenses")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        match choice:
            case 1: add_user_expense(database)
            case 2: summarize_expenses(database)
            case 3: 
                print("Thank you for using the Expense Tracker Application! 🙏")
                break
            case _: print("Enter a valid choice!!! 🚫")

def initialize_db(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        amount INT NOT NULL,
        category TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

def add_user_expense(database):
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = int(input("Enter expense amount: ₹"))
    
    expense_categories = [
        "🍔 Food",
        "💡 Utilities",
        "🚌 Transportation",
        "🩺 Healthcare",
        "🎉 Entertainment",
        "📚 Education",
        "🛀 Personal Care",
        "🛍️ Shopping",
        "✈️ Travel",
        "🤝 Charity & Donations",
        "✨ Miscellaneous"
    ]

    print("Categories List: ")
    for i, category_name in enumerate(expense_categories):
        if i == 0:
            print(f"{i+1}. {category_name}")
            print("- Groceries - Restaurants - Coffee Shops - Fast Food")
        if i == 1:
            print(f"{i+1}. {category_name}")
            print("- Electricity - Water - Gas - Recharge")
        if i == 2:
            print(f"{i+1}. {category_name}")
            print("- Public Transport - Fuel - Parking")
        if i == 3:
            print(f"{i+1}. {category_name}")
            print("- Doctor Visits - Medications - Dental Care")
        if i == 4:
            print(f"{i+1}. {category_name}")
            print("- Movies - Concerts - Subscriptions (Netflix, Spotify) - Sports Events")
        if i == 5:
            print(f"{i+1}. {category_name}")
            print("- Tuition Fees - Books - Online Courses - School Supplies")
        if i == 6:
            print(f"{i+1}. {category_name}")
            print("- Haircuts - Beauty Products - Gym Memberships - Spa")
        if i == 7:
            print(f"{i+1}. {category_name}")
            print("- Clothing - Electronics - Gifts - Home Decor")
        if i == 8:
            print(f"{i+1}. {category_name}")
            print("- Hotels - Car Rentals - Vacation Packages")
        if i == 9:
            print(f"{i+1}. {category_name}")
            print("- Donations to Charities - Fundraising Events")
        if i == 10:
            print(f"{i+1}. {category_name}")
            print("- Any other expenses not covered by the above categories")
            print()
        
    expense_category = input("Choose expense category from the above list: ")
    expense_payment_method = input("Enter expense payment method (e.g., Cash, Credit Card): ")
    expense_description = input("Enter expense description: ")

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(
    '''
    INSERT INTO Expense (name, amount, category, payment_method, description, timestamp) 
    VALUES (?, ?, ?, ?, ?, ?)
    ''',
    (expense_name, expense_amount, expense_category, expense_payment_method, expense_description, now)
    )

    conn.commit()
    conn.close()
    print("✅ Expense Added Successfully!\n")

def summarize_expenses(database):
    month = int(input("Enter month number (1-12): "))

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Expense WHERE strftime('%m', timestamp) = ?", (f'{month:02}',))
    rows = cursor.fetchall()

    while True:
        print("1. Get all expenses")
        print("2. Print amount spent category-wise")
        print("3. Print amount spent by payment method")
        print("4. Total amount spent")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            table = PrettyTable()
            table.field_names = ["ID", "Name", "Amount(₹)", "Category", "Payment Method", "Description", "Timestamp"]
            for row in rows:
                table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
            print("All Expenses:")
            print(table)

        elif choice == 2:
            amount_by_category = {}
            for row in rows:
                key = row[3]
                if key in amount_by_category:
                    amount_by_category[key] += row[2]
                else:
                    amount_by_category[key] = row[2]
            
            print("Expenses By Category 📈:")
            for key, amount in amount_by_category.items():
                print(f"  {key}: ₹{amount}")
            
        elif choice == 3:
            amount_by_payment_method = {}
            for row in rows:
                key = row[4]
                if key in amount_by_payment_method:
                    amount_by_payment_method[key] += row[2]
                else:
                    amount_by_payment_method[key] = row[2]
            
            print("Expenses By Payment Method 💳:")
            for key, amount in amount_by_payment_method.items():
                print(f"  {key}: ₹{amount}")

        elif choice == 4:
            total_spent = sum([int(row[2]) for row in rows])
            print(f"💵 Total Spent: ₹{total_spent}")

        elif choice == 5:
            break

        else:
            print("Enter a valid choice!!! 🚫")
    
    conn.close()

if __name__ == "__main__":
    main()
