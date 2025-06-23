import nltk
import spacy
import re
from nltk.chat.util import Chat, reflections

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Load spaCy with error handling
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import sys
    print("Downloading spaCy English model... (one-time operation)")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Enhanced patterns with better regex
pairs = [
    [
        r"(hi|hello|hey|greetings|good morning|good afternoon)",
        ["Hello! How can I help you today?", "Hi there! What can I do for you?"]
    ],
    [
        r"(.*)(your name|who are you)(.*)",
        ["I'm ChatBot, your friendly NLP assistant!",]
    ],
    [
        r"how are you(.*)",
        ["I'm just a program, but I'm functioning perfectly! How about you?"]
    ],
    [
        r"(.*)(weather|temperature|forecast)(.*)",
        ["I don't have live weather data, but you can check Weather.com or your favorite weather app!"]
    ],
    [
        r"(.*)(create|made|build|develop)(.*)(you|bot)(.*)",
        ["I was created using Python with NLTK and spaCy libraries!"]
    ],
    [
        r"(.*)(help|support|assist)(.*)",
        ["I can help with general questions. Try asking about technology, weather, or how I work!"]
    ],
    [
        r"(quit|bye|exit|goodbye)",
        ["Goodbye! Have a wonderful day!", "Bye! Come back anytime you need help."]
    ],
]

chatbot = Chat(pairs, reflections)

def process_with_spacy(text):
    """Enhanced NLP processing with better entity handling"""
    if not text.strip():
        return None
        
    doc = nlp(text.lower())
    
    # Check for specific patterns first
    if re.search(r"\b(time|current hour)\b", text.lower()):
        return "I don't have real-time access, but check your device's clock!"
    elif re.search(r"\b(date|today|day)\b", text.lower()):
        return "You can check the current date in your calendar or phone."
    
    # Only use entity detection if we have meaningful entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    if len(entities) >= 2:  # Only respond if multiple entities found
        return f"I detected these items: {entities}. Could you ask more specifically?"
    
    return None  # Fall back to rule-based

print("\n🤖 ChatBot: Hello! I'm your NLP assistant. Type 'quit' to exit.\n")

while True:
    try:
        user_input = input("👤 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'bye', 'exit']:
            print("🤖 ChatBot: Goodbye!")
            break
        
        # First try exact pattern matches
        response = chatbot.respond(user_input)
        if response:
            print(f"🤖 ChatBot: {response}")
            continue
            
        # Then try spaCy processing
        spacy_response = process_with_spacy(user_input)
        if spacy_response:
            print(f"🤖 ChatBot: {spacy_response}")
            continue
            
        # Final fallback
        print("🤖 ChatBot: I'm not sure I understand. Could you try rephrasing?")
        
    except KeyboardInterrupt:
        print("\n🤖 ChatBot: Goodbye!")
        break
    except Exception as e:
        print(f"🤖 ChatBot: Sorry, I encountered an error. Please try again.")
