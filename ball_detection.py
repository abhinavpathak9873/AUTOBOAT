import cv2
import numpy as np

def color_segmentation(frame, lower_bound, upper_bound):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    segmented = cv2.bitwise_and(frame, frame, mask=mask)
    return segmented

def draw_bounding_box(image, color, label, area, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    distance = round((3848.9*(area**(-0.511))/100),2) # function to estimate ball distance
    cv2.putText(image, f"{label} ({distance} m)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Set the lower and upper bounds for yellow, green, and blue in HSV format
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
60
lower_green = np.array([40, 40, 40])
upper_green = np.array([80, 255, 255])

lower_blue = np.array([100, 50, 50])
upper_blue = np.array([140, 255, 255])

# Open the webcam
cap = cv2.VideoCapture(1)

# Set maximum dimensions for the combined frame
max_width = 1000
max_height = 1000

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Resize the frame by reducing the width by a factor of 2
    resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=1)

    # Apply color segmentation for yellow, green, and blue
    yellow_segmented = color_segmentation(resized_frame, lower_yellow, upper_yellow)
    green_segmented = color_segmentation(resized_frame, lower_green, upper_green)
    blue_segmented = color_segmentation(resized_frame, lower_blue, upper_blue)

    # Find contours in the segmented images
    contours_yellow, _ = cv2.findContours(cv2.cvtColor(yellow_segmented, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(cv2.cvtColor(green_segmented, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(cv2.cvtColor(blue_segmented, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes with labels and areas for green, blue, and yellow objects
    detected_frame = resized_frame.copy()

    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area > 1000 and area<45000:
            draw_bounding_box(detected_frame, (0, 255, 0), "Green Ball", area, contour)

    for contour in contours_blue:
        area = cv2.contourArea(contour)
        if area > 1000 and area <45000:
            draw_bounding_box(detected_frame, (255, 0, 0), "Blue Ball", area, contour)

    for contour in contours_yellow:
        area = cv2.contourArea(contour)
        if area > 1000 and area<45000:
            draw_bounding_box(detected_frame, (0, 255, 255), "Yellow Ball", area, contour)

    # Resize the detected frame to fit within the maximum dimensions
    detected_frame = cv2.resize(detected_frame, (max_width, max_height))

    # Combine yellow, green, and blue segmented frames into two rows
    top_row = np.hstack((blue_segmented, green_segmented))
    bottom_row = np.hstack((yellow_segmented, resized_frame))
    combined_frame = np.vstack((top_row, bottom_row))

    # Resize the combined frame to fit within the maximum dimensions
    combined_frame = cv2.resize(combined_frame, (max_width, max_height))

    # Display the frames
    cv2.imshow('Combined', combined_frame)
    cv2.imshow('Detected', detected_frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
