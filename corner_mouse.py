import cv2
import numpy as np

######################## 画像準備 ##############################

# 画像をロードし、色空間をRGBに変換します
img = cv2.imread('frame100.jpg')
print("img size : " +str(img.shape))

sample = img.copy()

######################## マウス処理 ################################
def onMouse(event, x, y, flag, params):
    raw_img = params["img"]
    wname = params["wname"]
    point_list = params["point_list"]
    point_num = params["point_num"]
    
    ## クリックイベント
    ### 左クリックでポイント追加
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(point_list) < point_num:
            point_list.append([x, y])
    
    ### 右クリックでポイント削除
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(point_list) > 0:
            point_list.pop(-1)

    ## レーダーの作成, 描画
    img = raw_img.copy()
    h, w = img.shape[0], img.shape[1]
    cv2.line(img, (x, 0), (x, h), (255, 0, 0), 1)
    cv2.line(img, (0, y), (w, y), (255, 0, 0), 1)

    ## 点, 線の描画
    for i in range(len(point_list)):
        cv2.circle(img, (point_list[i][0], point_list[i][1]), 3, (0, 0, 255), 3)
        if 0 < i:
            cv2.line(img, (point_list[i][0], point_list[i][1]),
                     (point_list[i-1][0], point_list[i-1][1]), (0, 255, 0), 2)
        if i == point_num-1:
            cv2.line(img, (point_list[i][0], point_list[i][1]),
                     (point_list[0][0], point_list[0][1]), (0, 255, 0), 2)
    
    if 0 < len(point_list) < point_num:
        cv2.line(img, (x, y),
                     (point_list[len(point_list)-1][0], point_list[len(point_list)-1][1]), (0, 255, 0), 2)
    
    ## 座標情報をテキストで出力
    cv2.putText(img, "({0}, {1})".format(x, y), (0, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow(wname, img)


## 取得した座標情報を保存
def save_point_list(path, point_list):
    f = open(path, "w")
    for p in point_list:
        f.write(str(p[0]) + "," + str(p[1]) + "\n")
    f.close()


## 諸々設定
wname = "MouseEvent"
point_list = []
point_num = 4 #今回は矩形がほしかったので4
params = {
    "img": sample,
    "wname": wname,
    "point_list": point_list,
    "point_num": point_num,
}

## メイン
cv2.namedWindow(wname)
cv2.setMouseCallback(wname, onMouse, params)
cv2.imshow(wname, sample)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(point_list)

## 取得したポイントをcsvに保存
if len(point_list) == point_num:
    txt_path = "points.csv"
    save_point_list(txt_path, point_list)
    print("Save txt file:", txt_path)


pts1 = np.array(point_list, dtype = np.int32)
pts1.reshape([4, 1, 2])
