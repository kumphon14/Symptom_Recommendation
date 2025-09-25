# 🩺 Symptom Recommendation System  
ระบบแนะนำอาการผู้ป่วยด้วย "Association Rule Mining"

https://symptom001.streamlit.app/

<img width="748" height="786" alt="image" src="https://github.com/user-attachments/assets/78e065e8-03ab-4eb1-846f-61287afc498b" />

---

## 🔰 Introduction
This project is part of a **Data Science Candidate Assignment**.  
The objective is to build a **Symptom Recommendation System** that suggests possible related symptoms given an initial patient symptom (similar to how Netflix recommends movies).  

Project นี้มีเป้าหมายเพื่อ:
- วิเคราะห์ **อาการผู้ป่วย (symptoms)** ที่มักเกิดร่วมกัน  
- สร้างโมเดล baseline ด้วย **Association Rule Mining (Apriori)**  
- พัฒนา **API (FastAPI)** และ **UI (Streamlit)** สำหรับใช้งานและสาธิต  

---

## 💡 Why Association Rule?
Association Rule Mining is widely used in **Market Basket Analysis** and is suitable for healthcare symptom analysis:  

- **Unsupervised learning** → does not require labels  
- Finds **co-occurrence patterns** between symptoms  
- Produces **interpretable rules** (if–then format)  

ตัวอย่าง:  IF "Cough (ไอ)" THEN "Runny Nose (น้ำมูกไหล)"
Confidence = 0.72, Lift = 1.35

------------
## 📊 Data Preparation (Google Colab)

### Steps:
1. **Data Quality Check**  
   - Missing values (e.g., age, gender)  
   - Invalid values (e.g., age < 0, gender not in {male, female})  

2. **Symptom Extraction**  
   - From `search_term` (comma-separated symptoms)  
   - From `summary` (JSON field, yes_symptoms)  

3. **Data Cleaning**  
   - Normalize symptom names (ภาษาไทย + English)  
   - Manual mapping + fuzzy matching  
   - Reduced unique symptoms: ~329 → ~261 → ~70 frequent symptoms  

4. **One-Hot Encoding**  
   - Each patient = 1 row  
   - Each symptom = binary column (0/1)  

5. **Export for Modeling**  
   - `transaction_data.csv` (One-Hot data)  
   - `association_rules.csv` (Apriori output)  

---

## 🤖 Modeling

### Workflow
1. Load `transaction_data.csv`  
2. Apply **Apriori Algorithm** → generate frequent itemsets  
3. Derive **association rules** with metrics:  
   - Support, Confidence, Lift  
4. Filter rules with high confidence/lift  
5. Build `recommend_symptoms(symptom)` function

### Summary
- Successfully discovered **symptom clusters**  
- Created >70 rules with different support/confidence thresholds  
- Provides baseline model for recommendation  

---

## 🌐 API + UI

### FastAPI (Backend)
- Endpoint: `/recommend_symptom` (POST)  
- Input: `{age, gender, symptom, top_n}`  
- Output: Recommended symptoms in JSON  

Example:
```json
{
  "input": {
    "age": 26,
    "gender": "male",
    "symptom": "ไอ",
    "top_n": 3
  },
  "recommendations": ["น้ำมูกไหล", "เสมหะ"]
}

