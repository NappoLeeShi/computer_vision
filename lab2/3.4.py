import cv2

img = cv2.imread("./datatest/test.jpg")
if img is None:
    print("No img for 3.4")
    exit()

medBlur = cv2.medianBlur(img, 111)
cv2.imshow("med blur", medBlur)
_ = cv2.waitKey(0)

biFil = cv2.bilateralFilter(img, 75, 75, 75)
cv2.imshow("bi fil", biFil)
_ = cv2.waitKey(0)
