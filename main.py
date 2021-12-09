import json
from flask import Flask, render_template, request, redirect, url_for

from covid_updates.covid_data_handler import (
    covid_API_request, process_covid_csv_data)
from covid_updates.covid_news_handling import news_API_request

app = Flask(__name__)
CONF = json.load(open("config.json", "r"))
 

@app.route("/")
def index():
    news_articles = news_API_request()["articles"]
    local_covid_cases = covid_API_request(CONF["city"])["data"]
    national_covid_cases = covid_API_request(CONF["nation"], "nation")["data"]
    last7days_cases, _, _ = \
        process_covid_csv_data(local_covid_cases)
    national_last7days_cases, current_hospital_cases, total_deaths = \
        process_covid_csv_data(national_covid_cases)
    return render_template(
        "index.html",
        news_articles=news_articles,
        location="Exeter",
        nation_location="England",
        local_7day_infections=last7days_cases,
        national_7day_infections=national_last7days_cases,
        hospital_cases=current_hospital_cases,
        deaths_total=total_deaths
    )


@app.route("/index", methods=["POST", "GET"])
def update():
    if request.method == "GET":
        update = request.args.get("update")
        update = update.split("update=")[1].split("&")
        return redirect(url_for('index'))
 
 
if __name__ == "__main__":
    app.run(host=CONF.get("host", "0.0.0.0"), port=CONF.get("port", 3000))
