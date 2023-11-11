import csv
from datetime import datetime
import logging

from constants import *

class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.headers = []

    def read_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            self.headers = next(csvreader)
            return [row for row in csvreader]

class DataProcessor:
    def __init__(self, rows):
        self.filtered_rows = []
        self.earliest_check_in = None
        self.latest_check_in = None
        self.sorted_rows_names = []
        self.sorted_rows_jobs = []

        self.rows = rows

    def check_exceptions(self):
        required_fields = ["Street", "Zip", "City", "Last Check-In Date", "Company"]

        for index, row in enumerate(self.rows):
            if len(row) != CSV_COLUMN_SIZE:
                ExceptionLogger.log_error(f"Row: {index} contains fewer fields than expected")
            elif all(item == "" for item in row):
                ExceptionLogger.log_error(f"Row: {index} is empty")
            else:
                if any(row[col] == "" for col in [STREET_COLUMN, ZIP_COLUMN, CITY_COLUMN, LAST_CHECK_IN_DATE_COLUMN, COMPANY_COLUMN]):
                    ExceptionLogger.log_error(f"One or more required fields are empty in the row: {index}")
                else:
                    self.filtered_rows.append(row)

    def process_information(self):
        first_iteration = True

        for filtered_row in self.filtered_rows:
            if filtered_row[LAST_CHECK_IN_DATE_COLUMN] != "" and filtered_row[LAST_CHECK_IN_DATE_COLUMN] is not None:
                check_in_date = datetime.strptime(filtered_row[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y")

                if first_iteration:
                    first_iteration = False
                    self.earliest_check_in = filtered_row
                    self.latest_check_in = filtered_row

                if datetime.strptime(self.earliest_check_in[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y") > check_in_date:
                    self.earliest_check_in = filtered_row

                elif datetime.strptime(self.latest_check_in[LAST_CHECK_IN_DATE_COLUMN], "%d/%m/%Y") < check_in_date:
                    self.latest_check_in = filtered_row

        self.sorted_rows_names = sorted(self.filtered_rows, key=self.get_full_name)
        self.sorted_rows_jobs = sorted(self.filtered_rows, key=self.get_job)

    def display_data(self):
        print("\n****************************************")
        print("Customer with earliest check-in date: ", self.show_customer_data(self.earliest_check_in))
        print("Customer with latest check-in date: ", self.show_customer_data(self.latest_check_in))
        print("****************************************")
        print("List with customer’s full names ordered alphabetically: ", self.show_customer_data(self.sorted_rows_names))
        print("****************************************")
        print("List of the jobs ordered alphabetically: ", self.show_customer_data(self.sorted_rows_jobs))
        print("****************************************\n")

    @staticmethod
    def show_customer_data(rows):
        result = ""

        if isinstance(rows, list) and all(isinstance(sub_arr, list) for sub_arr in rows):
            for row in rows:
                result += "\n" + "- " + (
                        row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN] + " - Last check in: " +
                        row[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + row[JOB_COLUMN]
                )
        else:
            result += (
                    rows[FIRST_NAME_COLUMN] + " " + rows[LAST_NAME_COLUMN] + " - Last check in: " +
                    rows[LAST_CHECK_IN_DATE_COLUMN] + " - Job: " + rows[JOB_COLUMN]
            )

        return result

    @staticmethod
    def get_job(row):
        return row[JOB_COLUMN]

    @staticmethod
    def get_full_name(row):
        return row[FIRST_NAME_COLUMN] + " " + row[LAST_NAME_COLUMN]

class ExceptionLogger:
    @staticmethod
    def log_error(message):
        logging.error(message)

if __name__ == "__main__":
    csv_handler = DataReader('./data/Sample test file - Sheet1.csv')
    rows = csv_handler.read_data()

    data_processor = DataProcessor(rows)
    data_processor.check_exceptions()
    data_processor.process_information()
    data_processor.display_data()