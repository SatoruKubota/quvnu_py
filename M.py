import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
frame_5094 = cv2.imread("frame_5094.jpg")
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


############# 仮想コート上の選手位置の推定 ##################

#使用するデータフレーム
#df = pd.read_csv("5094.csv")
df = pd.read_csv("..\quvnu_csv\sp_frame_flag.csv")

# frameIndexごとにx, y座標をリストにまとめる
grouped = df.groupby('frameIndex').apply(lambda g: list(zip(g['x'], g['y']))).reset_index()
grouped.columns = ['frameIndex', 'coordinates']
print(grouped)
# 同じframeIndexの値をもつデータに対して、それぞれのx,y座標をまとめてリスト化
pt = grouped['coordinates'].to_list() # 変換したい座標リスト
print(f'pt is {type(pt)}')
print(pt)



"""
# それぞれの座標をMで変換
def apply_perspective_transform(coordinates, M):
    # 座標リストを numpy 配列に変換 (N, 1, 2) の形にする
    points = np.array(coordinates, dtype='float32').reshape(-1, 1, 2)
    
    # 変換行列 M を適用
    transformed_points = cv2.perspectiveTransform(points, M)
    
    # 変換後の座標をリスト形式に変換して返す
    transformed_coordinates = [(point[0][0], point[0][1]) for point in transformed_points]
    
    return transformed_coordinates

transformed_coordinates = apply_perspective_transform(pt, M)
print("変換後の座標:", transformed_coordinates)


for (x, y) in transformed_coordinates:
    cv2.circle(img3, (int(x), int(y)), radius=5, color=(255, 0, 0), thickness=-1)
    """

img3 = field_template.copy()

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
                cv2.circle(image, (int(x), int(y)), radius=5, color=(0, 0, 255), thickness=-1)
        # 描画結果を表示
        cv2.imshow(f'player posision:{frameIndex}', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        image = field_template.copy()
# 各 transformed_coordinates の (x, y) に対してマーカーを描画

# 変換と描画を実行
transform_and_draw_coordinates(grouped, img3, M)


"""
# 描画結果を表示
cv2.imshow("Image with Markers", img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""


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




"""
#################### test ###############

# 座標を元画像に描画
for coordinates_list in pt:
    # coordinates_list から座標ペア (x, y) を取得
    for coordinates in coordinates_list:
        # (x, y) 座標を取得
        x, y = coordinates
        cv2.circle(frame_5094, (int(x), int(y)), radius=5, color=(0, 0, 255), thickness=-1)

# 描画結果を表示
cv2.imshow("Image with Points", frame_5094)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""

