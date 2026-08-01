import cv2

# 2. DOC VA HIEN THI HINH ANH
image = cv2.imread("E:\daihoc\daihoc1\computervision\lab\datatest/test.jpg") #path tới ảnh trong datatest 
if image is None:
    print("No image")
    exit()
 
cv2.imshow("Image", image)
_ = cv2.waitKey(0)


# 3. CHUYEN DOI KHONG GIAN MAU
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Image",  gray_image)
_ = cv2.waitKey(0)

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow("HSV Image",  hsv_image)
_ = cv2.waitKey(0)

lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
cv2.imshow("LAB Image",  lab_image)
_ = cv2.waitKey(0)

# 4. CROP
h, w, _ = image.shape
crop_y_end = min(300, h)
crop_x_end = min(400, w)
cropped_image = image[50:crop_y_end, 100:crop_x_end]
cv2.imshow("Cropped Image", cropped_image)
_ = cv2.waitKey(0)

# RATIO
resized_ratio = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
resized_fixed = cv2.resize(image, (300, 400))
cv2.imshow("Ratio", resized_ratio)
cv2.imshow("Fixed", resized_fixed)
_ = cv2.waitKey(0)

# 5. DRAW
drawing_image = image.copy()

_ = cv2.line(drawing_image, (0, 0), (300, 400), (255, 0, 0), 3)
_ = cv2.rectangle(drawing_image, (0, 0), (100, 200), (0, 0, 255), 3)
_ = cv2.circle(drawing_image, (500, 500), 100, (0, 255, 0), -1)
text = "Skibid"
_ = cv2.putText(drawing_image, text, (500, 500), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 2)

cv2.imshow("Drawing Image", drawing_image)
_ = cv2.waitKey(0)

cv2.destroyAllWindows()