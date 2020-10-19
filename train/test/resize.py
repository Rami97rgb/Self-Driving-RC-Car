import cv2


#resize images to display them in the corner in case of a detection
img = cv2.imread('sign_3.jpg')
img = cv2.resize(img, (32,32))
cv2.imwrite('sign_0.jpg',img)
    
img1 = cv2.imread('sign_4.jpg')
img1 = cv2.resize(img1, (32,32))
cv2.imwrite('sign_1.jpg',img1)
