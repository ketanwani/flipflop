from ffproxy.plugins.flipflop_plugin import FlipFlopPlugin

class HeaderRemoverPlugin(FlipFlopPlugin):

    def process_request_headers(
        self,
        headers: dict[str, str],
        request_method: str,
    ) -> dict[str, str]:
        if('Host' in headers):
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
        return chunk

    def can_stream_response(self) -> bool:
        return True
