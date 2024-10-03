import unittest
import json
from unittest.mock import patch, mock_open
from flask import Flask
from app import app  # assuming the Flask app is defined in app.py

class TestSystemInfoAPI(unittest.TestCase):
    def setUp(self):
        # Creates a test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('os.getloadavg')
    @patch('os.statvfs')
    def test_get_system_info(self, mock_statvfs, mock_getloadavg):
        # Mock the system info
        mock_getloadavg.return_value = (1.23, 0.98, 0.67)
        mock_statvfs.return_value = type('statvfs', (object,), {
            'f_frsize': 4096,
            'f_bavail': 25000000
        })()

        response = self.app.get('/system-info')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['load_avg_1m'], 1.23)
        self.assertEqual(data['load_avg_5m'], 0.98)
        self.assertEqual(data['load_avg_15m'], 0.67)
        self.assertEqual(data['available_disk_space_bytes'], 102400000000)

    @patch('builtins.open', new_callable=mock_open, read_data='{"tech": {"return_value": "test_value"}}')
    def test_get_return_value(self, mock_file):
        response = self.app.get('/return-value')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['return_value'], 'test_value')

    @patch('builtins.open', new_callable=mock_open, read_data='{"tech": {}}')
    def test_get_return_value_key_error(self, mock_file):
        response = self.app.get('/return-value')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Key "return_value" not found in JSON file')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_return_value_file_not_found(self, mock_file):
        response = self.app.get('/return-value')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'JSON file not found')

    @patch('builtins.open', new_callable=mock_open, read_data='{"tech": {"return_value": "old_value"}}')
    def test_update_return_value(self, mock_file):
        updated_data = {"return_value": "new_value"}

        response = self.app.post('/return-value', json=updated_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Value updated successfully')
        self.assertEqual(data['new_return_value'], 'new_value')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_update_return_value_file_not_found(self, mock_file):
        updated_data = {"return_value": "new_value"}

        response = self.app.post('/return-value', json=updated_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'JSON file not found')

    def test_update_return_value_no_value_provided(self):
        response = self.app.post('/return-value', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'No value provided')

if __name__ == '__main__':
    unittest.main()
