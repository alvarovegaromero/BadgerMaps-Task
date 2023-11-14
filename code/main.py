import csv
from datetime import datetime

from constants import *
from exception_handler import ExceptionHandler

########################################
# Functions

# @brief Function for showing the information
def show_customer_data(rows):
    result = ""

    if(isinstance(rows, list) and all(isinstance(sub_arr, list) for sub_arr in rows)): # is array of arrays (rows)
        for row in rows:
            result += "\n" + "- " + (row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN] + " - Last check in: " + row[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + row[JOB_COLUMN])
    else: #or only one array (one row)
        result += (rows[FIRST_NAME_COLUMN] + " " + rows[LAST_NAME_COLUMN] + " - Last check in: " + rows[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + rows[JOB_COLUMN])

    return result

# @brief Function for getting the job of a certain row (array)
def get_job(row): #used as key for the sort function
    return row[JOB_COLUMN]

# @brief Function for getting the full name of a certain row (array)
def get_full_name(row): #used as key for the sort function
    return row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN]

########################################
# Read data and Check exceptions

file = open('./data/Sample test file - Sheet1.csv', 'r', encoding='utf-8')
csvreader = csv.reader(file)

headers = next(csvreader)

filtered_rows = []
required_fields = ["Street", "Zip", "City", "Last Check-In Date", "Company"]

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

    elif any(row[col] == "" for col in [STREET_COLUMN, ZIP_COLUMN, CITY_COLUMN, LAST_CHECK_IN_DATE_COLUMN, COMPANY_COLUMN]): # a required field is empty (or more)
        exception_handler.save_error(f"One or more required fields are empty in the row: {index}")

    # Information retrieval
    elif row[LAST_CHECK_IN_DATE_COLUMN] != None and row[LAST_CHECK_IN_DATE_COLUMN] != '':
        check_in_date = datetime.strptime(row[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y")

        if first_iteration:
            first_iteration = False
            earliest_check_in = row
            latest_check_in = row

        if datetime.strptime(earliest_check_in[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y") > check_in_date:
            earliest_check_in = row

        elif datetime.strptime(latest_check_in[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y") < check_in_date:
            latest_check_in = row

        filtered_rows.append(row)

file.close()

########################################
# Sort and Show data

sorted_rows_names = sorted(filtered_rows, key=get_full_name)
sorted_rows_jobs = sorted(filtered_rows, key=get_job)

print("\n****************************************")
print("Customer with earliest check-in date: " , show_customer_data(earliest_check_in))
print("Customer with latest check-in date: " , show_customer_data(latest_check_in))
print("****************************************")
print("List with customer’s full names ordered alphabetically: " , show_customer_data(sorted_rows_names))
print("****************************************")
print("List of the jobs ordered alphabetically: " , show_customer_data(sorted_rows_jobs))
print("****************************************\n")

