import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast

################# 変換行列を求める #############
# 画像上の座標
original_points = [[913, 291], [1917, 453], [1514, 1068], [1, 484]]
original_points = np.array(original_points, dtype=np.float32)

# 仮想コートの座標
field_template = cv2.imread("../quvnu_video/field_template.jpg")
height, width = field_template.shape[:2]
corners = [[0, 0], [width/2, 0], [width/2, height], [0, height]]
print(corners)
corners = np.array(corners, dtype=np.float32)

# 変換行列の取得
M = cv2.getPerspectiveTransform(original_points, corners)
np.set_printoptions(precision=5, suppress=True)
print(M)


############## 鳥瞰画像の生成テスト ################

# 元画像
frame_5094 = cv2.imread("../quvnu_video/frame_5094.jpg")
frame_5094 = cv2.cvtColor(frame_5094, cv2.COLOR_BGR2RGB)

# 元画像を射影変換し鳥瞰画像へ
w2, h2 = corners.max(axis=0).astype(int) + 50 # 鳥瞰画像サイズを拡張（見た目の調整） 
transformed_img = cv2.warpPerspective(frame_5094, M, (w2,h2) )

# 結果表示 
fig = plt.figure(figsize=(8,8))
fig.add_subplot(3,1,1).imshow(field_template)
fig.add_subplot(3,1,2).imshow(transformed_img)
fig.add_subplot(3,1,3).imshow(frame_5094)

plt.show()


############# 仮想コート上の攻撃選手位置の推定 ##################

#使用するデータフレーム
#df = pd.read_csv("5094.csv")
df = pd.read_csv("sp_frame_flag.csv")

# 攻撃選手のデータのみ残す
# color_flag列が1の行のみを残す
df = df.loc[df['color_flag'] == 1]

"""
df.to_csv("flag_check.csv", index=False)
print("処理完了")
"""

# frameIndexごとにx, y座標をリストにまとめる
grouped = df.groupby('frameIndex').apply(lambda g: list(zip(g['x'], g['y']))).reset_index()
grouped.columns = ['frameIndex', 'coordinates']
print(grouped)
#grouped.to_csv('grouped.csv', index=False)


# 同じframeIndexの値をもつデータに対して、それぞれのx,y座標をまとめてリスト化
pt = grouped['coordinates'].to_list() # 変換したい座標リスト
print(f'pt is {type(pt)}')
print(pt)


# 描画用イメージ
img3 = field_template.copy()


# 動画ファイルのパス
video_path = "..\quvnu_video\quvnu_ori.mp4"
# 保存先フォルダ
output_folder = "..\quvnu_video\OF_mapped"
# 動画を読み込む
cap = cv2.VideoCapture(video_path)


# 変換と描画を行う関数
def transform_and_draw_coordinates(df, image, M):

    for _, row in df.iterrows():
        coordinates = row['coordinates']
        frameIndex = row['frameIndex']
        # 座標リストを (N, 1, 2) の形に整形し、float32に変換
        points = np.array(coordinates, dtype='float32').reshape(-1, 1, 2)
        
        # 変換行列を適用
        transformed_points = cv2.perspectiveTransform(points, M)

        # 変換後の座標を描画
        for point in transformed_points:
            x, y = point[0]
            # 描画位置の調整、負の座標は描画しない
            if x >= 0 and y >= 0:
                #cv2.circle(image, (int(x), int(y)), radius=5, color=(0, 0, 255), thickness=-1)
                cv2.circle(image, (int(x), int(y)), radius=5, color=[163,83,21], thickness=-1)

        # 描画結果を表示
        # フレーム位置を指定
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
        ret, frame = cap.read()
        if not ret:
            print(f"Frame {frameIndex} could not be read.")
        
        cv2.imshow(f'player posision:{frameIndex}', image)

        # 1つのウィンドウで表示
        cv2.imshow(f'frame {frameIndex}', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        image = field_template.copy()
        # 新しい行をデータフレームに追加

# 各 transformed_coordinates の (x, y) に対してマーカーを描画

# 変換と描画を実行
transform_and_draw_coordinates(grouped, img3, M)



# coordinates 列に座標変換を適用

def transform_coordinates(coords, M):
    # 座標を numpy 配列に変換して適用
    coords_np = np.array(coords, dtype=np.float32).reshape(-1, 1, 2)
    transformed_coords = cv2.perspectiveTransform(coords_np, M)
    # 元のリスト形式に戻す
    return transformed_coords.reshape(-1, 2).astype(np.int32).tolist()

# 新しい列 transformed_coordinates に座標変換を追加
# new_dfを空のデータフレームとして初期化
new_df = pd.DataFrame(columns=['frameIndex', 'transformed_coordinates'])
new_df['frameIndex'] = grouped['frameIndex']
new_df['transformed_coordinates'] = grouped['coordinates'].apply(lambda coords: transform_coordinates(coords, M))


# 条件を満たす要素を削除する関数
def filter_coordinates(coords):
    return [(x, y) for x, y in coords if not (0 < x < 40 and 0 < y < 40)]

# "coordinates"列を更新
new_df["transformed_coordinates"] = new_df["transformed_coordinates"].apply(filter_coordinates)


# CSVとして保存
new_df.to_csv('in_field_OF.csv', index=False)


# 座標を描画する関数
def draw_coordinates_on_image(frame_index, coordinates):
    # 画像コピーを作成
    img_copy = field_template.copy()

    # 座標の描画
    for x, y in coordinates:
        cv2.circle(img_copy, (x, y), radius=5, color=(0, 0, 255), thickness=-1)  # 赤い点を描画

    # 画像にフレーム番号を表示
    cv2.putText(img_copy, f"Frame: {frame_index}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow(f"{frame_index}", img_copy)

"""

# 動画ファイルのパス
video_path = "..\quvnu_video\quvnu_ori.mp4"
# 保存先フォルダ
output_folder = "..\quvnu_video\OF_mapped"
# 動画を読み込む
cap = cv2.VideoCapture(video_path)

# 各frameIndexに対応するフレームに座標を描画
for _, row in df.iterrows():
    frame_index = row['frameIndex']
    coordinates = row['coordinates']

    # フレーム位置を指定
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()

    if not ret:
        print(f"Frame {frame_index} could not be read.")
        continue

    # 座標を描画
    for (x, y) in coordinates:
        cv2.circle(field_template, (int(x), int(y)), radius=5, color=(0, 0, 255), thickness=-1)

    # フレームを保存
    output_path = f"../{output_folder}/frame_{frame_index}.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Frame {frame_index} saved at {output_path}")

cap.release()
cv2.destroyAllWindows()
"""

