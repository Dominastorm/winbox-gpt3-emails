import os
import openai
from dotenv import load_dotenv
import random
import time

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_create(prompt, temperature=0.7, model="text-curie-001"):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0.49,
        presence_penalty=0
    )
    return response["choices"][0]["text"]

def topics_generator():
    all_major_topics = []
    while len(all_major_topics) < 100:
        topics = openai_create("Generate 100 topics for deep conversation").split('\n')
        topics = [topic.lstrip('1234567890.) ') for topic in topics if topic]
        topics = [topic for topic in topics if topic not in all_major_topics and len(topic.split(' ')) < 4]
        all_major_topics.extend(topics)
        time.sleep(1)

    # write all the major topics into a file "major_topics.txt"
    with open('major_topics.txt', 'a') as f:
        for topic in all_major_topics:
            f.write(topic + '\n')

    all_detailed_topics = []
    # generate more detailed topics for each major topic
    for i in all_major_topics:
        detailed_topics = openai_create(f"Generate 10 topics for deep conversation on {i}").split('\n')
        detailed_topics = [topic.lstrip('1234567890.) ') for topic in detailed_topics if topic]
        all_detailed_topics.extend(detailed_topics)
        time.sleep(1)
    
    # write all the detailed topics into a file "detailed_topics.txt"
    with open('detailed_topics.txt', 'a') as f:
        for topic in all_detailed_topics:
            f.write(topic + '\n')

    
    
topics_generator()
