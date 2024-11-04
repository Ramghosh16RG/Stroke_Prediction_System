from flask import Flask, request, render_template, flash, jsonify
import pickle

app = Flask(__name__)
app.secret_key = "apkofriowjfkf"

@app.route("/")
def index():
    return render_template('stroke.html')
@app.route('/norisk.html')
def norisk():
    return render_template('norisk.html')

@app.route('/doctor.html')
def doctor():
    return render_template('doctor.html')



@app.route("/output", methods=["POST", "GET"])
def output():
    if request.method == 'POST':
        g = request.form['gender']
        if g == "male":
            g = 1
        elif g == "female":
            g = 0
        else:
            g = 2

        a = request.form['age']
        if a.isdigit():
            a = int(a)
            a = ((a - 0.08) / (82 - 0.08))
        else:
            return "Please Enter a Valid Age"

        # Hyper-tension
        hyt = request.form['hypertension']
        hyt = hyt.lower()
        if hyt == "yes":
            hyt = 1
        else:
            hyt = 0

        # Heart disease
        ht = request.form['heart-disease']
        ht = ht.lower()
        if ht == "yes":
            ht = 1
        else:
            ht = 0

        # Marriage
        m = request.form['marriage']
        m = m.lower()
        if m == "yes":
            m = 1
        else:
            m = 0

        # Work type
        w = request.form['worktype']
        w = w.lower()
        if w == "government":
            w = 0
        elif w == "student":
            w = 1
        elif w == "private":
            w = 2
        elif w == "self-employed":
            w = 3
        else:
            w = 4

        # Residency type
        r = request.form['residency']
        r = r.lower()
        if r == "urban":
            r = 1
        else:
            r = 0

        # Glucose levels
        gl = request.form['glucose']
        gl = int(gl)
        gl = ((int(gl) - 55) / (271 - 55))

        # BMI
        b = request.form['bmi']
        b = int(b)
        b = ((b - 10.3) / (97.6 - 10.3))

        # Smoking
        s = request.form['smoking']
        if s == "unknown":
            s = 0
        elif s == "never smoked":
            s = 1
        elif s == "formerly smoked":
            s = 2
        elif s == "smokes":
            s = 3
        else:
            s = 0

        try:
            prediction_prob, prediction_rf = stroke_pred(g, a, hyt, ht, m, w, r, gl, b, s)
            print(f"Logistic Regression Predicted Probability: {prediction_prob}")

            # Adjusted threshold values
            no_risk_threshold = 1.0
            risk_threshold = 0.1

            # Classify predictions based on thresholds
            if prediction_prob >= no_risk_threshold:
                prediction = 'You have a significant risk of having a Stroke'
            elif prediction_prob >= risk_threshold:
                prediction = 'You have chances of having a Stroke'
            else:
                prediction = 'You have no risk of having a Stroke '

            return render_template('output.html', prediction=prediction, prob=prediction_prob)

        except ValueError:
            return "Please Enter Valid Values"

# Prediction model
def stroke_pred(g, a, hyt, ht, m, w, r, gl, b, s):
    # Load model
    model = pickle.load(open('model.pkl', 'rb'))

    # Predictions
    result_prob = model.predict_proba([[g, a, hyt, ht, m, w, r, gl, b, s]])[0, 1]
    result_rf = model.predict([[g, a, hyt, ht, m, w, r, gl, b, s]])

    return result_prob, result_rf[0]

if __name__ == "__main__":
    app.debug = True  # Enable debug mode
    app.run()
