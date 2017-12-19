import cv2, numpy as np

# Load and display the original image
img = cv2.imread("test.jpg")

# Create the basic black image 
mask = np.zeros(img.shape, dtype = "uint8")
cv2.namedWindow("keypoints", cv2.WINDOW_NORMAL)
cv2.resizeWindow("keypoints", 600, 400)
r = cv2.selectROI('keypoints', img, True)
print(r)
# Draw a white, filled rectangle on the mask image
x1 = r[0]
y1 = r[1]
x2 = x1 + r[2]
y2 = y1 + r[3]
mask_color = cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)
mask_color = cv2.cvtColor(mask_color,cv2.COLOR_BGR2GRAY)
res = cv2.bitwise_and(img,img,mask = mask_color)

# Display constructed mask
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Mask", 600, 400)
cv2.imshow("Mask", mask)

cv2.namedWindow("Res", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Res", 600, 400)
cv2.imshow("Res", res)

cv2.waitKey(0)