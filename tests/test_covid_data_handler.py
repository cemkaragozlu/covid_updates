from covid_updates.covid_data_handler import (
    parse_csv_data,
    process_covid_csv_data,
    covid_API_request,
    schedule_covid_updates
)


def test_parse_csv_data():
    data = parse_csv_data('tests/nation_2021-10-28.csv')
    assert len(data) == 638


def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'tests/nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544


def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)


def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=1, update_name='update test')
