import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

# CSVファイルを読み込み
df = pd.read_csv('cac.csv')

# frameIndexの範囲を指定して抽出（例えば、frameIndexが3から6の範囲）
start_frame = 0
#end_frame = 4999
end_frame = df['frameIndex'].iloc[-1]

# 条件に合う行を抽出
# 新しいyの列を計算
###############  y座標が足になるように  ######################
df['y'] = df['y'] + df['height']
df['x'] = df['x'] + df['width'] / 2
df_filtered = df[(df['frameIndex'] >= start_frame) & (df['frameIndex'] <= end_frame)]

# 結果を表示
print(df_filtered)

# フィルタリング結果をCSVファイルに出力
#output_path = f'{start_frame}_{end_frame}_coord.csv'
output_path = f'quvnu_coord.csv'

df_filtered.to_csv(output_path, index=False)