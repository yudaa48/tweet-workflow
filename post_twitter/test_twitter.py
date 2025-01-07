import tweepy
from dotenv import load_dotenv
import os
import logging
from datetime import datetime, timezone
from google.cloud import firestore

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

def test_twitter_credentials():
    """Test if Twitter credentials are working"""
    try:
        client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
        )
        
        # Try to get account info to verify credentials
        me = client.get_me()
        logging.info(f"Successfully authenticated as: {me.data.username}")
        return True
        
    except Exception as e:
        logging.error(f"Twitter authentication failed: {str(e)}")
        return False

def test_firestore_connection():
    """Test Firestore connection and add a test tweet"""
    try:
        db = firestore.Client()
        tweets_ref = db.collection('tweets')
        
        # Add a test tweet
        test_tweet = {
            'content': 'This is a test tweet from our vocabulary bot! #test',
            'status': 'pending',
            'created_at': datetime.now(timezone.utc)
        }
        
        tweet_ref = tweets_ref.document()
        tweet_ref.set(test_tweet)
        
        logging.info(f"Successfully added test tweet with ID: {tweet_ref.id}")
        return tweet_ref.id
        
    except Exception as e:
        logging.error(f"Firestore operation failed: {str(e)}")
        return None

def test_post_tweet():
    """Test posting a tweet"""
    try:
        client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
        )
        
        # Create a test tweet
        response = client.create_tweet(text="Testing our vocabulary bot! 📚 #test")
        logging.info(f"Successfully posted test tweet with ID: {response.data['id']}")
        return True
        
    except Exception as e:
        logging.error(f"Tweet posting failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n=== Testing Twitter Bot Components ===\n")
    
    print("1. Testing Twitter Credentials...")
    if test_twitter_credentials():
        print("✅ Twitter credentials are valid\n")
    else:
        print("❌ Twitter credentials test failed\n")
    
    print("2. Testing Firestore Connection...")
    tweet_id = test_firestore_connection()
    if tweet_id:
        print(f"✅ Successfully connected to Firestore and created test tweet: {tweet_id}\n")
    else:
        print("❌ Firestore test failed\n")
    
    print("3. Testing Tweet Posting...")
    if test_post_tweet():
        print("✅ Successfully posted test tweet\n")
    else:
        print("❌ Tweet posting test failed\n")

if __name__ == "__main__":
    main()