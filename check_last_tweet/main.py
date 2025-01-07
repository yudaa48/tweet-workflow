from google.cloud import firestore
import functions_framework
from datetime import datetime, timezone, timedelta
import logging

@functions_framework.http
def check_last_tweet(request):
    try:
        db = firestore.Client()
        tweets_ref = db.collection('tweets')
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        
        recent_tweets = tweets_ref.where('created_at', '>', one_hour_ago).limit(1).stream()
        
        can_tweet = not any(recent_tweets)
        
        return {
            "success": True,
            "can_tweet": can_tweet,
            "checked_time": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"success": False, "message": str(e)}