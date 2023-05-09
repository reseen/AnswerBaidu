from simpleCatPaw import SimpleCatPaw
from paddleocr import PaddleOCR

import subprocess
import pyperclip
import random
import sys
import os


# 临时文件目录，修改直接修改path的值即可
def filePath(fileName, path="D:/baidu"):

    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.abspath(os.path.join(path, fileName))


# 退出所有应用
def exitAll(cp):
    cp.stopApp("com.baidu.iknow")
    cp.exit()
    sys.exit()


# 将问题截图保存
def getQuestionImage(cp, path=filePath("question.png")):
    screenImage = cp.getScreenCap()

    top = 0
    bottom = 0
    lastColor = "000000"
    for i in range(500):
        color = cp.getColor(screenImage, 10, i)
        if lastColor != "F5F5F5" and color == "F5F5F5": # 寻找问题块的最上方
            top = i
        if lastColor == "F5F5F5" and color != "F5F5F5": # 寻找问题块的最下方
            bottom = i
            break
        lastColor = color

    cp.saveImage(screenImage, path, (0, top, -1, bottom))


# 获得 ChatGPT 答案 AHK
def chatGPT(question):
    checkString = question.lower()
    if "gpt" in checkString or "chat" in checkString:
        print("钓鱼问题，拒绝回答")
        return None
    adb_cmd = ".\\ahk\\AutoHotkey64.exe autoChatGPT.ahk %s " % question
    result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)
    resText_A = ""
    if result.returncode == 0:
        resText = pyperclip.paste()
        pyperclip.copy("")

        if len(resText) == 0: 
            print("AHK执行异常，未获得答案", result.stderr)
            return None

        # 过滤关键字 防止露馅
        filter = ["无法提供", "人工智能", "抱歉", "AI", "对不起"]
        for key in filter:
            if key in resText:
                print("chatGPT不知道这个问题")
                return None
        
        # 替换一些不合理的关键字
        resText = resText.replace("中国", "我们国家")
        resText = resText.replace("大陆", "我国")

            
        # 判断回答完毕 如果没结束则继续问
        if resText[-1] == "。" or resText[-1] == "！" or resText[-1] == "." or resText[-1] == "!" :
            return resText
        resText_A = resText

    else:
        print("AHK执行失败，未获得答案", result.stderr)
        return None

    # 一次回答不完则让其继续，只继续一次
    adb_cmd = ".\\ahk\\AutoHotkey64.exe autoChatGPT.ahk %s" % "继续"
    result = subprocess.run(adb_cmd.split(), capture_output=True, text=True)
    if result.returncode == 0:
        resText = pyperclip.paste()
        pyperclip.copy("")
       
        if len(resText) == 0: 
            print("AHK执行异常，未获得答案", result.stderr)
            return None
        
        # 替换一些不合理的关键字
        resText = resText.replace("中国", "我们国家")
        resText = resText.replace("大陆", "我国")

        resText = resText.strip()
        return resText_A  + resText

    else:
        print("AHK执行失败，未获得答案", result.stderr)
        return None


# 点击发布回答或取消回答
def clickSendorCancel(cp, pd, flag):
    cp.saveImage(cp.getScreenCap(), filePath("send.png"), (0, 0, -1, 200), 0.5)    # 判断顶部文本
    res = pd.ocr(filePath("send.png"), cls=True)                                   # 飞桨
    if flag is True:
        for item in res[0]:
            if "发布" in item[1][0]:
                x = int((item[0][0][0] + item[0][1][0]))                    # 左上角 右上角 坐标中点 zoom=0.5
                y = int((item[0][0][1] + item[0][3][1]))                    # 左上角 左下角 坐标中点 zoom=0.5
                cp.tap(x, y)
                print("发布答案")
    else:
        for item in res[0]:
            if "取消" in item[1][0]:
                x = int((item[0][0][0] + item[0][1][0]))                    # 左上角 右上角 坐标中点 zoom=0.5
                y = int((item[0][0][1] + item[0][3][1]))                    # 左上角 左下角 坐标中点 zoom=0.5
                cp.tap(x, y)
                print("取消发布")
    

# 判断当前是不是主页
def isHomePage(cp, pd):
    cp.saveImage(cp.getScreenCap(), filePath("title.png"), (0, 0, -1, 300), 0.5)   # 判断顶部文本
    res = pd.ocr(filePath('title.png'), cls=True)                                  # 飞桨 OCR
    for item in res[0]:
        if "知道广场" in item[1][0]:
           return True
        if "任务中心" in item[1][0]:
            return True
    return False


# 返回主页
def clickBackHome(cp, pd):
    print("回到主页")
    for i in range(6):
        if isHomePage(cp, pd) is False:
            cp.inputKeyCode("KEYCODE_BACK")
            cp.delay(500)
        else:
            print("回到主页 完成")
            break

    # 回到顶部
    cp.swipe(300, 900, 300, 1200, 100)
    cp.delay(500)
    cp.swipe(300, 900, 300, 1200, 100)
    cp.delay(500)
    cp.swipe(300, 900, 300, 1200, 100)
    cp.delay(500)

    # 刷新列表
    cp.swipe(300, 400, 300, 1200, 200)
    cp.delay(2000)


