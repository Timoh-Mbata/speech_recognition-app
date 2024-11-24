import streamlit as st
import speech_recognition as sr

# Function to handle transcription
def transcribe_speech(api_choice, lang_choice):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("Please speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        st.info("Recognizing...")

    try:
        if api_choice == "Google":
            text = recognizer.recognize_google(audio, language=lang_choice)
        elif api_choice == "Sphinx":
            text = recognizer.recognize_sphinx(audio)
        elif api_choice == "Microsoft Bing":
            text = recognizer.recognize_bing(audio, key="YOUR_BING_API_KEY", language=lang_choice)
        elif api_choice == "IBM Watson":
            text = recognizer.recognize_ibm(audio, username="YOUR_WATSON_USERNAME", password="YOUR_WATSON_PASSWORD", language=lang_choice)
        else:
            st.error("API not supported!")
            return None
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand your speech.")
    except sr.RequestError as e:
        st.error(f"Could not request results from the speech service; {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to save transcribed text
def save_text(text):
    if text:
        file_name = st.text_input("Enter file name", "transcription.txt")
        with open(file_name, "w") as file:
            file.write(text)
        st.success(f"Text saved to {file_name}")

# Streamlit UI components
st.title("Speech Recognition App")
api_option = st.selectbox(
    "Choose the Speech Recognition API",
    ["Google", "Sphinx", "Microsoft Bing", "IBM Watson"]
)
language_choice = st.selectbox(
    "Choose the language",
    ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT"]
)

is_recording = st.checkbox("Start/Stop Recording")

if is_recording:
    st.text("Recording... Please speak into the microphone.")
    text = transcribe_speech(api_option, language_choice)
    if text:
        st.write(f"Transcribed text: {text}")
        save_text(text)
else:
    st.text("Click to start recording.")
