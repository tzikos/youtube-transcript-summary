from youtube_transcript_api import YouTubeTranscriptApi, _errors
import openai
import streamlit as st 

st.header('YouTube video summary App')

st.write("An OpenAI API key is needed. Please visit https://platform.openai.com/account/api-keys and copy yours, or create a new one.")
st.write('Make sure that the video has subtitles!')

key = st.text_input("Paste your API key here: ") 
openai.api_key = str(key)

video_url = st.text_input("Enter the YouTube video URL: ")

question = st.text_input('What information do you need from this video?: ')
try:
    if st.button('Submit'):
        if (video_url and question and key):
            if "watch?v=" in video_url:
                video_id = video_url.split("watch?v=")[-1]
            else:
                video_id = video_url.split("/")[-1]

            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcripts_en = [t.fetch() for t in transcript_list if t.language_code == 'en']
                if not transcripts_en:
                    st.write("No English transcripts found")
                    

                text = " ".join(t['text'] for t in transcripts_en[0])
                #prompt = f'{question} from this text: {(lambda x: " ".join(random.sample(x.split(),3500)) if len(x.split())>4097 else x)(text)}'
                prompt = f'Answer this :{question} from this text: {text}, with "~" to be the last character of the response'
                if len(text.split())>4097:
                    st.write('The text is too long.')
                    
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0.9,
                    max_tokens=3000,
                    top_p=1,
                    frequency_penalty=0.8,
                    presence_penalty=0.9,
                    stop = '~'
                )
                summary = response["choices"][0]["text"]
                st.write(summary)
            except _errors.TranscriptsDisabled:
                st.write('Subtitles are disabled for this video.')
        else :
            'Provide a valid YouTube link and your question.'
except openai.error.AuthenticationError:
    print('Please provide a valid API key.')
