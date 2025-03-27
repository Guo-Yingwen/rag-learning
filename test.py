from flask import Flask, request

app = Flask(__name__)

@app.route("/index", methods=['GET'])
# 呈现 index 网页
def home():
    return "Hello World!"

@app.route("/index", methods=['POST'])
# 处理 用户上传的文件
def home_post():
    # 处理 POST 请求的数据
    data = request.get_json()  # 如果发送的是 JSON 数据
    # 这里可以添加处理 POST 数据的逻辑
    return {"message": "Received POST request", "data": data}

@app.route("/recall", methods=['GET'])
# 检索、召回
def recall():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)