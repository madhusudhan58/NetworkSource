from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Network Source Application Running on Azure Kubernetes"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8083, debug=True)