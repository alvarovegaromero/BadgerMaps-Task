from functions import *

if __name__ == "__main__":
    file_path = 'Sample test file - Sheet1.csv'
    headers, filtered_rows, earliest_check_in, latest_check_in = process_csv(file_path)

    # Sort and Show data
    sorted_rows_names = sorted(filtered_rows, key=get_full_name)
    sorted_rows_jobs = sorted(filtered_rows, key=get_job)

    # Show information
    show_information(earliest_check_in, latest_check_in, sorted_rows_names, sorted_rows_jobs)

