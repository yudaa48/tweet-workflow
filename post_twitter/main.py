import tweepy
from google.cloud import firestore
import functions_framework
from datetime import datetime, timezone
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Twitter credentials from .env
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Add logging for debugging
logging.basicConfig(level=logging.INFO)

@functions_framework.http
def post_twitter(request):
    try:
        # Log Twitter credentials existence (not actual values)
        logging.info(f"API Key exists: {bool(TWITTER_API_KEY)}")
        logging.info(f"API Secret exists: {bool(TWITTER_API_SECRET)}")
        logging.info(f"Access Token exists: {bool(TWITTER_ACCESS_TOKEN)}")
        logging.info(f"Access Secret exists: {bool(TWITTER_ACCESS_SECRET)}")
        
        request_json = request.get_json(silent=True) or {}
        tweet_id = request_json.get('tweet_id')
        
        if not tweet_id:
            return {"success": False, "message": "Tweet ID required"}
            
        db = firestore.Client()
        tweets_ref = db.collection('tweets')
        tweet_doc = tweets_ref.document(tweet_id).get()
        
        if not tweet_doc.exists:
            return {"success": False, "message": "Tweet not found"}
            
        tweet_data = tweet_doc.to_dict()
        
        # Initialize Twitter client with error handling
        try:
            client = tweepy.Client(
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_SECRET
            )
            logging.info("Twitter client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Twitter client: {str(e)}")
            return {"success": False, "message": f"Twitter client initialization failed: {str(e)}"}
        
        # Post tweet with error handling
        try:
            response = client.create_tweet(text=tweet_data['content'])
            logging.info(f"Tweet posted successfully: {response.data['id']}")
        except Exception as e:
            logging.error(f"Failed to post tweet: {str(e)}")
            return {"success": False, "message": f"Tweet posting failed: {str(e)}"}
        
        # Update Firestore
        tweets_ref.document(tweet_id).update({
            'twitter_id': response.data['id'],
            'posted_at': datetime.now(timezone.utc),
            'status': 'posted'
        })
        
        return {
            "success": True,
            "twitter_id": response.data['id'],
            "content": tweet_data['content']
        }
        
    except Exception as e:
        logging.error(f"Error in post_twitter: {str(e)}")
        return {"success": False, "message": str(e)}