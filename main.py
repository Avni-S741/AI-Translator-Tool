import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from gtts import gTTS
import os


st.set_page_config(page_title="AI Translator Tool", page_icon="💬", layout="centered")

# CSS styling 
st.markdown("""
    <style>
    /* Designing app background */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #f3e5f5);
        color: #2e2e2e;
        font-family: 'Segoe UI', sans-serif;
    }

            
    /* Designing main title */
    .title {
        text-align: center;
        font-size: 2.5em;
        font-weight: 700;
        color: #7e57c2; 
        text-shadow: 0 0 8px #b39ddb; 
    }

    /* Designing Subtitle / tagline */
    .subtitle {
        text-align: center;
        font-size: 1.1em;
        color: #6a1b9a; 
        margin-bottom: 25px;
    }

    /* Designing Widget labels */
    .stSelectbox label, .stRadio label, .stTextArea label {
        color: #4fc3f7 !important; 
        font-weight: 600;
    }
            
    /* Designing Radio buttons for input type */
.stRadio label {
    color: #4a148c !important;  
    font-weight: 600;
}
            
/* Widget container background - pastel friendly */
.css-1lcbmhc .stRadio, 
.css-1lcbmhc .stSelectbox, 
.css-1lcbmhc .stTextArea {
    background-color: #e6f0fa !important; /* very light pastel blue */
    padding: 10px;
    border-radius: 12px;
}


    /* Designing Buttons */
    div.stButton > button:first-child {
        background-color: #7e57c2; 
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5em 1em;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #9575cd; 
        box-shadow: 0 0 12px #b39ddb;
    }

    /* Designing Output / success box */
    .stSuccess {
        background-color: #e1bee7;
        border-left: 5px solid #7e57c2;
        color: #2e2e2e;
    }
    </style>
""", unsafe_allow_html=True)

 
st.markdown("<h1 class='title'>💬 AI Translator Tool</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'><i>Smart translation at your fingertips🌸....Because language should never be a barrier🍃...!!</i></p>", unsafe_allow_html=True)


#languages dictionary for reference
languages = {
    "Hindi": "hi",
    "Arabic": "ar",
    "Urdu": "ur",
    "Russian":"ru",
    "Italian":"it",
    "Portuguese":"pt",
    "Dutch":"nl",
    "Turkish":"tr",
    "Thai":"th",
    "Vietnamese":"vi",
    "Bengali":"bn",
    "Punjabi":"pa",
    "Gujarati":"gu",
     "Indonesian": "id",
    "Greek": "el",
    "Polish": "pl",
    "Romanian": "ro",
    "Czech": "cs",
    "Hungarian": "hu",
    "Finnish": "fi",
    "Swedish": "sv",
    "Norwegian": "no",
    "Tamil":"ta",
    "Telugu":"te",
    "Marathi":"mr",
    "Swahili":"sw",
    "Filipino":"tl",
    "German": "de",
    "English": "en",
    "Korean": "ko",
    "Mandarin": "chinese(simplified)",
    "Japanese": "ja",
    "Spanish": "es",
    "French": "fr",
}

lang_for_gtts= {
    "Hindi": "hi",
    "Arabic": "ar",
    "Urdu": "ur",
    "Russian":"ru",
    "Italian":"it",
    "Portuguese":"pt",
    "Dutch":"nl",
    "Turkish":"tr",
    "Thai":"th",
    "Vietnamese":"vi",
    "Bengali":"bn",
    "Punjabi":"pa",
    "Gujarati":"gu",
     "Indonesian": "id",
    "Greek": "el",
    "Polish": "pl",
    "Romanian": "ro",
    "Czech": "cs",
    "Hungarian": "hu",
    "Finnish": "fi",
    "Swedish": "sv",
    "Norwegian": "no",
    "Tamil":"ta",
    "Telugu":"te",
    "Marathi":"mr",
    "Swahili":"sw",
    "Filipino":"tl",
    "German": "de",
    "English": "en",
    "Korean": "ko",
    "Mandarin": "zh-cn",
    "Japanese": "ja",
    "Spanish": "es",
    "French": "fr",
}


languages = dict(sorted(languages.items()))


#using .selectbox to generate dropdown list of languages 
lang_from=st.selectbox("Translate from:",list(languages.keys()))
lang_to=st.selectbox("Translate to:",list(languages.keys()))

#using .radio to choose input type
input_type=st.radio("Choose input type:",("Text","Speech")).lower()
st.write("You chose:",input_type)

#action according to input type
 user_input=""
if input_type == "text":
   
    user_input = st.text_area("Enter your text:") 
elif input_type == "speech":
     r=sr.Recognizer() #creates a recognizer object which will later be used as 'r'...

     st.write("Click below to start recording your voice:")
     if st.button("Record"): 
        st.info("Recording started... speak now!")

         # webrtc_ctx creates a live channel between the browser and app....
        webrtc_ctx = webrtc_streamer(
            key="speech",
            mode=WebRtcMode.SENDRECV, # tells function that we want to send and recieve audio...
            audio_receiver_size=1024, #specify audio size....
            media_stream_constraints={"audio": True, "video": False}, # enable audio and disable video since we only need audio....
        )
        user_input = "" # initialize user_input as empty

        if webrtc_ctx.audio_receiver:# checks if audio reciever is active...
             audio = webrtc_ctx.audio_receiver.get_audio() # collect audio.... 
             if audio is not None: #checks if audio is not empty/full silence....
        
              audio_data = sr.AudioData(audio.tobytes(), 
                                        sample_rate=webrtc_ctx.sample_rate,
                                        sample_width=2
                                        )
        
             try:
                user_input = r.recognize_google(audio_data) # sends your audio to google and recieve text from it.... 
                st.success(f"You said: {user_input}")
             except sr.UnknownValueError:
                st.error("Sorry...we didn't get it...")
             except sr.RequestError:
                st.error("Speech recognition service unavailable.")
                 
#actual translating work
translated_text = ""  # empty string to start
translator=GoogleTranslator(source=languages[lang_from],target=languages[lang_to])
if user_input:
    #translator sends text inside user input to google translation engine...googletrans extracts the actual translated text...and .text make it accessible...
    translated_text=translator.translate(user_input)
st.success(translated_text)

#speech of translated text....

if translated_text: #if translated text is not empty then execute the code below this
    try:  
        speech=gTTS(translated_text,lang=lang_for_gtts[lang_to]) #'speech' now stores what to speak and in what language BUT NOT ACTUAL AUDIO
        audiofile="translated-audio.mp3" # made an audio file to store audio later
        speech.save(audiofile) #here speech(value inside speech variable) is getting generated as an actual audio inside audiofile
        st.audio(audiofile) #streamlit here plays the actual audio generated inside audiofile  
    
    except:   

        st.write("Unsupported language: Sorry, We can't provide you audio of this language....")








