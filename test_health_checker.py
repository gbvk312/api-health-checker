import unittest
from unittest.mock import patch, MagicMock
from health_checker import check_endpoint, EndpointResult
from urllib.error import HTTPError, URLError

class TestHealthChecker(unittest.TestCase):
    
    @patch('health_checker.urllib.request.urlopen')
    def test_check_endpoint_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_resp
        
        config = {
            "name": "Test API",
            "url": "https://test.com/api",
            "expected_status": 200
        }
        
        result = check_endpoint(config)
        
        self.assertTrue(result.success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.url, "https://test.com/api")

    @patch('health_checker.urllib.request.urlopen')
    def test_check_endpoint_unexpected_status(self, mock_urlopen):
        # Even if urlopen raises an HTTPError for 404, the checker handles it
        err_fp = MagicMock()
        mock_urlopen.side_effect = HTTPError('url', 404, 'Not Found', hdrs=None, fp=err_fp)
        
        config = {
            "name": "Test API",
            "url": "https://test.com/api",
            "expected_status": 200
        }
        
        result = check_endpoint(config)
        self.assertFalse(result.success)
        self.assertEqual(result.status_code, 404)
        self.assertIn("Expected [200], got 404", result.error_reason)

    @patch('health_checker.urllib.request.urlopen')
    def test_check_endpoint_connection_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Mock timeout")
        
        config = {
            "name": "Test API",
            "url": "https://test.com/timeout",
            "expected_status": 200
        }
        
        result = check_endpoint(config)
        self.assertFalse(result.success)
        self.assertIsNone(result.status_code)
        self.assertIn("Mock timeout", result.error_reason)

if __name__ == '__main__':
    unittest.main()
