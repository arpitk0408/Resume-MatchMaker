#!/usr/bin/env python
# coding: utf-8

# In[37]:


import streamlit as st
import re
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
import io
import plotly.graph_objects as go
# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def extract_text_from_pdf(file):
    try:
        return extract_text(io.BytesIO(file.getvalue()))
    except Exception as e:
        st.error(f"Failed to extract text from PDF: {str(e)}")
        return None

def preprocess_text(text):
    # Check if text is None or not a string, and return an empty string if so
    if not isinstance(text, str):
        return ""
    return " ".join(text.lower().strip().split())

def text_to_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.pooler_output.detach().numpy()

def calculate_similarity(text1, text2):
    emb1 = text_to_embedding(preprocess_text(text1))
    emb2 = text_to_embedding(preprocess_text(text2))
    return cosine_similarity(emb1, emb2)[0][0]

def extract_section(text, header):
    headers = {
        'experience': ['education', 'skills', 'projects', 'summary', 'objective'],
        'education': ['experience', 'skills', 'projects', 'summary', 'objective'],
        'skills': ['experience', 'education', 'projects', 'summary', 'objective']
    }
    all_headers = set([item for sublist in headers.values() for item in sublist])
    all_headers_regex = '|'.join(map(re.escape, all_headers))
    pattern = rf"(?<=\b{header}\b)([\s\S]*?)(?=\b({all_headers_regex})\b|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def read_uploaded_file(uploaded_file):
    try:
        return uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        try:
            uploaded_file.seek(0)
            return uploaded_file.read().decode('windows-1252')
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return uploaded_file.read().decode('iso-8859-1')

def overall_recommendation(scores):
    if all(score >= 0.85 for score in scores):
        return "Perfect match! Strongly consider applying."
    elif any(score < 0.75 for score in scores):
        return "You may not be a good match for this role."
    else:
        return "You are a good match for this role."

# Define the Plotly gauge chart function
def create_gauge_chart(score, title):
    if score < 0.75:
        gauge_value = (score - 0.3) * 100
    elif score < 0.85:
        gauge_value = (score - 0.5) * 200
    else:
        gauge_value = (score - 0.70) * 300
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': 'red'},
                {'range': [20, 40], 'color': 'orange'},
                {'range': [40, 60], 'color': 'yellow'},
                {'range': [60, 80], 'color': 'yellowgreen'},
                {'range': [80, 100], 'color': 'green'},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': gauge_value}
        }
    ))
    fig.update_layout(height=300)
    return fig


def main():
    st.title("Resume Matchmaker")

    with st.sidebar:
        st.header("Upload Files")
        resume_file = st.sidebar.file_uploader("Resume (PDF):", type=['pdf'])
        job_description_file = st.sidebar.file_uploader("Job Description (Text):", type=['txt'])

    resume_text = extract_text_from_pdf(resume_file) if resume_file else ""
    job_description_text = read_uploaded_file(job_description_file) if job_description_file else ""

    with st.form("User Text Input"):
        resume_text_area = st.text_area("Paste your resume here:", resume_text)
        job_description_text_area = st.text_area("Paste the job description here:", job_description_text)
        submitted = st.form_submit_button("Analyze")

    if submitted and resume_text_area and job_description_text_area:
        sections = ['experience', 'education', 'skills']
        scores = []

        for section in sections:
            with st.expander(f"{section.capitalize()} Section"):
                resume_section = extract_section(resume_text_area, section)
                job_desc_section = extract_section(job_description_text_area, section)
                similarity_score = calculate_similarity(resume_section, job_desc_section)
                scores.append(similarity_score)

                # Display gauge chart for each section
                gauge_chart = create_gauge_chart(similarity_score, f"{section.capitalize()} Section Match")
                st.plotly_chart(gauge_chart, use_container_width=True)

        # Calculate overall recommendation
        if scores:
            overall_score = sum(scores) / len(sections)
            overall_gauge_chart = create_gauge_chart(overall_score, "Overall Match")
            st.plotly_chart(overall_gauge_chart, use_container_width=True)

            recommendation = "Perfect match! Strongly consider applying." if all(score >= 0.85 for score in scores) else \
                             "Good match for this role." if all(score >= 0.7 for score in scores) else \
                             "You may not be a good match for this role."
            st.subheader("Overall Recommendation:")
            st.write(recommendation)

if __name__ == "__main__":
    main()

