import speech_recognition as sr
import os

def recognize_speech_from_mic(recognizer, microphone, language="en-US"):
    """Transcribe speech from recorded from `microphone`."""
    with microphone as source:
        print("Please say something")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=language)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def save_transcription(text, filename="transcriptions.txt"):
    """Save the transcription to a file."""
    with open(filename, "a") as file:
        file.write(text + "\n")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    language = input("Enter the language code (e.g., 'en-US' for English, 'es-ES' for Spanish): ").strip()

    while True:
        print("Say a word or phrase to see how it's spelled (or type 'exit' to quit):")
        response = recognize_speech_from_mic(recognizer, microphone, language)

        if response["success"] and response["transcription"]:
            transcription = response["transcription"]
            print(f"You said: {transcription}")
            save_transcription(transcription)
        else:
            print(f"Error: {response['error']}")
        
        retry = input("Do you want to try again? (yes/no): ").strip().lower()
        if retry != "yes":
            break

if __name__ == "__main__":
    main()
