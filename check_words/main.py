from google.cloud import firestore
import functions_framework
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)

@functions_framework.http
def check_words(request):
    try:
        request_json = request.get_json(silent=True) or {}
        check_type = request_json.get('check_type')
        
        db = firestore.Client()
        words_ref = db.collection('words')
        
        status_limits = {'5min': 2, '10min': 3, '3hour': 4}
        status_limit = status_limits.get(check_type)
        
        if not status_limit:
            return {"success": False, "message": f"Invalid check_type: {check_type}"}
            
        query = words_ref.where('status', '<=', status_limit).limit(5)
        
        words_data = []
        for doc in query.stream():
            word = doc.to_dict()
            word['id'] = doc.id
            words_data.append(word)
        
        return {
            "success": True,
            "words": words_data,
            "count": len(words_data),
            "status_limit": status_limit
        }
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"success": False, "message": str(e)}