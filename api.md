# API

## Authentication

Basic Authentication

## Endpoints

### GET /ls/{:path}

- [x] implemented

**Parameters:**

  * *string* path: base64-encoded path to directory

**Returns:** Array of file descriptions

**curl:**

		curl -X GET -i 'http://127.0.0.1:8000/ls?path=testdir'

### GET /files/{:path}

- [x] implemented

**Parameters:**

  * *string* path: base64-encoded path to file

**Returns:** The file to download

### POST /files/{:path}

- [ ] implemented

**Parameters:**

  * *string* path: base64-encoded path to file
  * *string* filename: filename

**Returns:** RC

### PATCH /files/{:path}

- [ ] implemented

**Headers:**

  * Content-Range: bytes 0-1023/146515
  * Content-Length: 1024

**Parameters:**

  * *string* path: base64-encoded path to file
  * *string* filename: filename

**Returns:** RC

### POST /cp

- [x] implemented

**Parameters:**

  * *string* from_path: base64-encoded path to file
  * *string* to_path: new path

**Returns:** RC

**curl:**

		curl -X POST -i 'http://127.0.0.1:8000/cp' --data 'from_path=test.txt&to_path=testdir/test2.txt'

### POST /mv

- [x] implemented

**Parameters:**

  * *string* from_path: base64-encoded path to file
  * *string* to_path: new path

**Returns:** RC

**curl:**

		curl -X POST -i 'http://127.0.0.1:8000/cp' --data 'from_path=test.txt&to_path=test2.txt'


### POST /mkdir/{:path}

- [x] implemented

**Parameters:**

  * *string* path: path
  * *string* name: directory name

**Returns:** RC

**curl:**

		curl -X POST -i 'http://127.0.0.1:8000/mkdir' --data 'path=&name=testdir'

### POST /mk/{:path}

- [x] implemented

**Parameters:**

  * *string* path: path to file
  * *string* name: filename

**Returns:** RC

**curl:**

		curl -X POST -i 'http://127.0.0.1:8000/mk' --data 'path=&name=testfile.txt'

### POST /rm/{:path}
- [x] implemented

**Parameters:**

  * *string* path: base64-encoded path to file

**Returns:** RC

### POST /rmdir/{:path}
- [x] implemented

**Parameters:**

  * *string* path: base64-encoded path to file
  * *int* recursive: recursively delete folder and contents (1: true, else: false)

**Returns:** RC


## Ressource Types

### FolderSummary

  * files: FileInfo []
  * dirs:  DirInfo []

### FileInfo

  * name: string,
  * hash_type: string (sha256 | sha512)
  * hash: string hash
  * last_change: unix timestamp

### DirInfo

  * name: string,
  * hash_type: string (sha256 | sha512)
  * hash: string hash
  * last_change: unix timestamp
