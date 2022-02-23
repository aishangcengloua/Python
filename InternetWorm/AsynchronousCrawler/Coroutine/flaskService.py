from flask import Flask
import time

app = Flask(__name__)

@app.route('/heige')
def index_heige() :
    time.sleep(2)
    return 'Hello heige'

@app.route('/james')
def index_james() :
    time.sleep(2)
    return 'Hello james'

@app.route('/tom')
def index_tom() :
    time.sleep(2)
    return 'Hello tom'

if __name__ == '__main__':
    app.run(threaded = True)