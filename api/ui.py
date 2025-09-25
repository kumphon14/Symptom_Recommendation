import streamlit as st
import pandas as pd
import requests
import os

import sys
from pathlib import Path

# เพิ่ม path ของ project root
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.recommender import load_rules, recommend_symptoms
# ----------------------
# Config
# ----------------------
st.set_page_config(page_title="Symptom Recommendation Demo", page_icon="🩺")
st.title("🩺 Symptom Recommendation System")
st.write("ใส่ข้อมูลผู้ป่วย + อาการเริ่มต้น เพื่อดูคำแนะนำอาการที่เกี่ยวข้อง")

# ----------------------
# Mode เลือก API หรือ Local
# ----------------------
USE_API = os.getenv("USE_API", "false").lower() == "true"

if not USE_API:
    # โหลด recommender.py มาใช้โดยตรง
    from src.recommender import load_rules, recommend_symptoms
    rules = load_rules("data/processed/association_rules.csv")

# ----------------------
# Input fields
# ----------------------
age = st.number_input("อายุ (Age)", min_value=0, max_value=120, value=26)
gender = st.selectbox("เพศ (Gender)", ["male", "female"])
symptom = st.text_input("อาการเริ่มต้น (Symptom)", "ไอ")
top_n = st.slider("จำนวนคำแนะนำ (Top-N)", 1, 10, 5)

# ----------------------
# Submit Button
# ----------------------
if st.button("🔍 แนะนำอาการ"):
    if USE_API:
        # ---- API MODE ----
        payload = {
            "age": age,
            "gender": gender,
            "symptom": symptom,
            "top_n": top_n
        }
        try:
            res = requests.post("http://127.0.0.1:8000/recommend_symptom", json=payload)
            if res.status_code == 200:
                recs = res.json().get("recommendations", [])
            else:
                st.error(f"❌ Error {res.status_code}: {res.text}")
                recs = []
        except Exception as e:
            st.error(f"🚨 ไม่สามารถเชื่อมต่อ API ได้: {e}")
            recs = []
    else:
        # ---- STANDALONE MODE ----
        recs = recommend_symptoms(symptom, rules, top_n=top_n)

    # ----------------------
    # Show Results
    # ----------------------
    st.subheader("✅ ผลลัพธ์การแนะนำ")
    if recs:
        df_recs = pd.DataFrame({
            "ลำดับ": range(1, len(recs) + 1),
            "อาการแนะนำ": recs
        })
        st.table(df_recs)
    else:
        st.warning("ไม่พบคำแนะนำอาการเพิ่มเติม")
