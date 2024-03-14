from PIL import ImageGrab
import io
import base64
import json
import websocket
import threading
import hashlib
import win32api,win32con

wsUserInfo = {}



def screenshot_to_base64(x, y, x1, y1):
    # 使用ImageGrab截取屏幕
    screenshot = ImageGrab.grab(bbox=(x, y, x1, y1))
    # screenshot = ImageGrab.grab()
    # 创建一个字节流缓冲区
    img_byte_arr = io.BytesIO()
    
    # 将截图保存到字节流中，格式为PNG
    screenshot.save(img_byte_arr, format='JPEG', quality=20)
    
    # 获取字节流的内容
    img_byte_arr = img_byte_arr.getvalue()
    
    # 将字节流编码为Base64字符串
    img_base64 = base64.b64encode(img_byte_arr)
    # print('结束截图')
    # 返回Base64编码的字符串
    return img_base64.decode('utf-8')

autoRun = False
userTemp = None
linkWS = None
screenW = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN))
screenH = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
screenCutTemp = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

def my_task():
    global autoRun
    global userTemp
    if (autoRun):
        cutScreen()
    # 重新设置Timer
    threading.Timer(3, my_task).start()

my_task()  # 初始化调用

def cutScreen():
    global linkWS
    global userTemp
    global wsUserInfo
    global screenW
    global screenH
    screenWJ = int(screenW / 10)
    screenHJ = int(screenH / 10)
    for xInd in range(10):
        for yInd in range(10):
            base64_screenshot = screenshot_to_base64(screenWJ * xInd, screenHJ * yInd, screenWJ * (xInd + 1), screenHJ * (yInd + 1))
            screenCutMD5 = hashlib.md5(base64_screenshot.encode()).hexdigest()
            if (screenCutTemp[xInd][yInd] != screenCutMD5):
                screenCutTemp[xInd][yInd] = screenCutMD5
                print('发送消息:' + userTemp['userID'])
                sendMessage = json.dumps({"route":"sendMessage","type":"ets","value": [xInd, yInd, base64_screenshot], "userID": wsUserInfo['userID'], "id": userTemp['userID']})
                linkWS.send(sendMessage)

def on_message(ws, message):
    global autoRun
    global userTemp
    global wsUserInfo
    global linkWS
    linkWS = ws
    print("Received message: %s" % message)
    temp = json.loads(message)
    userTemp = temp
    if (temp['type'] == 'getData'):
        cutScreen()
    if (temp['type'] == 'userInfo'):
        wsUserInfo = temp['value']
        print('登陆成功:' + wsUserInfo['userID'])
    if (temp['type'] == 'autoRun'):
        autoRun = True
    if (temp['type'] == 'stopAutoRun'):
        autoRun = False
    return ''

def on_error(ws, error):
    print("Error: %s" % error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    ws.send(json.dumps({"route":"login","type":"ets","admin":False}))

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://port.run:8083",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    
    ws.run_forever()



# 调用函数，获取Base64编码的屏幕截图
# base64_screenshot = screenshot_to_base64()

# # 打印或使用Base64编码的截图
# print(base64_screenshot)
