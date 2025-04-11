import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

ret, frame = camera.read()

if ret:
    cv2.imwrite("img.jpg", frame)
else:
    print("Error: Could not read frame.")

camera.release()