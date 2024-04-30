# Resume Matchmaker

## Overview
Resume Matchmaker is a Streamlit application designed to help users assess how well their resume aligns with a specific job description. By leveraging BERT (Bidirectional Encoder Representations from Transformers) for natural language processing, it analyzes and visually represents the similarity between sections of a resume and job requirements.

## Features
- **File Upload**: Users can upload resumes and job descriptions as PDF or text files.
- **Text Input**: Direct text input fields for users who prefer to paste the contents of their documents.
- **Similarity Analysis**: Compares sections like Experience, Education, and Skills between the resume and job description.
- **Visual Feedback**: Utilizes gauge charts to visually display the match quality of each section and overall.
- **Dynamic Recommendations**: Provides actionable recommendations based on the computed similarity scores.

## Installation

### Prerequisites
- Python 3.8 or later
- pip package manager

### Libraries
Install the necessary Python libraries using pip:

```bash
pip install streamlit transformers scikit-learn plotly pdfminer.six
```

## Usage

### Running the Application
To run the application locally, use the following command in your terminal:

```bash
streamlit run Resume_Analyser.py
```

### Using the Application
1. **Upload Files**: In the sidebar, upload your resume and the job description through the provided file uploader.
2. **Input Text Manually**: Optionally, paste the text directly into the text areas provided.
3. **Analysis**: Submit the form to analyze the documents. The results will be displayed as gauge charts representing the similarity scores for each section and overall.

## Configuration
No additional configuration is required to run the application with default settings. Adjustments can be made within the code for advanced users.

## Development
Want to contribute? Great! Here's how you can set up the development environment:

1. **Clone the repository**:
   ```bash
   git clone git clone https://github.com/your-username/resume-matchmaker.git
cd resume-matchmaker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Make changes and test**:
   Modify the code and run the application to see your changes.
