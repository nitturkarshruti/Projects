from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from google.cloud import generativeai as palm
import zapier_python as zapier

app = Flask(__name__)

# Initialize PaLM Client
palm.configure(api_key='AIzaSyDKOjp4ccw4rdJ2u7qaG-rsbWr7wRzslyE')

# Load pre-trained job recommendation model
model = joblib.load('job_recommendation_model_tfidf.pkl')
skills_df = pd.read_csv('job_data.csv')

# Zapier integration
zapier_client = zapier.Zapier('https://hooks.zapier.com/hooks/catch/20651393/255nzok/')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs():
    skills = request.form['skills']
    recommended_jobs = recommend_jobs_for_skills(skills)
    
    # Send a Zapier notification about the job recommendation
    zapier_client.send({
        'email': 'user@example.com', 
        'recommended_jobs': recommended_jobs
    })

    return jsonify(recommended_jobs)

def recommend_jobs_for_skills(skills):
    user_skills = set(skills.lower().split(','))
    matched_jobs = []

    for idx, row in skills_df.iterrows():
        job_skills = set(row['skills_required'].lower().split(','))
        job_desc = row['job_description']
        
        # Use PaLM for similarity analysis
        response = palm.compare_texts(
            context=skills, target=job_desc
        )
        similarity = response.result.score
        
        if user_skills.intersection(job_skills) or similarity > 0.75:
            matched_jobs.append(row['job_title'])
    
    return matched_jobs

if __name__ == '__main__':
    app.run(debug=True)
