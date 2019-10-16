import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # checks for validation in case JS fails
    if not request.form.get("firstname") or not request.form.get("lastname"):
        return render_template("error.html", message="You must provide your name!")

    # inputs form elements into CSV file and redirects to sheet
    with open("survey.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow((request.form.get("firstname"), request.form.get("lastname"), request.form.get("Gender"),
                         request.form.get("student"), request.form.get("comments"), request.form.get("compk")))
        file.close()
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # reads the CSV file and sends it to the table via AJAX to sheet.html
    with open("survey.csv", "r", newline='') as filer:
        read = csv.reader(filer)
        info = list(read)
    return render_template("sheet.html", info=info)