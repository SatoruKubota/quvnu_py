#指定したフレームがどうなってるかを確かめるプログラム
import cv2
import pandas as pd

# CSVファイルを読み込み
#df = pd.read_csv('cac_test.csv')
#df = pd.read_csv('filtered_data.csv')
#df = pd.read_csv('0_4999_coord.csv')
df = pd.read_csv('quvnu_coord.csv')#テスト
fps_correct = 1.998001998001998

def show_frame(video_path, frame_numbers):
    # 動画ファイルを読み込み
    cap = cv2.VideoCapture(video_path)
    
    # 動画が正しく読み込めたか確認
    if not cap.isOpened():
        print("Error: 動画ファイルを開けませんでした")
        return
    

    for frame_num in frame_numbers:

        # 指定したフレームに移動
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num*fps_correct) # ビデオは試合動画のfpsに合わせる
        
        # フレームを取得
        ret, frame = cap.read()
        
        # フレームが正しく取得できたか確認
        if not ret:
            print(f"Error: フレーム {frame_num} を取得できませんでした")
            return
        
        # フレームを表示
        
        # 指定されたフレームの x, y 座標をリスト形式で取得
        
        x_coords = df[df['frameIndex'] == frame_num]['x'].to_list()
        y_coords = df[df['frameIndex'] == frame_num]['y'].to_list()


        # x, y 座標をペアにしてリスト形式で取得
        coords = list(zip([int(x) for x in x_coords], [int(y) for y in y_coords]))
        for coord in coords:
            cv2.circle(frame, coord, 5, (0,255,0), 2)
        
        cv2.imshow(f'Frame {frame_num}', frame)
        
        # キーが押されるのを待つ
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break        
    # ウィンドウを閉じる
    cv2.destroyAllWindows()
    
    # キャプチャを解放
    cap.release()

# 使用例
#video_path = 'CAC_tracking.mp4'
frame_numbers = [2085, 2535, 8385, 10695, 19425, 22485, 23565, 30105, 33075, 36315, 36825, 39675, 42225, 45525]# 表示したいフレームリストを指定、CACの解析結果のフレーム
video_path_ori = 'quvnu_ori.mp4'
#show_frame(video_path, frame_number)

show_frame(video_path_ori, frame_numbers)# 表示したいのは試合動画のフレームに合わせたもの

#######################################################################
"""
# 動画のパスと保存するフレーム番号
video_path = 'quvnu_ori.mp4'  # 使用する動画のパス
frame_number = 4255  # 保存したいフレーム番号
output_image_path = 'frame_test.jpg'  # 保存する画像のパス

# 動画を読み込む
cap = cv2.VideoCapture(video_path)

# 動画が開けたか確認
if not cap.isOpened():
    print("動画を開けませんでした")
    exit()

# 指定されたフレームにジャンプする
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

# フレームを読み込む
ret, frame = cap.read()

if ret:
    # フレームが正常に読み込まれた場合、画像として保存
    cv2.imwrite(output_image_path, frame)
    print(f"フレーム {frame_number} を画像として保存しました：{output_image_path}")
else:
    print(f"フレーム {frame_number} の読み込みに失敗しました")

# 動画のリソースを解放
cap.release()

"""
