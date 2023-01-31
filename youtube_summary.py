from youtube_transcript_api import YouTubeTranscriptApi
import openai
import streamlit as st 

st.header('YouTube video summary App')


openai.api_key = "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"

video_url = st.text_input("Enter the YouTube video URL: ")

question = st.text_input('What do you want to ask for this video?: ')
if (video_url and question):
    video_id = video_url.split("watch?v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    transcripts_en = [t.fetch() for t in transcript_list if t.language_code == 'en']
    if not transcripts_en:
        print("No English transcripts found")
        

    text = " ".join(t['text'] for t in transcripts_en[0])
    #prompt = f'{question} from this text: {(lambda x: " ".join(random.sample(x.split(),3500)) if len(x.split())>4097 else x)(text)}'
    prompt = f'Answer this :{question} from this text: {text}'
    if len(text.split())>4097:
        print('The text is too long.')
        
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    summary = response["choices"][0]["text"]
    st.write(summary)
    

    