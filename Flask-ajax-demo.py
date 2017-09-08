from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/add')
def add():
    num = request.args.get('num', 0, type=int)
    data = num + 1
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()