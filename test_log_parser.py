import unittest
from log_parser import (loading_protocols, generate_lookup_table, generate_logs, save_data_to_file,protocols, lookup_table)

class TestLogParser(unittest.TestCase):
    #setup test to clear if there is data in files
    def setUp(self):
        protocols.clear()
        lookup_table.clear()

    # test to check if data can be correctly written to protocols file
    def test_loading_protocols(self):
        file_data = "protocol_number,protocol_name\n1,icmp\n6,tcp\n17,udp"
        with open('test_protocols.csv', 'w') as file:
            file.write(file_data)
        loading_protocols('test_protocols.csv')
        self.assertEqual(protocols, {1: 'icmp', 6: 'tcp', 17: 'udp'})

    # test to check if file not found test works correctly i.e it throws an error for protocols
    def test_loading_protocols_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            loading_protocols('file_not_found.csv')

    # test to check if incorrect data throws the value error and is handled correctly for protocols
    def test_loading_protocols_incorrect(self):
        file_data = "protocol_number,protocol_name\n1,icmp\n6,tcp\nincorrect"
        with open('test_protocols_incorrect.csv', 'w') as f:
            f.write(file_data)
        with self.assertRaises(ValueError):
            loading_protocols('test_protocols_incorrect.csv')

    # test to check if data can be correctly written to lookup_table file
    def test_generate_lookup_table(self):
        file_data = "dstport,protocol,tag\n80,tcp,http\n443,tcp,https\n53,udp,dns"
        with open('test_lookup_table.csv', 'w') as file:
            file.write(file_data)
        generate_lookup_table('test_lookup_table.csv')
        self.assertEqual(lookup_table, {(80, 'tcp'): 'http', (443, 'tcp'): 'https', (53, 'udp'): 'dns'})

    # test to check if file not found test works correctly i.e it throws an error for lookup_table
    def test_generate_lookup_table_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            generate_lookup_table('file_not_found.csv')

    # test to check if incorrect data throws the value error and is handled correctly for lookup_table
    def test_generate_lookup_table_incorrect(self):
        file_data = "dstport,protocol,tag\n80,tcp,http\n443,tcp,https\nincorrect"
        with open('test_lookup_table_incorrect.csv', 'w') as f:
            f.write(file_data)
        with self.assertRaises(ValueError):
            generate_lookup_table('test_lookup_table_incorrect.csv')

    # test to check if the logs are correctly generated
    def test_generate_logs(self):
        file_data = (
            "2 1234 eni-0ab 192.168.1.1 10.0.0.1 12345 80 6 1000 2000 1620140761 1620140821 ACCEPT OK\n"
            "2 1234 eni-0ab 192.168.1.2 10.0.0.2 54321 443 6 1500 3000 1620140761 1620140821 ACCEPT OK\n"
            "2 1234 eni-0ab 192.168.1.3 10.0.0.3 56789 53 17 500 1000 1620140761 1620140821 ACCEPT OK\n"
            "2 1234 eni-0ab 192.168.1.4 10.0.0.4 65432 8080 6 2000 4000 1620140761 1620140821 ACCEPT OK\n"
        )
        with open('test_flow_logs.txt', 'w') as file:
            file.write(file_data)

        protocols.update({6: 'tcp', 17: 'udp'})
        lookup_table.update({(80, 'tcp'): 'http', (443, 'tcp'): 'https', (53, 'udp'): 'dns'})
        tag_counts, port_protocol_counts = generate_logs('test_flow_logs.txt')
        self.assertEqual(tag_counts['http'], 1)
        self.assertEqual(tag_counts['https'], 1)
        self.assertEqual(tag_counts['dns'], 1)
        self.assertEqual(tag_counts['untagged'], 1)
        self.assertEqual(port_protocol_counts[(80, 'tcp')], 1)
        self.assertEqual(port_protocol_counts[(443, 'tcp')], 1)
        self.assertEqual(port_protocol_counts[(53, 'udp')], 1)
        self.assertEqual(port_protocol_counts[(8080, 'tcp')], 1)


    # Test to check if the data gets saved correctly
    def test_save_data_to_file(self):
        tag_count = {
            'untagged': 8,
            'sv_P2': 1,
            'sv_P1': 2,
            'email': 3
        }
        
        protocol_count = {
            (49153, 'tcp'): 1,
            (49154, 'tcp'): 1,
            (49155, 'tcp'): 1,
            (49156, 'tcp'): 1,
            (49157, 'tcp'): 1,
            (49158, 'tcp'): 1,
            (80, 'tcp'): 1,
            (1024, 'tcp'): 1,
            (443, 'tcp'): 1,
            (23, 'tcp'): 1,
            (25, 'tcp'): 1,
            (110, 'tcp'): 1,
            (993, 'tcp'): 1,
            (143, 'tcp'): 1
        }
        
        save_data_to_file(tag_count, protocol_count)

        with open('tag_count.csv', 'r') as file:
            content = file.read()
            self.assertIn("tag,count", content)
            self.assertIn("untagged,8", content)
            self.assertIn("sv_P2,1", content)
            self.assertIn("email,3", content)
        
        with open('port_protocol_count.csv', 'r') as file:
            content = file.read()
            self.assertIn("port,protocol,count", content)
            self.assertIn("49153,tcp,1", content)
            self.assertIn("49154,tcp,1", content)
            self.assertIn("49155,tcp,1", content)
            self.assertIn("49156,tcp,1", content)
            self.assertIn("49157,tcp,1", content)
            self.assertIn("49158,tcp,1", content)
            self.assertIn("80,tcp,1", content)
            self.assertIn("1024,tcp,1", content)
            self.assertIn("443,tcp,1", content)
            self.assertIn("23,tcp,1", content)
            self.assertIn("25,tcp,1", content)
            self.assertIn("110,tcp,1", content)
            self.assertIn("993,tcp,1", content)
            self.assertIn("143,tcp,1", content)


if __name__ == '__main__':
    unittest.main()
