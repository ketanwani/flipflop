from ffproxy.plugins.flipflop_plugin_mode import FlipFlopPluginMode
from ffproxy.flipflop_config import FlipFlopConfig
from typing import Awaitable, Dict

class FlipFlopPlugin:
    """
    Base class for creating plugins in the FlipFlop reverse proxy library.

    This class serves as the foundation for implementing custom plugins that can modify and extend the behavior of the
    reverse proxy. Users can create their own plugins by deriving from this class and implementing the required methods.

    Note:
        - Users should derive from this class to create custom plugins and implement the required methods.
        - Each plugin can be registered with the `PluginChain` to form a chain of plugins that process requests and
          responses in the desired order.
        - When implementing custom plugins, developers should ensure that the plugins do not interfere with the
          expected behavior of the reverse proxy and backend systems.
    """

    def __init__(self, name: str, config: FlipFlopConfig, mode: FlipFlopPluginMode = FlipFlopPluginMode.ENABLED):
        """
        Initialize the FlipFlopPlugin instance.

        Args:
            name (str): The name of the plugin.
            config (FlipFlopConfig): Configuration object that can be used by the plugin to access shared settings.
            mode (FlipFlopPluginMode, optional): The initial mode of the plugin. Defaults to FlipFlopPluginMode.ENABLED.
        """
        self._name = name
        self._mode = mode
        self._config = config

    def get_mode() -> FlipFlopPluginMode:
        """
        Get the current mode of the plugin (enabled or disabled).

        Returns:
            FlipFlopPluginMode: The current mode of the plugin.
        """
        return self._mode

    def set_mode(self, mode: FlipFlopPluginMode):
        """
        Set the mode of the plugin (enabled or disabled).

        Args:
            mode (FlipFlopPluginMode): The new mode of the plugin.
        """
        self._mode = mode

    def get_name(self) -> str:
        """
        Get the name of the plugin.

        Returns:
            str: The name of the plugin.
        """
        return self._name

    def set_config(self, config: FlipFlopConfig):
        """
        Set the configuration object for the plugin.

        Args:
            config (FlipFlopConfig): The configuration object to be set for the plugin.
        """
        self._config = config

    def process_request_headers(headers: dict[str, str], request_method: str) -> dict[str, str]:
        """
        Process and modify the incoming request headers before forwarding the request to the backend server.

        Args:
            headers (dict[str, str]): The dictionary containing the incoming request headers.
            request_method (str): The HTTP request method (e.g., GET, POST, etc.).

        Returns:
            dict[str, str]: The modified request headers.
        """
        pass

    def process_response(chunk: bytes, content_type: str, content_disposition: str, encoding: str) -> bytes:
        """
        Process and modify the incoming response from the backend server before sending it to the client.

        Args:
            chunk (bytes): The chunk of response content received from the backend server.
            content_type (str): The Content-Type header of the response.
            content_disposition (str): The Content-Disposition header of the response.
            encoding (str): The character encoding used in the response.

        Returns:
            bytes: The modified response content.
        """
        pass

    def can_stream_response() -> bool:
        """
        Check if the plugin supports streaming of responses.

        Returns:
            bool: True if the plugin supports streaming responses, False otherwise.
        """
        pass
