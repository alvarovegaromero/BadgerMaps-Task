#import pandas as pd 
import csv #manage csv files
from datetime import datetime #manage dates easily 
import logging

# Constants for mapping columns in CSV with indexes of the array
FIRST_NAME_COLUMN = 0
LAST_NAME_COLUMN = 1
STREET_COLUMN = 2
ZIP_COLUMN = 3
CITY_COLUMN = 4
TYPE_COLUMN = 5
LAST_CHECK_IN_DATE_COLUMN = 6
JOB_COLUMN = 7
PHONE_COLUMN = 8
COMPANY_COLUMN = 9
CSV_COLUMN_SIZE = 10 #size of the CSV file
########################################

# Functions used

# @brief Function for showing the information
def show_customer_data(rows):
    result = ""
    
    if(isinstance(rows, list) and all(isinstance(sub_arr, list) for sub_arr in rows)): # is array of arrays (rows)
        for row in rows:
            result += "\n" + "- " + (row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN] + " - Last check in: " + row[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + row[JOB_COLUMN])
    else: #or only one array (one row)
        result += (rows[FIRST_NAME_COLUMN] + " " + rows[LAST_NAME_COLUMN] + " - Last check in: " + rows[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + rows[JOB_COLUMN])

    return result

def get_job(row): #used as key for the sort function
    return row[JOB_COLUMN]

def get_full_name(row): #used as key for the sort function
    return row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN]

########################################


# Read data
file = open('Sample test file - Sheet1.csv', 'r', encoding='utf-8')

csvreader = csv.reader(file)

headers = []
headers = next(csvreader)

rows = [] 
for row in csvreader:
    rows.append(row) 

# Check exceptions

filtered_rows = []
sorted_rows_names = []
required_fields = ["Street", "Zip", "City", "Last Check-In Date", "Company"]

logging.basicConfig(filename='exceptions.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') #INFO OR SUPERIOR

logging.info("New CSV file processing")

for row in rows:
    if(len(row) != 10):
        logging.error("Row contains less fields than expected")
    elif(all(item == "" for item in row)):
        logging.error("Empty row found")
    else:
        row_dict = {field: value for field, value in zip(required_fields, row)}
        if not all(row_dict[field] for field in required_fields) or (row[LAST_CHECK_IN_DATE_COLUMN] == ""): # se me cuela el check in
            logging.error("One or more required fields are empty in the row")
        else:
            #print(row)            
            filtered_rows.append(row)
    
logging.shutdown()

#########################################

# Information retrievals

earliest_check_in = None
latest_check_in = None
first_iteration = True

for filtered_row in filtered_rows:
    if filtered_row[LAST_CHECK_IN_DATE_COLUMN] != None and filtered_row[LAST_CHECK_IN_DATE_COLUMN] != '':
        check_in_date = datetime.strptime(filtered_row[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y")

        if first_iteration:
            first_iteration = False
            earliest_check_in = filtered_row
            latest_check_in = filtered_row

        if  datetime.strptime(earliest_check_in[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y") > check_in_date:
            earliest_check_in = filtered_row

        elif datetime.strptime(latest_check_in[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y") < check_in_date:
            latest_check_in = filtered_row

sorted_rows_names = sorted(filtered_rows, key=get_full_name)
sorted_rows_jobs = sorted(filtered_rows, key=get_job)

########################################

# Show data

print("\n****************************************")
print("Customer with earliest check-in date: " , show_customer_data(earliest_check_in))
print("Customer with latest check-in date: " , show_customer_data(latest_check_in))
print("****************************************")
print("List with customer’s full names ordered alphabetically: " , show_customer_data(sorted_rows_names))
print("****************************************")
print("List of the jobs ordered alphabetically: " , show_customer_data(sorted_rows_jobs))
print("****************************************\n")
########################################
"""
"""

file.close()



#doubt about exeptions
#
#Al ser los campos requeridos estos: : Street, Zip, City, Last Check-in Date and 
#Company, si alguna fila tiene estos campos pero no tiene el nombre y/o la de trabajos, que deberia hacer para cuando me toque ordenar las filas por nombre y job

""" Using pandas
df = pd.read_csv('Sample test file - Sheet1.csv', encoding='utf-8')

# Convierte la columna de fechas al formato datetime
df['Last Check-In Date'] = pd.to_datetime(df['Last Check-In Date'], format='%d/%m/%Y', errors='coerce')

# Encuentra la fecha más temprana y la más reciente
earliest_check_in = df[df['Last Check-In Date'] == df['Last Check-In Date'].min()]
latest_check_in = df[df['Last Check-In Date'] == df['Last Check-In Date'].max()]

# Muestra los resultados
print("Cliente con la fecha de check-in más temprana:")
print(earliest_check_in)
print("\nCliente con la fecha de check-in más reciente:")
print(latest_check_in)
"""

