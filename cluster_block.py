import numpy as np
import pandas as pd
from collections import defaultdict
import ast  # 文字列をリストに変換するため

# データフレームの準備
df = pd.read_csv('in_field_OF.csv')

# 画像のサイズ
img_width = 800
img_height = 400

# ブロックの境界
x_boundaries = [0, 100, 240, 800]
y_boundaries_0_240 = [0, 100, 200, 300, 400]
y_boundaries_241_800 = [0, 200, 400]

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
    
    return block_x, block_y

# 各フレームごとに処理
for index, row in df.iterrows():
    frame_index = row["frameIndex"]
    # 座標リストを文字列からリストに変換
    coordinates = ast.literal_eval(row["transformed_coordinates"])
    
    block_counts = defaultdict(int)
    
    # 各座標についてブロックを特定してカウント
    for x, y in coordinates:
        try:
            block = find_block(x, y)
            block_counts[block] += 1
        except ValueError as e:
            print(f"座標 ({x}, {y}) が範囲外のためスキップします: {e}")

    # 出力
    #print(f"座標リスト {index + 1} のブロックごとの人数:")

    # ブロックごとの人数をリスト化してソート
    sorted_blocks = sorted(block_counts.items())

    # パターンを判定（順番を無視してセットで比較）
    pattern_1 = {((0, 1), 1), ((1, 0), 1), ((2, 0), 1)}
    pattern_2 = {((1, 1), 1), ((1, 2), 1), ((2, 0), 1)}
    pattern_22 = {((1, 1), 1), ((1, 2), 1), ((2, 1), 1)}

    if set(sorted_blocks) == pattern_1:
        print("パターンⅠ")
    elif set(sorted_blocks) == pattern_2:
        print("パターンⅡ")
    elif set(sorted_blocks) == pattern_22:
        print("パターンⅡ 逆サイド")
    else:
        print("その他")

    # ブロックごとの人数を出力
    print(f"座標リスト {index + 1} のブロックごとの人数:")

    for (block_x, block_y), count in sorted_blocks:
        block_label = {0: "S", 1: "M", 2: "L"}.get(block_x, "範囲外")
        print(f"  {block_label}{block_y}: {count} 人")
    print()