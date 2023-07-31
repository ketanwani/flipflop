import re
from ffproxy.plugins.flipflop_plugin import FlipFlopPlugin

class UrlReplacerPlugin(FlipFlopPlugin):

    def process_request_headers(
        self,
        headers: dict[str, str],
        request_method: str,
    ) -> dict[str, str]:
        # Your implementation to generate the request headers
        # Modify the headers or perform other actions here
        return headers

    def process_response(
        self,
        chunk: bytes,
        content_type: str,
        content_disposition: str,
        encoding: str
    ) -> bytes:
        if(content_type != "image/png" and encoding):
            source = self._config.get_target_url()
            target = self._config.get_source_url()
            modified_content = re.sub(source, target, chunk.decode(encoding))
        else:
            modified_content = chunk
        return modified_content

    def can_stream_response(self) -> bool:
        # Your implementation to determine if streaming response is supported
        return True
