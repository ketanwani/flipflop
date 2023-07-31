import requests
from django.http import HttpResponse
from ffproxy.flipflop_config import FlipFlopConfig
from ffproxy.plugins.flipflop_plugin_chain import PluginChain
from ffproxy.plugins.url_replacer_plugin import UrlReplacerPlugin
from ffproxy.plugins.header_remover_plugin import HeaderRemoverPlugin
from ffproxy.plugins.flipflop_plugin_mode import FlipFlopPluginMode
class FlipFlopProxyHandler:

    def __init__(self, config: FlipFlopConfig):
        self._config = config
        self._plugin_chain = PluginChain()

        url_replacer = UrlReplacerPlugin("URL Replacer", config, FlipFlopPluginMode.ENABLED)
        header_remover = HeaderRemoverPlugin("Header Remover", config, FlipFlopPluginMode.ENABLED)
        self._plugin_chain.add_plugin(url_replacer)
        self._plugin_chain.add_plugin(header_remover)

        for key in config.get_plugins():
            self._plugin_chain.add_plugin(config.get_plugins()[key])

    def handle_request(self, request, rest_of_path):
        # Get the CSRF token from the incoming request
        csrf_token = request.COOKIES.get('csrftoken')

        # Define the backend URL where the requests will be forwarded
        source = self._config.get_target_url()
        backend_url = 'https://{}'.format(source)

        # Construct the complete request URL for the backend
        request_url = f"{backend_url}/{rest_of_path}"

        # Preserve the original request method, body, and headers
        original_request_method = request.method
        original_request_body = request.body
        original_request_headers = {key: value for key, value in request.headers.items()}
        original_request_headers = self._plugin_chain.process_request_headers(original_request_headers, original_request_method)

        # Construct the headers for the new request to the backend
        new_request_headers = {
            'X-CSRFToken': csrf_token,
            **original_request_headers,
        }

        # Make the request to the backend using requests library
        try:
            response = requests.request(
                method=original_request_method,
                url=request_url,
                data=original_request_body,
                headers=new_request_headers
            )
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500, content_type='text/plain')

        # Get the content type and status code from the response
        content_type = response.headers.get('Content-Type', 'text/plain')
        status_code = response.status_code
        modified_content = self._plugin_chain.process_response(response)

        return HttpResponse(modified_content, status=status_code, content_type=content_type)
