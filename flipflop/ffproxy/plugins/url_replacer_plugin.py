import re
from ffproxy.plugins.flipflop_plugin import FlipFlopPlugin

class UrlReplacerPlugin(FlipFlopPlugin):
    """
    Plugin class to replace URLs in the incoming response before sending it to the client.

    This plugin allows users to perform URL replacement in the incoming response content before it is sent to the client.

    Note:
        - Users should carefully implement the URL replacement logic to avoid unintended modifications to the response
          content.
        - This plugin is useful for replacing specific URLs, such as backend URLs, with reverse proxy URLs to ensure
          correct routing of requests.
        - When configuring the `PluginChain`, the `UrlReplacerPlugin` should be added in the desired order to ensure that
          URL replacements are performed as needed.
    """

    def process_request_headers(
        self,
        headers: dict[str, str],
        request_method: str,
    ) -> dict[str, str]:
        """
        Process and modify the incoming request headers (optional method).

        This method is called when an incoming request is received by the reverse proxy. It allows users to inspect and
        modify the request headers before forwarding the request to the backend server.

        Args:
            headers (dict[str, str]): The dictionary containing the incoming request headers.
            request_method (str): The HTTP request method (e.g., GET, POST, etc.).

        Returns:
            dict[str, str]: The modified request headers (optional). If not implemented, the original headers will be used.
        """
        return headers

    def process_response(
        self,
        chunk: bytes,
        content_type: str,
        content_disposition: str,
        encoding: str
    ) -> bytes:
        """
        Process and modify the incoming response from the backend server by replacing URLs in the response content.

        This method is called when an incoming response is received from the backend server. It allows users to inspect
        and modify the response content by performing URL replacements.

        Args:
            chunk (bytes): The chunk of response content received from the backend server.
            content_type (str): The Content-Type header of the response.
            content_disposition (str): The Content-Disposition header of the response.
            encoding (str): The character encoding used in the response.

        Returns:
            bytes: The modified response content with URLs replaced.
        """
        if content_type != "image/png" and encoding:
            source = self._config.get_target_url()
            target = self._config.get_source_url()
            modified_content = re.sub(source, target, chunk.decode(encoding))
        else:
            modified_content = chunk
        return modified_content

    def can_stream_response() -> bool:
        """
        Check if the plugin supports streaming of responses (optional method).

        Returns:
            bool: True if the plugin supports streaming responses, False otherwise.
        """
        return True
