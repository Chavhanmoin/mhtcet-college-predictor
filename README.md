# 🎓 MHT-CET College Predictor

A Machine Learning project to help students predict eligible engineering colleges based on their MHT-CET rank, category, gender, and seat type. It uses real historical admission cutoff data from MHT-CET centralized counselling (CAP rounds).


## 📊 About the Dataset

The dataset includes cutoff ranks from previous years’ MHT-CET CAP rounds, published by DTE Maharashtra.

### Dataset Features:
- year: Admission year (2016–2021)
- institute_type: Government, Private, Autonomous
- institute_short: Short name (e.g., VJTI, COEP)
- program_name: Engineering branch (e.g., Computer Engineering)
- degree_short: Degree type (e.g., B.E., B.Tech)
- category: Reservation category (OPEN, OBC, SC, ST, etc.)
- seat_type: Quota type (HU, OHU, Minority)
- gender: Gender-based allocation
- opening_rank: First admitted rank
- closing_rank`: Last admitted rank

📁 Source: Official data from DTE Maharashtra CAP round reports.

---

## 🚀 Features

- Predicts possible colleges and branches based on user input
- Uses cleaned, real-world MHT-CET data
- Easy to run ML pipeline
- Helps students make informed decisions for option form filling

---

## ⚙️ How to Set Up and Run the Project (All Steps Included)

> 🛠️ Follow these steps to set up, train, and use the predictor:

```bash
# Step 1: Clone the repository
git clone https://github.com/Chavhanmoin/mhtcet-college-predictor.git
cd mhtcet-college-predictor

# Step 2: (Optional) Create a virtual environment
conda create -n cetenv python=3.10
conda activate cetenv

# Step 3: Install required Python packages
pip install -r requirements.txt

# Step 4: Trained machine learning model
trained_model_clg.pkl

# Step 5: Run the predictor application
python app.py
