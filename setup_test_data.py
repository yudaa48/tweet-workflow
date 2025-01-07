from google.cloud import firestore
from datetime import datetime, UTC

def setup_test_data():
    db = firestore.Client()
    
    # Add a test word
    words_ref = db.collection('words')
    test_word = {
        'status': 2,
        'created_at': datetime.now(UTC),
        'test': True,
        'word': 'test_word'
    }
    
    try:
        # Add the test document
        word_ref = words_ref.add(test_word)
        print(f"Successfully added test word with ID: {word_ref[1].id}")
        
        # Verify it was added
        doc = words_ref.document(word_ref[1].id).get()
        if doc.exists:
            print("Document successfully verified")
            print(f"Document data: {doc.to_dict()}")
        else:
            print("Document was not created successfully")
            
    except Exception as e:
        print(f"Error setting up test data: {str(e)}")

if __name__ == "__main__":
    setup_test_data()