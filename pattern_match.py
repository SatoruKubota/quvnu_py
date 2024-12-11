import pandas as pd
import numpy as np

# patterns: 各パターンの座標
patterns = [
    [(77, 132), (169, 89), (311, 106)],  # Pattern 1
    [(136, 161), (143, 252), (308, 158)],  # Pattern 2
    [(185, 92), (183, 167), (184, 253)]   # Pattern 3
]

# CSVファイルを読み込む
df = pd.read_csv('in_field_OF_best.csv')

# transformed_coordinates列を利用して座標データを取り出す
def parse_coordinates(coords_str):
    return eval(coords_str)  # 文字列をリストに変換

df['coords'] = df['transformed_coordinates'].apply(parse_coordinates)

# 距離を計算し、その距離を基に確率を求める関数
def calculate_probability_for_pattern(coords, pattern, sigma=100):
    probabilities = []
    
    # 各座標がパターン内のどの座標に近いかを計算
    for coord in coords:
        prob_for_coord = []
        for p in pattern:
            # ユークリッド距離を計算
            distance = np.linalg.norm(np.array(coord) - np.array(p))
            # 距離に基づいて確率を計算（小さいほど高確率）
            prob = np.exp(-distance ** 2 / (2 * sigma ** 2))
            prob_for_coord.append(prob)
        
        # 確率の正規化
        total_prob = sum(prob_for_coord)
        normalized_probs = [p / total_prob for p in prob_for_coord]
        probabilities.append(normalized_probs)
    
    return probabilities

def classify_pattern(coords, patterns):
    prob_sums = []
    all_probabilities = []
    
    for pattern in patterns:
        prob = calculate_probability_for_pattern(coords, pattern)
        
        # インデックスの使用済みを追跡するためのセット
        used_indices = set()
        prob_sum = 0

        # 各座標の確率リストから、未使用の最大値を選ぶ
        for coord_probs in prob:
            max_prob = 0
            best_idx = -1  # 初期値として無効なインデックスを設定
            for idx, p in enumerate(coord_probs):
                if idx not in used_indices and p > max_prob:
                    max_prob = p
                    best_idx = idx  # 最大確率を持つインデックスを記録
            if best_idx != -1:  # 有効なインデックスが見つかった場合のみ更新
                prob_sum += max_prob
                used_indices.add(best_idx)  # インデックスを使用済みに登録

        
        prob_sums.append(prob_sum)
        all_probabilities.append(prob)  # 各座標の確率も保持
    
    # 最も確率が大きいパターンを選択
    max_prob_sum_index = np.argmax(prob_sums)
    return prob_sums, all_probabilities, max_prob_sum_index + 1

# 結果を求める
def display_classification_results(row):
    coords = row['coords']  # 各行の座標
    prob_sums, all_probabilities, pattern_number = classify_pattern(coords, patterns)

    # 確率合計をすべて表示（小数第二位まで）
    for i, prob_sum in enumerate(prob_sums, 1):
        print(f"パターン {i} の確率合計: {prob_sum:.2f}")

    # 最も確率が大きいパターンを表示
    print(f"\n座標 {coords} はパターン {pattern_number} に分類されます。")

    # 最も高い確率合計を持つパターンの詳細確率を表示（小数第二位まで）
    selected_probabilities = all_probabilities[pattern_number - 1]  # 選ばれたパターンの詳細確率
    print(f"\nパターン {pattern_number} の座標ごとの確率:")
    for i, prob_for_coord in enumerate(selected_probabilities):
        print(f"座標 {coords[i]} の確率: {', '.join([f'{prob:.2f}' for prob in prob_for_coord])}")

# データフレームの各行に対して結果を表示
for _, row in df.iterrows():
    print(f"\nframeIndex {row['frameIndex']} の結果:")
    display_classification_results(row)
