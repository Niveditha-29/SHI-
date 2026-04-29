import pyttsx3

def speak_text(text: str, lang: str="en"):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # pick voice heuristically — system dependent
        if lang.startswith("hi"):
            if len(voices) > 0:
                engine.setProperty('voice', voices[-1].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        # non-fatal: TTS may fail on headless servers
        print("TTS error:", e)

def personality_response(intent: str):
    mapping = {
        "greet":"Hey there! 😊 How can I help with groundwater data?",
        "goodbye":"Goodbye! Stay safe 💧",
        "help":"You can ask about groundwater levels, trends, submit reports, or request recommendations."
    }
    return mapping.get(intent, "I'm ready to help with groundwater queries.")


