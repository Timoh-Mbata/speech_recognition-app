import streamlit as st
import streamlit.components.v1 as components

# Function to transcribe speech using the browser-based Web Speech API
def browser_speech_recognition():
    # Embedding HTML and JavaScript for browser-based speech recognition
    components.html("""
    <html>
        <body>
            <h2>Speech Recognition</h2>
            <button id="startButton">Start Recording</button>
            <p id="status"></p>
            <p id="transcribedText"></p>
            <script>
                var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.lang = 'en-US'; // You can change language here
                recognition.continuous = true;
                recognition.interimResults = true;

                document.getElementById('startButton').onclick = function() {
                    recognition.start();
                    document.getElementById('status').textContent = "Listening...";
                };

                recognition.onresult = function(event) {
                    var transcript = '';
                    for (var i = event.resultIndex; i < event.results.length; i++) {
                        transcript += event.results[i][0].transcript;
                    }
                    document.getElementById('transcribedText').textContent = transcript;
                    // Send the result back to Streamlit app (optional)
                    window.parent.postMessage({type: 'set_text', text: transcript}, '*');
                };

                recognition.onerror = function(event) {
                    document.getElementById('status').textContent = "Error occurred: " + event.error;
                };
            </script>
        </body>
    </html>
    """, height=400)

# Streamlit UI components
st.title("Speech Recognition App (Browser-based)")
st.markdown("This app uses your browser's speech recognition API.")

# Display browser-based speech recognition
browser_speech_recognition()

# Optionally, you can collect the transcribed text from the browser and show it in your Streamlit app.
st.markdown("### Transcribed Text")
transcribed_text = st.text_area("Text from Speech", height=200)
