import pandas as pd
import ast

# CSVファイルの読み込み
input_csv = "new_data2.csv"  # 入力ファイル名を指定
output_csv = "output_with_coords.csv"  # 出力ファイル名を指定

# CSVの読み込み
df = pd.read_csv(input_csv)

# x, y 列を (x, y) タプルに変換してリスト化
coord_data = (
    df.groupby("frameIndex", group_keys=False)  # group_keys=False を追加
    .apply(lambda group: list(zip(group["x_projected"], group["y_projected"])))
    .reset_index(name="coord")
)

#print(type(coord_data["coord"].iloc[0]))
# coord列の文字列をリストに変換
#coord_data["coord"] = coord_data["coord"].apply(ast.literal_eval)

# 重心を計算
def calculate_centroid(coords):
    x_coords = [x for x, y in coords]
    y_coords = [y for x, y in coords]
    centroid_x = sum(x_coords) / len(x_coords)
    centroid_y = sum(y_coords) / len(y_coords)
    return (centroid_x, centroid_y)

coord_data["centroid"] = coord_data["coord"].apply(calculate_centroid)


# 新しいDataFrameを作成
output_df = coord_data

# CSVファイルとして保存
output_df.to_csv(output_csv, index=False)

print(f"新しいCSVファイルが作成されました: {output_csv}")


# frameIndexのリストを指定
#frame_indexes = [1740, 2130, 2580, 8370, 9510, 10710, 19410, 22530, 23580, 36360, 36840, 39780, 44820, 45540, 47130]
frame_indexes = [1710, 2100, 2550, 6360, 7410, 8340, 9480, 10680, 16890, 19380, 22500, 23550, 33210, 36330, 36810, 39750, 41580, 42000, 42330, 44790, 45510, 47100]

# 指定したframeIndexのcentroidを出力
for frame_index in frame_indexes:
    centroid = coord_data[coord_data['frameIndex'] == frame_index]['centroid'].values
    centroid
    if centroid.size > 0:
        print(f"frameIndex {frame_index}: {centroid[0]}")
    else:
        print(f"frameIndex {frame_index}のデータが見つかりませんでした")

# 指定されたframeIndexに基づいてフィルタリング
filtered_df = coord_data[coord_data['frameIndex'].isin(frame_indexes)][['frameIndex', 'coord', 'centroid']]
# centroid列のx座標を条件にフィルタリング
filtered_df = filtered_df[filtered_df["centroid"].apply(lambda c: c[0] <= 150)]

# right_base 列を追加
filtered_df["right_base"] = filtered_df["centroid"].apply(lambda c: 1 if c[1] < 200 else 0)

# 必要であれば新しいCSVファイルとして保存
filtered_df.to_csv('ck_frame.csv', index=False)

column_as_list = filtered_df["frameIndex"].tolist()
print(column_as_list)