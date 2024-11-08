import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

# CSVファイルを読み込み
#df = pd.read_csv('0_4999_coord.csv')
df = pd.read_csv('quvnu_coord.csv')
#df = df.drop(0)

# 列名を確認
print(df.head())
print(df.columns)


# 4点の座標を指定
points = [(1, 480),(912, 294), (1918, 453) , (1517, 1068)]

# ポリゴンを作成
polygon = Polygon(points)

# ポリゴン内のデータを保持するフィルタリング関数
###############     ピッチ内の選手のみカウント   ##################
def is_inside_polygon(row, polygon):
    point = Point(row['x'], row['y'])
    return polygon.contains(point)

# データフレームをフィルタリング
df_filtered = df[df.apply(is_inside_polygon, axis=1, args=(polygon,))]

# フィルタリング結果をCSVファイルに出力
#output_path = 'filtered_points.csv'
output_path = 'quvnu_points.csv'

df_filtered.to_csv(output_path, index=False)

print(f'Filtered data saved to {output_path}')