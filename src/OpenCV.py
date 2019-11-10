import cv2
import sys
import numpy as np
import statistics

# 画像を読み込む。
halfimg = cv2.imread(r"C:\Users\hirayama\Desktop\python_test\monster1.jpg")

# コマンドライン引数
'''
args = sys.argv
print(args)
print('第一引数：'+args[1])
print('第二引数：'+args[2])
'''

orgHeight, orgWidth = halfimg.shape[:2]
size = (int(orgWidth/10), int(orgHeight/10))
img = cv2.resize(halfimg, size)

# グレースケールに変換する。
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2値化する。
thresh, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)

# 輪郭を抽出する。
contours, hierarchy = cv2.findContours(
    binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
# ノイズを除去
filter_contours = []
average = max(map(cv2.contourArea,contours))
for cnt2 in contours:
    area = cv2.contourArea(cnt2)
    if area < average:
        continue
    filter_contours.append(cnt2)
#print(filter_contours)

# マスクを作成する
mask = np.zeros_like(binary)

# 輪郭内部（透明化しない画素）を255で塗りつぶす。
for cnt in filter_contours:
    cv2.drawContours(mask, filter_contours, -1, color=255, thickness=-1)

# RGBAに変換する
rgba = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

# マスクをアルファチャンネルに設定する。
rgba[..., 3] = mask


# すべての輪郭を描画
#cv2.drawContours(img, contours, -1, color=(0, 255, 0), thickness=2)

# 保存する。
cv2.imwrite(r"C:\Users\hirayama\Desktop\python_test\result.png", rgba)




# 画像サイズ
height, width, channels = rgba.shape[:3]
R_sum = 0
G_sum = 0
B_sum = 0
a255_sum = 0
a0_sum = 0
Color_rgba = 0
gray_sum = 0
for w in range(width):
    for h in range(height):
        #print(rgba[h][w])

        if rgba[h][w][3] == 255:
            R_sum += rgba[h][w][2]
            G_sum += rgba[h][w][1]
            B_sum += rgba[h][w][0]
            a255_sum += 1
            gray_sum += gray[h][w]

        else:
            a0_sum += 1



# 明るさの平均
print('明るさの平均'+str(int(gray_sum/a255_sum/255*100)))
# 合計のpx
total_rgb = R_sum + G_sum + B_sum
print('R:{}'.format(int(R_sum/total_rgb*100)))
print('G:{}'.format(int(G_sum/total_rgb*100)))
print('B:{}'.format(int(B_sum/total_rgb*100)))
# 全体に対する画像のpx
all_px = a255_sum + a0_sum
print('全体に対する画像のpx:{}'.format(int(a255_sum/all_px*100)))

# 重心を求める
# 各輪郭の重心を計算する。

for i, cnt in enumerate(filter_contours):
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        print(f"contour {i}: ({cx}, {cy})")


# 表示
cv2.imshow("img", rgba)
cv2.waitKey(0)

