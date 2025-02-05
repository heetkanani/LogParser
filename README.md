# Log Parser - Illumio Take Home Assessement Summer 2025

## Problem
Write a program that can parse a file containing [flow log data](/flowlogs.txt) and maps each row to a tag based on a [lookup table](/lookup_table.csv)
1. The program should generate an [tag count output file](/tag_count.csv)  containing the count of matches for each tag
2. The program should generate an [port/protocol combination output file](/port_protocol_count.csv) containing the count of matches for each port/protocol combination 


## Assumptions

1. This program only supports the version 2 logs only.
2. A few protocols are listed under the [protocols](/protocols.csv) file

## Requirements

The program should generate an output file containing the following:

1. Count of matches for each tag:

   ```
   Tag,Count
   sv_P2,1
   sv_P1,2
   sv_P4,1
   email,3
   Untagged,9
   ```

2. Count of matches for each port/protocol combination

   ```
   Port,Protocol,Count
   22,tcp,1
   23,tcp,1
   25,tcp,1
   110,tcp,1
   143,tcp,1
   443,tcp,1
   993,tcp,1
   1024,tcp,1
   49158,tcp,1
   80,tcp,1
   ```

## Specifications

- Input file as well as the file containing tag mappings are plain text (ascii) files.
- The flow log file size can be up to 10 MB 
- The lookup file can have up to 10000 mappings
- The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above. 
  and sv_P2 in the sample above.
- The matches should be case insensitive 

## Running the application

```
python log_parser.py
```
This program will first read the data from the [flowlogs.txt](/flowlogs.txt) and the lookup data from the [lookup_table.csv](/lookup_table.csv) and then `the count of matches for each tag's` output will be saved in [tag_count.csv](/tag_count.csv) and `the count of matches for each port/protocol combination's` output will be saved in [port_protocol_count.csv](/port_protocol_count.csv).

Necessary logging mechanism is added for debugging purposes and also, [config file](/config.ini) is created so that the files name can we changed if required.

## Testing

To run the unit test file use the following command:

```
python -m unittest test_log_parser.py
```

## Given Data Information
1. The data in the file `lookup_table.csv` is in the below format

```
dstport,protocol,tag
25,tcp,sv_P1
68,udp,sv_P2
23,tcp,sv_P1
31,udp,SV_P3
443,tcp,sv_P2
```
2. The data in the file `flowlogs.txt` is in the AWS VPC flow logs format with the only version 2 supported

Reference: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html

```
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK 
```
the mapping for the above log is in the below format:

```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
```
