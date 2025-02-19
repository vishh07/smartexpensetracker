# expense_tracker.py

import pandas as pd
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        """Initialize the expense tracker with basic categories"""
        self.expenses = []
        self.categories = [
            "Food",
            "Transportation",
            "Shopping",
            "Bills",
            "Entertainment",
            "Others"
        ]
    
    def add_expense(self, date, description, amount, category):
        """Add a new expense"""
        if category not in self.categories:
            raise ValueError(f"Category must be one of {self.categories}")
            
        expense = {
            'date': date,
            'description': description,
            'amount': float(amount),
            'category': category
        }
        self.expenses.append(expense)
        return "Expense added successfully!"
    
    def view_expenses(self):
        """View all expenses"""
        return pd.DataFrame(self.expenses)
    
    def get_total_expenses(self):
        """Calculate total expenses"""
        if not self.expenses:
            return 0
        return sum(expense['amount'] for expense in self.expenses)
    
    def get_expenses_by_category(self):
        """Get total expenses by category"""
        df = pd.DataFrame(self.expenses)
        if df.empty:
            return pd.Series(0, index=self.categories)
        return df.groupby('category')['amount'].sum()

# Example usage file (main.py)
def main():
    # Create an instance of ExpenseTracker
    tracker = ExpenseTracker()
    
    while True:
        print("\n=== Expense Tracker Menu ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Expenses")
        print("4. View Expenses by Category")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            # Get expense details from user
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            print("\nAvailable categories:")
            for i, category in enumerate(tracker.categories, 1):
                print(f"{i}. {category}")
            cat_choice = int(input("Choose category number: "))
            category = tracker.categories[cat_choice-1]
            
            # Add expense
            try:
                tracker.add_expense(date, description, amount, category)
                print("Expense added successfully!")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            expenses_df = tracker.view_expenses()
            if expenses_df.empty:
                print("No expenses recorded yet!")
            else:
                print("\nAll Expenses:")
                print(expenses_df)
                
        elif choice == "3":
            total = tracker.get_total_expenses()
            print(f"\nTotal Expenses: ${total:.2f}")
            
        elif choice == "4":
            expenses_by_cat = tracker.get_expenses_by_category()
            print("\nExpenses by Category:")
            for category, amount in expenses_by_cat.items():
                print(f"{category}: ${amount:.2f}")
                
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()