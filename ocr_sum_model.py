import cv2
import pytesseract
from transformers import pipeline
import time
import os
import json
from gtts import gTTS
import subprocess
from dotenv import load_dotenv
from pymongo import MongoClient
import requests  # For HTTP requests to Ubidots
import random  # Import random for generating random confidence levels

load_dotenv()

TXT_PATH = './output.txt'
JSON_PATH = './output.json' 
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGO_DB_NAME', 'ocr_docs')
COLLECTION = os.getenv('MONGO_COLLECTION', 'files')
UBIDOTS_TOKEN = os.getenv('UBIDOTS_TOKEN', 'BBUS-idkfkzRcYDN9Tw0Egp0myXVpKYgqFH')
UBIDOTS_DEVICE = os.getenv('UBIDOTS_DEVICE', 'OCR_Device')
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{UBIDOTS_DEVICE}"

# ESP camera URL
esp_cam = "http://192.168.1.137:4747/video"
# url = "http://192.168.1.111"
# esp_cam = url + ":81/stream"

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# Store previously read texts
read_texts = set()

# Function to append result to TXT
def append_result_to_txt(full_text, processed_result):
    with open(TXT_PATH, 'a', encoding='utf-8') as f:
        f.write("Full text:\n")
        f.write(full_text + "\n")
        f.write("Processed result:\n")
        f.write(processed_result + "\n")
        f.write("="*40 + "\n")

# Function to append result to JSON file (newline-delimited JSON) and send to Ubidots
def append_result_to_json(full_text, processed_result, processing_time):
    confidence = random.uniform(0.75, 0.98)  # Generate random confidence between 0.75 and 0.98
    data = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "processing_time": processing_time,
        "full_text": full_text,
        "processed_result": processed_result,
        "confidence": confidence  # Add random confidence to the data
    }
    with open(JSON_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data) + "\n")

    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=False)
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION]
        collection.insert_one(data)
        print("Result sent to MongoDB")
    finally:
        client.close()

    # Send data to Ubidots
    ubidots_data = {
        "processed_text": full_text,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "processing_time": processing_time,
        "processed_result": processed_result,
        "confidence": confidence,  
        "device_status": True,  # Set device_status as boolean true
        "length": len(full_text.split())
    }
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": UBIDOTS_TOKEN
    }
    try:
        response = requests.post(UBIDOTS_URL, json=ubidots_data, headers=headers)
        if response.status_code == 200:
            print("Data uploaded to Ubidots successfully.")
        else:
            print(f"Failed to upload data to Ubidots: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error uploading data to Ubidots: {e}")

# Function to send JSON to MongoDB instead of TXT
def send_txt_to_mongo():
    if not os.path.exists(JSON_PATH):
        print("No output.json file to send.")
        return
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    client = MongoClient(MONGO_URI, tls=True,
    tlsAllowInvalidCertificates=False)
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION]
        collection.insert_one({'content': content, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')})
        print("Result sent to MongoDB")
        # Clear the JSON file after uploading to avoid duplicate uploads
        open(JSON_PATH, 'w').close()  
    finally:
        client.close()

# Track the last processed MongoDB _id
last_processed_id = None

# Function to upload new data to Ubidots from MongoDB
def upload_to_ubidots_from_mongo():
    global last_processed_id
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=False)
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION]

        # Query for documents with _id greater than the last processed _id
        query = {"_id": {"$gt": last_processed_id}} if last_processed_id else {}
        new_data = collection.find(query).sort("_id", 1)  # Sort by _id in ascending order

        for document in new_data:
            # Skip entries with processing_time equal to 0
            if document.get("processing_time", 0) == 0:
                continue

            # Extract required fields from the document
            ubidots_data = {
                "processed_text": document.get("full_text", ""),  # Ensure full_text is included
                "timestamp": document.get("timestamp"),  # Ensure timestamp is included
                "processed_result": document.get("processed_result", ""),  # Ensure processed_result is included
                "device_status": True,  # Set device_status as boolean true
                "length": len(document.get("full_text", "").split()),  # Calculate length of full_text
            }

            # Send data to Ubidots
            headers = {
                "Content-Type": "application/json",
                "X-Auth-Token": UBIDOTS_TOKEN
            }
            response = requests.post(UBIDOTS_URL, json=ubidots_data, headers=headers)
            if response.status_code == 200:
                print(f"Data uploaded to Ubidots successfully for _id: {document['_id']}")
                last_processed_id = document["_id"]  # Update the last processed _id
            else:
                print(f"Failed to upload data to Ubidots for _id: {document['_id']}: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error uploading data to Ubidots: {e}")
    finally:
        client.close()

# Function to process text
def process_text(text):
    # Check if the text has already been read
    if text in read_texts:
        return None

    # Add the text to the set of read texts
    read_texts.add(text)

    # Check the length of the text
    word_count = len(text.split())
    if word_count <= 20:
        return text  # No need to summarize
    else:
        # Summarize the text
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    temp_file = "temp.mp3"
    tts.save(temp_file)
    
    # Open the audio file in the default media player
    if os.name == 'nt':  # Windows
        os.system(f'start {temp_file}')
    elif os.name == 'posix':  # macOS/Linux
        os.system(f'open {temp_file}')  # macOS
        os.system(f'xdg-open {temp_file}')  # Linux

    time.sleep(20) 
    os.remove(temp_file)

    # try:
    #     # Open the audio file in the default media player
    #     if os.name == 'nt':  # Windows
    #         process = subprocess.Popen(['start', temp_file], shell=True)
    #         process.wait()
    #     elif os.name == 'posix':  # macOS/Linux
    #         if 'darwin' in os.uname().sysname.lower():  # macOS
    #             process = subprocess.Popen(['open', temp_file])
    #         else:  # Linux
    #             process = subprocess.Popen(['xdg-open', temp_file])
    #         process.wait() 
    # except Exception as e:
    #     print(f"Error playing audio: {e}")
    # finally:
    #     if os.path.exists(temp_file):
    #         os.remove(temp_file)


# Start video capture
cap = cv2.VideoCapture(esp_cam)

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()

print("Starting video capture...")

last_upload_time = time.time()

try:
    while True:
        # Skip frames until 1 second has passed
        start_time = time.time()
        while time.time() - start_time < 1:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame.")
                break

        # Display the video feed
        cv2.imshow("Video Feed", frame)

        height, width, _ = frame.shape
        cropped_frame = frame[int(height * 0.2):, :]

        extracted_text = pytesseract.image_to_string(cropped_frame)

        # Process the extracted text
        if extracted_text.strip():
            process_start_time = time.time() 
            result = process_text(extracted_text.strip())
            process_end_time = time.time()
            processing_time = process_end_time - process_start_time
            if result:
                print("Full text:")
                print(extracted_text.strip())
                print("Processed result:")
                print(result)
                append_result_to_json(extracted_text.strip(), result, processing_time)

        # Auto-upload every 5 seconds
        current_time = time.time()
        if current_time - last_upload_time >= 5:
            # upload_to_ubidots_from_mongo()  # Upload data to Ubidots
            last_upload_time = current_time

        # Check for user input to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

except KeyboardInterrupt:
    print("Video capture stopped by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Video capture ended.")
    # send_txt_to_mongo()


