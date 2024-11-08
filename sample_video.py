import cv2

# 使用例
input_video_path = r"C:\Users\くぼたさとる\futsal\m2\CAC\CAC_tracking_1Mbps.mp4"  # 入力動画ファイルのパス

cap = cv2.VideoCapture(input_video_path)



# 入力動画のプロパティを取得
original_fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


"""
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break


    frame_count += 1
    #print(frame_count)

print(frame_count)
"""
print(total_frames)
# リソースを解放
cap.release() 
cv2.destroyAllWindows()




