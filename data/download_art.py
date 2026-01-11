import requests
import os
from PIL import Image
from io import BytesIO
import time

# Configuration
SAVE_FOLDER = "art_gallery"
SEARCH_QUERY = "portrait"
LIMIT = 50

# Create folder if doesn't already exist
def setup_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"Created folder: {SAVE_FOLDER}")

def get_object_ids():
    """Ask The Met for IDs of objects that match 'portrait'"""
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={SEARCH_QUERY}&hasImages=true&medium=Paintings"
    response = requests.get(url)
    data = response.json()
    
    # The API returns a list of IDs
    total = data['total']
    ids = data['objectIDs'][:LIMIT] # Just take the first few
    print(f"Found {total} paintings. Fetching the first {len(ids)}...")
    return ids

def download_image(object_id):
    """Get details for a specific ID and download the image"""
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Get the image URL
        img_url = data.get('primaryImageSmall')
        title = data.get('title', 'Untitled')
        
        if not img_url:
            return
            
        # Download the actual image bytes
        img_response = requests.get(img_url)
        img = Image.open(BytesIO(img_response.content))
        
        # Save it
        filename = f"{SAVE_FOLDER}/{object_id}.jpg"
        img.save(filename)
        print(f"Saved: {title} ({object_id})")
        
    except Exception as e:
        print(f"⚠️ Could not download {object_id}: {e}")

if __name__ == "__main__":
    setup_folder()
    ids = get_object_ids()
    
    print("Starting download sequence:")
    for i, obj_id in enumerate(ids):
        download_image(obj_id)
        time.sleep(0.1) # Add some time for the API so it doesnt overload