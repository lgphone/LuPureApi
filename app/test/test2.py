# 导入Flask类
from flask import Flask

# 生成该类的一个实例
app = Flask(__name__)
import time

# 调用app的路由方法
@app.route('/')
def hello_world():
    time.sleep(10)
    return 'Hello World2'


# 开始执行
if __name__ == '__main__':
    # 打开调试窗口
    app.debug = True

    # run可以指定host参数，指定ip,0.0.0.0表示全网段
    # app.run()
    app.run(host='0.0.0.0', port=5001)
