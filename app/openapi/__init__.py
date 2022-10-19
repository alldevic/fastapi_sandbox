"""
OpenAPi schema and ui customizations
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from .rapidoc import get_rapidoc_html
from .snippets import generate_snippets

class CustomOpenapi:
    """
    Customize openapi for app
    """

    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def register(self) -> None:
        """
        Apply new schema and ui. SRP missing
        """
        self.app.add_route("/docs", self.rapidoc_html, include_in_schema=False)
        self.app.openapi = self.get_openapi_schema

    def get_openapi_schema(self):
        """
        Get custom schema info
        """
        if self.app.openapi_schema:
            return self.app.openapi_schema

        openapi_schema = get_openapi(
            title="FastAPI Sandbox",
            version="0.0.1",
            description="## Testing some useful things \n - test \n - test1",
            routes=self.app.routes,
        )

        generate_snippets(openapi_schema, ['python', 'js', 'curl'])

        self.app.openapi_schema = openapi_schema

        return self.app.openapi_schema

    def rapidoc_html(self, req: Request) -> HTMLResponse:
        """
        Get rapidoc for current schema
        """
        root_path = req.scope.get("root_path", "").rstrip("/")
        openapi_url = root_path + self.app.openapi_url
        return get_rapidoc_html(
            openapi_url=openapi_url,
            title=self.app.title + " - RapiDoc",
            rapidoc_js_url="/static/js/rapidoc-min.js",
            add_debug_support=True,
        )

    # def add_examples(openapi_schema: dict, examples_dir):
    #     for filename in os.listdir(examples_dir):
    #         if isinstance(examples_dir, pathlib.PurePath):
    #             file_path = pathlib.Path(examples_dir / filename)
    #         else:
    #             file_path = pathlib.Path(examples_dir + "/" + filename)
    #         if file_path.suffix in lang_extension_lookup:
    #             parts = file_path.stem.split("-")
    #             if len(parts) >= 2:
    #                 route_method_schema = openapi_schema["paths"]["/" + "/".join(parts[:-1])][parts[-1]]
    #                 code_samples = route_method_schema.get("x-codeSamples", [])
    #                 code_samples.append(
    #                     {"lang": lang_extension_lookup[file_path.suffix], "source": file_path.read_text()}
    #                 )
    #                 route_method_schema["x-codeSamples"] = code_samples
    #             else:
    #                 logger.warning(
    #                     "Example filename does not meet format of {route_path}_{http_method}.{lang_extensions}"
    #                 )
    #         else:
    #             logger.warning(f"Not a valid example file: {filename}")
