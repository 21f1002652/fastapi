from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  # Converts FastAPI to serverless handler
import csv
from typing import List
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load CSV
students_data = []
csv_path = os.path.join(os.path.dirname(__file__), "..", "students.csv")
with open(csv_path, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        students_data.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })

@app.get("/api")
def get_students(class_: List[str] = Query(None, alias="class")):
    if class_:
        filtered = [s for s in students_data if s["class"] in class_]
        return {"students": filtered}
    return {"students": students_data}

# Convert to serverless handler
handler = Mangum(app)
