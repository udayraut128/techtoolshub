from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_file
import pandas as pd
import os
from app.services.group_service import create_balanced_groups, calculate_stats

group = Blueprint('group', __name__)


# ---------------------------------
# Group Generator Page
# ---------------------------------
@group.route("/group-generator", methods=["GET", "POST"])
def group_generator():

    if request.method == "POST":
        file = request.files["file"]
        num_groups = int(request.form["groups"])

        if not file or file.filename == "":
            return redirect(url_for("group.group_generator"))

        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath) if file.filename.endswith(".csv") else pd.read_excel(filepath)
        except:
            return "Error reading file"

        # Required columns check
        required_columns = ["Grade in pre", "Gender"]
        for col in required_columns:
            if col not in df.columns:
                return f"Missing column: {col}"

        groups = create_balanced_groups(df, num_groups)

        # 🔥 Build data for template
        group_data = []
        group_averages = []
        all_students = []

        for i, g in enumerate(groups):
            avg, male, female = calculate_stats(g)
            group_averages.append(avg)

            group_data.append({
                "students": g,
                "avg": avg,
                "male": male,
                "female": female
            })

            for student in g:
                student_copy = student.copy()
                student_copy["Group"] = f"Group {i+1}"
                all_students.append(student_copy)

        # Save Excel
        output_file = os.path.join(current_app.config['UPLOAD_FOLDER'], "group_output.xlsx")
        pd.DataFrame(all_students).to_excel(output_file, index=False)

        highest_avg = max(group_averages)
        lowest_avg = min(group_averages)
        gap = round(highest_avg - lowest_avg, 2)
        overall_avg = round(df["Grade in pre"].mean(), 2)

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
# Download Excel File
# ---------------------------------
@group.route("/download-group")
def download_group():

    file_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        "group_output.xlsx"
    )

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    return "File not found", 404