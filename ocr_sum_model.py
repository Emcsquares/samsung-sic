import cv2
import pytesseract
from transformers import pipeline
import time
import os
import json  # added for JSON support

# Add dotenv for environment variable loading
from dotenv import load_dotenv

# Add pymongo for MongoDB integration
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

TXT_PATH = './output.txt'
JSON_PATH = './output.json'  # added JSON output path
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGO_DB_NAME', 'ocr_docs')
COLLECTION = os.getenv('MONGO_COLLECTION', 'files')

# ESP camera URL
esp_cam = "http://192.168.130.70:4747/video"

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

# New function to append result to JSON file (newline-delimited JSON)
def append_result_to_json(full_text, processed_result, processing_time):
    data = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "processing_time": processing_time,
        "full_text": full_text,
        "processed_result": processed_result
    }
    with open(JSON_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data) + "\n")

    client = MongoClient(MONGO_URI, tls=True,
    tlsAllowInvalidCertificates=False)
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION]
        collection.insert_one(data)
        print("Result sent to MongoDB")
        # Clear the JSON file after uploading to avoid duplicate uploads
        open(JSON_PATH, 'w').close()  
    finally:
        client.close()

# Function to send JSON to MongoDB instead of TXT
# def send_txt_to_mongo():
#     if not os.path.exists(JSON_PATH):
#         print("No output.json file to send.")
#         return
#     with open(JSON_PATH, 'r', encoding='utf-8') as f:
#         content = f.read()
#     client = MongoClient(MONGO_URI, tls=True,
#     tlsAllowInvalidCertificates=False)
#     try:
#         db = client[DB_NAME]
#         collection = db[COLLECTION]
#         collection.insert_one({'content': content, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')})
#         print("Result sent to MongoDB")
#         # Clear the JSON file after uploading to avoid duplicate uploads
#         open(JSON_PATH, 'w').close()  
#     finally:
#         client.close()

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

        # Crop the frame to exclude metadata overlay
        # Adjust the cropping coordinates based on your video feed
        height, width, _ = frame.shape
        cropped_frame = frame[int(height * 0.2):, :]  # Crop the top 20% of the frame

        # Perform OCR on the cropped frame
        extracted_text = pytesseract.image_to_string(cropped_frame)

        # Process the extracted text
        if extracted_text.strip():
            process_start_time = time.time()  # start processing time measurement
            result = process_text(extracted_text.strip())
            process_end_time = time.time()
            processing_time = process_end_time - process_start_time
            if result:
                print("Full text:")
                print(extracted_text.strip())
                print("Processed result:")
                print(result)
                # Save to JSON file
                append_result_to_json(extracted_text.strip(), result, processing_time)

        # Auto-upload every 5 seconds
        current_time = time.time()
        if current_time - last_upload_time >= 5:
            # send_txt_to_mongo()
            last_upload_time = current_time

        # Check for user input to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

except KeyboardInterrupt:
    print("Video capture stopped by user.")

finally:
    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("Video capture ended.")
    # Optionally, send one last upload at the end
    # send_txt_to_mongo()


