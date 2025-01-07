from google.cloud import firestore
import functions_framework
from datetime import datetime, timezone
import logging
import random

@functions_framework.http
def create_tweet(request):
    try:
        request_json = request.get_json(silent=True) or {}
        words = request_json.get('words', [])
        check_type = request_json.get('check_type')

        if not words:
            return {"success": False, "message": "No words provided"}
            
        selected_word = random.choice(words)
        tweet_content = f"📚 Word: {selected_word.get('word')}\n"
        if 'definition' in selected_word:
            tweet_content += f"📖 {selected_word['definition']}\n"
        if 'example' in selected_word:
            tweet_content += f"✏️ {selected_word['example']}"
        
        db = firestore.Client()
        tweets_ref = db.collection('tweets')
        tweet_ref = tweets_ref.document()
        
        tweet_data = {
            'content': tweet_content,
            'created_at': datetime.now(timezone.utc),
            'word_id': selected_word.get('id'),
            'status': 'pending'
        }
        tweet_ref.set(tweet_data)
        
        return {
            "success": True,
            "tweet_id": tweet_ref.id,
            "content": tweet_content
        }
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"success": False, "message": str(e)}