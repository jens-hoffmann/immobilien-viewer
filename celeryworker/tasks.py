import os
from collections import namedtuple

import requests

from celerysetup import app as celery_app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


fields = ['Aktenzeichen', 'Amtsgericht', 'Objekt', 'Verkehrswert', 'Termin', 'Beschreibung']
Immobilie = namedtuple("Immobilie", fields,
                       defaults=(None,) * len(fields))

def get_elements_from_table(driver, table):
    wait = WebDriverWait(driver, 10)
    line_elements = table.find_elements(By.XPATH, ".//tbody/tr")

    immo_dict_list = list()
    immo_dict = dict()

    for line in line_elements:
        columns = line.find_elements(By.XPATH, "./td")
        link_element = line.find_elements(By.XPATH, "./td/b/a")
        if len(link_element) > 0:
            original_window = driver.current_window_handle
            assert len(driver.window_handles) == 1

            link_element[0].click()
            wait.until(EC.number_of_windows_to_be(2))
            # Loop through until we find a new window handle
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            detail_table_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
            for detail_row in detail_table_rows:
                detail_columns = detail_row.find_elements(By.XPATH, "./td")
                if detail_columns[0].text == "Beschreibung:":
                    immo_dict['Beschreibung'] = detail_columns[1].text
            driver.close()
            driver.switch_to.window(original_window)

        if len(columns) > 1:
            if any(columns[0].text.startswith(key) for key in Immobilie._fields):
                key = next((x for x in Immobilie._fields if columns[0].text.startswith(x)), None)
                if key is not None:
                    immo_dict[key] = columns[1].text

        elif len(columns) == 1:
            immo = Immobilie(**immo_dict)
            immo_dict_list.append(immo)

    return immo_dict_list

@celery_app.task(name='zvg_scraping', queue="scrapingtasks")
def zvg_scraping(state: str):
    url = 'https://www.zvg-portal.de/index.php?button=Termine%20suchen'

    selenium_service = os.environ.get('SELENIUM_SERVICE')

    driver = webdriver.Remote(selenium_service, options=webdriver.ChromeOptions())
    driver.get(url)
    select_state_element = driver.find_element(By.XPATH, "//select[@name='land_abk']")
    select_state_class = Select(select_state_element)
    select_state_class.select_by_visible_text(state)

    select_object_element = driver.find_element(By.XPATH, "//select[@name='obj_liste']")
    select_object_class = Select(select_object_element)
    select_object_class.select_by_value('3')
    select_object_class.select_by_value('15')

    driver.find_element(By.XPATH, "//button[text()='<=']").click()
    driver.find_element(By.XPATH, "//button[text()='Suchen']").click()

    table_elements = driver.find_elements(By.XPATH, "//table")

    immo_dict_list = list()
    if len(table_elements) == 1:    # no tables for multiple pages
        table = driver.find_element(By.XPATH, "//table")
        immo_dict_list = get_elements_from_table(driver, table)
    elif len(table_elements) == 3:  # additional tables for pages
        pagenr = 0
        while True:
            pages = driver.find_elements(By.XPATH, "//table[1]/tbody/tr/td/button[@class='seiten_nr']")
            if pagenr == len(pages):
                break
            pages[pagenr].click()
            table = driver.find_element(By.XPATH, "//table[2]")
            immo_dict_list += get_elements_from_table(driver, table)

            pagenr += 1

    driver.quit()

    df = pd.DataFrame.from_records(immo_dict_list, columns=Immobilie._fields)
    df = df.astype('string')
    df['Aktenzeichen'] = df['Aktenzeichen'].str.replace('(?P<aktenzeichen>\d+ K \d+\/\d+) \(Detailansicht\)', lambda m: m.groupdict()['aktenzeichen'], regex=True)
    df = df[~(df['Termin'].str.endswith("wurde aufgehoben.", na=False))]
    df[["Objekttyp", "Lage"]] = df['Objekt'].str.split(': ', expand=True)
    df["Objekttyp"] = df["Objekttyp"].str.replace("Einfamilienhaus", "house")
    repl = lambda m: m.groupdict()['wert']
    df['Verkehrswert_zahl'] = df['Verkehrswert'].str.replace('(?P<wert>\d+\.\d+).+', repl,
                                                        regex=True)
    df['Verkehrswert_zahl'] = pd.to_numeric(df['Verkehrswert_zahl'].str.replace('[\.]', '', regex=True), errors='coerce')
    df['Verkehrswert_zahl'] = df['Verkehrswert_zahl'].fillna(0)

    for k, row in df.iterrows():
        payload = {}
        row_dict = row.to_dict()
        payload['title'] = row_dict['Objekt'].strip()
        payload['description'] = row_dict['Beschreibung'].strip()
        payload['provider'] = f"Amtsgericht: {row_dict['Amtsgericht'].strip()}"
        payload['provider_id'] = row_dict['Aktenzeichen']
        payload['price'] = row_dict['Verkehrswert_zahl']
        payload['url'] = url
        payload['location'] = row_dict['Lage']
        payload['type'] = row_dict['Objekttyp']
        payload['resource'] = {
            "name": "ZVG-Portal",
            "base_url": url,
            "crawler": __name__
        }
        postresult.delay(payload)

        return f"Scraping {state} successful."

@celery_app.task(name='postresult', queue="posttasks")
def postresult(payload: dict):
    webserver = os.environ.get('WEBSERVER', 'localhost:8000')
    url = f"http://{webserver}/immoviewer/api/immobilie/"
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    if not response.status_code in list([201, 409]):
        handle_failed_task.delay(payload)
        raise Exception(f"Posting task failed with status {response.status_code}: {response.text}")
    else:
        return f"Post successful with status: {response.status_code}"

@celery_app.task(name='handle_failed_task', queue='dead_letter')
def handle_failed_task( payload: str):
    return f"Failed task with payload: {payload}"
