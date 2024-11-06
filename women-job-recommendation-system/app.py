from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load pre-trained model
model = joblib.load('job_recommendation_model.pkl')
skills_df = pd.read_csv('job_skills.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs():
    skills = request.form['skills']
    recommended_jobs = recommend_jobs_for_skills(skills)
    return jsonify(recommended_jobs)

def recommend_jobs_for_skills(skills):
    # Preprocessing skills and job recommendation logic
    user_skills = set(skills.lower().split(','))
    matched_jobs = []

    for idx, row in skills_df.iterrows():
        job_skills = set(row['skills_required'].lower().split(','))
        if user_skills.intersection(job_skills):
            matched_jobs.append(row['job_title'])
    
    return matched_jobs

if __name__ == '__main__':
    app.run(debug=True)
