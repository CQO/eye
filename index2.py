import subprocess
import time
from PIL import ImageGrab

# 配置RTMP服务器地址
rtmp_url = 'rtmp://196806.push.tlivecloud.com/live/test'

# 配置ffmpeg命令
command = [
    './ffmpeg',
    '-f', 'image2pipe',
    '-vcodec', 'mjpeg',
    '-i', '-',
    '-vcodec', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'veryfast',
    '-f', 'flv',
    rtmp_url
]


# 启动ffmpeg进程
# proc = subprocess.Popen(command, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
proc = subprocess.Popen(command, stdin=subprocess.PIPE)
while True:
    try:
        # 捕获屏幕
        screenshot = ImageGrab.grab()
        
        # 将截图保存到ffmpeg进程的stdin
        screenshot.save(proc.stdin, 'JPEG', quality=30)
        
    finally: {}
    # 间隔一定时间（根据需要调整）
    time.sleep(1/30)  # 假设目标是30fps
        

# 关闭进程（在适当的时候）
proc.stdin.close()
proc.wait()