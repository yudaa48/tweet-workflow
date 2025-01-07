# Test Individual Functions

## 1. Check Words Function
```bash
# Test 5-minute check
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"check_type": "5min"}' \
  [FUNCTION_URL]

# Test 10-minute check
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"check_type": "10min"}' \
  [FUNCTION_URL]

# Test 3-hour check
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"check_type": "3hour"}' \
  [FUNCTION_URL]
```

## 2. Check Last Tweet Function
```bash
# Check if we can tweet
curl -X POST \
  -H "Content-Type: application/json" \
  [FUNCTION_URL]
```

## 3. Create Tweet Function
```bash
# Create tweet with sample word
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "words": [{
      "word": "serendipity",
      "definition": "finding something good without looking for it",
      "example": "Finding a $20 bill in an old coat was pure serendipity."
    }],
    "check_type": "5min"
  }' \
  [FUNCTION_URL]
```

## 4. Post Twitter Function
```bash
# Post tweet using tweet_id
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "tweet_id": "YOUR_TWEET_ID"
  }' \
  [FUNCTION_URL]
```

## 5. Complete Workflow Test
```bash
# Test complete workflow
gcloud workflows execute tweet-workflow \
    --data='{"CHECK_TYPE": "5min"}' \
    --location=us-central1

# Test workflow with different intervals
gcloud workflows execute tweet-workflow \
    --data='{"CHECK_TYPE": "10min"}' \
    --location=us-central1

gcloud workflows execute tweet-workflow \
    --data='{"CHECK_TYPE": "3hour"}' \
    --location=us-central1
```

## Check Results and Logs

### View Function Logs
```bash
# Check words function logs
gcloud functions logs read check_words --limit=10

# Check last tweet function logs
gcloud functions logs read check_last_tweet --limit=10

# Create tweet function logs
gcloud functions logs read create_tweet --limit=10

# Post twitter function logs
gcloud functions logs read post_twitter --limit=10
```

### View Workflow Executions
```bash
# List recent workflow executions
gcloud workflows executions list tweet-workflow --location=us-central1

# Get details of specific execution
gcloud workflows executions describe EXECUTION_ID \
    --workflow=tweet-workflow \
    --location=us-central1
```

### Check Firestore Data
```bash
# Using Firebase console:
1. Go to Firebase Console
2. Select your project
3. Navigate to Firestore
4. Check 'words' and 'tweets' collections
```

## Expected Responses

### Check Words Response
```json
{
    "success": true,
    "words": [
        {
            "word": "example_word",
            "definition": "example definition",
            "example": "example usage",
            "status": 2
        }
    ],
    "count": 1
}
```

### Check Last Tweet Response
```json
{
    "success": true,
    "can_tweet": true,
    "checked_time": "2025-01-07T04:28:31.723256+00:00"
}
```

### Create Tweet Response
```json
{
    "success": true,
    "tweet_id": "generated_id",
    "content": "📚 Word: example\n📖 Definition\n✏️ Example usage"
}
```

### Post Twitter Response
```json
{
    "success": true,
    "twitter_id": "twitter_post_id",
    "content": "tweet content"
}
```