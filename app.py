from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import joblib
import hashlib
import os
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://co2022mrchavhan:DpJBBep3cItaABJk@cluster0.zgbyrmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0pyth"
client = MongoClient(MONGO_URI)
db = client['college_prediction_2']
users_collection = db['users']

# Load dataset and model
college = pd.read_csv("MHTCET_RANK_last_dance_3 - MHTCET_RANK_last_dance_3.csv")
model = joblib.load("trained_model_clg.pkl")

# Create mapping if model was trained with encoded labels
college_names = college['college_name'].unique()
label_to_college = {i: name for i, name in enumerate(college_names)}

seat_type_map = {
    'MI': 0,
    'MI-MH': 1,
    'OBC': 2,
    'OPEN': 3,
    'SC': 4,
    'ST': 5
}

branch_map = {
    'Computer Engineering': 0,
    'Electrical Engineering': 1,
    'Electronics and Telecommunication Engg': 2,
    'Information Technology': 3
}

def predict_college(sample_input):
    try:
        transformed_input = {
            'min': float(sample_input['min']),
            'Min Rank': int(sample_input['Min Rank']),
            'seat_type': seat_type_map.get(sample_input['seat_type'], -1),
            'branch': branch_map.get(sample_input['branch'], -1)
        }
    except Exception as e:
        return f"Error in input conversion: {str(e)}"

    if transformed_input['seat_type'] == -1 or transformed_input['branch'] == -1:
        return "Invalid seat type or branch selected."

    sample_df = pd.DataFrame([transformed_input], columns=['min', 'Min Rank', 'seat_type', 'branch'])
    predicted_label = model.predict(sample_df)[0]

    college_name = label_to_college.get(predicted_label, f"Unknown College ID: {predicted_label}")
    return college_name

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    if 'username' in session:
        branch = sorted(college["branch"].unique())
        seat_type = sorted(college["seat_type"].unique())
        return render_template('form.html', branch=branch, seat_type=seat_type)
    else:
        return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' in session:
        try:
            min_rank = request.form.get('min_rank')
            min_score = request.form.get('min_score')
            branch = request.form.get('branch')
            seat_type = request.form.get('seat_type')

            sample_input = {
                "Min Rank": min_rank,
                "min": min_score,
                "seat_type": seat_type,
                "branch": branch
            }

            predicted_college = predict_college(sample_input)
            return predicted_college
        except Exception as e:
            return f"Error during prediction: {str(e)}"
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if users_collection.find_one({'$or': [{'username': username}, {'email': email}, {'phone': phone}]}):
            return 'Username, email, or phone number already exists!'

        users_collection.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'username': username,
            'password': hashed_password
        })

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = users_collection.find_one({'username': username, 'password': hashed_password})
        if user:
            session['username'] = username
            return redirect(url_for('form'))

        return 'Invalid username or password'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
