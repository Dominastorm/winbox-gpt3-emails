import os
import openai
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_create(prompt, temperature):
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=temperature,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.49,
        presence_penalty=0
    )
    return response["choices"][0]["text"]

def generate_subject_lines(topic):
    lines = openai_create("Provide five subject lines for an email about " + topic, 0.5).split("\n")[2:]
    return lines

def generate_email_body(subject_line, receiver="David"):
    subject_line = subject_line.lstrip('123456789').lstrip('. ') 
    prompt ="Write an email body for \nSubject: " + subject_line + "\nTo:" + receiver
    return openai_create(prompt, 0.5).lstrip('\n')

def generate_email_response(email):
    prompt = "Write a reply to this email: \n'''\n" + email + "\n'''\n"
    return openai_create(prompt, 0.5).lstrip('\n')

def generate_email_and_response(topic):
    lines = generate_subject_lines(topic)
    print("\nGenerted subject lines:")
    for line in lines:
        print(line)
    subject_line = lines[int(input("\nChoose the subject line that suits you the best: ")) - 1]
    # generate email body using the subject line
    email_body = generate_email_body(subject_line)
    print("\nGenerated email body:\n")
    print(email_body)
    # generate response to email using the email
    email_response = generate_email_response(email_body)
    print("\nGenerated email response:\n")
    print(email_response)

generate_email_and_response("Hoverboard")
