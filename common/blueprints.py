import functools
import pathlib

import flask

import yaml

swagger = flask.Blueprint('swagger', __name__)
current_directory_path = pathlib.Path(__file__).parent


@swagger.route('/api/v1/email/swagger.json', methods=['GET'])
@functools.lru_cache(maxsize=1)
def host_swagger():
    with (current_directory_path / '..' / 'swagger' / 'email.yml').open('r') as f:
        return flask.jsonify(yaml.load(f.read()))
