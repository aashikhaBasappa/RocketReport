# from flask import Flask, render_template, request, jsonify
# import requests
#
# app = Flask(__name__)
#
# # News API configuration
# NEWS_API_KEY = "8b701c212811423085c8e331b22d52c1"
# BASE_URL = 'https://newsapi.org/v2/top-headlines'
#
# # Hugging Face GPT-Neo configuration
# HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
# HUGGINGFACE_HEADERS = {"Authorization": "Bearer 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"}
#
#
# def fetch_news(category):
#     """Fetch news articles based on category."""
#     params = {
#         'apiKey': NEWS_API_KEY,
#         'pageSize': 5,  # Limit to 5 articles for simplicity
#     }
#
#     # Handle political category by searching for "politics" if the category is "political"
#     if category == 'political':
#         params['q'] = 'politics'  # Use query for political content
#     else:
#         params['category'] = category  # Use category for other types of news
#
#     response = requests.get(BASE_URL, params=params)
#     if response.status_code == 200:
#         articles = response.json().get('articles', [])
#         return [(article['title'], article['url']) for article in articles]
#     else:
#         return [("Error fetching news", "")]
#
#
# def query_huggingface(prompt):
#     """Send a prompt to GPT-Neo via Hugging Face Inference API and return the response."""
#     payload = {"inputs": prompt}
#     try:
#         response = requests.post(HUGGINGFACE_API_URL, headers=HUGGINGFACE_HEADERS, json=payload)
#         response.raise_for_status()  # Raise an error for bad status codes
#         result = response.json()
#         # Extract the generated text from the response
#         if result and isinstance(result, list):
#             return result[0]["generated_text"]
#         else:
#             return "Error: Unexpected response format from Hugging Face API."
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"
#
#
# @app.route('/')
# def index():
#     """Render the homepage."""
#     return render_template('index.html')
#
#
# @app.route('/chat', methods=['POST'])
# def chat():
#     """Handle chatbot interactions."""
#     user_input = request.form['user_input']
#     # Pass the user input to GPT-Neo and get the response
#     prompt = f"The following is a conversation with an AI assistant. The assistant is helpful, creative, and friendly.\n\nUser: {user_input}\nAI:"
#     chatbot_response = query_huggingface(prompt)
#     return jsonify({'response': chatbot_response})
#
#
# @app.route('/get_news', methods=['POST'])
# def get_news():
#     """Fetch news articles based on category."""
#     category = request.form['category']
#     news = fetch_news(category)
#     return jsonify(news)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)



import requests
from datetime import datetime
import openai
import pyttsx3
from googletrans import Translator
from gtts import gTTS
import pygame

# # OpenAI API setup
# openai.api_key = "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"

# News API setup
NEWS_API_KEY = "8b701c212811423085c8e331b22d52c1"
BASE_URL = 'https://newsapi.org/v2/top-headlines'
NEWS_BASE_URL = 'https://newsapi.org/v2/top-headlines'


