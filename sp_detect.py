import cv2
import os
import pandas as pd
import numpy as np

# CSVファイルを読み込み
df = pd.read_csv('../quvnu_csv/quvnu_data.csv',header=0)#最初の行を列名として使用し、データは2行目から始まる

# 入力動画ファイルのパス
input_video_path = '../quvnu_video/quvnu_ori.mp4'  # ここに入力動画ファイルのパスを指定
output_folder = '../quvnu_video/quvnu_videos'  # 出力動画を保存するフォルダ

#CAC解析時のfps情報
cac_tracking_path = '../quvnu_video/CAC_tracking.mp4'
cac_cap = cv2.VideoCapture(cac_tracking_path)
cac_fps = cac_cap.get(cv2.CAP_PROP_FPS)

# フォルダが存在しない場合は作成する
os.makedirs(output_folder, exist_ok=True)

# 動画ファイルを読み込む
cap = cv2.VideoCapture(input_video_path)

# 動画のフレームレートとフレーム総数を取得
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'ori_tatal_frame:{total_frames}')
cac_total_frames = int(cac_cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'cac_tatal_frame:{cac_total_frames}')

#トラッキングビデオと入力動画のfpsを補正
fps_correct = fps/cac_fps
print(fps_correct)

# 切り取る基準のフレーム番号のリスト
frame_list = [2550, 8340, 10680, 19390, 23520, 36840] #テスト用
#frame_list = [2100, 2550, 8400, 10710, 19440, 22500, 23580, 30120, 33090, 36330, 36840, 39690, 42240, 45540]

correct_frame_float = [x * fps_correct for x in frame_list]
correct_frame = [int(value) for value in correct_frame_float]

print(correct_frame)
# 抽出フレームの範囲を指定
offset_before = 60
offset_after = 120
# fps補正、オフセットの値が小さいためfpsの誤差は許容（fps_correct：1.998→2.0）
offset_before_correct = offset_before*int(round(fps_correct))
offset_after_correct = offset_after*int(round(fps_correct))



# フレームリスト内の各フレーム番号に対して処理を行う
# 各frame_numberに対して抽出したデータを保持するデータフレーム
sp_frame_df = pd.DataFrame()

#for idx, frame_number in enumerate(frame_list):
for idx, frame_number in enumerate(correct_frame):
    start_frame = max(0, frame_number - offset_before_correct)  # 30フレーム前（0未満にならないように）
    end_frame = min(total_frames - 1, frame_number + offset_after_correct)  # 120フレーム後（総フレーム数を超えないように）

    # 出力動画のファイル名を設定
    #output_video_path = os.path.join(output_folder, f'output_{idx}.mp4')
    output_video_path = os.path.join(output_folder, f'quvnu_{idx}.mp4')

    # 動画の書き出し用オブジェクトを作成
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ))

    # 指定範囲のフレームを読み込んで保存する
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)  # 開始フレームにシーク

    for i in range(start_frame, end_frame + 1):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)  # フレームを保存

    out.release()  # 出力動画を保存
    print(f'Video segment saved: {output_video_path}')


cap.release()
print('All segments have been processed and saved.')

################## SP開始シーンの前後のトラッキングデータを抽出 ######################
"""
for frameIndex in frame_list:#データフレーム抽出には補正前のframe_listを使用
    start_frame = max(0, frameIndex - offset_before)  # 30フレーム前（0未満にならないように）
    end_frame = min(total_frames - 1, frameIndex + offset_after)  # 120フレーム後（総フレーム数を超えないように）

    filtered_df = df[(df['frameIndex'] >= start_frame) & (df['frameIndex'] <= end_frame)]
    sp_frame_df = pd.concat([sp_frame_df, filtered_df], ignore_index=True)
"""

##################### SP開始シーンのみのトラッキングデータ ###########################
# frameIndexの中で、frame_numbersの要素と一致する行を抽出
sp_frame_df = df[df['frameIndex'].isin(frame_list)]

# 結果をCSVファイルに出力
output_path = '../quvnu_csv/quvnu_sp_frame.csv'
sp_frame_df.to_csv(output_path, index=False)
print(f'Filtered data saved to {output_path}')
