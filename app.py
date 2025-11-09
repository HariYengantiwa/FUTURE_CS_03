from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from io import BytesIO
import os
import magic
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

app = Flask(__name__)
app.secret_key = get_random_bytes(16)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# AES constants
KDF_SALT_BYTES = 16
AES_KEY_BYTES = 32
NONCE_BYTES = 12
TAG_BYTES = 16
KDF_ITERATIONS = 100000


def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=AES_KEY_BYTES, count=KDF_ITERATIONS)


def encrypt_bytes(data, password):
    salt = get_random_bytes(KDF_SALT_BYTES)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=get_random_bytes(NONCE_BYTES))
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return salt + cipher.nonce + tag + ciphertext


def decrypt_bytes(blob, password):
    salt = blob[:KDF_SALT_BYTES]
    nonce = blob[KDF_SALT_BYTES:KDF_SALT_BYTES + NONCE_BYTES]
    tag = blob[KDF_SALT_BYTES + NONCE_BYTES:KDF_SALT_BYTES + NONCE_BYTES + TAG_BYTES]
    ciphertext = blob[KDF_SALT_BYTES + NONCE_BYTES + TAG_BYTES:]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    action = request.form.get('action')
    password = request.form.get('password')
    file = request.files.get('file')

    if not file or file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    raw = file.read()

    try:
        if action == 'encrypt':
            if not password:
                flash('Please enter a password to encrypt')
                return redirect(url_for('index'))
            encrypted = encrypt_bytes(raw, password)
            out_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.enc')
            with open(out_path, 'wb') as f:
                f.write(encrypted)
            flash(f'Encrypted file saved as {filename}.enc')
            return redirect(url_for('index'))

        elif action == 'decrypt':
            if not password:
                flash('Please enter a password to decrypt')
                return redirect(url_for('index'))

            decrypted = decrypt_bytes(raw, password)

            # Detect MIME type
            m = magic.Magic(mime=True)
            mime_type = m.from_buffer(decrypted)

            if mime_type.startswith('text'):
                text = decrypted.decode('utf-8', errors='replace')
                return render_template('display_text.html', text=text, filename=filename)
            else:
                return send_file(BytesIO(decrypted), download_name=filename.replace('.enc', ''), as_attachment=True)

        else:
            flash('Invalid action selected')
            return redirect(url_for('index'))

    except Exception as e:
        flash('Error: ' + str(e))
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
