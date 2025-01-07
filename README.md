# Automated Twitter Vocabulary Bot

A Cloud-based system that automatically posts vocabulary words to Twitter at specified intervals. The system maintains a word database with different status levels and ensures proper tweet timing to avoid spamming.

## Features

### Word Management
- Maintains vocabulary words with different status levels (1-4)
- Automatically selects words based on status and timing
- Uses Gemini AI to generate new vocabulary words
- Tracks word usage and last tweet times

### Tweet Scheduling
- Three different check intervals:
  - Every 5 minutes for words with status ≤ 2
  - Every 10 minutes for words with status ≤ 3
  - Every hour for words with status ≤ 4
- Rate limiting: Ensures 1-hour gap between tweets
- Queue system for tweet management

### Tweet Format
- Word with definition
- Example usage
- Emojis for better readability
- Automatic formatting and posting

## Tech Stack

### Google Cloud Platform
- Cloud Functions (Python 3.9)
- Cloud Workflows
- Cloud Scheduler
- Firestore Database

### APIs & Libraries
- Twitter API (via tweepy)
- Google Gemini AI API
- Python Libraries:
  - tweepy
  - google-cloud-firestore
  - google-generativeai
  - python-dotenv

## Project Structure

```
Workflows/
├── check_words/
│   ├── main.py
│   └── requirements.txt
├── check_last_tweet/
│   ├── main.py
│   └── requirements.txt
├── create_tweet/
│   ├── main.py
│   └── requirements.txt
├── post_twitter/
│   ├── main.py
│   └── requirements.txt
└── workflow.yaml
```

## Setup & Deployment

### Prerequisites
1. Google Cloud Platform account
2. Twitter Developer Account
3. Twitter API credentials
4. Google Cloud CLI installed

### Environment Setup
1. Create `.env` file with Twitter credentials:
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

### Deploy Cloud Functions

```bash
# Deploy check_words function
gcloud functions deploy check_words \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --source check_words

# Deploy check_last_tweet function
gcloud functions deploy check_last_tweet \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --source check_last_tweet

# Deploy create_tweet function
gcloud functions deploy create_tweet \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --source create_tweet

# Deploy post_twitter function
gcloud functions deploy post_twitter \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --source post_twitter
```

### Deploy Workflow
```bash
gcloud workflows deploy tweet-workflow \
    --source=workflow.yaml \
    --location=us-central1
```

## Testing

### Test Individual Functions
```bash
# Test check_words
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"check_type": "5min"}' \
  [CHECK_WORDS_FUNCTION_URL]

# Test workflow
gcloud workflows execute tweet-workflow \
    --data='{"CHECK_TYPE": "5min"}' \
    --location=us-central1
```

## Usage

### Manual Execution
```bash
gcloud workflows execute tweet-workflow \
    --data='{"CHECK_TYPE": "5min"}' \
    --location=us-central1
```

### Automated Scheduling
Set up Cloud Scheduler jobs for automated execution:
```bash
gcloud scheduler jobs create http tweet-5min \
    --schedule="*/5 * * * *" \
    --uri=[WORKFLOW_URL] \
    --message-body='{"CHECK_TYPE":"5min"}' \
    --location=us-central1
```

## Monitoring

### View Logs
```bash
# View function logs
gcloud functions logs read [FUNCTION_NAME]

# View workflow executions
gcloud workflows executions list tweet-workflow
```

## Error Handling
- Comprehensive error checking at each step
- Detailed logging for troubleshooting
- Multiple end states for different scenarios
- Clear error messages and status reporting

## Security
- Environment variables for sensitive data
- Authentication for API endpoints
- Rate limiting to prevent spam
- Secure credential management

## Future Enhancements
- Add more word categories
- Implement hashtag management
- Add analytics for tweet performance
- Enhance word generation with more context
- Add support for images or media

## Contributing
Feel free to submit issues and enhancement requests.

## License
[MIT License](LICENSE)