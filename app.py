import streamlit as st
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os


# Configure the model if available
GEMINI_API_KEY = os.getenv('TestProject2')
model = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash',
        api_key=GEMINI_API_KEY,
        temperature=0.9
    )

# Sidebar: upload resume (PDF only)
st.sidebar.title('UPLOAD YOUR RESUME (Only PDF)')
file = st.sidebar.file_uploader('RESUME', type=['pdf'])
if file:
    file_text = text_extractor(file)
    st.sidebar.success('File Uploaded Successfully')
    st.write('Extracted resume text (preview):')
    st.text(file_text[:1000])

# Main app
st.title('🧠 SKILLMATCH: AI-Powered Resume Skill Matching')
st.markdown('This application will match and analyze your resume and the job description provided')
tips = """
Follow these steps:
1. Upload a PDF resume in the sidebar
2. Provide a job description to match
"""
st.write(tips)

job_desc = st.text_area('Paste the Job Description here:', height=200,key ='job_description',max_chars=5000)

if st.button('MATCH NOW'):
    with st.spinner('Processing....'):
        prompt = f'''
        <role> You are an expert career coach and resume analyzer.
        <goal> Your task is to compare a applicant's resume with a job description provided by the applicant.
        <context> The following content is the applicant's resume:
        * Resume : {file_text}
        * Job Description : {job_desc}
        <format> The report should follow these steps
        * Give a brief description of applicant in 3 to 5 lines. 
        * Describe in percentage what are the chances of this resume getting selected for the job role(give approximate).
        * Need not to be exact percentage  you can give interval of percentage like 70-80%.
        * Give the expected ATS score along with matching and non-matching keywords.
        * Perform SWOT analysis and explain each parameter that is strength,weakness,opportunity and threat in detail.
        * Give what all current resume that are required to be added or removed to match the job description.
        * Show both current version and imporved version of resume.
        * Create two smaple resume which can maximize the ATS score for the job description provided.

        <Instructions>
        * Use bullet points wherever necessary.
        * Create tables for description where ever required
        * Strictly do not add any new skill in new resume which is not present in the job description or current resume.
        * The format of the sample resume should be in such a way that it can be copy pasted directly to resume file. 
        '''



        response = model.invoke(prompt)
        st.write(response.content)