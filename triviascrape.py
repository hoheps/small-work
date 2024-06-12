#requires: youtube-transcript-api, scrapetube, google-generativeai
# too lazy to make a requirements.txt B)
import pathlib
import textwrap
import google.generativeai as genai
import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
import csv
import time
from io import StringIO
import re
import os
# from IPython.display import display
# from IPython.display import Markdown
# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
# Used to securely store your API key
#from google.colab import userdata
def grab_questions(videoID,model):
    # data = [] # i used to output it as a tuple
    transcript = YouTubeTranscriptApi.get_transcript(videoID)
    xscript = " ".join(x['text'] for x in transcript)
    response = model.generate_content("Return the questions and answers from this transcript. Include round name. There are 10 questions in each section. Skip questions that refer to pictures: " + xscript)
    #print(response.text)
    return response.text

def parse_text(original_text,model):
    #time.sleep(20)
    time.sleep(20)
    pre_text = model.generate_content('''Convert this into a unformatted string with the question, and answer and newline after every question and answer pair. Include the round name at the top. Remove all questions with no answers. Format it as follows:
Q: {question} A: {answer}
The next lines are the script to be converted.
''' + original_text)
    text = pre_text.text
    round_name_pattern = r"Round \d+: (.*?)\*\*"
    round_names = re.findall(round_name_pattern, text)
    clean_text = text.replace('*','')
    split_round = re.split(r'Round \d+:', clean_text)
    data = []
    for i, round_name in enumerate(round_names):
        round_name = round_name.strip()
        rounds = split_round[i+1] #first block is ''
        # print(f"{round_name}")
        # nightmare regex
        round_pattern = r"Q: (.*?)\nA: (.*?)\n\n"
        
        matches = re.findall(round_pattern, rounds)
        if len(matches) < 9: #normall 10x q per round
            return False
        if len(split_round[1:]) < 3: #at least 3 rounds per game
            return False
        for question, answer in matches:
            # Replace '**' with an empty string in the question
            question = question.strip()
            # print(f"Question: {question}")
            # print(f"Answer: {answer}\n")
            data.append((round_name,question,answer))
    return(data)



api_key = 'find your own' #smile
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')
videos = scrapetube.get_channel(channel_username="thetrivialist",content_type="streams")
i = 0
#data = []
for x in videos:
    i += 1
    #if i<18:
        #continue
    #if i>50:
    #    break
    videoID = x['videoId']
    name = x["title"]['runs'][0]['text'].lower()
    savename = ''.join(x.lower() for x in name if x.isalnum())
    if 'trivia' not in name or 'king' in name or 'quiz' in name or 'championship' in name:
        continue
    print(savename,x['videoId'], i)
    #text = grab_questions(videoID, model) #i had it pass data before and make a big file, but doing it batches for now
    j = 0
    q = 0
    new_data = []
    while j < 20 and not new_data:
        #grab questions up to 20 times :)
        j+=1
        if q%2 == 0:
            print('grabbing questions')
            time.sleep(10)
            text = grab_questions(videoID, model)
        #try to parse text, if it fails, it'll try again, and if it fails again, grab questions again
        try:
            print("trying formatting")
            new_data = parse_text(text, model)
            if not new_data:
                q += 1
                continue
            #don't need this
            break
        except Exception as e:
            print(f'Error: {e}')
    filesavename = savename+'.csv'
    if os.path.isfile(filesavename+'.csv'):
        with open('temp', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['Round','Question','Answer'])
            csv_writer.writerows(new_data)
        new_size = os.path.getsize('temp')
        old_size = os.path.getsize(savename+'.csv')
        if new_size>old_size:
            with open(filesavename, "w", newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Round','Question','Answer'])
                csv_writer.writerows(new_data)
    else:
        with open(filesavename, "w", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Round','Question','Answer'])
            csv_writer.writerows(new_data)
    print(f'saved file: {filesavename}')

print(i)
