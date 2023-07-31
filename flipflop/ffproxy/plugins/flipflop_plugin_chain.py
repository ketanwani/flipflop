from ffproxy.plugins.flipflop_plugin import FlipFlopPlugin
import requests
class PluginChain:
    plugins = {}

    def add_plugin(self, plugin: FlipFlopPlugin):
        if(plugin.get_name() not in self.plugins):
            self.plugins[plugin.get_name] = plugin


    def remove_plugin(self, plugin: FlipFlopPlugin):
        if(plugin.get_name() in plugins):
            plugins.pop(plugin.get_name())

    def process_response(self, response: requests.Response) -> bytes:
        content_type = response.headers.get('Content-Type', 'text/plain')
        content_disposition = response.headers.get('Content-Disposition', '')
        for key in self.plugins:
            chunk = self.plugins[key].process_response(response.content, content_type, content_disposition, response.encoding)
        return chunk

    def process_request_headers(self, request_headers: dict[str, str], original_request_method: str) -> dict[str, str]:
        for key in self.plugins:
            request_headers = self.plugins[key].process_request_headers(request_headers, original_request_method)
        return request_headers
