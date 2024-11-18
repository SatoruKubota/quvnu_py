import numpy as np
import math
from random import sample
import pandas as pd
import ast

# 1. 特徴量計算関数
def calculate_features(points):
    """3人の座標から形状特徴量（辺の長さと内角）を計算"""
    # 座標を取り出す
    (x1, y1), (x2, y2), (x3, y3) = points
    
    # 辺の長さ
    a = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)  # 辺a
    b = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)  # 辺b
    c = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # 辺c
    
    # 内角を計算
    angle1 = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))  # ∠1
    angle2 = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))  # ∠2
    angle3 = 180.0 - angle1 - angle2  # ∠3


    # 特徴量ベクトルを返す
    return [angle1, angle2, angle3]

# 2. クラスタリング関数
def k_means_custom(features, k):
    """k-means のクラスタリングを手動で実装"""
    # 初期の重心をランダムに選択
    centroids = sample(features, k)
    prev_labels = [-1] * len(features)
    
    while True:
        labels = []
        
        # 各特徴量を最も近いクラスタに割り当て
        for feature in features:
            distances = [np.linalg.norm(np.array(feature) - np.array(centroid)
                                        ) for centroid in centroids]
            labels.append(np.argmin(distances))  # 最小距離のクラスタ番号
        
        # ラベルが変わらなければ終了
        if labels == prev_labels:
            break
        prev_labels = labels
        
        # 新しい重心を計算
        for i in range(k):
            cluster_points = [features[j] for j in range(len(features)) if labels[j] == i]
            if cluster_points:
                centroids[i] = np.mean(cluster_points, axis=0)
    
    return labels, centroids

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

# 4. 特徴量計算
features = [calculate_features(points) for points in coordinates_list]

# 5. クラスタリング（クラスタ数を3に設定）
k = 2
labels, centroids = k_means_custom(features, k)

# 結果を表示
print("クラスタラベル:", labels)
print("クラスタ重心:", centroids)
