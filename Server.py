from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/profile/<username>')
def profile_page(username):
    return 'Welcome to ' + username + "'s profile!"

@app.route('/liam')
def liam():
    return 'Liam is the best!'

if __name__ == '__main__':
    app.run()
