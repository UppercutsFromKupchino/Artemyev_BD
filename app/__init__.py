from flask import Flask

app = Flask(__name__)
app.secret_key = 'iwantgamedev'


from app import routes

