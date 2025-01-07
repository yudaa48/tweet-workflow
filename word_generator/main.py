import google.generativeai as genai
from google.cloud import firestore
import functions_framework
from datetime import datetime, timezone
import json
import logging
import random

# Configure Gemini
GEMINI_API_KEY = "AIzaSyCipUnqzS5HxN0Lcs7cC9vTRyGiT-Hwm1c"
genai.configure(api_key=GEMINI_API_KEY)

# List of topics to randomize word generation
TOPICS = [
    "academic", "literature", "science", "arts", "business", 
    "psychology", "philosophy", "technology", "nature", "society"
]

# System instruction for word generation
def get_random_prompt():
    topic = random.choice(TOPICS)
    difficulty = random.choice(["basic", "intermediate", "advanced"])
    type_word = random.choice(["adjective", "noun", "verb", "adverb"])
    
    return f"""Generate one random {difficulty} {type_word} related to {topic}. 
Give me exactly this JSON format:
[
  {{
    "word": "unique word here",
    "definition": "clear definition",
    "example": "practical example sentence",
    "status": {random.randint(1, 3)},
    "part_of_speech": "{type_word}",
    "difficulty_level": "{difficulty}",
    "topic": "{topic}"
  }}
]

Important:
- Generate a DIFFERENT word each time
- Word should be educational and useful
- Must not be a very common word
- Ensure word hasn't been used before
- Return ONLY the JSON array"""

def generate_words_with_gemini():
    """Use Gemini to generate vocabulary words"""
    try:
        # Initialize model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Generate content with random prompt
        prompt = get_random_prompt()
        logging.info(f"Using prompt with parameters: {prompt}")
        
        response = model.generate_content(prompt)
        logging.info(f"Raw Gemini response: {response.text}")
        
        # Parse response
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:-3]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:-3]
        
        clean_text = clean_text.strip()
        logging.info(f"Cleaned text: {clean_text}")
        
        word_data = json.loads(clean_text)
        logging.info(f"Parsed word data: {word_data}")
        
        return word_data
        
    except Exception as e:
        logging.error(f"Error in generate_words: {str(e)}", exc_info=True)
        logging.error(f"Response text: {response.text if 'response' in locals() else 'No response'}")
        return []

@functions_framework.http
def generate_word(request):
    """Cloud Function to generate and store new words"""
    try:
        # Generate word
        logging.info("Starting word generation...")
        words_data = generate_words_with_gemini()
        
        if not words_data:
            return {
                "success": False,
                "error": "No words generated",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        # Initialize Firestore
        db = firestore.Client()
        words_ref = db.collection('words')
        
        # Process each word
        added_words = []
        for word_data in words_data:
            word_id = word_data['word'].lower()
            logging.info(f"Processing word: {word_id}")
            
            # Check for existing word
            if words_ref.document(word_id).get().exists:
                logging.info(f"Word '{word_id}' already exists, generating another...")
                continue
            
            # Add metadata
            word_data.update({
                'created_at': datetime.now(timezone.utc),
                'last_updated': datetime.now(timezone.utc),
                'generated_by': 'gemini-1.5-flash',
                'times_used': 0,
                'last_tweeted': None,
                'generation_time': datetime.now(timezone.utc).isoformat()
            })
            
            # Save to Firestore
            words_ref.document(word_id).set(word_data)
            added_words.append({
                'word': word_data['word'],
                'status': word_data['status'],
                'part_of_speech': word_data.get('part_of_speech', 'N/A'),
                'topic': word_data.get('topic', 'general'),
                'definition': word_data['definition']
            })
            logging.info(f"Added new word: {word_id}")
        
        result = {
            "success": True,
            "words_added": added_words,
            "count": len(added_words),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logging.info(f"Function completed. Result: {result}")
        return result
        
    except Exception as e:
        logging.error(f"Error in generate_word: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }