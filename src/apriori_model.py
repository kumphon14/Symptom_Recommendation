import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


# 1. Load Transaction Data

def load_transaction_data(filepath="../data/processed/transaction_data.csv"):
    # print(f"📥 Loading transaction data from {filepath}")
    df = pd.read_csv(filepath)
    df = df.astype(bool)  # Convert to Boolean
    # print(f"✅ Shape: {df.shape[0]} patients x {df.shape[1]} symptoms")
    return df


# 2. Run Apriori Algorithm

def train_apriori(transaction_df, min_support=0.01):
    print(f"⚡ Running Apriori with min_support={min_support}")
    frequent_itemsets = apriori(transaction_df, 
                                min_support=min_support, 
                                use_colnames=True)
    print(f"🔎 Found {len(frequent_itemsets)} frequent itemsets")
    return frequent_itemsets


# 3. Generate Association Rules

def generate_rules(frequent_itemsets, metric="lift", min_threshold=0.7):
    rules = association_rules(frequent_itemsets, 
                              metric=metric, 
                              min_threshold=min_threshold)
    print(f"➡️ Generated {len(rules)} rules")
    return rules


# 4. Main Script

if __name__ == "__main__":
    transaction_df = load_transaction_data()
    frequent_itemsets = train_apriori(transaction_df, min_support=0.01)
    rules = generate_rules(frequent_itemsets, metric="lift", min_threshold=0.7)

    frequent_itemsets.to_csv("../data/processed/frequent_itemsets.csv", 
                             index=False, encoding="utf-8-sig")
    rules.to_csv("../data/processed/association_rules.csv", 
                 index=False, encoding="utf-8-sig")

    print("🎯 Saved frequent_itemsets.csv and association_rules.csv")
