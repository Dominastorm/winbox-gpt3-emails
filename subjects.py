import os
import openai
from dotenv import load_dotenv
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


def major_topics_generator(no_of_topics):
    # read major topics from file "major_topics.txt"
    with open('major_topics.txt', 'r') as f:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        all_major_topics = [topic.rstrip('\n ') for topic in f.readlines()]
    # storing the index starting from which the topics are generated
    major_index = len(all_major_topics)

    # generate more detailed topics for each major topic
    while len(all_major_topics) < no_of_topics:
        topics = openai_create("Generate 100 topics for deep conversation").split('\n')
        topics = [topic.lstrip('1234567890.)- ').rstrip('\n ') for topic in topics if topic]
        topics = [topic for topic in topics if topic not in all_major_topics and len(topic.split(' ')) < 4]
        all_major_topics.extend(topics)
        time.sleep(1)

    # write all the new major topics into a file "major_topics.txt"
    with open('major_topics.txt', 'a') as f:
        for topic in all_major_topics[major_index:]:
            f.write(topic + '\n')


def detailed_topics_generator():
    # read detailed topics from file "detailed_topics.txt"
    with open('detailed_topics.txt', 'r') as f:
        all_detailed_topics = f.readlines()
    # storing the index starting from which the topics are generated
    detailed_index = len(all_detailed_topics)

    # read major topics from file "major_topics.txt"
    with open('major_topics.txt', 'r') as f:
        all_major_topics = f.readlines()
    # since some major topics are also generated in the process, we can store those as well    
    # store the index starting from which the topics are generated
    new_major_topics = []
    
    # generate topics with each of the following tones 
    tones = ['curious', 'urgent', 'excited', 'happy', 'sad', 'angry', 'fearful', 'neutral', 'surprised']

    # generate more detailed topics for each major topic
    for topic in all_major_topics[:1]:
        for tone in tones:
            generated_topics = openai_create(f"Write 10 sub-topics for {topic} in {tone} statements").split('\n')
            detailed_topics = [topic.lstrip('1234567890.)- ').strip('\n') for topic in generated_topics if topic and 5 < len(topic.split(' ')) < 12 and '?' not in topic and topic not in all_detailed_topics]
            major_topics = [topic.lstrip('1234567890.)- ').strip('\n') for topic in generated_topics if topic and len(topic.split(' ')) < 5 and '?' not in topic and topic not in all_major_topics]
            all_detailed_topics.extend(detailed_topics)
            new_major_topics.extend(major_topics)
            time.sleep(1)
    
    # write all the new detailed topics into a file "detailed_topics.txt"
    with open('detailed_topics.txt', 'a') as f:
        for topic in all_detailed_topics[detailed_index:]:
            f.write(topic + '\n')

    # write all the new major topics into a file "major_topics.txt"
    with open('major_topics.txt', 'a') as f:
        for topic in new_major_topics:
            f.write(topic + '\n')

detailed_topics_generator()