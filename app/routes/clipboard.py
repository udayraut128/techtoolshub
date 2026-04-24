from flask import Blueprint, render_template, request, jsonify
import uuid

clipboard = Blueprint("clipboard", __name__)

CLIPBOARD_DATA = {}


@clipboard.route("/clipboard", methods=["GET", "POST"])
def clipboard_page():

    # 🔹 SAVE / UPDATE
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        text = data.get("text", "")
        clip_id = data.get("id")

        # 👉 If ID exists → update
        if clip_id and clip_id in CLIPBOARD_DATA:
            CLIPBOARD_DATA[clip_id] = text
        else:
            # 👉 Create new only once
            clip_id = str(uuid.uuid4())[:8]
            CLIPBOARD_DATA[clip_id] = text

        return jsonify({
            "id": clip_id,
            "url": f"/clipboard?id={clip_id}"
        })

    # 🔹 FETCH (GET)
    clip_id = request.args.get("id")
    data = ""

    if clip_id:
        data = CLIPBOARD_DATA.get(clip_id, "")

    return render_template(
        "clipboard.html",
        data=data,
        clip_id=clip_id
    )