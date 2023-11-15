from constants import *
from datetime import datetime

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

def show_information(earliest_check_in, latest_check_in, sorted_rows_names, sorted_rows_jobs):  
    print("\n****************************************")
    print("Customer with earliest check-in date: " , show_customer_data(earliest_check_in))
    print("Customer with latest check-in date: " , show_customer_data(latest_check_in))
    print("****************************************")
    print("List with customer’s full names ordered alphabetically: " , show_customer_data(sorted_rows_names))
    print("****************************************")
    print("List of the jobs ordered alphabetically: " , show_customer_data(sorted_rows_jobs))
    print("****************************************\n")

# @brief Function for getting the job of a certain row (array)
def get_job(row): #used as key for the sort function
    return row[JOB_COLUMN]

# @brief Function for getting the full name of a certain row (array)
def get_full_name(row): #used as key for the sort function
    return row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN]

def format_date(date):
    return (datetime.strptime(date, "%d/%m/%Y"))