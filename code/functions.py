import csv
from datetime import datetime


from constants import *
from exception_handler import ExceptionHandler

########################################
# Functions

# @brief Function for showing the information related to a list of customer
def show_customers_information(rows):
    result = ""

    for row in rows:
        result += "\n" + "- " + (row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN] + " - Last check in: " + row[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + row[JOB_COLUMN])
    
    return result

# @brief Function for showing the information of a certain customer
def show_customer_information(row):
    return (row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN] + " - Last check in: " + row[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + row[JOB_COLUMN])

# @brief Function for showing the information
def show_information(earliest_check_in, latest_check_in, sorted_rows_names, sorted_rows_jobs):  
    print("\n****************************************")
    print("Customer with earliest check-in date: " , show_customer_information(earliest_check_in))
    print("Customer with latest check-in date: " , show_customer_information(latest_check_in))
    print("****************************************")
    print("List with customer’s full names ordered alphabetically: " , show_customers_information(sorted_rows_names))
    print("****************************************")
    print("List of the jobs ordered alphabetically: " , show_customers_information(sorted_rows_jobs))
    print("****************************************\n")


# @brief Function for getting the job of a certain row (array)
def get_job(row): #used as key for the sort function
    return row[JOB_COLUMN]

# @brief Function for getting the full name of a certain row (array)
def get_full_name(row): #used as key for the sort function
    return row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN]


# @brief Function for formatting the date into a certain format to allow operating with it
def format_date(date):
    return (datetime.strptime(date, "%d/%m/%Y"))

# @brief Function for processing a CSV file, and retrieving the earliest and latest check in dates and filtered rows
def process_csv(file_path):
    with open(f'./data/{file_path}', 'r', encoding='utf-8') as file:
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
            if len(row) != CSV_COLUMN_SIZE: #Row have fewer fields than expected
                exception_handler.save_error(f"Row: {index} contains fewer fields than expected")
            elif all(item == "" for item in row): #Row is empty
                exception_handler.save_error(f"Row: {index} is empty")
            elif any(row[col] == "" for col in required_fields_columns): #Row doesn't contain (at least) required field
                exception_handler.save_error(f"One or more required fields are empty in the row: {index}")
                
            else: #Information retrieval. Get earliest and lastest check in date
                check_in_date = format_date(row[LAST_CHECK_IN_DATE_COLUMN])

                if first_iteration:
                    first_iteration = False
                    earliest_check_in = row
                    latest_check_in = row
                elif format_date(earliest_check_in[LAST_CHECK_IN_DATE_COLUMN]) > check_in_date:
                    earliest_check_in = row
                elif format_date(latest_check_in[LAST_CHECK_IN_DATE_COLUMN]) < check_in_date:
                    latest_check_in = row

                filtered_rows.append(row)

    return headers, filtered_rows, earliest_check_in, latest_check_in
