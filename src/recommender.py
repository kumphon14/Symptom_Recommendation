import pandas as pd


# 1. Load Rules

def load_rules(filepath="../data/processed/association_rules.csv"):
   
    # Load association rules created with Apriori.
    
    #print(f"📥 Loading rules from {filepath}")
    rules = pd.read_csv(filepath)

    # Convert antecedents and consequents from string -> set

    rules['antecedents'] = rules['antecedents'].apply(
        lambda x: set(eval(x)) if isinstance(x, str) else set()
    )
    rules['consequents'] = rules['consequents'].apply(
        lambda x: set(eval(x)) if isinstance(x, str) else set()
    )

    print(f"✅ Loaded {len(rules)} rules")
    return rules

# 2. Recommend Symptoms

def recommend_symptoms(symptom, rules_df, top_n=5):
    
    # Introduce new symptoms according to association rules

    # Terms that should not be recommended
    non_symptom_terms = [
        "การรักษาก่อนหน้า",
        "Previous treatment",
        "ประวัติอุบัติเหตุ",
        "History of trauma",
        "ประวัติความดันสูง",
        "History of hypertension (high blood pressure)",
        "ประวัติโรคกระเพาะ",
        # demographic
        "male", "female",
    ]

    # Select the rule that antecedent has symptom
    filtered = rules_df[rules_df['antecedents'].apply(lambda x: symptom in x)]
    filtered = filtered.sort_values(by="confidence", ascending=False)

    recommendations = []
    for consequents in filtered['consequents']:
        for c in consequents:
            if c != symptom and c not in non_symptom_terms:
                recommendations.append(c)

    # Unique top-N night
    return list(dict.fromkeys(recommendations))[:top_n]



# 3. Main (for testing)

if __name__ == "__main__":
    rules = load_rules()

