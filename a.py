import cv2
import pandas as pd
import os

def save_frames(video_path, frame_numbers, output_folder):
    """
    指定した複数のフレーム番号の画像を動画から保存する。
    
    Args:
        video_path (str): 動画ファイルのパス。
        frame_numbers (list of int): 保存したいフレーム番号のリスト（0から始まる）。
        output_folder (str): フレーム画像を保存するフォルダのパス。
    """
    # 出力フォルダを作成（存在しない場合）
    os.makedirs(output_folder, exist_ok=True)

    # 動画を読み込む
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 動画を読み込めませんでした。")
        return

    # 動画の総フレーム数を取得
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"動画の総フレーム数: {total_frames}")

    # 指定したフレーム番号を順に処理
    for frame_number in frame_numbers:
        # フレーム番号の範囲をチェック
        if frame_number < 0 or frame_number >= total_frames:
            print(f"Warning: フレーム番号 {frame_number} は無効です（範囲外）。")
            continue

        # 指定したフレーム番号へ移動
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # フレームを取得
        ret, frame = cap.read()
        if not ret:
            print(f"Error: フレーム {frame_number} を取得できませんでした。")
            continue

        # フレームを保存
        output_path = os.path.join(output_folder, f"frame_{frame_number}.png")
        cv2.imwrite(output_path, frame)
        print(f"フレーム {frame_number} を {output_path} に保存しました。")

    # 総フレーム数とフレームレートを取得
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"fps : {fps}")
    # 時間を計算
    duration_seconds = total_frames / fps
    minutes = int(duration_seconds // 60)
    seconds = duration_seconds % 60
    
    print(f"動画の時間: {minutes}分 {seconds:.2f}秒")

    # リソース解放
    cap.release()
    print("すべての処理が完了しました。")

frame_numbers = [3600, 12000, 13560, 14010, 64080, 64800]   # 表示したいフレーム番号のリストを指定

# 使用例
video_path_ori = '../quvnu_video/quvnu_ori.mp4'
video_path_rslt = '../quvnu_video/CAC_tracking.mp4'

output_folder_ori = "../quvnu_video/test_frames_ori"  # オリジナル動画の保存先フォルダ
output_folder_rslt = "../quvnu_video/test_frames_rslt"  # 結果動画の保存先フォルダ

# 各動画に対してフレームを保存
save_frames(video_path_ori, frame_numbers, output_folder_ori)
save_frames(video_path_rslt, frame_numbers, output_folder_rslt)
