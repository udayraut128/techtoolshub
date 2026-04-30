from flask import Blueprint, render_template, request, send_file
import os
import uuid
from moviepy import VideoFileClip

mp3_converter = Blueprint("mp3_converter", __name__)

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
CONVERT_FOLDER = os.path.join(BASE_DIR, "converted")

# Create folders automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERT_FOLDER, exist_ok=True)


@mp3_converter.route("/mp4-to-mp3", methods=["GET", "POST"])
def home():

    converted_file = None

    if request.method == "POST":

        video = request.files.get("video")

        if video:

            # unique filename
            unique_name = str(uuid.uuid4())

            video_path = os.path.join(
                UPLOAD_FOLDER,
                unique_name + ".mp4"
            )

            mp3_filename = unique_name + ".mp3"

            mp3_path = os.path.join(
                CONVERT_FOLDER,
                mp3_filename
            )

            # save video
            video.save(video_path)

            try:
                # convert
                clip = VideoFileClip(video_path)

                clip.audio.write_audiofile(
                    mp3_path,
                    bitrate="192k"
                )

                clip.close()

                converted_file = mp3_filename

            except Exception as e:
                return f"Conversion Error: {e}"

    return render_template(
        "mp3_converter.html",
        converted_file=converted_file
    )


@mp3_converter.route("/download-mp3/<file>")
def download_mp3(file):

    file_path = os.path.join(CONVERT_FOLDER, file)

    return send_file(
        file_path,
        as_attachment=True
    )