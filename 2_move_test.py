#一定時間での人の移動量合計
#移動量の合計が少ないフレームがセットプレーシーンであると判断
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import warnings
import re
# 特定の警告を無視する
warnings.filterwarnings(
    "ignore", 
    category=DeprecationWarning, 
    message=".*DataFrameGroupBy.apply operated on the grouping columns.*"
)



# CSVファイルを読み込み
#df = pd.read_csv('cac.csv')#元データ
df = pd.read_csv('new_data2.csv')#テスト

#df = pd.read_csv('0_4999_coord.csv')#0_5000
#df = pd.read_csv('filtered_points.csv')#コート内
#count_df = pd.read_csv('filtered_data.csv', header=0)#人数フィルタリング
count_df = pd.read_csv('../quvnu_csv/quvnu_data.csv', header=0)#人数フィルタリング



# 列名を確認
print(df.head())
print(df.columns)


# 各person_idの移動距離を計算する関数
def calculate_movement(data):
    #data = data.sort_values(by='frameIndex')
    
    if len(data) < 2:  # データが1行以下の場合、移動距離は0とする
        return 0

    data['dx'] = data['x_projected'].diff().fillna(0)
    data['dy'] = data['y_projected'].diff().fillna(0)
    data['distance'] = np.sqrt(data['dx']**2 + data['dy']**2)
    # 移動距離の合計
    total_distance = data['distance'].sum()


#################　平均移動距離　####################
    """
    # フレーム数
    num_frames = len(data) - 1  # 差分を計算しているため、フレーム数はデータの長さ - 1
    
    # 平均移動距離の計算
    average_distance = total_distance / num_frames if num_frames > 0 else 0

    return average_distance
    """

    return total_distance


# フレーム(30フレームで1秒)ごとの移動距離を計算
frame_window = 30
movement_data = []

# 1行目のframeIndexの値を取得
frame_index_value = int(df.iloc[1]['frameIndex'])

for frame in range(frame_index_value, df['frameIndex'].max() - frame_window + 1, frame_window):
#for frame in range(42000, 45000, frame_window):
    window_data = df[(df['frameIndex'] >= frame) & (df['frameIndex'] < frame + frame_window)]

    if window_data.empty:
        movement_sum = 500
    else:
        # groupby後に必要な列だけを選択する
        grouped_data = window_data.groupby('personId').apply(lambda group: calculate_movement(group))
        movement_sum = grouped_data.sum()
    movement_data.append(movement_sum)




# 連続した一定値以下のカウントと、連続していた値のリスト
count = 0
consecutive_values = []
sp_values = []

# 3回以上一定値以下の値が続いた回数のカウンター
pattern_count = 0

# リストをループして処理
for i in range(len(movement_data)):
    value = movement_data[i]

    if value <= 250:
        # 一定値以下の値の場合、カウントを増やし、値を保存
        count += 1
        consecutive_values.append(value)
    else:
        # 一定値以上の値が出たときに、前の値をチェック
        if count >= 3:
            #print(f"一定値以下の値が3回以上続いた後、{value}が出現しました。続いた値: {consecutive_values}")
            #sp_values.append(consecutive_values[count-1])
            sp_values.append((i-1)*30)

        # カウントと保存した値をリセット
        count = 0
        consecutive_values = []


# 1列目のデータを取得
# CSVの1列目が0インデックスとして読み込まれる
#column_data = count_df.iloc[:, 0].astype(int).tolist()
column_data = count_df["frameIndex"].astype(int).tolist()

# target_values内の値で、1列目に存在するものを抽出
found_values = [value for value in sp_values if value in column_data]
#found_values = [x - 30 for x in found_values]
# 結果を出力
print(f"SP開始フレーム: {found_values}")

# 結果を出力
#print(f"sp候補: {sp_values}")

#見つかった値: 
#[2130, 2580, 8430, 10740, 19470, 22530, 23610, 30150, 33120, 36360, 36870, 39720, 42270, 45570]


# グラフ化
#print(movement_data)
plt.figure(figsize=(10, 6))
plt.plot(movement_data, marker='o')
plt.xlabel('Frame Number')
plt.ylabel('Total Movement Distance')
plt.title('Total Movement Distance in 30-Frame Windows')
plt.grid(True)
plt.show()