# 回答一次问题
def answerOnce(pd, cp):

    # 选择问题分类
    print("选择 <悬赏最高 / 最新> 类问题")
    cp.saveImage(cp.getScreenCap(), filePath("home.png"), zoom=0.5)
    res = pd.ocr(filePath('home.png'), cls=True)                # 飞桨 OCR

    for item in res[0]:
        # if "高悬赏" in item[1][0]:
        if "最新" in item[1][0]:
            x = int((item[0][0][0] + item[0][1][0]))            # 左上角 右上角 坐标中点 zoom=0.5
            y = int((item[0][0][1] + item[0][3][1]))            # 左上角 左下角 坐标中点 zoom=0.5
            cp.tap(x , y)                                       # 回答 悬赏最高 / 最新 的问题
            cp.delay(1000)
            cp.swipe(300, y, 300, 500, 1500)                    # 慢慢滑动到上面一点 多出来几个问题
            cp.delay(200)
            break

    # 找写回答按钮，随机点有可能点到广告
    print("寻找 <写回答> 按钮")
    cp.saveImage(cp.getScreenCap(), filePath("write.png"), zoom=0.5)
    res = pd.ocr(filePath('write.png'), cls=True)               # 飞桨 OCR
    btnPos = []
    for item in res[0]:
        if "写回答" in item[1][0]:
            y = int((item[0][0][1] + item[0][3][1]))            # 左上角 左下角 坐标中点 zoom=0.5
            btnPos.append(y)
    
    if len(btnPos) == 0:
        print("没找到 <写回答> 按钮")
        return
    
    index = 0                                                   # 回答第一个问题
    index = random.randint(0, len(btnPos)-1)                    # 随机回答一个问题
    print("点击 <写回答> 按钮 index = %d" % index)

    cp.tap(300, btnPos[random.randint(0, index)])               
    cp.delay(1000)

    # 寻找我来答按钮
    print("寻找 <我来答> 按钮")
    for i in range(3):
        # 找我来答按钮，并点击，三次没找到则退出
        cp.saveImage(cp.getScreenCap(), filePath("letme.png"), zoom=0.5)
        res = pd.ocr(filePath('letme.png'), cls=True)           # 飞桨 OCR
        for item in res[0]:
            if "我来答" in item[1][0]:
                x = int((item[0][0][0] + item[0][1][0]))        # 左上角 右上角 坐标中点
                y = int((item[0][0][1] + item[0][3][1]))        # 左上角 左下角 坐标中点
                cp.tap(x, y)
                i = -1
                break
        if i < 0:
            print("点击 <我来答> 按钮")
            cp.delay(2000)
            break   
        elif i == 2:
            print("没有找到 <我来答> 按钮")
            exitAll(cp)
        else:
            print("重新寻找 <我来答> 按钮")
            cp.swipe(300, 300, 300, 295, 500)                   # 随便滑一下，防止相同图片反复识别不出来
            cp.delay(1000)

    # 获取问题
    getQuestionImage(cp, filePath('question.png'))              # 问题截图
    res = pd.ocr(filePath('question.png'), cls=True)            # 飞桨 OCR
    question = ""
    for item in res[0]:
        if "问题详情" not in item[1][0]:
            question = question + item[1][0]                    # 排除问题详情

    answerText = chatGPT(question)
    if answerText is None:
        clickSendorCancel(cp, pd, False)                        # 点击取消
        clickBackHome(cp, pd)                                   # 回到主页
    else:
        cp.tap(100, 500)
        cp.delay(500)
        cp.setKeyboard()
        answerList = answerText.split("\n")
        for item in answerList:
            if len(item) > 1:
                cp.inputText(item)
                cp.delay(200)                                   # 为了防止键盘关闭 多点两下 激活键盘
                cp.tap(10, 300)
                cp.delay(500)
                cp.tap(10, 600)
                cp.inputKeyCode("KEYCODE_ENTER")
                cp.delay(500)

        print("问题回答完毕")
        clickSendorCancel(cp, pd, True)                         # 发布答案
        cp.delay(5000)                                          # 等待提交完成
        clickBackHome(cp, pd)                                   # 回到主页
    

if __name__ == "__main__":
    cp = SimpleCatPaw()
    print("SimpleCatPaw Ready.")

    cp.startApp("com.baidu.iknow/.activity.common.PrologueActivity")    # 启动百度知道
    print("Start Baidu Iknow")

    pd = PaddleOCR(use_angle_cls=True, show_log=False, lang="ch")
    print("Paddle Server Chinese OCR Ready.")

    # 等待APP启动完成
    for i in range(10):
        if isHomePage(cp, pd):
            print("已进入主页，开始答题。")
            break

        if i == 9:
            print("百度知道APP首页检测失败，退出。")
            exitAll(cp)
    
    # 答60次题
    for i in range(60):
        answerOnce(pd, cp)

    # 结束应用
    print("完成回答，退出应用。")
    exitAll(cp)