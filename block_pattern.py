import numpy as np
import pandas as pd
import ast
import itertools

# ブロックの中心座標を定義
blocks = {
    (0, 0): (50, 50),
    (0, 1): (50, 150),
    (0, 2): (50, 250),
    (0, 3): (50, 350),
    (1, 0): (150, 50),
    (1, 1): (150, 150),
    (1, 2): (150, 250),
    (1, 3): (150, 350),
    (2, 0): (250, 50),
    (2, 1): (250, 150),
    (2, 2): (250, 250),
    (2, 3): (250, 350),
    (3, 0): (350, 50),
    (3, 1): (350, 150),
    (3, 2): (350, 250),
    (3, 3): (350, 350),
}

# 距離に基づく確率を計算
def calculate_block_probabilities(x, y, blocks, sigma=50):
    probabilities = {}
    for block, (center_x, center_y) in blocks.items():
        distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        probabilities[block] = np.exp(-distance ** 2 / (2 * sigma ** 2))
    
    # 正規化
    total = sum(probabilities.values())
    for block in probabilities:
        probabilities[block] /= total
    
    # 上位4つを保持
    top_4 = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)[:4]
    return top_4

# パターンを定義
pattern_1 = {(0, 1): 1.0, (1, 0): 1.0, (3, 1): 1.0}  # パターンⅠ
pattern_2 = {(1, 1): 1.0, (1, 2): 1.0, (3, 1): 1.0}  # パターンⅡ
pattern_3 = {(2, 0): 1.0, (2, 1): 1.0, (2, 2): 1.0}  # パターンⅢ

def check_pattern_combinations(all_probabilities, pattern):
    """
    指定されたパターンを作れるか確認し、確率の合計を返す
    - all_probabilities: 各人の上位4つのブロック [(block, prob), ...] のリスト（3人分）
    - pattern: 指定パターン {block: expected_prob}
    """
    # すべてのブロックの組み合わせを生成
    combinations = itertools.product(*all_probabilities)
    
    best_combination_prob_sum = 0
    for combination in combinations:
        blocks_in_combination = {block for block, prob in combination}
        if blocks_in_combination == set(pattern.keys()):
            prob_sum = sum(prob for block, prob in combination if block in pattern)
            best_combination_prob_sum = max(best_combination_prob_sum, prob_sum)
    
    return best_combination_prob_sum

# データフレームを読み込み
df = pd.read_csv('in_field_OF.csv')

# 各フレームごとに処理
for index, row in df.iterrows():
    frame_index = row["frameIndex"]
    coordinates = ast.literal_eval(row["transformed_coordinates"])  # 座標をリストに変換

    print(f"フレーム {frame_index}:")

    # 各人のブロック確率データを保持
    all_probabilities = []
    
    for person_idx, (x, y) in enumerate(coordinates):
        probabilities = calculate_block_probabilities(x, y, blocks)
        all_probabilities.append(probabilities)
        print(f"  人 {person_idx + 1} の上位4ブロック所属確率:")
        for block, prob in probabilities:
            print(f"    ブロック {block}: {prob:.2f}")

    # パターンごとの確率合計を確認
    prob_sum_1 = check_pattern_combinations(all_probabilities, pattern_1)
    prob_sum_2 = check_pattern_combinations(all_probabilities, pattern_2)
    prob_sum_3 = check_pattern_combinations(all_probabilities, pattern_3)

    # 確率値に対応するパターン名を定義
    patterns = {
    "Pattern 1": prob_sum_1,
    "Pattern 2": prob_sum_2,
    "Pattern 3": prob_sum_3,
    }
    # 最大値を持つパターンを取得
    max_pattern = max(patterns, key=patterns.get)
    max_value = patterns[max_pattern]
    """
    # 結果を出力
    if prob_sum_1 == 0 and prob_sum_2 == 0:
        print("  -> どちらのパターンも作成できません")
    elif prob_sum_1 >= prob_sum_2:
        print(f"  -> パターンⅠ が作成可能です (確率合計: {prob_sum_1:.2f})")
    else:
        print(f"  -> パターンⅡ が作成可能です (確率合計: {prob_sum_2:.2f})")
    print()
    """
    # 結果を出力
    if max_value >= 1.15:
        # 結果を表示
        print(f"{max_pattern} (値: {max_value})")
    elif max_value < 1.15:
        print(f"パターンを判別できません (値：{max_value})")
    print()