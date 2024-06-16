import cv2
import numpy as np

# Load the image
image_path = '/content/picture.PNG'
def detect_rectangles(image):

  # Convert the image to grayscale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Apply Gaussian blur
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)

  # Use Canny edge detector
  edges = cv2.Canny(blurred, 50, 150)

  # Find contours
  contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Function to detect if a contour is a rectangle
  def is_rectangle(contour):
      approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
      return len(approx) == 4

  # List to store rectangle bounding boxes and hierarchy levels
  rectangles = []

  # Process each contour
  for contour in contours:
      if is_rectangle(contour):
          x, y, w, h = cv2.boundingRect(contour)
          rectangles.append((x, y, w, h))

  # Sort rectangles by area (smallest to largest)
  rectangles = sorted(rectangles, key=lambda x: x[2] * x[3])

  # Determine nesting levels
  levels = [0] * len(rectangles)
  for i in range(len(rectangles)):
      for j in range(i + 1, len(rectangles)):
          # Check if rectangle i is inside rectangle j
          if (rectangles[i][0] > rectangles[j][0] and
              rectangles[i][1] > rectangles[j][1] and
              rectangles[i][0] + rectangles[i][2] < rectangles[j][0] + rectangles[j][2] and
              rectangles[i][1] + rectangles[i][3] < rectangles[j][1] + rectangles[j][3]):
              levels[i] += 1
  levels = [i//2+1 for i in levels]
  # Draw rectangles and their levels on the image
  for i, (x, y, w, h) in enumerate(rectangles):
      cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(image, str(levels[i]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
  return image


import cv2

# Open the video file or capture device
video_path = 'path_to_your_video.mp4'  # Replace with your video file path
cap = cv2.VideoCapture(0)

# Check if the video capture has been initialized
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Loop through all frames
while True:
    # Read a frame
    ret, frame = cap.read()

    # Break the loop if there are no more frames
    if not ret:
        break
    frame= detect_rectangles(frame)
    # Display the frame
    cv2.imshow('Frame', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
