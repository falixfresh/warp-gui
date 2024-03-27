import os
from flask import Flask, render_template, request, make_response
from winotify import Notification
from flaskwebgui import FlaskUI

def notification(text):
    toast = Notification(app_id="WARP GUI", title="WARP", msg=text)
    toast.show()

def run(command):
    stream = os.popen(command)
    return stream.read()

def status():
    output = run("warp-cli status")
    output = output.split('\n')
    for row in output:
        data = row.split(':', maxsplit=1)
        if data[0] == 'Status update':
                return data[1].strip()
        
def connect():
    result = run('warp-cli connect')
    if result.startswith("Success") == True:
        return True
    return False

def check():
     if status().startswith("Connected") == True:
          return "Your internet is private."
     elif status().startswith("Connecting") == True:
          return "Connecting..."
     elif status().startswith("Disconnected") == True:
          return ("Your internet is not private.")
     
def account_type():
    result = run('warp-cli registration show')
    try:
        data = result.split('\n')
        result = data[0].split(': ')
        return result[1].lower()
    except:
        return False
    
def account():
     if account_type().startswith("free") == True:
          return "WARP"
     elif account_type().startswith("limited") == True:
          return "WARP+"
     elif account_type().startswith("team") == True:
          return "Teams"

def forstatuspage():
    if status().startswith("Connected") == True:
          return "true"
    elif status().startswith("Disconnected") == True:
          return "false"
    elif status().startswith("Connecting") == True:
         return "connecting"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'switch' in request.form:
            if status().startswith("Connected"):
                os.system('warp-cli disconnect')
            else:
                os.system('warp-cli connect')
    return render_template('index.html', connected=status().startswith("Connected"), check=check(), acctype=account())

@app.route("/status", methods=['POST', 'GET'])
def statuspage():
    return forstatuspage()

@app.route("/acctype", methods=['POST', 'GET'])
def accountpage():
    return account()

@app.route("/connect", methods=['POST', 'GET'])
def pageconnect():
    os.system("warp-cli connect")
    notification("Подключаемся...")

@app.route("/disconnect", methods=['POST', 'GET'])
def pagedisconnect():
    os.system("warp-cli disconnect")
    notification("Теперь ваше интернет-подключение больше не конфидециально.")

if __name__ == '__main__':
    FlaskUI(app=app, server="flask", port=5001, width=420, height=450).run()