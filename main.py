from datetime import date
import db
import matplotlib.pyplot as plt

def show_expenses():
    expenses = db.get_all_expenses()
    if not expenses:
        print("\nNo expenses yet.")
        return
    print(f"\n{'ID':<5}{'Amount':<10}{'Category':<15}{'Date':<12}Note")
    print("-" * 55)
    for id_, amount, category, note, day in expenses:
        print(f"{id_:<5}{amount:<10.2f}{category:<15}{day:<12}{note}")

def add():
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    category = input("Category (e.g. Food, Travel): ").strip().title()
    note = input("Note (optional): ").strip()
    db.add_expense(amount, category, note, str(date.today()))
    print("Expense added.")

def edit():
    show_expenses()
    try:
        expense_id = int(input("\nID to edit: "))
        amount = float(input("New amount: "))
    except ValueError:
        print("Please enter valid numbers.")
        return
    category = input("New category: ").strip().title()
    note = input("New note: ").strip()
    db.update_expense(expense_id, amount, category, note)
    print("Expense updated.")

def delete():
    show_expenses()
    try:
        expense_id = int(input("\nID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    db.delete_expense(expense_id)
    print("Expense deleted.")

def summary():
    default = str(date.today())[:7]
    month = input(f"Month (YYYY-MM) [{default}]: ").strip() or default
    rows = db.get_monthly_summary(month)
    if not rows:
        print(f"No expenses found for {month}.")
        return

    total = sum(amount for _, amount in rows)
    print(f"\nSpending for {month}")
    print("-" * 32)
    for category, amount in rows:
        print(f"{category:<15}{amount:>10.2f}  ({amount / total * 100:.0f}%)")
    print("-" * 32)
    print(f"{'Total':<15}{total:>10.2f}")

    if input("\nShow chart? (y/n): ").strip().lower() == "y":
        categories = [c for c, _ in rows]
        amounts = [a for _, a in rows]
        plt.figure(figsize=(7, 5))
        plt.bar(categories, amounts)
        plt.title(f"Spending by Category - {month}")
        plt.ylabel("Amount (₹)")
        plt.show()


def main():
    db.create_table()
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Edit expense")
        print("4. Delete expense")
        print("5. Monthly summary")
        print("6. Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            edit()
        elif choice == "4":
            delete()
        elif choice == "5":
            summary()
        elif choice == "6":
            print("Bye!")
            break
        else:
            print("Invalid choice.")
            
if __name__ == "__main__":
    main()