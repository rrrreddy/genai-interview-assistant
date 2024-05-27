import cohere
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Cohere client with the API key from the environment variable
cohere_api_key = os.getenv('COHERE_API_KEY')
cohere_client = cohere.Client(cohere_api_key)

# Function to store the initial context (resume and job description)
def store_context(resume_text, job_description):
    return f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}\n\n"

# Enhanced function to answer questions based on the stored context and a new question
def answer_questions(context, question):
    prompt = (
        f"You are an interviewee being asked questions based on your resume and a job description. "
        f"Provide a detailed and structured response to the following question.\n\n"
        f"{context}"
        f"Question:\n"
        f"{question}\n\n"
        "Answer as if you are the interviewee:"
    )
    response = cohere_client.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=500  # Adjust max_tokens to a higher value as needed
    )
    
    # Format the response in a structured way
    detailed_response = response.generations[0].text.strip()
    formatted_response = format_response(detailed_response)
    return formatted_response

def format_response(detailed_response):
    # Here we add basic formatting, such as headings and bold points
    formatted_response = ""
    lines = detailed_response.split('\n')
    
    for line in lines:
        if line.strip().endswith(':'):
            # Heading
            formatted_response += f"### {line.strip()}\n"
        elif line.strip():
            # Regular bullet points
            formatted_response += f"- **{line.strip()}**\n"
    
    return formatted_response
