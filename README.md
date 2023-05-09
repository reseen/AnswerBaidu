# AnswerBaidu

本着薅羊毛绝不花一分钱的心态，采用完全免费的方案，实现了一个用ChatGTP回答百度知道问题的脚本，采用技术如下：

- adb： 控制基本的手机动作
- adbKeyboard： 实现中文的输入
- paddle ocr： 实现手机截图的文本识别
- ahk：作为RPA方案，向chatGPT提问，并获得答案
- tampemonkey：一个简易的脚本，用来标记chatGPT页面元素（原始页面找图失败率很高）

## 使用方法
 
- 手机安装 ```百度知道APP```
- 手机安装 ```Answer/apk/``` 文件夹下的 ADBKeyboard.apk，并在输入法设置中选择启用该输入法
- 电脑配置 python 环境，在 ```Answer```文件夹下，执行 ``` python baidu.py ``` 然后提示缺什么包，就安装什么包
- 浏览器安装 tampemonkey 插件，然后新建脚本，将 ```Answer/chatMark.user.js``` 内容复制到脚本编辑器，然后保存


## python pip 安装注意的点

#### paddle

```bash
pip install paddlepaddle==2.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddleocr>=2.0.1
```

注意，paddle 安装最新版本。新版 paddle 的识别结果，比老版本多嵌套一层列表，如需要使用老版本，需要修改以下代码：

```python
# 将 baidu.py 文件中， paddle 所有识别结果的迭代目标进行替换

# 比如 将
res = pd.ocr(filePath('title.png'), ls=True)
for item in res[0]:

# 改为
res = pd.ocr(filePath('title.png'), ls=True)
for item in res:

```

#### FindImage
```bash
pip install findimage
```

安装完成后报错如下：
```
ImportError: Bindings generation error. Submodule name should always start with a parent module name. Parent name: cv2.cv2. Submodule name: cv2
```

解决方法：
``` python
# 将 site-packages\findimage\__init__.py 文件，第 18 行
from cv2 import cv2

# 改为
import cv2
```
这个包现在其实没用，可以删掉相关代码

## 可选配置

#### 临时文件路径修改
```python
# baidu.py 第12行
def filePath(fileName, path="D:/baidu"):
```
建议修改到内存虚拟磁盘中，以保护硬盘

#### 答题类型
```python
# baidu.py 第172行
# if "高悬赏" in item[1][0]:
if "最新" in item[1][0]:
```
默认回答 “最新” 问题，可选回答“最高悬赏”问题

#### 答题顺序
```python
index = 0                                                   # 回答第一个问题
index = random.randint(0, len(btnPos)-1)                    # 随机回答一个问题
```
默认随即回答一道题问题，可选回答第一题


#### 关键词筛选、过滤
```python
# baidu.py 第50行起，直至函数结束，看着修改即可
if "gtp" in checkString or "char" in checkString:
    print("钓鱼问题，拒绝回答")
    return None
    ......
```


## 其他问题

#### 为什么不用 selenium？

使用 ```--remote-debugging-port``` 参数启动Chrome浏览器后，chatGTP不给答案

#### 为什么不用 openai API？
即使有免费额度，用完还是要收钱，不确定百度知道答一道题的收益，能不能覆盖 API 的成本

#### 油猴脚本加载不上？
刷新页面即可，如果墙不稳定可能要多刷几次

#### 可以改进的点
- 目前手机元素定位是通过文本识别进行的，低效，但通用性略好一点，如果自己用，可以根据流程直接点击固定坐标，稳定可靠
- 还有一种方法是通过 adb 指令获取 Activity 的元素，然后解析元素内容，不确定可不可行
- 其实可以用 python 起个 http 服务，然后直接和油猴脚本通讯，获取 chatGPT 内容，这样浏览器应该无须在前台，后面有时间可以考虑尝试一下

#### 使用建议
- 勇敢的去修改任何一行代码，这就是依托答辩
- 注意使用时长，封号了对谁都不好
- 在虚拟机中实现后台运行

祝大家玩的开心~


