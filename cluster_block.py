import numpy as np
from collections import defaultdict
import pandas as pd
import ast

# 画像の大きさ
img_width = 800
img_height = 400

# 横方向のブロックの境界（分割範囲）
x_boundaries = [0, 100, 240, 800]

# 縦方向のブロックの境界
y_boundaries_0_240 = [0, 100, 200, 300, 400]  # 横が0~240の範囲
y_boundaries_241_800 = [0, 200, 400]          # 横が241~800の範囲

# 3. 入力データ
coordinates_list = []
in_field_df = pd.read_csv("in_field_player.csv")

# 新しいデータフレームを作成
new_df = pd.DataFrame(columns=["frameIndex", "transformed_coordinates"])

# 各行を処理
for _, row in in_field_df.iterrows():
    try:
        # 文字列のリスト形式をリストに変換
        coordinates = ast.literal_eval(row["transformed_coordinates"])

        # y座標が小さい順に並べ替え
        coordinates_sorted = sorted(coordinates, key=lambda x: x[1])  # x[1]はy座標

        # 並べ替えた座標を新しい行として追加
        new_row = {"frameIndex": row["frameIndex"], "transformed_coordinates": coordinates_sorted}
        new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)
    except Exception as e:
        print(f"Error processing row {row['frameIndex']}: {e}")

# 結果を表示
print(new_df)


# データフレームをループして処理
for _, row in new_df.iterrows():
    try:
        # 文字列のリスト形式をリストに変換
        coordinates = row["transformed_coordinates"]
        coordinates_list.append(coordinates)  # 変換したリストをcoordinates_listに追加
        
    except ValueError as e:
        print(f"変換エラー: {e} (frameIndex: {row['frameIndex']})")
        coordinates_list.append([])  # エラー時には空のリストを追加

# 最後にcoordinates_listが作成される
print(coordinates_list)



# ブロックインデックスを計算する関数
def find_block(x, y):
    # 横方向のブロックインデックス
    if x < x_boundaries[0] or x >= x_boundaries[-1]:
        raise ValueError(f"x座標が範囲外です: {x}")
    block_x = next(i for i in range(len(x_boundaries) - 1) if x_boundaries[i] <= x < x_boundaries[i + 1])
    
    # 縦方向のブロックインデックス
    if block_x < 2:  # x < 240の場合
        y_boundaries = y_boundaries_0_240
    else:  # x >= 240の場合
        y_boundaries = y_boundaries_241_800
    
    if y < y_boundaries[0] or y >= y_boundaries[-1]:
        raise ValueError(f"y座標が範囲外です: {y}")
    block_y = next(i for i in range(len(y_boundaries) - 1) if y_boundaries[i] <= y < y_boundaries[i + 1])
    
    return block_y, block_x

# 各リストごとにブロックごとの人数をカウント
for idx, person_coordinates in enumerate(coordinates_list):
    block_counts = defaultdict(int)  # ブロックごとの人数を格納

    # 各座標についてブロックを特定してカウント
    for x, y in person_coordinates:
        try:
            block = find_block(x, y)
            block_counts[block] += 1
        except ValueError as e:
            print(f"座標 ({x}, {y}) が範囲外のためスキップします: {e}")

    # 出力
    print(f"座標リスト {idx + 1} のブロックごとの人数:")
    for (block_y, block_x), count in sorted(block_counts.items()):
        # block_x をラベルに変換
        block_label = {0: "S", 1: "M", 2: "L"}.get(block_x, "範囲外")
        print(f"  ブロック {block_label}{block_y}: {count} 人")
    print()
