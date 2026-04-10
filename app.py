from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify, send_from_directory
import pandas as pd
import os
import qrcode
import random
import string
import uuid

app = Flask(__name__)

# -------------------------------
# Configurations
# -------------------------------
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Store file mappings (temporary memory)
file_map = {}


# ---------------------------------
# Snake Distribution Algorithm
# ---------------------------------
def create_balanced_groups(df, num_groups):
    df = df.sort_values(by="Grade in pre", ascending=False).reset_index(drop=True)
    groups = [[] for _ in range(num_groups)]

    direction = 1
    group_index = 0

    for _, row in df.iterrows():
        groups[group_index].append(row.to_dict())

        if direction == 1:
            group_index += 1
            if group_index == num_groups:
                group_index -= 1
                direction = -1
        else:
            group_index -= 1
            if group_index < 0:
                group_index += 1
                direction = 1

    return groups


# ---------------------------------
# Calculate Stats
# ---------------------------------
def calculate_stats(group):
    df = pd.DataFrame(group)
    avg_marks = round(df["Grade in pre"].mean(), 2)
    male_count = len(df[df["Gender"] == "Male"])
    female_count = len(df[df["Gender"] == "Female"])
    return avg_marks, male_count, female_count


# ---------------------------------
# Generate Short ID
# ---------------------------------
def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# ---------------------------------
# Home Page
# ---------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------
# QR Code Generator
# ---------------------------------
@app.route("/qr", methods=["GET", "POST"])
def qr():
    qr_image = None

    if request.method == "POST":
        url = request.form["url"]

        img = qrcode.make(url)

        filename = ''.join(random.choices(string.ascii_letters, k=6)) + ".png"
        path = os.path.join(STATIC_FOLDER, filename)
        img.save(path)

        qr_image = f"/static/{filename}"

    return render_template("qr.html", qr_image=qr_image)


# ---------------------------------
# Group Generator Tool
# ---------------------------------
@app.route("/group-generator", methods=["GET", "POST"])
def group_generator():

    if request.method == "POST":

        file = request.files["file"]
        num_groups = int(request.form["groups"])

        if not file or file.filename == "":
            return redirect(url_for("group_generator"))

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            if file.filename.endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
        except:
            return "Error reading file"

        required_columns = ["Grade in pre", "Gender"]
        for col in required_columns:
            if col not in df.columns:
                return f"Missing column: {col}"

        groups = create_balanced_groups(df, num_groups)

        group_data = []
        all_students = []
        group_averages = []

        for i, group in enumerate(groups):

            avg, male, female = calculate_stats(group)
            group_averages.append(avg)

            group_data.append({
                "students": group,
                "avg": avg,
                "male": male,
                "female": female
            })

            for student in group:
                student_copy = student.copy()
                student_copy["Group"] = f"Group {i+1}"
                all_students.append(student_copy)

        highest_avg = max(group_averages)
        lowest_avg = min(group_averages)
        gap = round(highest_avg - lowest_avg, 2)
        overall_avg = round(df["Grade in pre"].mean(), 2)

        output_file = os.path.join(UPLOAD_FOLDER, "group_output.xlsx")
        pd.DataFrame(all_students).to_excel(output_file, index=False)

        return render_template(
            "result.html",
            groups=group_data,
            highest_avg=highest_avg,
            lowest_avg=lowest_avg,
            gap=gap,
            overall_avg=overall_avg
        )

    return render_template("group_generator.html")


# ---------------------------------
# Download Result File
# ---------------------------------
@app.route("/download")
def download():
    file_path = os.path.join(UPLOAD_FOLDER, "group_output.xlsx")
    return send_file(file_path, as_attachment=True)


# ---------------------------------
# Share Page
# ---------------------------------
@app.route("/share")
def share():
    return render_template("share.html")


# ---------------------------------
# Upload File (QR + Link)
# ---------------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    unique_name = str(uuid.uuid4()) + "_" + file.filename
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(file_path)

    short_id = generate_short_id()
    file_map[short_id] = unique_name

    short_url = f"{request.host_url}file/{short_id}"

    # QR Code
    qr_filename = f"{short_id}.png"
    qr_path = os.path.join(STATIC_FOLDER, qr_filename)

    img = qrcode.make(short_url)
    img.save(qr_path)

    return jsonify({
        "url": short_url,
        "qr": f"/static/{qr_filename}"
    })


# ---------------------------------
# Show Download Page (NO auto download)
# ---------------------------------
@app.route("/file/<short_id>")
def file_page(short_id):
    if short_id in file_map:
        return render_template("download.html", file_id=short_id)
    return "File not found", 404


# ---------------------------------
# Actual Download (button click)
# ---------------------------------
@app.route("/download/<short_id>")
def download_file(short_id):
    if short_id in file_map:
        filename = file_map[short_id]
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return "File not found", 404


# ---------------------------------
# Run App
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)