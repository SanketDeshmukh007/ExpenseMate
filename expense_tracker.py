from expense import Expense
import calendar
import datetime

def main():
    print(f"🎯 Running Expense Tracker!")

    expense_file_path = "expenses.csv"
    budget = 5000

    while(True):
        print("1. Add an expense")
        print("2. Summarize expenses")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if(choice == 1):
            # Get user input for expense
            expense = get_user_expense()

            # Write their expense to a file
            save_expense_to_file(expense, expense_file_path)

        elif(choice == 2):
            # Read file and summarize expenses
            summarize_expenses(expense_file_path, budget)
        elif(choice == 3): 
            print("Thank You! For Using Expense Tracker Application!!")
            break
        else:
            print("Enter valid choice!!!")

def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = int(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🏠 Hostel",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")
        
        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            expense_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category= expense_category, amount= expense_amount)
            return new_expense
        else:
            print("Invalid category. Please try again!")
        

def save_expense_to_file(expense, expense_file_path):
    print(f"🎯 Saving User Expense {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding='utf-8') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expenses")
    expenses = []
    with open(expense_file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            expense_name, expense_amount, expense_category = stripped_line.split(",")
            line_expense = Expense(name=expense_name,category=expense_category,amount=int(expense_amount))
            expenses.append(line_expense)
    
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    
    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ₹{amount}")
    
    total_spent = sum([int(ex.amount) for ex in expenses])
    print(f"💵 Total Spent: ₹{total_spent}")

    remaining_budget = budget - total_spent
    if remaining_budget < 0:
        print(red(f"⚠️  Budget Exceeded by ₹{-remaining_budget}!"))
    else:
        print(f"✅ Budget Remaining: ₹{remaining_budget}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: ₹{daily_budget}"))

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

if __name__ == "__main__":
    main()