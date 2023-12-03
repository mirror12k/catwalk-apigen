def generate_api(api_definition, target, fixed_endpoint='http://example.com/api'):
    """
    Generates code that calls the given APIs. The target language for code generation can be specified.
    - "browser-js": Generates JavaScript code using fetch.
    - "python": Generates Python code using requests, with the action sent as part of the args.

    Args:
    api_definition (list): A list of dictionaries defining API endpoints.
    target (str): Target language for the generated code ("browser-js" or "python").

    Returns:
    str: A string containing the generated code in the specified target language.
    """

    if target == "browser-js":
        # JavaScript code generation
        js_template = f"""
const api_endpoint = '{fixed_endpoint}';

function callApi(action, args) {{
    const auth_token = localStorage.getItem('auth_token');
    const headers = {{
        'Content-Type': 'application/json'
    }};

    if (auth_token) {{
        headers['Authorization'] = 'Bearer ' + auth_token;
    }}

    args.action = action;
    return fetch(api_endpoint, {{
        method: 'POST',
        headers: headers,
        body: JSON.stringify(args)
    }}).then(response => response.json());
}}
"""

        export_block = "export default {\n"

        export_block += """
    get_auth_token: () => localStorage.getItem('auth_token'),
    set_auth_token: token => localStorage.setItem('auth_token', token),
    clear_auth_token: () => localStorage.setItem('auth_token', ''),
"""

        for endpoint in api_definition:
            action = endpoint['action']
            args = endpoint['args']
            func_name = action.split('/')[-1].replace('/', '_')
            args_list = ', '.join(args)
            export_block += f"""
    {func_name}: ({args_list}) => callApi('{action}', {{{', '.join([f"'{arg}': {arg}" for arg in args])}}}),
"""

        export_block += "};\n"

        return js_template + export_block

    elif target == "python":
        # Python code generation with action as part of args and handling auth_token
        python_template = f"""
import requests

class API:
    api_endpoint = "{fixed_endpoint}"
    auth_token = None

    @staticmethod
    def set_auth_token(token):
        API.auth_token = token

    @staticmethod
    def clear_auth_token():
        API.auth_token = None

    @staticmethod
    def call_api(action, args):
        headers = {{}}
        if API.auth_token:
            headers['Authorization'] = 'Bearer ' + API.auth_token
        args['action'] = action
        response = requests.post(API.api_endpoint, json=args, headers=headers)
        return response.json()
"""

        # Add functions for each endpoint
        for endpoint in api_definition:
            action = endpoint['action']
            args = endpoint['args']
            func_name = action.split('/')[-1].replace('/', '_')
            args_list = ', '.join(args)
            python_template += f"""
    @staticmethod
    def {func_name}({args_list}):
        args = {{{', '.join([f"'{arg}': {arg}" for arg in args])}}}
        return API.call_api('{action}', args)
"""

        return python_template

    elif target == "java":
        # Java code generation
        java_template = """
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
"""

        # Add functions for each endpoint
        for endpoint in api_definition:
            action = endpoint['action']
            args = endpoint['args']
            func_name = action.split('/')[-1].replace('/', '_')
            arg_list = ', '.join([f'String {arg}' for arg in args])

            # Generate Java function
            java_template += f"""
    public static String {func_name}({arg_list}) {{
        JSONObject args = new JSONObject();
"""
            for arg in args:
                java_template += f"        args.put(\"{arg}\", {arg});\n"

            java_template += f"        return callApi(\"{action}\", args);\n    }}\n"

        java_template += "}\n"
        return java_template

    else:
        raise ValueError("Unsupported target language")
