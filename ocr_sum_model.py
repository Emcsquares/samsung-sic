# import cv2 
# import pytesseract
# import numpy as np
# from pytesseract import Output
# from transformers import pipeline

# # Image path
# image_pathh = './image/proper.jpg'
# img = cv2.imread(image_pathh)

# # OCR
# extracted_text = pytesseract.image_to_string(img)

# # Summarize
# # Load the summarization pipeline (using TensorFlow)
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
# print("Full text: ")
# print(extracted_text)

# print("Summary:")
# print(summary[0]['summary_text'])

#---------------------------------------------------------------------------------------------------------

# import cv2
# import pytesseract
# from pytesseract import Output
# from transformers import pipeline
# import time

# # Initialize the summarization pipeline
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# # Initialize a set to store processed texts
# processed_texts = set()

# # Function to perform OCR and summarization
# def process_frame(frame):
#     # Perform OCR on the frame
#     extracted_text = pytesseract.image_to_string(frame)
    
#     # Check if the text is readable and not already processed
#     if extracted_text.strip() and extracted_text not in processed_texts:
#         print("New text detected:")
#         print(extracted_text)
        
#         # Add the text to the processed set
#         processed_texts.add(extracted_text)
        
#         # Summarize the text
#         try:
#             summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
#             print("Summary:")
#             print(summary[0]['summary_text'])
#         except Exception as e:
#             print(f"Error during summarization: {e}")
#     else:
#         print("No new readable text detected or text already processed.")

# # Open the camera
# cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# # Set the frame rate to 1 FPS
# fps = 1
# frame_interval = int(1000 / fps)  # Interval in milliseconds

# print("Starting real-time scanning... Press 'q' to quit.")

# while True:
#     # Capture a frame
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to capture frame. Exiting...")
#         break
    
#     # Resize the frame for better OCR performance (optional)
#     frame = cv2.resize(frame, (640, 480))
    
#     # Process the frame
#     process_frame(frame)
    
#     # Display the frame (optional)
#     cv2.imshow("Camera Feed", frame)
    
#     # Wait for the frame interval or until 'q' is pressed
#     if cv2.waitKey(frame_interval) & 0xFF == ord('q'):
#         print("Exiting...")
#         break

# # Release the camera and close OpenCV windows
# cap.release()
# cv2.destroyAllWindows()

#------------------------------------------------------------------------------------------------------------

# import cv2
# import pytesseract
# from pytesseract import Output
# from transformers import pipeline
# import time
# from datetime import datetime
# import numpy as np

# # Initialize the summarization pipeline
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# # Initialize a set to store processed texts
# processed_texts = set()

# # Function to enhance the frame (sharpening and contrast adjustment)
# def enhance_frame(frame):
#     # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Apply a sharpening filter
#     kernel = np.array([[0, -1, 0],
#                        [-1, 5, -1],
#                        [0, -1, 0]])
#     sharpened = cv2.filter2D(gray, -1, kernel)
    
#     # Apply adaptive histogram equalization for better contrast
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     enhanced = clahe.apply(sharpened)
    
#     return enhanced

# # Function to detect motion between frames
# def detect_motion(prev_frame, current_frame):
#     # Compute the absolute difference between frames
#     diff = cv2.absdiff(prev_frame, current_frame)
#     gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
#     motion_score = cv2.countNonZero(thresh)
    
#     # If motion score is high, prompt the user
#     if motion_score > 5000:  # Adjust threshold based on testing
#         print("Motion detected! Please hold the camera steady.")
#         return True
#     return False

# # Function to check if the frame is blurry
# def is_blurry(frame):
#     # Compute the Laplacian variance
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    
#     # If variance is below a threshold, the image is blurry
#     if variance < 100:  # Adjust threshold based on testing
#         print("Frame is blurry! Please hold the camera steady.")
#         return True
#     return False

# # Function to process a frame (OCR and summarization)
# def process_frame(frame):
#     # Start timing the processing
#     start_time = time.time()
    
#     # Perform OCR on the frame
#     extracted_text = pytesseract.image_to_string(frame)
    
#     # Get the current timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     # Check if the text is readable and not already processed
#     if extracted_text.strip() and extracted_text not in processed_texts:
#         print(f"\n[{timestamp}] New text detected:")
#         print(extracted_text)
        
#         # Add the text to the processed set
#         processed_texts.add(extracted_text)
        
#         # Count the number of words in the extracted text
#         word_count = len(extracted_text.split())
        
#         if word_count < 20:
#             # Output the whole text if fewer than 20 words
#             print("Output (less than 20 words):")
#             print(extracted_text)
#         else:
#             # Summarize the text if 20 or more words
#             try:
#                 summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
#                 print("Summary:")
#                 print(summary[0]['summary_text'])
#             except Exception as e:
#                 print(f"Error during summarization: {e}")
#     else:
#         print(f"\n[{timestamp}] No new readable text detected or text already processed.")
#         print("Tip: Hold the camera steady or adjust focus for better results.")
    
