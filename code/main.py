import csv

from functions import *
from constants import *
from exception_handler import ExceptionHandler

file = open('./data/Sample test file - Sheet1.csv', 'r', encoding='utf-8')
csvreader = csv.reader(file)

headers = next(csvreader)

filtered_rows = []

required_fields_columns = [STREET_COLUMN, ZIP_COLUMN, CITY_COLUMN, LAST_CHECK_IN_DATE_COLUMN, COMPANY_COLUMN]

exception_handler = ExceptionHandler('exceptions')
exception_handler.save_information("New CSV file processing")

earliest_check_in = None
latest_check_in = None

first_iteration = True

for index, row in enumerate(csvreader):
    if len(row) != CSV_COLUMN_SIZE: # row contains less fields
        exception_handler.save_error(f"Row: {index} contains less fields than expected")

    elif all(item == "" for item in row): # row is empty
        exception_handler.save_error(f"Row: {index} is empty")

    elif any(row[col] == "" for col in required_fields_columns): # a required field is empty (or more)
        exception_handler.save_error(f"One or more required fields are empty in the row: {index}")

    # Exceptions checked - Information retrieval
    elif row[LAST_CHECK_IN_DATE_COLUMN] != None and row[LAST_CHECK_IN_DATE_COLUMN] != '':
        check_in_date = format_date(row[LAST_CHECK_IN_DATE_COLUMN])

        if first_iteration: # First iteration --> Use it as *current* earliest and latest
            first_iteration = False
            earliest_check_in = row
            latest_check_in = row

        elif (format_date(earliest_check_in[LAST_CHECK_IN_DATE_COLUMN]) > check_in_date): 
            earliest_check_in = row

        elif (format_date(latest_check_in[LAST_CHECK_IN_DATE_COLUMN]) < check_in_date): 
            latest_check_in = row

        filtered_rows.append(row)

file.close()

########################################
# Sort and Show data

sorted_rows_names = sorted(filtered_rows, key=get_full_name)
sorted_rows_jobs = sorted(filtered_rows, key=get_job)

show_information(earliest_check_in, latest_check_in, sorted_rows_names, sorted_rows_jobs)

