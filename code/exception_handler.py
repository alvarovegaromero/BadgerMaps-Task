import logging

class ExceptionHandler:

    def __init__(self, filename):
        self.filename = filename
        self.initialize()

    def initialize(self):
        logging.basicConfig(filename=f'./exceptions/{self.filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def __del__(self):
        logging.shutdown()

    def save_information(self, message):
        logging.info(f'{message}')

    def save_error(self, message):
        logging.error(f'{message}')