#     # End timing the processing
#     end_time = time.time()
#     process_time = end_time - start_time
#     print(f"Processing time: {process_time:.2f} seconds")

# # Open the camera
# cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# # Set the frame rate to 1 FPS
# fps = 1
# frame_interval = int(1000 / fps)  # Interval in milliseconds

# # Set camera resolution (optional)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# print("Starting real-time scanning... Press 'q' to quit.")

# prev_frame = None  # To store the previous frame for motion detection

# while True:
#     # Capture a frame
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to capture frame. Exiting...")
#         break
    
#     # Resize the frame for better OCR performance (optional)
#     frame = cv2.resize(frame, (640, 480))
    
#     # Detect motion (if there is a previous frame)
#     if prev_frame is not None and detect_motion(prev_frame, frame):
#         prev_frame = frame.copy()
#         continue  # Skip processing if motion is detected
    
#     # Check if the frame is blurry
#     if is_blurry(frame):
#         prev_frame = frame.copy()
#         continue  # Skip processing if the frame is blurry
    
#     # Enhance the frame
#     enhanced_frame = enhance_frame(frame)
    
#     # Process the frame (OCR and summarization)
#     process_frame(enhanced_frame)
    
#     # Update the previous frame
#     prev_frame = frame.copy()
    
#     # Display the frame (optional)
#     cv2.imshow("Camera Feed", frame)
    
#     # Wait for the frame interval or until 'q' is pressed
#     if cv2.waitKey(frame_interval) & 0xFF == ord('q'):
#         print("Exiting...")
#         break

# # Release the camera and close OpenCV windows
# cap.release()
# cv2.destroyAllWindows()

#--------------------------------------------------------------------------------------------------

# import cv2
# import pytesseract
# from pytesseract import Output
# from transformers import pipeline
# import time
# from datetime import datetime
# import numpy as np

# # Initialize the summarization pipeline
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# # Initialize a set to store processed texts
# processed_texts = set()

# # Function to enhance the frame (sharpening and contrast adjustment)
# def enhance_frame(frame):
#     # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Apply a sharpening filter
#     kernel = np.array([[0, -1, 0],
#                        [-1, 5, -1],
#                        [0, -1, 0]])
#     sharpened = cv2.filter2D(gray, -1, kernel)
    
#     # Apply adaptive histogram equalization for better contrast
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     enhanced = clahe.apply(sharpened)
    
#     return enhanced

# # Function to detect motion between frames
# def detect_motion(prev_frame, current_frame):
#     # Compute the absolute difference between frames
#     diff = cv2.absdiff(prev_frame, current_frame)
#     gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
#     motion_score = cv2.countNonZero(thresh)
    
#     # If motion score is high, prompt the user
#     if motion_score > 5000:  # Adjust threshold based on testing
#         print("Motion detected! Please hold the camera steady.")
#         return True
#     return False

# # Function to check if the frame is blurry
# def is_blurry(frame):
#     # Compute the Laplacian variance
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    
#     # If variance is below a threshold, the image is blurry
#     if variance < 100:  # Adjust threshold based on testing
#         print("Frame is blurry! Please hold the camera steady.")
#         return True
#     return False

# # Function to process a frame (OCR and summarization)
# def process_frame(frame):
#     # Start timing the processing
#     start_time = time.time()
    
#     # Perform OCR on the frame and get detailed data
#     ocr_data = pytesseract.image_to_data(frame, output_type=Output.DICT)
    
#     # Extract text and confidence scores
#     extracted_text = " ".join([ocr_data['text'][i] for i in range(len(ocr_data['text'])) if int(ocr_data['conf'][i]) > 50])  # Only include words with confidence > 50
#     confidence_scores = [int(ocr_data['conf'][i]) for i in range(len(ocr_data['text'])) if int(ocr_data['conf'][i]) > 50]
    
#     # Calculate the mean confidence score
#     mean_confidence = np.mean(confidence_scores) if confidence_scores else 0
    
#     # Get the current timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     # Check if the text is readable and not already processed
#     if extracted_text.strip() and extracted_text not in processed_texts:
#         print(f"\n[{timestamp}] New text detected:")
#         print(f"Extracted Text: {extracted_text}")
#         print(f"Mean Confidence Score: {mean_confidence:.2f}")
        
#         # Add the text to the processed set
#         processed_texts.add(extracted_text)
        
#         # Count the number of words in the extracted text
#         word_count = len(extracted_text.split())
        
