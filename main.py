import os

from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from shutil import copyfile, move, copytree


UPLOAD_DIRECTORY = os.path.join(os.getcwd(), 'data')

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)


@api.route('/ls')
def list_files():
    """Endpoint to list files on the server."""
    path = request.args.get('path')
    print(path)
    files = []
    folders = []

    search_path = os.path.join(UPLOAD_DIRECTORY, path)
    if is_safe_path(UPLOAD_DIRECTORY, search_path) == False:
        abort(404)

    for filename in os.listdir(search_path):
        path = os.path.join(search_path, filename)
        if os.path.isfile(path):
            files.append(filename)
        else:
            folders.append(filename)
    resp = {}
    resp['files'] = files
    resp['folders'] = folders
    return jsonify(resp)

@api.route('/mkdir', methods=['POST'])
def make_dir():
    """Endpoint to list files on the server."""
    path = request.form.get('path')
    dirname = request.form.get('dirname')

    target_path = ""

    if path is None:
        target_path = UPLOAD_DIRECTORY
    else:
        target_path = os.path.join(UPLOAD_DIRECTORY, path)
    folder_path = os.path.join(target_path, dirname)
    if is_safe_path(UPLOAD_DIRECTORY, folder_path) == False:
        abort(404)
    os.mkdir(folder_path);
    rc = {}
    rc['rc'] = 0
    rc['message'] = "OK"
    return jsonify(rc)

@api.route('/cp', methods=['POST'])
def copy_route():
    """Endpoint to list files on the server."""
    from_path = request.form.get('from_path')
    to_path = request.form.get('to_path')

    full_from_path = ""
    full_to_path = ""
    full_from_path = os.path.join(UPLOAD_DIRECTORY, from_path)
    full_to_path = os.path.join(UPLOAD_DIRECTORY, to_path)
    if is_safe_path(UPLOAD_DIRECTORY, full_from_path) == False:
        abort(404)
    if is_safe_path(UPLOAD_DIRECTORY, full_to_path) == False:
        abort(404)
    if os.path.isfile(full_from_path):
        copyfile(full_from_path, full_to_path)
    else:
        copytree(full_from_path, full_to_path)
    rc = {}
    rc['rc'] = 0
    rc['message'] = "OK"
    return jsonify(rc)

@api.route('/mv', methods=['POST'])
def move_route():
    """Endpoint to list files on the server."""
    from_path = request.form.get('from_path')
    to_path = request.form.get('to_path')

    full_from_path = ""
    full_to_path = ""
    full_from_path = os.path.join(UPLOAD_DIRECTORY, from_path)
    full_to_path = os.path.join(UPLOAD_DIRECTORY, to_path)
    if is_safe_path(UPLOAD_DIRECTORY, full_from_path) == False:
        abort(404)
    if is_safe_path(UPLOAD_DIRECTORY, full_to_path) == False:
        abort(404)
    if os.path.isfile(full_from_path):
        move(full_from_path, full_to_path)
    rc = {}
    rc['rc'] = 0
    rc['message'] = "OK"
    return jsonify(rc)

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
