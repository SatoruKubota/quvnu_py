import numpy as np
from random import sample
import pandas as pd
import ast

# 1. 重心の計算
def calculate_centroid(points):
    # 必要な座標数だけ取り出す（2つ、3つ、またはそれ以上）
    x_c = np.mean([x for (x, y) in points])
    y_c = np.mean([y for (x, y) in points])
    return (x_c, y_c)


# 2. 重心からの相対座標を計算
def calculate_relative_coordinates(points, centroid):
    return [(x - centroid[0], y - centroid[1]) for x, y in points]

# 3. k-meansの手動実装
def k_means_custom(features, k):
    """k-means のクラスタリングを手動で実装"""
    # 初期の重心をランダムに選択
    centroids = sample(features, k)
    prev_labels = [-1] * len(features)
    
    while True:
        labels = []
        
        # 各特徴量を最も近いクラスタに割り当て
        for feature in features:
            distances = [np.linalg.norm(np.array(feature) - np.array(centroid)) for centroid in centroids]
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


# 4. 各画像の相対座標を計算
relative_coordinates_list = []
for points in coordinates_list:
    centroid = calculate_centroid(points)
    relative_coordinates = calculate_relative_coordinates(points, centroid)
    relative_coordinates_list.append(relative_coordinates)

# 5. k-meansを使用してクラスタリング
# 相対座標のリストを特徴量として渡す
labels, centroids = k_means_custom(relative_coordinates_list, 3)

# 結果を表示
print("クラスタリング結果:", labels)
print("クラスタの重心:", centroids)
