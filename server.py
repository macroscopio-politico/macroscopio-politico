from flask import Flask, render_template
from flask_assets import Environment, Bundle

server = Flask(__name__)
assets = Environment(server)

css = Bundle('css/base.css', 'css/team.css', output='gen/packed.css')
assets.register('css_all', css)


@server.after_request
def add_header(response):
    response.headers["Cache-Control"] = "public, max-age=300"
    return response


@server.route('/team')
def team():
    return render_template('team.html')


@server.route('/about')
def about():
    return render_template('about.html')


@server.route('/')
def index():
    return render_template('index.html')
