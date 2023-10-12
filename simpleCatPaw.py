import numpy as np
import cv2
import findimage
import subprocess

class SimpleCatPaw:
    
    def __init__(self):
        pass


    # 延时
    def delay(self, ms):
        cv2.waitKey(ms)


    # 退出
    def exit(self):
        cv2.destroyAllWindows()


    # 显示设备列表
    def showDeviceList(self):
        adb_cmd = ".\\adb\\adb devices"
        result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)

        if result.returncode == 0:
            print(result.stdout)
        else:
            print("设备列表获取失败：", result.stderr)


    # 显示图像
    def showImage(self, image, zoom=0.3, title='SimpleCatPaw'):
        if image is not None:
            height, width = image.shape[:2]
            scaled_image = cv2.resize(image, (int(width * zoom), int(height * zoom)))
            cv2.imshow(title, scaled_image)
            cv2.waitKey(50)

    
    # 显示当前屏幕
    def showScreen(self, zoom=0.3):
        self.showImage(self.getScreenCap(), zoom, "SimpleCatPaw Screen")


    # 获取屏幕截图
    def getScreenCap(self):
        adb_cmd = ".\\adb\\adb exec-out screencap -p"
        result = subprocess.run(adb_cmd.split(), capture_output=True)

        try:
            # 将二进制数据解码成图像
            image_data = np.frombuffer(result.stdout, np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            if image.shape[0] > 0 and image.shape[1] > 0:
                return image
            else:
                print("截图失败：未获取到正确的图像尺寸")
                return None
            
        except Exception as e:
            print("截图失败：", e)
            return None

    # 启动应用
    def startApp(self, param):
        adb_cmd = ".\\adb\\adb shell am start %s" % param
        result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)

        if result.returncode == 0:
            print(result.stdout)
        else:
            print("启动应用失败：", result.stderr)


    # 结束应用
    def stopApp(self, param):
        adb_cmd = ".\\adb\\adb shell am force-stop %s" % param
        subprocess.run(adb_cmd.split(), capture_output=True, text=True)


    # 输入按键事件
    def inputKeyCode(self, keycode):
        adb_cmd = ".\\adb\\adb shell input keyevent '%s'" % keycode
        result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)

        if result.returncode == 0:
            return True
        else:
            print("inputKeyCode 执行失败：", result.stderr)
            return False
        

    # 设置输入法
    def setKeyboard(self):
        adb_cmd = ".\\adb\\adb shell ime set com.android.adbkeyboard/.AdbIME"
        result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)

        if result.returncode == 0:
            return True
        else:
            print("setKeyboard 执行失败：", result.stderr)
            return False


    # 输入文本
    def inputText(self, msg):
        if len(msg) > 0:
            adb_cmd = ".\\adb\\adb shell am broadcast -a ADB_INPUT_TEXT --es msg '%s'" % msg
            result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)
            print(adb_cmd)
            if result.returncode == 0:
                return True
            else:
                print("inputText 执行失败：", result.stderr)
                return False


    # 点击屏幕
    def tap(self, x, y):
        adb_cmd = ".\\adb\\adb shell input tap %d %d" % (int(x), int(y))
        result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)

        if result.returncode == 0:
            print("%s 成功" % adb_cmd)
        else:
            print("%s 执行失败" % adb_cmd, result.stderr)


    # 滑动屏幕
    def swipe(self, sx, sy, ex, ey, delay=1000):
        adb_cmd = ".\\adb\\adb shell input swipe %d %d %d %d %d" % (int(sx), int(sy), int(ex), int(ey), int(delay))
        result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)

        if result.returncode == 0:
            print("%s 成功" % adb_cmd)
        else:
            print("%s 执行失败" % adb_cmd, result.stderr)
    

    # 获得图像某个像素的颜色
    def getColor(self, image, x, y):
        return "%02X%02X%02X" % (image[y][x][2], image[y][x][1], image[y][x][0])
    

    # 保存图像
    def saveImage(self, image, path, range=None, zoom=1):     
        cropImg = image.copy()
        if range is not None:
            sx = range[0]   # 左上角 x 坐标
            sy = range[1]   # 左上角 y 坐标
            ex = range[2]   # 右下角 x 坐标
            ey = range[3]   # 右下角 y 坐标
            if ex <= 0 : ex = image.shape[1]
            if ey <= 0 : ey = image.shape[0]

            cropImg = cropImg[sy:ey, sx:ex]

        # self.showImage(cropImg)
        # cv2.waitKey(0)
        if zoom != 1:
            height, width = cropImg.shape[:2]
            cropImg = cv2.resize(cropImg, (int(width * zoom), int(height * zoom)))
        cv2.imwrite(path, cropImg)

    # 屏幕中找小图
    def findImage(self, path, mode='all', range=None):
        tempImg = cv2.imread(path)
        cropImg = self.getScreenCap()
        if range is not None:
            sx = range[0]   # 左上角 x 坐标
            sy = range[1]   # 左上角 y 坐标
            ex = range[2]   # 右下角 x 坐标
            ey = range[3]   # 右下角 y 坐标
            cropImg = cropImg[sy:ey, sx:ex]
            
            # self.showImage(cropImg)
            # cv2.waitKey(0)

        match_result = findimage.find_all_template(cropImg, tempImg)

        if mode == "all":
            return match_result
        
        if mode == "y-min":
            result = None
            for res in match_result:
                if result is None:
                    result = res
                else:
                    if res['rectangle'][0][1] < result['rectangle'][0][1]:
                        result = res
            return result
        
        return match_result

        # for res in match_result:
        #     print(res['rectangle'])
        #     cv2.rectangle(cropImg, res['rectangle'][0], res['rectangle'][3], (0, 0, 255), 2)

        # self.showImage(cropImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
