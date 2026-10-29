import csv
from datetime import date, datetime
from collections import defaultdict
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"


# Read expenses from CSV
def load_expenses():
    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# Add a new expense
def add_expense():
    expense_date = input("Enter date (YYYY-MM-DD): ")
    datetime.strptime(expense_date, "%Y-%m-%d")

    category = input("Enter category: ").strip().title()
    amount = float(input("Enter amount: "))
    note = input("Enter note: ").strip()

    if not category or amount <= 0:
        print("Enter a valid category and positive amount.")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([expense_date, category, amount, note])

    print("Expense added successfully!")


# Display all expenses
def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    for item in expenses:
        print(
            item["Date"], "|",
            item["Category"], "| Rs.",
            item["Amount"], "|",
            item["Note"]
        )


# Calculate total spending
def total_expenses():
    expenses = load_expenses()
    total = sum(float(item["Amount"]) for item in expenses)
    print(f"Total expenses: Rs. {total:.2f}")


# Calculate spending by category
def category_summary():
    expenses = load_expenses()
    totals = defaultdict(float)

    for item in expenses:
        totals[item["Category"]] += float(item["Amount"])

    print("\nCategory-wise expenses:")
    for category, amount in sorted(totals.items()):
        print(f"{category}: Rs. {amount:.2f}")


# Calculate spending for a selected month
def monthly_summary():
    month = input("Enter month (YYYY-MM): ")

    datetime.strptime(month, "%Y-%m")
    expenses = load_expenses()

    total = sum(
        float(item["Amount"])
        for item in expenses
        if item["Date"].startswith(month)
    )

    print(f"Expenses for {month}: Rs. {total:.2f}")


# Draw category-wise expense chart
def show_chart():
    expenses = load_expenses()
    totals = defaultdict(float)

    for item in expenses:
        totals[item["Category"]] += float(item["Amount"])

    if not totals:
        print("No data available for chart.")
        return

    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (Rs.)")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()


# Main menu
while True:
    print("\n--- PERSONAL EXPENSE TRACKER ---")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Total expenses")
    print("4. Category-wise summary")
    print("5. Monthly summary")
    print("6. Show chart")
    print("7. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expenses()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            show_chart()
        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Enter 1 to 7.")

    except ValueError:
        print("Invalid input. Check the date or amount.")
    except FileNotFoundError:
        print("expenses.csv file not found.")