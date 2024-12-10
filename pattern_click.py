import cv2

# パターンごとのクリック位置を保存するリスト
pattern_clicks = []

# 現在のウィンドウ番号
window_index = 0

# クリック回数のカウント
click_count = 0

# パターンごとのウィンドウ名
window_names = ["pattern1", "pattern2", "pattern3", "pattern4"]  # 必要に応じて追加可能

# 一時的にクリックを保存するリスト（1パターン分）
current_clicks = []

# マウスクリック時のコールバック関数
def click_event(event, x, y, flags, param):
    global click_count, window_index, current_clicks, image
    if event == cv2.EVENT_LBUTTONDOWN:  # 左クリック時
        current_clicks.append((x, y))  # 現在のクリック位置を保存
        print(f"Clicked at: ({x}, {y}) in {window_names[window_index]}")
        # 表示にクリックした位置を追加
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow(window_names[window_index], image)
        click_count += 1

        # 3回クリックされたら次のウィンドウへ
        if click_count >= 3:
            # 現在のクリック位置を全体のリストに追加
            pattern_clicks.append(current_clicks.copy())
            current_clicks.clear()
            click_count = 0
            window_index += 1

            if window_index < len(window_names):
                # 次のウィンドウを表示
                cv2.destroyAllWindows()
                display_window()
            else:
                print("All patterns completed. Exiting...")
                cv2.destroyAllWindows()

# ウィンドウを表示する関数
def display_window():
    global image
    # 画像のリロード
    image = cv2.imread('../quvnu_video/field_template.jpg')

    if image is None:
        print("Image not found. Make sure 'field_template.jpg' exists in the working directory.")
    else:
        cv2.imshow(window_names[window_index], image)
        cv2.setMouseCallback(window_names[window_index], click_event)

# 初回ウィンドウの表示
display_window()

# 任意のキーで終了
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Exiting on 'q' key press...")
        cv2.destroyAllWindows()
        break

# 最終的なクリック位置を表示
print("Click positions by pattern:", pattern_clicks)
