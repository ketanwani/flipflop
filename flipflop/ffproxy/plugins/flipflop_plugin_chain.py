from ffproxy.plugins.flipflop_plugin import FlipFlopPlugin
import requests
class PluginChain:
    """
    Class representing a chain of plugins to be applied sequentially to incoming requests and responses.

    The `PluginChain` class allows users to add and remove multiple `FlipFlopPlugin` instances to form a chain of
    plugins. This chain is then used to process incoming requests and responses by applying each plugin's logic
    sequentially.
    Note:
        - The `PluginChain` class acts as a container for plugins, allowing users to manage and apply multiple plugins
          to incoming requests and responses.
        - Plugins are executed in the order they are added to the chain. Users should consider the order of plugins
          carefully to achieve the desired processing of requests and responses.
    """

    plugins = {}

    def add_plugin(self, plugin: FlipFlopPlugin):
        """
        Add a `FlipFlopPlugin` instance to the plugin chain.

        This method adds a `FlipFlopPlugin` instance to the chain by storing it in the `plugins` dictionary.

        Args:
            plugin (FlipFlopPlugin): The `FlipFlopPlugin` instance to be added to the chain.
        """
        if plugin.get_name() not in self.plugins:
            self.plugins[plugin.get_name()] = plugin

    def remove_plugin(self, plugin: FlipFlopPlugin):
        """
        Remove a `FlipFlopPlugin` instance from the plugin chain.

        This method removes a `FlipFlopPlugin` instance from the chain by deleting it from the `plugins` dictionary.

        Args:
            plugin (FlipFlopPlugin): The `FlipFlopPlugin` instance to be removed from the chain.
        """
        if plugin.get_name() in self.plugins:
            self.plugins.pop(plugin.get_name())

    def process_response(self, response: requests.Response) -> bytes:
        """
        Process the incoming response using the registered plugins and return the modified response content.

        This method applies the registered plugins to the incoming response, allowing each plugin to modify the response
        content before it is sent to the client.

        Args:
            response (requests.Response): The incoming response object received from the backend server.

        Returns:
            bytes: The modified response content after applying all registered plugins.
        """
        content_type = response.headers.get('Content-Type', 'text/plain')
        content_disposition = response.headers.get('Content-Disposition', '')
        for key in self.plugins:
            chunk = self.plugins[key].process_response(
                response.content, content_type, content_disposition, response.encoding
            )
        return chunk

    def process_request_headers(self, request_headers: dict[str, str], original_request_method: str) -> dict[str, str]:
        """
        Process the incoming request headers using the registered plugins and return the modified request headers.

        This method applies the registered plugins to the incoming request headers, allowing each plugin to modify the
        headers before the request is forwarded to the backend server.

        Args:
            request_headers (dict[str, str]): The dictionary containing the incoming request headers.
            original_request_method (str): The HTTP request method of the original request (e.g., GET, POST, etc.).

        Returns:
            dict[str, str]: The modified request headers after applying all registered plugins.
        """
        for key in self.plugins:
            request_headers = self.plugins[key].process_request_headers(request_headers, original_request_method)
        return request_headers
