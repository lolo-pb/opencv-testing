import cv2

image = cv2.imread("example-micrography.png")
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
