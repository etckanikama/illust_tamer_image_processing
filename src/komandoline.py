import sys
import cv2
a = r"C:\Users\hirayama\Desktop\python_test\iOS.jpg"
b = r"C:\Users\hirayama\Desktop\python_test\result.png"
img = cv2.imread(a)

args = sys.argv
print(args)
print('第一引数：'+args[1])
print('第二引数：'+args[2])


# 保存する。
cv2.imwrite(b, img)