from expense_processor import ExpenseProcessor

processor = ExpenseProcessor()
processor.train_model("labeled_expenses.csv")
