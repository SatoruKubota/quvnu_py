import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルを読み込む（ファイルパスを適宜変更してください）
df = pd.read_csv('filtered_data.csv')


# frameIndexの出現回数をカウント
frame_counts = df['frameIndex'].value_counts().sort_index()

# frameIndexの出現回数をカウント
frame_counts = df['frameIndex'].value_counts().sort_index()
print(f"型は{type(frame_counts)}")

# グラフ化
plt.figure(figsize=(10, 6))
plt.bar(frame_counts.index, frame_counts.values, color='skyblue')
plt.title('Count of each frameIndex')
plt.xlabel('frameIndex')
plt.ylabel('Count')
plt.xticks(rotation=90)  # 横軸のラベルを見やすくするために回転
plt.tight_layout()  # レイアウト調整
plt.show()

"""
# カウント結果をCSVファイルに出力
output_path = 'human_counts.csv'
frame_counts.to_csv(output_path, index=False)
"""