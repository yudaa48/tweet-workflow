from google.cloud import firestore
from datetime import datetime, timezone, timedelta

def validate_scheduler_results():
    db = firestore.Client()
    
    # Get current time
    now = datetime.now(timezone.utc)
    one_hour_ago = now - timedelta(hours=1)
    
    print("=== Checking Recent Tweets ===")
    tweets_ref = db.collection('tweets')
    recent_tweets = tweets_ref.where('created_at', '>', one_hour_ago).stream()
    
    for tweet in recent_tweets:
        tweet_data = tweet.to_dict()
        print(f"\nTweet ID: {tweet.id}")
        print(f"Content: {tweet_data.get('content')}")
        print(f"Created At: {tweet_data.get('created_at')}")
        print(f"Check Type: {tweet_data.get('check_type')}")
        print(f"Word ID: {tweet_data.get('word_id')}")
        print("-" * 50)
    
    print("\n=== Checking Words Status ===")
    words_ref = db.collection('words')
    words = words_ref.stream()
    
    status_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for word in words:
        word_data = word.to_dict()
        status = word_data.get('status', 0)
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nWord Status Distribution:")
    for status, count in status_counts.items():
        print(f"Status {status}: {count} words")

if __name__ == "__main__":
    validate_scheduler_results()