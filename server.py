from flask import (
    Flask,
    render_template,
)
from flask_assets import (
    Bundle,
    Environment,
)

server = Flask(__name__, instance_relative_config=True)


assets = Environment(server)
css = Bundle('css/bootstrap.css', 'css/bootswatch.css', 'css/base.css', 'css/team.css', output='gen/packed.css')
assets.register('css_all', css)


@server.route('/team')
def team():
    return render_template('team.html')


@server.route('/about')
def about():
    return render_template('about.html')


@server.route('/')
def index():
    return render_template('index.html')
