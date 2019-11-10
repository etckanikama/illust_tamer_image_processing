import cv2
import numpy as np

# 画像を読み込む。
img = cv2.imread(r"C:\Users\hirayama\Desktop\python_test\monster1.jpg")

# グレースケールに変換する。
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2値化する。
thresh, binary = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

# 輪郭を抽出する。
contours, hierarchy = cv2.findContours(
    binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# マスクを作成する
mask = np.zeros_like(binary)

# 輪郭内部（透明化しない画素）を255で塗りつぶす。
cv2.drawContours(mask, contours, -1, color=255, thickness=-1)

# RGBAに変換する
rgba = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

# マスクをアルファチャンネルに設定する。
rgba[..., 3] = mask

### 追加したコード

# すべての輪郭を構成する点
all_points = np.concatenate(contours).reshape(-1, 2)

# x, y の最小値、最大値を探す。
xmin, ymin, xmax, ymax = (
    all_points[:, 0].min(),
    all_points[:, 1].min(),
    all_points[:, 0].max(),
    all_points[:, 1].max(),
)
# その範囲でクロップする。
cropped = rgba[ymin:ymax + 1, xmin:xmax + 1]
print(cropped.shape)  # (419, 852, 4)

# 保存する。
cv2.imwrite(r"C:\Users\hirayama\Desktop\python_test\cropped.png", cropped)

# BGR値の取得
print(cropped[200, 200])  # [167 116  55 255]

# 画像の大きさ(px)
h, w = cropped.shape[:2]
print(w, h)  # 624 852

# 表示
cv2.imshow("img", cropped)
cv2.waitKey(0)