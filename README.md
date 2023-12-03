# Catwalk APIGen
A utility to quickly generate api modules for other languages without any dependencies.

## Features:
Catwalk generates code for the following platforms:
- Browser-JS.
- Python3.
- Java.


## Install:
`pip install git+https://github.com/mirror12k/catwalk-apigen`

## Usage:
```py
from catwalk_apigen import generate_api

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

# Generate JavaScript code
js_code = generate_api(api_definition, "browser-js")
print("JavaScript Code:\n", js_code)

# Generate Python code
python_code = generate_api(api_definition, "python")
print("\nPython Code:\n", python_code)

# Generate Python code
python_code = generate_api(api_definition, "java")
print("\nJava Code:\n", python_code)
```

