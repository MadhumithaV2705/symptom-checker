from flask import Flask, render_template, request
import json

app = Flask(__name__)

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
            advice = "Consult doctor if severe"
        elif result == "Covid-19":
            advice = "Isolate and consult doctor"
        elif result == "Allergy":
            advice = "Avoid allergens and take medication"

    return render_template("index.html", result=result, advice=advice)

if __name__ == "__main__":
    app.run(debug=True)