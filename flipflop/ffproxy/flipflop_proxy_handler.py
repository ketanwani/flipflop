import requests
from django.http import HttpResponse
from ffproxy.flipflop_config import FlipFlopConfig
from ffproxy.plugins.flipflop_plugin_chain import PluginChain
from ffproxy.plugins.url_replacer_plugin import UrlReplacerPlugin
from ffproxy.plugins.header_remover_plugin import HeaderRemoverPlugin
from ffproxy.plugins.flipflop_plugin_mode import FlipFlopPluginMode

class FlipFlopProxyHandler:
    """
    Class representing the FlipFlop reverse proxy handler.

    The `FlipFlopProxyHandler` class is responsible for handling incoming requests from clients and forwarding them to
    the backend server. It utilizes the `PluginChain` to apply registered plugins before forwarding the requests.

    Note:
        - Users should create a `FlipFlopConfig` instance with essential configuration settings and pass it to the
          `FlipFlopProxyHandler` constructor.
        - The `handle_request` method is the main entry point to process incoming requests and forward them to the
          backend. The response from the backend will be modified based on the registered plugins before being returned
          to the client.
    """

    def __init__(self, config: FlipFlopConfig):
        """
        Initialize the FlipFlopProxyHandler instance with the specified configuration settings.

        Args:
            config (FlipFlopConfig): The configuration settings for the FlipFlop reverse proxy.
        """
        self._config = config
        self._plugin_chain = PluginChain()

        # Create and add built-in plugins (UrlReplacerPlugin and HeaderRemoverPlugin) to the plugin chain
        url_replacer = UrlReplacerPlugin("URL Replacer", config, FlipFlopPluginMode.ENABLED)
        header_remover = HeaderRemoverPlugin("Header Remover", config, FlipFlopPluginMode.ENABLED)
        self._plugin_chain.add_plugin(url_replacer)
        self._plugin_chain.add_plugin(header_remover)

        # Add user-defined plugins from the config to the plugin chain
        for key in config.get_plugins():
            self._plugin_chain.add_plugin(config.get_plugins()[key])

    def handle_request(self, request, rest_of_path):
        """
        Handle the incoming request from the client and forward it to the backend server.

        Args:
            request: The incoming HTTP request from the client.
            rest_of_path (str): The portion of the URL path after the reverse proxy URL.

        Returns:
            HttpResponse: The HTTP response to be sent back to the client.
        """
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
