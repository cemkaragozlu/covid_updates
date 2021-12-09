import time
import sched
import requests
import logging
from urllib.parse import urlencode
from json import dumps


def parse_csv_data(path):
    with open(path, "r") as f:
        lines = [x[:-1].split(",") for x in f.readlines()]
    result = []
    for i in range(1, len(lines)):
        obj = {}
        for title in range(7):
            obj.update({lines[0][title]: lines[i][title]})
        result.append(obj)
    return result


def process_covid_csv_data(rows):
    last7days_cases = 0
    current_hospital_cases = None
    total_deaths = None
    start_counting = False
    counter = 0
    for row in range(len(rows)):
        new_cases = rows[row]["newCasesBySpecimenDate"]
        cases = rows[row]["hospitalCases"]
        deaths = rows[row]["cumDailyNsoDeathsByDeathDate"]
        if current_hospital_cases is None and cases:
            current_hospital_cases = int(cases)
        if total_deaths is None and deaths:
            total_deaths = int(deaths)
        # ignore 1st valid entry for last 7 days cases
        if new_cases and not start_counting:
            start_counting = True
            continue
        if start_counting and counter < 7:
            last7days_cases += int(new_cases)
            counter += 1
    logging.info("Covid data processing successful")
    return last7days_cases, current_hospital_cases, total_deaths


def covid_API_request(location="exeter", location_type="ltla"):
    filters = [
        f"areaType={ location_type }",
        f"areaName={ location }"
    ]

    structure = {
        "areaType": "areaType",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "date": "date",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate",
        "hospitalCases": "cumDeaths28DaysByPublishDate",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate"
    }

    api_params = {
        "filters": str.join(";", filters),
        "structure": dumps(structure, separators=(",", ":"))
    }
    encoded_params = urlencode(api_params)
    endpoint = f"/v1/data?{ encoded_params }"
    request = requests.get(f"https://api.coronavirus.data.gov.uk{endpoint}")
    logging.info(f"Covid API request status: {request}")
    return request.json()


def schedule_covid_updates(update_interval, update_name):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(update_interval, 1, covid_API_request)
    logging.info(f"Covid updates scheduled for {update_interval}")
    s.run()
