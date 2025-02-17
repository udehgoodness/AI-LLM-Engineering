import gradio as gr
import openai
import os
from gtts import gTTS
import speech_recognition as sr


# Ensure this script is run in an activated virtual environment
# The following commands should not be in the script but run separately in the terminal:
# python -m venv venv
# source venv/bin/activate  (On macOS/Linux)
# venv\Scripts\activate  (On Windows)
# pip install --upgrade pip
# pip install gradio openai gtts speechrecognition

# Set your OpenAI API key
openai.api_key = "your_openai_api_key_here"

def generate_response(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI interview coach."},
                  {"role": "user", "content": input_text}]
    )
    reply = response['choices'][0]['message']['content']
    
    # Convert text to speech
    tts = gTTS(reply)
    audio_path = "response.mp3"
    tts.save(audio_path)
    
    return reply, audio_path

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

def process_input(text_input, audio_input):
    if audio_input is not None:
        text_input = transcribe_audio(audio_input)
    
    response_text, response_audio = generate_response(text_input)
    return response_text, response_audio

# Create Gradio interface
interface = gr.Interface(
    fn=process_input,
    inputs=[gr.Textbox(label="Enter your question"), gr.Audio(source="upload", type="filepath", label="Or upload an audio file")],
    outputs=[gr.Textbox(label="AI Response"), gr.Audio(label="Audio Response")],
    title="AI Interview Prep Tool",
    description="Ask your interview question via text or audio, and receive a response in both formats."
)

if __name__ == "__main__":
    print("Ensure you are running this script in a virtual environment.")
    interface.launch()
