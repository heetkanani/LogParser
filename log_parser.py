from collections import defaultdict
from typing import Dict, Tuple

import csv
import logging

protocols: Dict[int, str] = {}
lookup_table: Dict[Tuple[int, str], str] = {}

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(message)s')

def loading_protocols(file: str):

    logging.info(f"Loading the protocols.csv file")
    with open(file, 'r') as protocol_file:
        csv_reader = csv.DictReader(protocol_file)
        for csv_row in csv_reader:
            protocols[int(csv_row['protocol_number'])] = csv_row['protocol_name']

def generate_lookup_table(file: str):

    logging.info(f"Generating the lookup table from lookup_table.csv")
    with open(file, 'r') as lookup_file:
        csv_reader = csv.DictReader(lookup_file)
        for csv_row in csv_reader:
            lookup_value = (int(csv_row['dstport']), csv_row['protocol'])
            lookup_table[lookup_value] = csv_row['tag'] 

def generate_logs(file: str):
    tag_count = defaultdict(int)
    protocol_count = defaultdict(int)

    logging.info(f"Generating logs and calculating the count")
    with open(file, 'r') as log_file:
        for entry in log_file:
            value = entry.split()
            if len(value) < 14:
                continue
            
            destination_port = int(value[6])
            protocol_name = protocols.get(int(value[7]), 'unknown')
            # print("DP: "+ str(destination_port)+" protcolName: "+str(protocol_name))

            dest_protocol = (destination_port, protocol_name)
            tag = lookup_table.get(dest_protocol, 'untagged')

            tag_count[tag] += 1
            protocol_count[dest_protocol] += 1

    return tag_count, protocol_count
def save_data_to_file(tag_count: Dict[str, int], protocol_count: Dict[Tuple[int, str], int]):
    logging.info(f"Saving data to tag_count_output.txt and port_protocol_count_output.txt")
    with open('tag_count_output.csv','w') as data_file:
        data_file.write("tag,count\n")
        for tag, count in tag_count.items():
            data_file.write(f"{tag},{count}\n")

    with open("port_protocol_count_output.csv", 'w') as data_file:
        data_file.write("port,portocol,count\n")
        for (port, protocol), count in protocol_count.items():
            data_file.write(f"{port},{protocol},{count}\n")

def main():
    loading_protocols('protocols.csv')
    generate_lookup_table('lookup_table.csv')
    tag_count, protocol_count = generate_logs('flowlogs.txt')
    save_data_to_file(tag_count, protocol_count)

if __name__ == '__main__':
    main()

