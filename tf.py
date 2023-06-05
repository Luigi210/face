import cv2
from deepface import DeepFace
import face_recognition as fc


# Open the default camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

square_start, square_end = (440, 100), (840, 650)

square_x = square_start[0]
square_y = square_start[1]

square_width = square_end[0] - square_x
square_height = square_end[1] - square_y

while True:
    # Read a new frame from the camera
    ret, img = cap.read()
    mirrored_img = cv2.flip(img, 1)

    # Display the resulting frame
    DeepFace.stream('deleted', model_name='Facenet')

    # Wait for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

# arch -arm64 python3
# python3-intel64