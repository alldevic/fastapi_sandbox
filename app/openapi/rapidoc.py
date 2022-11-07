"""
Add RapiDoc integration
https://github.com/rapi-doc/RapiDoc
"""

import json
from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder
from starlette.responses import HTMLResponse

rapidoc_default_parameters = {
    "render-style": "view",
    "show-header": True,
    "allow-search": False,
    "allow-spec-url-load": False,
    "allow-spec-file-load": False,
    "allow-server-selection": False,
    "allow-spec-file-download": False,
    "schema-style": "table",
    "schema-description-expanded": True,
    "load-fonts": False,
}


def get_rapidoc_html(
    *,
    openapi_url: str,
    title: str,
    rapidoc_js_url: str = "https://unpkg.com/rapidoc@9.3.3/dist/rapidoc-min.js",
    fastapi_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    rapidoc_parameters: Optional[Dict[str, Any]] = None,
    add_debug_support: Optional[str] = False,
) -> HTMLResponse:
    """
    RapiDocAPI documentation from OpenAPI Specification
    """
    current_rapidoc_parameters = rapidoc_default_parameters.copy()
    if rapidoc_parameters:
        current_rapidoc_parameters.update(rapidoc_parameters)

    html = f"""
      <!doctype html>
      <html lang="en">
      <head>
        <title>{title}</title>
        <link rel="shortcut icon" href="{fastapi_favicon_url}">
        <script type="module" src="{rapidoc_js_url}"></script>
      </head>
      <body>
        <rapi-doc
          id = "thedoc"
          spec-url = "{openapi_url}"
    """

    for key, value in current_rapidoc_parameters.items():
        html += f"{key} = {json.dumps(jsonable_encoder(value))}\n"

    html += "></rapi-doc>"
    if add_debug_support:
        html += """
            <script>
            document.addEventListener('DOMContentLoaded', event =>
                document.getElementById("thedoc")
                        .addEventListener('after-try', _ => JSON.parse('[]'))
            )
            document.addEventListener('keydown', function (e) {
               if (e.ctrlKey && e.shiftKey && e.code === "KeyF"){
                    document.getElementById("thedoc").showAdvancedSearchDialog = \
                        !document.getElementById("thedoc").showAdvancedSearchDialog;
                }
            });
            </script>
        """
    html += "</body></html>"
    return HTMLResponse(html)
