"""
Generate code samples for openapi schema
"""


def generate_snippets(openapi_schema, langs: list[str]):
    for route_path in openapi_schema["paths"]:
            for route_method_schema in openapi_schema["paths"][route_path].keys():
                code_samples = openapi_schema["paths"][route_path][route_method_schema].get("x-codeSamples", [])
                code_samples.append({"lang": "python", "label": "Python 3", "source": 'print("Hello!")'})
                openapi_schema["paths"][route_path][route_method_schema]["x-codeSamples"] = code_samples
