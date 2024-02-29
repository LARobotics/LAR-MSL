import logging
import datetime
import consts

filename = "./../../logs/"
filename += datetime.datetime.now().strftime('%Y_%m')
filename += "/"
filename += datetime.datetime.now().strftime('%d_%H-%M-%S')
filename += ".log"

# Set up logging
logging.basicConfig(
    filename=filename,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',  # Customize the log format
    datefmt='%H:%M:%S'  # Customize the date format
)

# Define a function for writing to the log file
def log_message(msg):
    #timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #log_str = f'{timestamp} - {msg}'
    if consts.LOG_FILE:
        logging.info(msg)

if __name__ == "__main__":
    # Use the function to log messages
    log_message('Starting my code...')
    log_message('Processing data...')
    log_message('Finished processing data.')