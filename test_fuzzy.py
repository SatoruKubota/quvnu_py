import numpy as np
import pandas as pd
import ast
from collections import defaultdict

# ファジー所属関数の定義
def membership_function(value, start, peak, end):
    """
    ファジー所属関数を計算
    - value: 評価する値（座標）
    - start: 所属度が0になる開始点
    - peak: 所属度が1になる頂点
    - end: 所属度が0になる終了点
    """
    if value <= start or value >= end:
        return 0.0
    elif start < value < peak:
        return (value - start) / (peak - start)
    elif peak <= value < end:
        return (end - value) / (end - peak)
    else:
        return 0.0

# ブロック定義 (各ブロックはx, yの範囲で定義)
blocks = {
    (0, 0): {"x": [0, 50, 100], "y": [0, 50, 100]},
    (0, 1): {"x": [0, 50, 100], "y": [100, 150, 200]},
    (0, 2): {"x": [0, 50, 100], "y": [200, 250, 300]},
    (0, 3): {"x": [0, 50, 100], "y": [300, 350, 400]},
    (1, 0): {"x": [100, 175, 250], "y": [0, 50, 100]},
    (1, 1): {"x": [100, 175, 250], "y": [100, 150, 200]},
    (1, 2): {"x": [100, 175, 250], "y": [200, 250, 300]},
    (1, 3): {"x": [100, 175, 250], "y": [300, 350, 400]},
    (2, 0): {"x": [250, 325, 400], "y": [0, 100, 200]},
    (2, 1): {"x": [250, 325, 400], "y": [200, 300, 400]}
}

# ファジー所属度で人数を計算する関数
def calculate_fuzzy_block_counts(coordinates):
    block_counts = defaultdict(float)
    for x, y in coordinates:
        for (block_x, block_y), boundaries in blocks.items():
            x_membership = membership_function(x, *boundaries["x"])
            y_membership = membership_function(y, *boundaries["y"])
            # 所属度の積でブロック内のカウントを増加
            block_counts[(block_x, block_y)] += x_membership + y_membership
    return block_counts

# データフレームを読み込み
df = pd.read_csv('in_field_OF.csv')

# 各フレームごとに処理
for index, row in df.iterrows():
    frame_index = row["frameIndex"]
    coordinates = ast.literal_eval(row["transformed_coordinates"])  # 座標をリストに変換

    # ファジー所属度でブロックごとの人数を計算
    block_counts = calculate_fuzzy_block_counts(coordinates)

    # 結果を出力
    print(f"フレーム {frame_index} のファジーブロックごとの人数:")
    for (block_x, block_y), count in sorted(block_counts.items()):
        print(f"  ブロック ({block_x}, {block_y}): {count:.2f} 人")

    # ファジー値によるパターン判定（例として基準パターンを定義）
    pattern_1 = {(0, 1): 1.0, (1, 0): 1.0, (2, 0): 1.0}  # パターンⅠ
    pattern_2 = {(1, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0}  # パターンⅡ

    def fuzzy_match(block_counts, pattern, threshold=0.5):
        return all(abs(block_counts.get(key, -1) - val) <= threshold for key, val in pattern.items())

    if fuzzy_match(block_counts, pattern_1):
        print("パターンⅠ")
    elif fuzzy_match(block_counts, pattern_2):
        print("パターンⅡ")
    else:
        print("その他")

    print()
######