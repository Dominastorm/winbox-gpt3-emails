import os
import openai
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_create(prompt, temperature=0.5, model="text-curie-001"):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.49,
        presence_penalty=0
    )
    return response["choices"][0]["text"]

def generate_email(sender, receiver):
    subject = openai_create(f"Write a subject line\nSender: {sender}\nReceiver: {receiver}", model="text-davinci-002").strip('\nSubject:')
    email = openai_create(f"Write an email with greeting and closing line\nSender: {sender}\nReceiver: {receiver}\nSubject: {subject}").lstrip('\n')
    print(f"To: {receiver}\nFrom: {sender}\nSubject:{subject}\n\n{email}")
    

def generate_email_and_response(sender, receiver):
    print("\n\n**************EMAIL****************\n\n")
    generate_email(sender, receiver)
    print("\n\n**************RESPONSE****************\n\n")
    generate_email(receiver, sender)