#         if word_count < 20:
#             # Output the whole text if fewer than 20 words
#             print("Output (less than 20 words):")
#             print(extracted_text)
#         else:
#             # Summarize the text if 20 or more words
#             try:
#                 summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
#                 print("Summary:")
#                 print(summary[0]['summary_text'])
#             except Exception as e:
#                 print(f"Error during summarization: {e}")
#     else:
#         print(f"\n[{timestamp}] No new readable text detected or text already processed.")
#         print("Tip: Hold the camera steady or adjust focus for better results.")
    
#     # End timing the processing
#     end_time = time.time()
#     process_time = end_time - start_time
#     print(f"Processing time: {process_time:.2f} seconds")

# # Open the camera
# # cap = cv2.VideoCapture(0)
# # esp_url = "http://192.168.162.69" 
# # esp_cam = esp_url + ":81/stream"

# esp_cam="http://10.16.37.104:4747/video"
# cap = cv2.VideoCapture(esp_cam)

# # Set the frame rate to 1 FPS
# fps = 1
# frame_interval = int(1000 / fps)  # Interval in milliseconds

# # Set camera resolution (optional)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# print("Starting real-time scanning... Press 'q' to quit.")

# prev_frame = None  # To store the previous frame for motion detection

# while True:
#     # Capture a frame
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to capture frame. Exiting...")
#         break
    
#     # Resize the frame for better OCR performance (optional)
#     frame = cv2.resize(frame, (640, 480))
    
#     # Detect motion (if there is a previous frame)
#     if prev_frame is not None and detect_motion(prev_frame, frame):
#         prev_frame = frame.copy()
#         continue  # Skip processing if motion is detected
    
#     # Check if the frame is blurry
#     if is_blurry(frame):
#         prev_frame = frame.copy()
#         continue  # Skip processing if the frame is blurry
    
#     # Enhance the frame
#     enhanced_frame = enhance_frame(frame)
    
#     # Process the frame (OCR and summarization)
#     process_frame(enhanced_frame)
    
#     # Update the previous frame
#     prev_frame = frame.copy()
    
#     # Display the frame (optional)
#     cv2.imshow("Camera Feed", frame)
    
#     # Wait for the frame interval or until 'q' is pressed
#     if cv2.waitKey(frame_interval) & 0xFF == ord('q'):
#         print("Exiting...")
#         break

# # Release the camera and close OpenCV windows
# cap.release()
# # cv2.destroyAllWindows()

#---------------------------------------------------------------------------------------------------------------

# import cv2
# import pytesseract
# from transformers import pipeline

# # ESP camera URL
# esp_cam = "http://10.16.37.104:4747/video"

# # Initialize the summarization pipeline
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# # Store previously read texts
# read_texts = set()

# # Function to process text
# def process_text(text):
#     # Check if the text has already been read
#     if text in read_texts:
#         return None

#     # Add the text to the set of read texts
#     read_texts.add(text)

#     # Check the length of the text
#     word_count = len(text.split())
#     if word_count <= 20:
#         return text  # No need to summarize
#     else:
#         # Summarize the text
#         summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
#         return summary[0]['summary_text']

# # Start video capture
# cap = cv2.VideoCapture(esp_cam)

# if not cap.isOpened():
#     print("Error: Unable to open video stream.")
#     exit()

# print("Starting video capture...")

# try:
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Unable to read frame.")
#             break

#         # Display the video feed
#         cv2.imshow("Video Feed", frame)

#         # Crop the frame to exclude metadata overlay
#         # Adjust the cropping coordinates based on your video feed
#         height, width, _ = frame.shape
#         cropped_frame = frame[int(height * 0.2):, :]  # Crop the top 20% of the frame

#         # Perform OCR on the cropped frame
#         extracted_text = pytesseract.image_to_string(cropped_frame)

#         # Process the extracted text
#         if extracted_text.strip():  # Check if text is not empty
#             result = process_text(extracted_text.strip())
#             if result:
#                 print("Full text:")
#                 print(extracted_text.strip())
#                 print("Processed result:")
#                 print(result)

#         # Check for user input to quit
#         if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
#             break

# except KeyboardInterrupt:
#     print("Video capture stopped by user.")

# finally:
#     # Release the video capture object and close all OpenCV windows
#     cap.release()
#     cv2.destroyAllWindows()
#     print("Video capture ended.")

#---------------------------------------------------------------------------------------------------------

import cv2
import pytesseract
from transformers import pipeline
import time

# ESP camera URL
esp_cam = "http://10.16.37.104:4747/video"

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# Store previously read texts
read_texts = set()

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
            result = process_text(extracted_text.strip())
            if result:
                print("Full text:")
                print(extracted_text.strip())
                print("Processed result:")
                print(result)

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


