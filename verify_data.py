from google.cloud import firestore

def verify_data():
    db = firestore.Client()
    
    # Check words collection
    print("=== Checking Words Collection ===")
    words_ref = db.collection('words')
    words = words_ref.where('status', '<=', 2).stream()  # This matches our 5min check logic
    
    for word in words:
        print(f"Found word document:")
        print(f"ID: {word.id}")
        print(f"Data: {word.to_dict()}")
        print("---")

if __name__ == "__main__":
    verify_data()