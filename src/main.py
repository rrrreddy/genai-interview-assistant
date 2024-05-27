import streamlit as st
from src.get_response import store_context, answer_questions

def initialize_session_state():
    if "context" not in st.session_state:
        st.session_state.context = None
    if "qa_pairs" not in st.session_state:
        st.session_state.qa_pairs = []

def input_resume_and_job_description():
    st.subheader("Input Resume and Job Description")
    resume_input = st.text_area("Enter your resume text:", height=200)
    job_description_input = st.text_area("Enter the job description text:", height=200)

    if st.button("Submit Resume and Job Description"):
        if resume_input.strip() and job_description_input.strip():
            st.session_state.context = store_context(resume_input, job_description_input)
            st.session_state.qa_pairs = []  # Clear previous Q&A pairs when new context is submitted
            st.success("Context stored successfully. You can now ask questions.")
            st.rerun()
        else:
            st.warning("Please enter both the resume and the job description text.")

def input_question():
    st.subheader("Ask Questions")
    question_input = st.text_input("Enter a question based on the resume and job description:")
    
    if st.button("Answer Question"):
        if st.session_state.context and question_input.strip():
            answer = answer_questions(st.session_state.context, question_input)
            st.session_state.qa_pairs.insert(0, (question_input, answer))  # Insert at the beginning to keep the latest at the top
            st.rerun()
        else:
            st.warning("Please enter a question.")

def display_qa_pairs():
    if st.session_state.qa_pairs:
        st.subheader("Questions and Answers:")
        for i, (question, answer) in enumerate(st.session_state.qa_pairs):
            st.write(f"**Q{i+1}:** {question}")
            st.markdown(answer, unsafe_allow_html=True)

def clear_context_and_qa():
    if st.button("Clear Context and Q&A"):
        st.session_state.context = None
        st.session_state.qa_pairs = []
        st.success("Context and Q&A cleared. Please enter new resume and job description.")
        st.rerun()

def add_social_links():
    st.sidebar.title("Follow Me")
    st.sidebar.write("[GitHub](https://github.com/rrrreddy)")
    st.sidebar.write("[LinkedIn](https://www.linkedin.com/in/raghu-konda/)")

def run_app():
    st.title("Interview Assistant")
    st.write("This app uses Cohere's NLP capabilities to simulate an interviewee and answer questions based on your resume and job description.")

    add_social_links()

    initialize_session_state()

    if st.session_state.context is None:
        input_resume_and_job_description()
    else:
        st.success("Context is already stored. You can ask questions based on it.")
        input_question()
        display_qa_pairs()
        clear_context_and_qa()

    st.write("Designed by Raghu!")
