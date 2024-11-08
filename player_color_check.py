import concurrent.futures
import cv2
import pandas as pd
import numpy as np
import time

start_time = time.time()


# CSVファイルの読み込み
df = pd.read_csv("quvnu_sp_frame.csv")
# 使用するcsvファイルの下準備、frameIndexの調整
df_color = df
fps_correct = 1.998001998001998 ############# 変更する必要あり ##########
df_color['frameIndex'] = df_color['frameIndex'] * fps_correct
df_color['frameIndex'] = df_color['frameIndex'].astype(int)
df_color['y'] = df_color['y'] - df_color['height']
df_color['x'] = df_color['x'] - (df_color['width'] / 2)
df_color.to_csv('sp_frame_coord_adjust.csv', index=False)

# 動画ファイルのパス
video_path = "quvnu_ori.mp4"
cap = cv2.VideoCapture(video_path)

# 青色の閾値 (HSV色空間)
lower_blue = np.array([100, 150, 0])
upper_blue = np.array([140, 255, 255])

# 結果を保存するリスト
color_flags = []

fps_correct = 1.998001998001998 


# 各フレームに対して処理
for index, row in df_color.iterrows():
    frame_index = row['frameIndex']
    person_id = row['personId']
    x = int(row['x'])
    y = int(row['y'])
    width = int(row['width'])
    height = int(row['height'])

    # 動画の指定したフレームにシーク
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    if not ret:
        print(f"Frame {frame_index} not found.")
        color_flags.append("エラー")  # エラー時のフラグ
        continue
    else:
        # bounding_box上半分に青色があるか判定
        upper_half_box = frame[y:y + height // 2, x:x + width]

        # BGRからHSVに変換
        hsv = cv2.cvtColor(upper_half_box, cv2.COLOR_BGR2HSV)
        
        # 青色範囲のマスクを作成
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # マスク内のピクセルをチェックし、青色が含まれているか確認
        if np.any(mask > 0):
            color_flags.append(1)  # 青色あり
            print(1)
        else:
            color_flags.append(0)  # 青色なし
            print(0)
cap.release()



"""
# 並列処理でフレーム処理を実行
with concurrent.futures.ThreadPoolExecutor() as executor:
    color_flags = list(executor.map(process_frame, [row for _, row in df.iterrows()]))
"""

# 結果を保存
df_color['color_flag'] = color_flags
df_color.to_csv("sp_frame_with_color_flag.csv", index=False)
print("処理完了")


end_time = time.time()
print(f"処理時間: {end_time - start_time}秒")