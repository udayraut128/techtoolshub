from flask import Blueprint, render_template, request
import nepali_datetime

date_converter = Blueprint("date_converter", __name__)

@date_converter.route("/date-converter", methods=["GET", "POST"])
def convert_date():

    result = None

    if request.method == "POST":
        date_type = request.form.get("type")

        try:
            if date_type == "bs_to_ad":
                year = int(request.form.get("year"))
                month = int(request.form.get("month"))
                day = int(request.form.get("day"))

                bs_date = nepali_datetime.date(year, month, day)
                ad_date = bs_date.to_datetime_date()

                result = f"AD: {ad_date}"

            else:
                year = int(request.form.get("year"))
                month = int(request.form.get("month"))
                day = int(request.form.get("day"))

                ad_date = nepali_datetime.date.from_datetime_date(
                    __import__("datetime").date(year, month, day)
                )

                result = f"BS: {ad_date}"

        except Exception as e:
            result = "Invalid Date ❌"

    return render_template("date_converter.html", result=result)