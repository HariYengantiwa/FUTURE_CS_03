## Features
- Upload any file and encrypt it using AES-256-GCM with a passphrase.
- Download encrypted files, or upload an encrypted file and decrypt it with the passphrase.
- If decrypted content is text, it is displayed in-browser.
- Simple moving blue particles visual effect over a background video.


## Setup
1. Create a Python virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Place your background video at `static/video.mp4` (or remove the video tag in `templates/index.html`).
4. Run: `python app.py` and open `http://127.0.0.1:5000`


## Security notes (demo only)
- This is a demo. For production use:
- Use HTTPS.
- Run behind a production WSGI server (gunicorn/uvicorn) and reverse proxy.
- Use secure storage for files and consider HSM or KMS for key management.
- Rate-limit and protect endpoints.