import os
import zipfile
import random
import string
import qrcode

def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def handle_file_upload(files, upload_folder, static_folder, host_url):
    short_id = generate_short_id()

    upload_path = os.path.join(upload_folder, short_id)
    os.makedirs(upload_path, exist_ok=True)

    saved_files = []

    # Save files
    for file in files:
        filename = file.filename
        file_path = os.path.join(upload_path, filename)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        saved_files.append(file_path)

    # Create ZIP
    zip_filename = f"{short_id}.zip"
    zip_path = os.path.join(upload_folder, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in saved_files:
            arcname = os.path.relpath(file_path, upload_path)
            zipf.write(file_path, arcname)

    # Generate URL
    short_url = f"{host_url}file/{short_id}"

    # Generate QR
    qr_filename = f"{short_id}.png"
    qr_path = os.path.join(static_folder, qr_filename)

    img = qrcode.make(short_url)
    img.save(qr_path)

    return short_id, short_url, qr_filename