from ffproxy.plugins.flipflop_plugin import FlipFlopPlugin

class HeaderRemoverPlugin(FlipFlopPlugin):
    """
    Plugin class to remove specific headers from the incoming request before forwarding it to the backend server.

    This plugin allows users to remove certain headers from the incoming request before it is sent to the backend server.

    Note:
        - Users should ensure that the removal of headers does not interfere with the expected behavior of the reverse proxy
          and backend systems.
        - When configuring the `PluginChain`, the `HeaderRemoverPlugin` should be added in the desired order to remove
          headers before they are processed by other plugins.
    """

    def process_request_headers(
        self,
        headers: dict[str, str],
        request_method: str,
    ) -> dict[str, str]:
        """
        Process and modify the incoming request headers by removing specific headers.

        This method is called when an incoming request is received by the reverse proxy. It allows users to inspect and
        modify the request headers before forwarding the request to the backend server.

        Args:
            headers (dict[str, str]): The dictionary containing the incoming request headers.
            request_method (str): The HTTP request method (e.g., GET, POST, etc.).

        Returns:
            dict[str, str]: The modified request headers after removing specific headers.
        """
        if 'Host' in headers:
            del headers['Host']

        # Remove the "Content-Length" header to avoid conflicts
        if 'Content-Length' in headers:
            del headers['Content-Length']

        return headers

    def process_response(
        self,
        chunk: bytes,
        content_type: str,
        content_disposition: str,
        encoding: str,
    ) -> bytes:
        """
        Process and modify the incoming response from the backend server before sending it to the client.

        This method is called when an incoming response is received from the backend server. It allows users to inspect
        and modify the response content, content type, content disposition, and encoding before sending the response to
        the client.

        Args:
            chunk (bytes): The chunk of response content received from the backend server.
            content_type (str): The Content-Type header of the response.
            content_disposition (str): The Content-Disposition header of the response.
            encoding (str): The character encoding used in the response.

        Returns:
            bytes: The modified response content.
        """
        return chunk

    def can_stream_response() -> bool:
        """
        Check if the plugin supports streaming of responses.

        Returns:
            bool: True if the plugin supports streaming responses, False otherwise.
        """
        return True
