import pandas as pd

# CSVファイルを読み込み
#df = pd.read_csv('filtered_points.csv')
df = pd.read_csv('quvnu_points.csv')


#追加
# 各frameIndexの出現回数をカウント
frame_counts = df['frameIndex'].value_counts()

# 出現回数が8回以上のframeIndexを取得
frequent_frame_indices = frame_counts[frame_counts >= 7].index
#frequent_frame_indices = frame_counts.index

# 該当するframeIndexのみをフィルタリング
df_frequent_frames = df[df['frameIndex'].isin(frequent_frame_indices)]

"""
# 結果を表示
print("frameIndexが8回以上出現するフレームのframeIndex:")
print(frequent_frame_indices)
"""

# 更新されたデータフレームを新しいCSVファイルとして保存
#df_frequent_frames.to_csv('filtered_data.csv', index=False)
df_frequent_frames.to_csv('quvnu_data.csv', index=False)

print("新しいCSVファイルが作成されました。")