import pandas as pd
import numpy as np

class ExpenseProcessor:
    def __init__(self):
        self.categories = {
            'food': ['restaurant', 'cafe', 'grocery', 'food', 'meal', 'dining'],
            'transportation': ['uber', 'lyft', 'taxi', 'gas', 'fuel', 'transit', 'parking'],
            'shopping': ['amazon', 'walmart', 'target', 'store', 'market'],
            'bills': ['electricity', 'water', 'internet', 'phone', 'insurance', 'rent'],
            'entertainment': ['movie', 'netflix', 'spotify', 'theatre', 'game'],
            'others': []
        }

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import spacy
import pickle

class ExpenseProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        self.trained = False

    def train_model(self, csv_file):
        """Train NLP model on labeled expense descriptions"""
        df = pd.read_csv(csv_file)
        if 'description' not in df.columns or 'category' not in df.columns:
            raise ValueError("CSV must contain 'description' and 'category' columns")

        X = df['description']
        y = df['category']

        X_vectors = self.vectorizer.fit_transform(X)
        self.model.fit(X_vectors, y)
        self.trained = True

        # Save trained model
        with open("expense_model.pkl", "wb") as f:
            pickle.dump((self.vectorizer, self.model), f)

    def load_model(self):
        """Load trained model"""
        try:
            with open("expense_model.pkl", "rb") as f:
                self.vectorizer, self.model = pickle.load(f)
                self.trained = True
        except FileNotFoundError:
            raise FileNotFoundError("Model not trained. Run train_model() first.")

    def categorize_transaction(self, description):
        """Categorize a transaction using NLP"""
        if not self.trained:
            self.load_model()

        description_vector = self.vectorizer.transform([description])
        category = self.model.predict(description_vector)[0]
        return category


    def process_file(self, filepath):
        """Process the uploaded CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(filepath)
            
            # Basic validation
            required_columns = ['date', 'description', 'amount']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")
            
            # Process the data
            df['category'] = df['description'].apply(self.categorize_transaction)
            df['date'] = pd.to_datetime(df['date'])
            
            # Generate insights
            insights = {
                'total_expenses': float(df['amount'].sum()),
                'category_breakdown': df.groupby('category')['amount'].sum().to_dict(),
                'monthly_spending': df.groupby(df['date'].dt.strftime('%Y-%m'))['amount'].sum().to_dict(),
                'top_expenses': df.nlargest(5, 'amount')[['date', 'description', 'amount', 'category']].to_dict('records'),
                'category_counts': df['category'].value_counts().to_dict()
            }
            
            return {
                'success': True,
                'insights': insights
            }
            
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")