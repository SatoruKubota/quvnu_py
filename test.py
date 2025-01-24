import pandas as pd
import ast
import matplotlib.pyplot as plt
import cv2

# データフレームの作成
data = {
    "frameIndex": [4195, 5094, 21338, 38721, 47052, 73546],
    "coords": [
        "[(144, 224), (152, 212), (345, 255)]",
        "[(175, 92), (385, 121), (25, 155)]",
        "[(171, 226), (144, 173), (336, 194)]",
        "[(109, 144), (362, 146), (214, 123)]",
        "[(128, 156), (167, 231), (325, 240)]",
        "[(385, 99), (175, 95), (110, 131)]",
    ]
}
df = pd.DataFrame(data)

# coords列をリストに変換
df["coords"] = df["coords"].apply(ast.literal_eval)

# 各フレームごとに描画
for index, row in df.iterrows():
    frame_index = row["frameIndex"]
    coords = row["coords"]

    # 座標の分解
    x_coords, y_coords = zip(*coords)

    # 描画
    plt.figure()
    plt.scatter(x_coords, y_coords, color="blue")
    plt.title(f"Frame: {frame_index}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

field_template = cv2.imread("../quvnu_video/field_template.jpg")
height, width, channels = field_template.shape
print(height,width)