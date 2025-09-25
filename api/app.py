from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import sys

# เพิ่ม path ของ src
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from recommender import load_rules, recommend_symptoms

# โหลด rules
rules = load_rules("../data/processed/association_rules.csv")

app = FastAPI(
    title="Symptom Recommendation API",
    description="Recommend symptoms based on patient profile + one initial symptom",
    version="1.0.0"
)

# -------------------------
# Patient Profile Schema
# -------------------------
class PatientProfile(BaseModel):
    age: int
    gender: str
    symptom: str
    top_n: int = 5

    class Config:
        schema_extra = {
            "example": {
                "age": 26,
                "gender": "male",
                "symptom": "ไอ",
                "top_n": 3
            }
        }

# -------------------------
# Root Test
# -------------------------
@app.get("/")
def root():
    return {"message": "Symptom Recommendation API is running 🚀"}

# -------------------------
# Recommend Symptoms
# -------------------------
@app.post("/recommend_symptom")
def recommend_symptom(profile: PatientProfile):
    # baseline ยังไม่ได้ใช้ age/gender
    recs = recommend_symptoms(profile.symptom, rules, top_n=profile.top_n)

    return {
        "input": profile.dict(),
        "recommendations": recs
    }