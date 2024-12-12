import concurrent.futures
import cv2
import pandas as pd
import numpy as np
import time

start_time = time.time()


# CSVファイルの読み込み
df = pd.read_csv("new_data2.csv")
# 使用するframeの絞り込み
frameIndex_list = [2100, 2550, 8340, 10680, 16890, 19380, 23550, 33210, 36810, 45510]
# frameIndex列が指定リストの値と一致する行のみを抽出
df = df[df['frameIndex'].isin(frameIndex_list)]

# 使用するcsvファイルの下準備、frameIndexの調整
df_color = df.copy()
fps_correct = 1.998001998001998 ############# 変更する必要あり ##########
df_color['frameIndex'] = df_color['frameIndex'] * fps_correct
df_color['frameIndex'] = df_color['frameIndex'].astype(int)
df_color['y'] = df_color['y'] - df_color['height']
df_color['x'] = df_color['x'] - (df_color['width'] / 2)
#df_color.to_csv('../quvnu_csv/sp_frame_upper_left.csv', index=False)
# sp_frame_coord_adjust.csvはboundingboxの上半分を切り取るため

# 動画ファイルのパス
video_path = "../quvnu_video/quvnu_ori.mp4"
cap = cv2.VideoCapture(video_path)


################## クリック位置の色を取得 #####################
# 画像ファイルのパスを指定
image_path = "../quvnu_video/frame_5094.jpg"

# 画像を読み込む
image = cv2.imread(image_path)
image = cv2.GaussianBlur(image, (15, 15), 0)

# グローバル変数を使用して色を保持
color_hsv = None


# ウィンドウを先に作成する
cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)

# マウスクリックイベント時に呼び出される関数
def get_color_on_click(event, x, y, flags, param):
    global color_hsv  # グローバル変数を使用することを宣言
    if event == cv2.EVENT_LBUTTONDOWN:  # 左クリックが押されたとき
        # クリックした位置の色 (BGR)
        color_bgr = image[y, x]
        # BGRからHSVに変換
        color_hsv = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        # 色情報を表示
        print(f"クリック位置: ({x}, {y}), 色 (HSV): {color_hsv}")

# setMouseCallbackを呼び出してマウスイベントを設定する
cv2.setMouseCallback("Image", get_color_on_click)

# 画像を表示し、ユーザーが「q」を押すまで待機
while True:
    cv2.imshow("Image", image)  # 画像を表示
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ウィンドウを閉じる
cv2.destroyAllWindows()

# グローバル変数に保存された色を使用
print(f"最終的に取得した色: {color_hsv}")


# HSV から BGR に変換
color_bgr = cv2.cvtColor(np.uint8([[color_hsv]]), cv2.COLOR_HSV2BGR)[0][0]
print(color_bgr)

# 色を画像で表示
color_checker = np.zeros((100, 100, 3), dtype=np.uint8)
color_checker[:, :] = color_bgr

cv2.imshow("Color", color_checker)
cv2.waitKey(0)
cv2.destroyAllWindows()


######################## 閾値の設定 #########################
# 青色の閾値 (HSV色空間)
lower_bound = np.array([max(color_hsv[0]-10 , 0), max(color_hsv[1] - 40, 0), max(color_hsv[2] - 40, 0)])
upper_bound = np.array([min(color_hsv[0]+10 , 179), min(color_hsv[1] + 40, 255), min(color_hsv[2] + 40, 255)])


# 結果を保存するリスト
color_flags = []
color_ratios = []

# 各フレームに対して処理
for index, row in df_color.iterrows():
    frame_index = row['frameIndex']
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
        #upper_half_box = cv2.GaussianBlur(upper_half_box, (25, 25), 0)

        # BGRからHSVに変換
        upper_half_box_hsv = cv2.cvtColor(upper_half_box, cv2.COLOR_BGR2HSV)
        
        # 青色範囲のマスクを作成
        mask = cv2.inRange(upper_half_box_hsv, lower_bound, upper_bound)
        
        # マスク内のピクセルをチェックし、青色が含まれているか確認
        if np.sum(mask > 0) > 15:
            color_flags.append(1)  # 青色あり
            #print(1)
        else:
            color_flags.append(0)  # 青色なし
            #print(0)
        
        # 範囲内のピクセル数と全ピクセル数
        matching_pixels = np.count_nonzero(mask)
        total_pixels = upper_half_box.size // 3  # RGBの3チャンネル分を除く

        # 範囲内の割合を計算
        percentage = (matching_pixels / total_pixels) * 100
        color_ratios.append(percentage)  # percentage を color_ratios に記録

cap.release()



"""
# 並列処理でフレーム処理を実行
with concurrent.futures.ThreadPoolExecutor() as executor:
    color_flags = list(executor.map(process_frame, [row for _, row in df.iterrows()]))
"""

# 結果を保存
df['frameIndex'] = (df['frameIndex'] * fps_correct).astype(int)
df['color_flag'] = color_flags
df['color_ratio'] = color_ratios

df.to_csv("sp_frame_flag.csv", index=False)
#df.to_csv("../quvnu_csv/sp_frame_flag.csv", index=False)
print("処理完了")


end_time = time.time()
print(f"処理時間: {end_time - start_time}秒")