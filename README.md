# 🩺 Symptom Recommendation System  
ระบบแนะนำอาการผู้ป่วยด้วย "Association Rule Mining"

https://symptom001.streamlit.app/

<img width="748" height="786" alt="image" src="https://github.com/user-attachments/assets/78e065e8-03ab-4eb1-846f-61287afc498b" />

----------

## 🔰 Introduction
This project is part of a **Data Science Candidate Assignment**.  
The objective is to build a **Symptom Recommendation System** that suggests possible related symptoms given an initial patient symptom (similar to how Netflix recommends movies).  

Project นี้มีเป้าหมายเพื่อ:
- วิเคราะห์ **อาการผู้ป่วย (symptoms)** ที่มักเกิดร่วมกัน  
- สร้างโมเดล baseline ด้วย **Association Rule Mining (Apriori)**  
- พัฒนา **API (FastAPI)** และ **UI (Streamlit)** สำหรับใช้งานและสาธิต  

------------

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

------------

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

------------

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
```
------------
## Evaluation
🎯 Precision@5 = 0.275
- เมื่อโมเดลแนะนำ 5 อาการ (Top-5)
- มีเพียง 27.5% เท่านั้นที่ตรงกับอาการจริงของผู้ป่วยใน dataset

ตัวอย่าง:
- ถ้าผู้ป่วยมีอาการ {ไอ, น้ำมูกไหล, เสมหะ}
- โมเดลแนะนำ {น้ำมูกไหล, ไข้, ปวดหัว, เหนื่อย, เสมหะ}
- ใน 5 คำแนะนำ มี 2 คำที่ถูกต้อง (น้ำมูกไหล, เสมหะ)

Precision = 2/5 = 0.4
โดยเฉลี่ยแล้วทุก record ที่ test → ได้ค่าเฉลี่ยออกมา = 0.275

✅ สรุป: ความแม่นยำค่อนข้างต่ำ → อาจต้องปรับพารามิเตอร์ (min_support, min_confidence) หรือทำ data cleaning/mapping ให้ดีกว่านี้

🔎Coverage = 11.43%
- association rules ที่โมเดลสร้างขึ้น ครอบคลุมเพียง 11.43% ของอาการทั้งหมด ที่มีใน dataset

ตัวอย่าง:

- สมมติ dataset มี 70 อาการไม่ซ้ำ
- แต่ rules ครอบคลุมได้แค่ 8 อาการ
- Coverage = 8 / 70 = 11.43%

✅ สรุป: coverage ต่ำ แปลว่า rules ที่สร้างขึ้นยังไม่สามารถครอบคลุมอาการส่วนใหญ่ใน dataset ได้ บางอาการมี support ต่ำ → ไม่ถูกเลือกเป็น frequent itemsets กฎอาจกระจุกอยู่ที่ common symptoms เช่น "ไอ", "น้ำมูกไหล"

<img width="953" height="645" alt="image" src="https://github.com/user-attachments/assets/c230adcb-b0c4-489b-a24c-54dccf0cbc8b" />

- โมเดล baseline ทำงานได้โอเคใน Top-1 ถึง Top-3
- แต่เมื่อ K เพิ่มขึ้น → precision ตกลงอย่างมาก
- ถ้าใช้จริง อาจต้องเลือก trade-off:
- Precision สูง → แนะนำแค่ 1–3 อาการ
- Coverage สูง → ยอม precision ต่ำ แต่ให้ user ได้ list ยาวขึ้น
