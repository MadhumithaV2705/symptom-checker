from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load symptom data
with open("symptoms.json") as f:
    data = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    advice = ""

    if request.method == "POST":
        user_symptoms = request.form.getlist("symptoms")

        max_match = 0
        predicted_disease = "No match found"

        for disease, symptoms in data.items():
            match = len(set(user_symptoms) & set(symptoms))
            if match > max_match:
                max_match = match
                predicted_disease = disease

        result = predicted_disease

        # Advice logic
        if result == "Cold":
            advice = "Take rest and drink fluids"
        elif result == "Flu":
            advice = "Consult a doctor if symptoms are severe"
        elif result == "Covid-19":
            advice = "Isolate and consult a doctor immediately"
        elif result == "Allergy":
            advice = "Avoid allergens and take proper medication"
        else:
            advice = "No clear match. Please consult a doctor."

    return render_template("index.html", result=result, advice=advice)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)