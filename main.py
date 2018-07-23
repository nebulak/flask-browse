import os

from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_DIRECTORY = './data'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)


@api.route('/ls')
def list_files():
    """Endpoint to list files on the server."""
    path = request.args.get('path')
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route('/files/<path:path>')
def get_file(path):
    """ Download a file.

        Download a file from server.

        :param string path: base64-encoded path in url
        :return: The requested file
    """
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route('/files/path', methods=['POST'])
def post_file():
    """Upload a file.
    """
    path = request.args.get('path')
    filename = request.args.get('filename')

    if '/' in filename:
        # Return 400 BAD REQUEST
        abort(400, 'no subdirectories directories allowed')

    filename = secure_filename(filename)

    with open(os.path.join(UPLOAD_DIRECTORY, filename), 'wb') as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return '', 201


# source: https://security.openstack.org/guidelines/dg_using-file-paths.html
def is_safe_path(basedir, path, follow_symlinks=True):
  # resolves symbolic links
  if follow_symlinks:
    return os.path.realpath(path).startswith(basedir)

  return os.path.abspath(path).startswith(basedir)



if __name__ == '__main__':
    api.run(debug=True, port=8000)
