import cv2
import numpy as np

backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2, cv2.CAP_ANY]

for backend in backends:
    cap = cv2.VideoCapture(0, backend)
    if cap.isOpened():
        print(f"Używany backend: {backend}")
        break
else:
    print("Nie udało się otworzyć kamery za pomocą dostępnych backendów.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się odczytać ramki z kamery.")
        break

    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    green_lower = np.array([40, 70, 70], np.uint8)
    green_upper = np.array([80, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    blue_lower = np.array([90, 100, 100], np.uint8)
    blue_upper = np.array([130, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    yellow_lower = np.array([15, 100, 100], np.uint8)
    yellow_upper = np.array([35, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    kernel = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    green_mask = cv2.dilate(green_mask, kernel)
    res_green = cv2.bitwise_and(frame, frame, mask=green_mask)

    blue_mask = cv2.dilate(blue_mask, kernel)
    res_blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    yellow_mask = cv2.dilate(yellow_mask, kernel)
    res_yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

    contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(frame, "Yellow Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255))

    cv2.imshow("Multiple Color Detection in Real-Time", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
