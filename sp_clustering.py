import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd

# CSVファイルからデータフレームを読み込む
df = pd.read_csv('new_dataframe.csv')
# 最初の数行で型を確認
#print(df['transformed_coordinates'].apply(type).head())


# 各coordinatesの要素数を確認
for points in df['transformed_coordinates']:
    points = eval(points)  # 文字列をリストとして評価
    print(len(points))  # 各coordinatesリストの要素数を確認



# 特徴量の計算 (3人間の距離)
features = []
for points in df['transformed_coordinates']:
    points = eval(points)
    (x1, y1), (x2, y2), (x3, y3) = points
    # 3人の間の距離を計算
    d12 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)  # 人1と人2の距離
    d13 = np.sqrt((x3 - x1)**2 + (y3 - y1)**2)  # 人1と人3の距離
    d23 = np.sqrt((x3 - x2)**2 + (y3 - y2)**2)  # 人2と人3の距離
    features.append([d12, d13, d23])

# シルエット分析で最適なクラスタ数を推定
silhouette_scores = []
max_clusters = 7  # 最大クラスタ数を指定
for i in range(2, max_clusters + 1):
    kmeans = KMeans(n_clusters=i, random_state=0).fit(features)
    score = silhouette_score(features, kmeans.labels_)
    silhouette_scores.append(score)

# シルエットスコアのリストを表示して確認
print("シルエットスコア:", silhouette_scores)

# シルエットスコアのグラフをプロット
plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
plt.xlabel("クラスタ数")
plt.ylabel("シルエットスコア")
plt.title("シルエット分析による最適クラスタ数の推定")
plt.show()
