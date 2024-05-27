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
    context = f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}\n\n"
    return context


# Function to answer questions based on the stored context and a new question
def answer_questions(context, question):
    prompt = (
        f"{context}"
        f"Question:\n"
        f"{question}\n\n"
        "Answer:"
    )
    response = cohere_client.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=500  # Adjust max_tokens to a higher value as needed
    )
    return response.generations[0].text.strip()
