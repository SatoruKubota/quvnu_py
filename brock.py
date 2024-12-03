import matplotlib.pyplot as plt
import pandas as pd
import ast

# CSVを読み込む
file_path = "in_field_OF.csv"
df = pd.read_csv(file_path)

# 仮想コートの設定
court_width = 800  # 横の長さ
court_height = 400  # 縦の長さ

# 各フレームのプロットを作成
for index, row in df.iterrows():
    coordinates = ast.literal_eval(row['transformed_coordinates'])  # 文字列をリストに変換
    x_vals = [coord[0] for coord in coordinates]
    y_vals = [coord[1] for coord in coordinates]

    # 新しいプロットを作成
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, court_width)
    ax.set_ylim(0, court_height)
    ax.set_aspect('equal')

    # コートの分割線
    for i in range(1, 4):  # 縦方向（4分割）
        ax.axhline(i * court_height / 4, color='gray', linestyle='--', linewidth=0.5)
    for j in range(1, 8):  # 横方向（8分割）
        ax.axvline(j * court_width / 8, color='gray', linestyle='--', linewidth=0.5)

    # 座標をプロット（左上基準にするため、y軸を反転）
    ax.scatter(x_vals, y_vals, color='blue', label=f"Frame {row['frameIndex']}", s=50)

    # y軸を反転（左上が基準）
    ax.invert_yaxis()

    # タイトルとラベル
    ax.set_title(f"Coordinates on Virtual Court - Frame {row['frameIndex']}")
    ax.set_xlabel("Width")
    ax.set_ylabel("Height")
    ax.legend(loc='upper right', fontsize='small')

    # 描画
    plt.show()
