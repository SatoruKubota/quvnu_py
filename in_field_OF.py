import pandas as pd

# sp_frame_flag.csvを読み込む
sp_frame_flag_df = pd.read_csv("sp_frame_flag.csv")

# 必要な行を抽出して、新しいコピーを作成
filtered_df = sp_frame_flag_df[sp_frame_flag_df['color_flag'] == 1].copy()

# coord列を作成（x_projectedとy_projectedをタプルとして格納）
filtered_df['coord'] = list(zip(filtered_df['x_projected'].astype(int), filtered_df['y_projected'].astype(int)))

# 不要な列を削除
columns_to_drop = ['personId', 'x', 'y', 'width', 'height', 'confidence', 'color_flag', 'x_projected', 'y_projected']
filtered_df.drop(columns=columns_to_drop, inplace=True)

# frameIndexごとにcoordをリスト化してまとめる
grouped_df = (
    filtered_df.groupby("frameIndex")
    .agg({'coord': list})  # coord列をリストとしてまとめる
    .reset_index()         # インデックスをリセットして元の形式に戻す
)

# 結果を新しいCSVファイルとして保存
grouped_df.to_csv("in_field_OF.csv", index=False)