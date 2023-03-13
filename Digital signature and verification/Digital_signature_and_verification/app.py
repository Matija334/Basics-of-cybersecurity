import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        file = request.files.get('file')
        private_key = request.files.get('key').read()
        if not file or not private_key:
            return render_template('sign.html', error="Upload both file and private key!")

        try:
            key = RSA.import_key(private_key)
            file_hash = SHA256.new(file.read())
            signature = pkcs1_15.new(key).sign(file_hash)

            with open('uploads/' + "signature.txt", 'wb') as f:
                f.write(base64.b64encode(signature))

            return render_template('index.html', result="File signed successfully!")
        except Exception as e:
            return render_template('sign.html', error=f"Error signing file: {str(e)}")
    else:
        return render_template('sign.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        file = request.files.get('file').read()
        public_key = request.files.get('key').read()
        signature = request.files.get('signature').read()

        if not file or not public_key or not signature:
            return render_template('verify.html', error="Upload all requested files!")

        try:
            key = RSA.import_key(public_key)
            file_hash = SHA256.new(file)

            pkcs1_15.new(key).verify(file_hash, base64.b64decode(signature))
            return render_template('index.html', result="Signature is valid!")
        except ValueError:
            return render_template('verify.html', error="Signature is NOT valid!")
        except Exception as e:
            return render_template('verify.html', error=f"Error verifying signature: {str(e)}")
    else:
        return render_template('verify.html')


if __name__ == '__main__':
    app.run()