def fetch_news(category=None, country=None):
    """Fetch news articles by category or country."""
    params = {
        'apiKey': NEWS_API_KEY,
        'category': category,
        'country': country,
        'pageSize': 5,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return [(article['title'], article['url']) for article in articles]
    else:
        return [("Error fetching news", "")]


def generate_response_with_openai(prompt):
    """Generate a response using OpenAI's GPT model."""
    try:
        completion = openai.ChatCompletion.create(
            model= "text-embedding-3-large",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating response: {str(e)}"
def fetch_news_1(category=None, country='us'):
    """
    Fetch top news articles based on category and country.
    """
    params = {
        'apiKey': NEWS_API_KEY,
        'category': category,
        'country': country,
        'pageSize': 5,  # Number of articles
    }
    response = requests.get(NEWS_BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        if not articles:
            return f"No news highlights available for {category or 'general'}."
        highlights = [
            f"{idx + 1}. {article['title']} ({article['source']['name']})\nURL: {article['url']}"
            for idx, article in enumerate(articles)
        ]
        highlights_urlless = [
            f"{idx + 1}. {article['title']} ({article['source']['name']})\n"
            for idx, article in enumerate(articles)
        ]
        return "\n".join(highlights) , "\n".join(highlights_urlless)
    else:
        error_message = response.json().get('message', 'Unknown error')
        return f"Error fetching news: {error_message}"

# Initialize the translator
# def translator (language_code, text):
#     translator = Translator()
#
#     # Original text to translate
#     # text = "Hello, this code is a test."
#
#     # Translate the text to Russian
#     translated = translator.translate(text, src='en', dest=language_code)
#
#     # Print the original and translated text
#     print("Original Text:", text)
#     print("Translated Text:", translated.text)
#
#     # Use gTTS to convert the translated text to speech
#     tts = gTTS(translated.text, lang=language_code)
#
#     # Initialize pygame mixer for playing sound
#     pygame.mixer.init()
#
#     # Save the speech to a temporary file and immediately load it
#     tts.save("temp_test.mp3")
#     pygame.mixer.music.load("temp_test.mp3")
#     pygame.mixer.music.play()
#
#     # Block the program until the speech finishes
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)  # Wait for the sound to finish
from deep_translator import GoogleTranslator

def translator(language_code, text):
    """Translate text using deep-translator's Google Translator."""
    try:
        translated_text = GoogleTranslator(source='en', target=language_code).translate(text)
        # print("Original Text:", text)
        # print("Translated Text:", translated_text)
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return f"Error: Unable to translate text to {language_code}"


def chatbot():
    language_codes = {
        1: ("English", "en"),
        2: ("Spanish", "es"),
        3: ("French", "fr"),
        4: ("German", "de"),
        5: ("Italian", "it"),
        6: ("Portuguese", "pt"),
        7: ("Dutch", "nl"),
        8: ("Russian", "ru"),
        9: ("Chinese (Mandarin)", "zh-CN"),
        10: ("Japanese", "ja"),
        11: ("Korean", "ko"),
        12: ("Arabic", "ar"),
        13: ("Hindi", "hi"),
        14: ("Bengali", "bn"),
        15: ("Punjabi", "pa"),
        16: ("Tamil", "ta"),
        17: ("Telugu", "te"),
        18: ("Malayalam", "ml"),
        19: ("Kannada", "kn"),
        20: ("Marathi", "mr"),
        21: ("Gujarati", "gu"),
        22: ("Urdu", "ur"),
        23: ("Greek", "el"),
        24: ("Turkish", "tr"),
        25: ("Swedish", "sv"),
        26: ("Danish", "da"),
        27: ("Norwegian", "no"),
        28: ("Finnish", "fi"),
        29: ("Polish", "pl"),
        30: ("Czech", "cs"),
        31: ("Hungarian", "hu"),
        32: ("Romanian", "ro"),
        33: ("Ukrainian", "uk"),
        34: ("Thai", "th"),
        35: ("Vietnamese", "vi"),
        36: ("Indonesian", "id"),
        37: ("Filipino", "tl"),
        38: ("Swahili", "sw"),
        39: ("Catalan", "ca"),
        40: ("Basque", "eu"),
        41: ("Galician", "gl"),
        42: ("Icelandic", "is"),
        43: ("Serbian", "sr"),
        44: ("Croatian", "hr"),
        45: ("Bosnian", "bs"),
        46: ("Slovak", "sk"),
        47: ("Latvian", "lv"),
        48: ("Lithuanian", "lt"),
        49: ("Estonian", "et"),
        50: ("Albanian", "sq"),
    }

    """Interactive chatbot function."""
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    # Text to speak
    text = "Hello, this is a text-to-speech example."

    # Convert text to speech
    # engine.say(text)
    # engine.runAndWait()
    # start outputs
    print("Welcome to Rocket Report!")
    engine.say("Welcome to Earth Updates Chatbot with AI!")
    engine.runAndWait()
    engine.say("Enter a number to select a language: ")
    engine.runAndWait()
    for number, (language_name, language_code) in language_codes.items():
        print(f"{number}. {language_name}")
        # engine.say(f"{number}. {language_name}")
        engine.runAndWait()
    language_number = int(input("Enter a number to select a language: "))

    # If-Else Loop to check the number and print the language name and code
    if language_number in language_codes:
        language_name, language_code = language_codes[language_number]
        print(f"Selected Language: {language_name}\nLanguage Code: {language_code}")
        engine.say(f"Selected Language: {language_name}\nLanguage Code: {language_code}")
        language_code_selected = language_code
        engine.runAndWait()
    else:
        print("Invalid number, please enter a valid number between 1 and 50.")
        engine.say("Invalid number, please enter a valid number between 1 and 50.")
        engine.runAndWait()
    print(translator(language_code_selected,"I can provide daily updates"))
    engine.say(translator(language_code_selected,"I can provide daily updates"))
    engine.runAndWait()
    print(translator(language_code_selected,"Topics: Political, Social, Economic, Sports, General"))
    engine.say(translator(language_code_selected,"Topics: Political, Social, Economic, Sports, General"))
    engine.runAndWait()
    # print("Regions: US, UK, India, etc.\n")
    # engine.say("Regions: US, UK, India, etc.")
    # engine.runAndWait()

    while True:
        print(translator(language_code_selected,"\nOptions:"))
        engine.say(translator(language_code_selected,"Options:"))
        engine.runAndWait()
        print(translator(language_code_selected,"1. Get General daily updates"))
        engine.say(translator(language_code_selected,"1. Get General daily updates"))
        engine.runAndWait()
        print(translator(language_code_selected,"2. Get daily updates by topic"))
        engine.say(translator(language_code_selected,"2. Get daily updates by topic"))
        engine.runAndWait()
        # print("3. Get daily updates by region")
        # engine.say("3. Get daily updates by region")
        # engine.runAndWait()
        print(translator(language_code_selected,"3. Exit\n"))
        engine.say(translator(language_code_selected,"3. Exit"))
        engine.runAndWait()

        engine.say(translator(language_code_selected,"Enter your choice (1 or 2 or 3 or 4):"))
        engine.runAndWait()
        choice = input(translator(language_code_selected,"Enter your choice (1/2/3/4): ")).strip()

        if choice == '2':
            engine.say(translator(language_code_selected,"Enter topic (political, social, economic, sports): "))
            engine.runAndWait()

            topic = input(translator(language_code_selected,"Enter topic (political, social, economic, sports): ")).lower()
            category_map = {
                'political': 'general',
                'social': 'entertainment',
                'economic': 'business',
                'sports': 'sports',
            }
            category = category_map.get(topic)
            if category:
                news = fetch_news(category=category)
                print(translator(language_code_selected,f"\n{topic.capitalize()} Updates:"))
                engine.say(translator(language_code_selected,f"\n{topic.capitalize()} Updates:"))
                engine.runAndWait()
                for idx, (title, url) in enumerate(news, start=1):
                    print(translator(language_code_selected,f"{idx}. {title} - {url}"))
                    engine.say(translator(language_code_selected,f"{idx}. {title}"))
                    engine.runAndWait()
            else:
                print(translator(language_code_selected,"Invalid topic. Try again."))
                engine.say(translator(language_code_selected,"Invalid topic. Try again."))
                engine.runAndWait()

        # elif choice == '3':
        #     engine.say("Enter country code (e.g., us for USA, in for India): ")
        #     country = input("Enter country code (e.g., us for USA, in for India): ").lower()
        #     news = fetch_news(country=country)
        #     print(f"\nUpdates from {country.upper()}:")
        #     engine.say(f"\nUpdates from {country.upper()}:")
        #     engine.runAndWait()
        #     for idx, (title, url) in enumerate(news, start=1):
        #         print(f"{idx}. {title} - {url}")
        #         engine.say(f"{idx}. {title}")
        #         engine.runAndWait()

        elif choice == '1':
            print(translator(language_code_selected,"Fetching today's news highlights..."))
            engine.say(translator(language_code_selected,"Fetching today's news highlights"))
            engine.runAndWait()
            today = datetime.now().strftime('%Y-%m-%d')
            print(translator(language_code_selected,f"Date: {today}"))
            engine.say(translator(language_code_selected,f"Date: {today}"))
            engine.runAndWait()

            # General News Highlights
            print(translator(language_code_selected,"\nGeneral News Highlights:"))
            general_highlights = fetch_news_1()  # No category specified for general news
            print(translator(language_code_selected,general_highlights[0]))
            engine.say(translator(language_code_selected,general_highlights[1]))
            engine.runAndWait()

        elif choice == '3':
            print(translator(language_code_selected,"Goodbye!"))
            engine.say(translator(language_code_selected,"Goodbye"))
            engine.runAndWait()
            break

        else:
            print(translator(language_code_selected,"Invalid choice. Try again."))
            engine.say(translator(language_code_selected,"Invalid choice. Try again."))
            engine.runAndWait()


if __name__ == '__main__':
    chatbot()

