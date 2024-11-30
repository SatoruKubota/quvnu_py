import numpy as np
import matplotlib.pyplot as plt

# 画像の大きさ
img_width = 800
img_height = 400

# 横方向のブロックの境界（分割範囲）
x_boundaries = [0, 100, 240, 800]

# 縦方向のブロックの境界
y_boundaries_0_240 = [0, 100, 200, 300, 400]  # 横が0~240の範囲
y_boundaries_241_800 = [0, 200, 400]          # 横が241~800の範囲

# 各人の座標 (x, y) のリスト
person_coordinates = [(50, 50), (120, 150), (200, 350), (300, 250), (600, 100), (700, 350)]

# 描画の準備
fig, ax = plt.subplots(figsize=(10, 5))

# 背景を設定（画像サイズ）
ax.set_xlim(0, img_width)
ax.set_ylim(0, img_height)
ax.invert_yaxis()  # 画像の原点を左上に揃える
ax.set_aspect('equal', adjustable='box')  # アスペクト比を維持

# 横方向の境界線を描画
for i in range(len(x_boundaries) - 1):
    x_start = x_boundaries[i]
    x_end = x_boundaries[i + 1]
    if x_start < 240:  # 横幅が 0〜240 の範囲
        for y in y_boundaries_0_240:
            ax.plot([x_start, x_end], [y, y], color="blue", linestyle="--", linewidth=0.8)
    else:  # 横幅が 241〜800 の範囲
        for y in y_boundaries_241_800:
            ax.plot([x_start, x_end], [y, y], color="blue", linestyle="--", linewidth=0.8)

# 縦方向の境界線を描画
for x in x_boundaries:
    if x < 240:  # 横が 0〜240 の範囲
        ax.plot([x, x], [0, img_height], color="red", linestyle="--", linewidth=0.8)
    else:  # 横が 241〜800 の範囲
        for y_start, y_end in zip(y_boundaries_241_800[:-1], y_boundaries_241_800[1:]):
            ax.plot([x, x], [y_start, y_end], color="red", linestyle="--", linewidth=0.8)

# 各座標点を描画
for x, y in person_coordinates:
    ax.plot(x, y, 'o', color='green', label="Person" if 'Person' not in ax.get_legend_handles_labels()[1] else "")

# ラベルと凡例を追加
ax.set_title("Block Boundaries with Points")
ax.set_xlabel("Width (pixels)")
ax.set_ylabel("Height (pixels)")
ax.legend(loc="upper right")

# プロットの表示
plt.show()
