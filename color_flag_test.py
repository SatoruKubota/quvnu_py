import cv2
import pandas as pd
import numpy as np

df = pd.read_csv("sp_frame_flag.csv")
# 動画ファイルのパス
video_path = "../quvnu_video/quvnu_ori.mp4"
cap = cv2.VideoCapture(video_path)

# フレームごとに color_flag が 1 の選手の bounding box を表示
for frame_index, group in df.groupby('frameIndex'):
    # color_flag == 1 の行をフィルタリング
    selected_players = group[group['color_flag'] == 1]

    # フレームの取得
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    if not ret:
        print(f"Frame {frame_index} not found.")
        continue

    # bounding box を描画
    for _, row in selected_players.iterrows():
        x, y, width, height = int(row['x']-row['width']/2), int(row['y']-row['height']), int(row['width']), int(row['height']/2)
        # Bounding box の描画 (緑の枠線)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # テキストラベルを描画
        cv2.putText(frame, f"Player", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # フレームを表示
    cv2.imshow(f"Frame {frame_index}", frame)

    # キー入力待ち
    key = cv2.waitKey(0)  # 次のフレームを表示するにはキーを押す
    if key == 27:  # ESCキーで終了
        break

# すべてのウィンドウを閉じる
cv2.destroyAllWindows()