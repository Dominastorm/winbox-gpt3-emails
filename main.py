import os
import openai
from dotenv import load_dotenv
import random

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_create(prompt, temperature=0.7, model="text-curie-001"):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=80,
        top_p=1,
        frequency_penalty=0.49,
        presence_penalty=0
    )
    return response["choices"][0]["text"]


def generate_greeting_and_closing(sender, receiver):
    # choose a random email greeting with name
    greeting = random.choice(["Dear", "Hello", "Hi", "Hey", "Good morning", "Good afternoon", "Good evening"])
    greeting = f"{greeting} {receiver}"

    # choose a random email closing line with name
    closing = random.choice(["Sincerely", "Best regards", "Thanks", "Thank you", "Regards", "Best wishes", "Sincerely"])
    closing = f"{closing},\n{sender}"

    return greeting, closing


def email_builder(sender, receiver):
    # generate content for email and response
    first_email_content, second_email_content = generate_email_content(sender, receiver)

    # generate greeting and closing for email
    first_greeting, first_closing = generate_greeting_and_closing(sender, receiver)
    # combine greeting, email content and closing for email
    first_email = f"{first_greeting}\n\n{first_email_content}\n\n{first_closing}"

    # generate greeting and closing for response
    second_greeting, second_closing = generate_greeting_and_closing(receiver, sender)
    # combine greeting, email content and closing for response
    second_email = f"{second_greeting}\n\n{second_email_content}\n\n{second_closing}"

    return first_email, second_email


def generate_email_content(sender, receiver):
    text = openai_create(f"Two bots {sender} and {receiver} are in the middle of a discussion. Each speaking in 2 lines.")
    text = [i.split(":") for i in text.split('\n') if i]
    # check if the conversaation length is 2
    if len(text) == 2:
        # check if it has been generated in the correct format
        if text[0][0] == sender and text[1][0] == receiver:
            # extract dialogue from text
            first_email_content = text[0][1].lstrip(' ')
            second_email_content = text[1][1].lstrip(' ')
            return first_email_content, second_email_content
        # regenerate if the conversation is not in the correct format
        else:
            return generate_email_content(sender, receiver)

    # Alternative generation format: In case the dialogues are 
    # generated in the lines after the names
    # check if the conversaation length is 4
    elif len(text) == 4:
        # check if it has been generated in the correct format
        if text[0][0] == sender and text[2][0] == receiver:
            # extract dialogue from text
            first_email_content = text[1][0].lstrip(' ')
            second_email_content = text[3][0].lstrip(' ')
            return first_email_content, second_email_content
        # regenerate if the conversation is not in the correct format
        else:
            return generate_email_content(sender, receiver)
    # regenerate if the conversation length is not 2 or 4
    else:
        return generate_email_content(sender, receiver)


def print_email_and_response(sender, receiver):
    first_email, second_email = email_builder(sender, receiver)
    print("\n\n**************EMAIL****************\n\n")
    print(first_email)    
    print("\n\n**************RESPONSE****************\n\n")
    print(second_email)

print_email_and_response("Dhruv", "Kushagra")