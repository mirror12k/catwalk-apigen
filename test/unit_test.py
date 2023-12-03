import unittest
import xmlrunner
import sys
sys.path.append('.')
from catwalk_apigen import *


import requests
from unittest.mock import patch


class TestGenerateJSAPI(unittest.TestCase):
    def test_api_generation(self):
        # API definition example
        api_definition = [
            {
                'action': '/lambda/send',
                'args': ['message']
            },
            {
                'action': '/lambda/stats',
                'args': []
            }
        ]

        # Expected JavaScript code
        expected_js_code = """
const api_endpoint = 'http://example.com/api';

function callApi(action, args) {
    const auth_token = localStorage.getItem('auth_token');
    const headers = {
        'Content-Type': 'application/json'
    };

    if (auth_token) {
        headers['Authorization'] = 'Bearer ' + auth_token;
    }

    args.action = action;
    return fetch(api_endpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(args)
    }).then(response => response.json());
}
export default {

    get_auth_token: () => localStorage.getItem('auth_token'),
    set_auth_token: token => localStorage.setItem('auth_token', token),
    clear_auth_token: () => localStorage.setItem('auth_token', ''),

    send: (message) => callApi('/lambda/send', {'message': message}),

    stats: () => callApi('/lambda/stats', {}),
};
"""
        # Generate JavaScript code
        generated_js_code = generate_api(api_definition, 'browser-js')

        # Compare the generated code with the expected code
        self.assertEqual(generated_js_code.strip(), expected_js_code.strip())




import os
import importlib.util
import tempfile


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # API definition
        api_definition = [
            {
                'action': '/lambda/send',
                'args': ['message']
            },
            {
                'action': '/lambda/stats',
                'args': []
            }
        ]

        # Generate Python code for the API
        python_code = generate_api(api_definition, "python")

        # Create a temporary file to save the generated code
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, "api_module.py")
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(python_code)

        # Dynamically import the generated module
        spec = importlib.util.spec_from_file_location("api_module", temp_file_path)
        api_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(api_module)
        cls.API = api_module.API

    @patch('requests.post')
    def test_send(self, mock_post):
        # Setup mock response
        mock_response = mock_post.return_value
        mock_response.json.return_value = {'status': 'success'}

        # Call the send function
        response = self.API.send('test message')

        # Asserts
        mock_post.assert_called_once_with(
            'http://example.com/api',
            json={'action': '/lambda/send', 'message': 'test message'},
            headers={}
        )
        self.assertEqual(response, {'status': 'success'})

    @patch('requests.post')
    def test_stats_with_auth_token(self, mock_post):
        # Setup mock response
        mock_response = mock_post.return_value
        mock_response.json.return_value = {'data': 'some stats'}

        # Set auth token and call the stats function
        self.API.set_auth_token('token123')
        response = self.API.stats()

        # Asserts
        mock_post.assert_called_once_with(
            'http://example.com/api',
            json={'action': '/lambda/stats'},
            headers={'Authorization': 'Bearer token123'}
        )
        self.assertEqual(response, {'data': 'some stats'})

        # Clear auth token after test
        self.API.clear_auth_token()

class TestJavaApiGenerator(unittest.TestCase):
    def test_java_api_generation(self):
        # Example API definition
        api_definition = [
            {
                'action': '/lambda/send',
                'args': ['message']
            },
            {
                'action': '/lambda/stats',
                'args': []
            }
        ]

        # Expected Java code
        expected_java_code = """
import java.io.*;
import java.net.*;
import org.json.JSONObject;

public class ApiClient {
    private static final String API_ENDPOINT = "http://example.com/api";

    private static String callApi(String action, JSONObject args) {
        try {
            URL url = new URL(API_ENDPOINT);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json; utf-8");
            conn.setRequestProperty("Accept", "application/json");
            conn.setDoOutput(true);

            args.put("action", action);
            try(OutputStream os = conn.getOutputStream()) {
                byte[] input = args.toString().getBytes("utf-8");
                os.write(input, 0, input.length);           
            }

            try(BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine = null;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                return response.toString();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public static String send(String message) {
        JSONObject args = new JSONObject();
        args.put("message", message);
        return callApi("/lambda/send", args);
    }

    public static String stats() {
        JSONObject args = new JSONObject();
        return callApi("/lambda/stats", args);
    }
}
""".strip()

        # Generate Java code using the provided function
        generated_java_code = generate_api(api_definition, "java").strip()

        # Compare the generated code with the expected code
        self.assertEqual(generated_java_code, expected_java_code)


# Running the tests
unittest.main(testRunner=xmlrunner.XMLTestRunner(output='xml-test-reports'))
