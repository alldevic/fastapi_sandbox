"""
Add RapiDoc integration
https://github.com/rapi-doc/RapiDoc
"""

from starlette.responses import HTMLResponse

rapidoc_default_parameters = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}


def get_rapidoc_html(
    *,
    openapi_url: str,
    title: str,
    rapidoc_js_url: str = "https://unpkg.com/rapidoc@9.3.3/dist/rapidoc-min.js",
) -> HTMLResponse:
    """
    RapiDocAPI documentation from OpenAPI Specification
    """
    html = f"""
      <!doctype html>
      <html lang="en">
      <head>
        <title>{title}</title>
        <script type="module" src="{rapidoc_js_url}"></script>
      </head>
      <body>
        <rapi-doc 
          id = "thedoc"
          spec-url = "{openapi_url}" 
          render-style = "view"
          show-header = "false"
          allow-spec-url-load = "false"
          allow-spec-file-load = "false"
          allow-server-selection = "false"
          allow-spec-file-download = "false"
          schema-style = "table"
          schema-description-expanded = "true"
          load-fonts = "false"
        >
        </rapi-doc>
        <script>
          document.addEventListener('DOMContentLoaded', event =>
            document.getElementById("thedoc").addEventListener('after-try', _ =>
              JSON.parse('[]'
              )
            )
          )
        </script>
      </body>
      </html>
    """
    return HTMLResponse(html)
