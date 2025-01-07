import google.generativeai as genai
from google.cloud import firestore
from datetime import datetime, timezone
import json
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# System instruction for word generation
SYSTEM_INSTRUCTION = """Generate one interesting and educational vocabulary word. Give me exactly this JSON format:
[
  {
    "word": "ephemeral",
    "definition": "lasting for a very short time",
    "example": "The ephemeral beauty of a rainbow",
    "status": 2,
    "part_of_speech": "adjective",
    "difficulty_level": "intermediate",
    "topic": "general"
  }
]

Important:
- Word should be educational and useful
- Definition must be clear and concise
- Example should be practical and demonstrative
- Status should be between 1-3 (1=easy, 2=medium, 3=hard)
- Include part of speech
- Avoid very technical or specialized terms
"""

def generate_words_with_gemini():
    """Use Gemini to generate vocabulary words"""
    try:
        # Initialize model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Generate content
        response = model.generate_content(SYSTEM_INSTRUCTION)
        logging.info(f"Raw response: {response.text}")
        
        # Parse response
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:-3]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:-3]
        
        clean_text = clean_text.strip()
        word_data = json.loads(clean_text)
        logging.info(f"Parsed word data: {word_data}")
        
        return word_data
        
    except Exception as e:
        logging.error(f"Error in generate_words: {str(e)}", exc_info=True)
        return []

def add_word_to_firestore(word_data):
    """Add generated word to Firestore"""
    try:
        db = firestore.Client()
        words_ref = db.collection('words')
        
        # Process word
        word_id = word_data['word'].lower()
        
        # Check for existing word
        if words_ref.document(word_id).get().exists:
            logging.info(f"Word '{word_id}' already exists")
            return False
        
        # Add metadata
        word_data.update({
            'created_at': datetime.now(timezone.utc),
            'last_updated': datetime.now(timezone.utc),
            'generated_by': 'gemini-1.5-flash',
            'times_used': 0,
            'last_tweeted': None
        })
        
        # Save to Firestore
        words_ref.document(word_id).set(word_data)
        logging.info(f"Added new word: {word_id}")
        
        # Log detailed word info
        logging.info(f"Word details:")
        logging.info(f"- Part of speech: {word_data.get('part_of_speech', 'N/A')}")
        logging.info(f"- Difficulty level: {word_data.get('difficulty_level', 'N/A')}")
        logging.info(f"- Topic: {word_data.get('topic', 'N/A')}")
        return True
        
    except Exception as e:
        logging.error(f"Error adding word to Firestore: {str(e)}", exc_info=True)
        return False

def main():
    """Main function to test word generation and storage"""
    try:
        # Generate word
        logging.info("Starting word generation...")
        words_data = generate_words_with_gemini()
        
        if not words_data:
            logging.error("No words generated")
            return
        
        # Process each word
        added_words = []
        for word_data in words_data:
            if add_word_to_firestore(word_data):
                added_words.append({
                    'word': word_data['word'],
                    'status': word_data['status'],
                    'part_of_speech': word_data.get('part_of_speech', 'N/A')
                })
        
        # Print results
        print("\nResults:")
        print(f"Words generated: {len(words_data)}")
        print(f"Words added: {len(added_words)}")
        if added_words:
            print("\nAdded words:")
            for word in added_words:
                print(f"- {word['word']} ({word['part_of_speech']}, status: {word['status']})")
            
    except Exception as e:
        logging.error(f"Error in main: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()