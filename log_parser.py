from collections import defaultdict
from typing import Dict, Tuple

import csv
import configparser
import logging

#Initializing the config.ini file
configuration = configparser.ConfigParser()
configuration.read('config.ini')

#Getting the file names from the config file
PROTOCOLS_FILE = configuration['files']['protocols_file']
FLOW_LOGS_FILE = configuration['files']['flow_logs_file']
LOOKUP_TABLE_FILE = configuration['files']['lookup_table_file']
TAG_COUNT_FILE = configuration['files']['tag_count_file']
PORT_PROTOCOL_COUNT_FILE = configuration['files']['port_protocol_count_file']

protocols: Dict[int, str] = {}
lookup_table: Dict[Tuple[int, str], str] = {}

#Initiaizing the logging mechanism
logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(message)s')

def loading_protocols(file: str):
    """
    Loads the data from the protocols.csv file.

    Args:
        file (str): the name of the csv file.
    
    Raises:
        FileNotFoundError: if a specific file is not found then it will throw this error.
    """
    logging.info(f"Loading the {PROTOCOLS_FILE} file")
    try:
        with open(file, 'r') as protocol_file:
            csv_reader = csv.DictReader(protocol_file)
            for csv_row in csv_reader:
                protocols[int(csv_row['protocol_number'])] = csv_row['protocol_name']

    except FileNotFoundError:
        logging.error(f"Could not find the {PROTOCOLS_FILE} file")
        raise


def generate_lookup_table(file: str):
    """
    Reads the data from lookup_table.csv file.

    Args:
        file (str): the name of the csv file.
    
    Raises:
        FileNotFoundError: if a specific file is not found then it will throw this error.
    """
    logging.info(f"Generating the lookup table from {LOOKUP_TABLE_FILE}")
    try:
        with open(file, 'r') as lookup_file:
            csv_reader = csv.DictReader(lookup_file)
            for csv_row in csv_reader:
                lookup_value = (int(csv_row['dstport']), csv_row['protocol'])
                lookup_table[lookup_value] = csv_row['tag'] 

    except FileNotFoundError:
        logging.error(f"Could not find the {LOOKUP_TABLE_FILE} file")
        raise


def generate_logs(file: str):
    """
    Reads the flowlog.txt file to calculate the tag count and port protocol count.

    Args:
        file (str): the name of the csv file.
    
    Returns:
        Tuple[Dict[str, int], Dict[Tuple[int, str], int]]: 
            - tags as keys and tag count as values.
            - (destination port, protocol) as keys and port protocol count as values.
    
    Raises:
        FileNotFoundError: if a specific file is not found then it will throw this error.
    """
    tag_count = defaultdict(int)
    protocol_count = defaultdict(int)

    logging.info(f"Generating logs and calculating the count")
    try:
        with open(file, 'r') as log_file:
            for entry in log_file:
                value = entry.split()
                if len(value) < 14:
                    continue
                
                destination_port = int(value[6])
                protocol_name = protocols.get(int(value[7]), 'unknown')

                dest_protocol = (destination_port, protocol_name)
                tag = lookup_table.get(dest_protocol, 'untagged')

                tag_count[tag] += 1
                protocol_count[dest_protocol] += 1

    except FileNotFoundError:
        logging.error(f"Could not find the {FLOW_LOGS_FILE} file")
        raise

    return tag_count, protocol_count


def save_data_to_file(tag_count: Dict[str, int], protocol_count: Dict[Tuple[int, str], int]):
    """
    Saves the generated count into the tag_count.csv and port_protocol_count.csv.

    Args:
        tag_count (Dict[str, int]): saving the tag counts.
        protocol_count (Dict[Tuple[int, str], int]): saving the port protocol counts.
    
    Raises:
        Exception: If the execution is interrupted then the exception is thrown.
    """
    logging.info(f"Saving data to {TAG_COUNT_FILE } and {PORT_PROTOCOL_COUNT_FILE}")
    try:
        with open(TAG_COUNT_FILE,'w') as data_file:
            data_file.write("tag,count\n")
            for tag, count in tag_count.items():
                data_file.write(f"{tag},{count}\n")

        with open(PORT_PROTOCOL_COUNT_FILE, 'w') as data_file:
            data_file.write("port,protocol,count\n")
            for (port, protocol), count in protocol_count.items():
                data_file.write(f"{port},{protocol},{count}\n")

    except Exception as e:
        logging.error(f"Could not find the {FLOW_LOGS_FILE} file: {e}")
        raise

def main():
    """
    Main function that performes the operations like loading the data, generate the csv table and then
    saving the data into the specified files.

    Raises:
        Exception: If the execution is interrupted then the exception is thrown.
    """
    try:
        loading_protocols(PROTOCOLS_FILE)
        generate_lookup_table(LOOKUP_TABLE_FILE)
        tag_count, protocol_count = generate_logs(FLOW_LOGS_FILE)
        save_data_to_file(tag_count, protocol_count)

    except Exception as e:
        logging.error(f"Could not run the program correctly: {e}")
        raise


if __name__ == '__main__':
    main()

