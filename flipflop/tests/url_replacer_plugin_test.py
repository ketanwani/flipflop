import unittest
from ffproxy.plugins.url_replacer_plugin import UrlReplacerPlugin
from ffproxy.flipflop_config import FlipFlopConfig
from ffproxy.plugins.flipflop_plugin_mode import FlipFlopPluginMode

class TestUrlReplacerPlugin(unittest.TestCase):
    def setUp(self):
        self.backend_url = "backend.example.com"
        self.source_url = "reverse-proxy.example.com"
        self.config = FlipFlopConfig(self.source_url, self.backend_url)
        self.url_replacer = UrlReplacerPlugin("URL Replacer", self.config, FlipFlopPluginMode.ENABLED)

    def test_process_response_replace_urls(self):
        content = b"This is a test content with https://backend.example.com in it."
        content_type = "text/html"
        content_disposition = ""
        encoding = "utf-8"

        expected_replaced_content = "This is a test content with https://reverse-proxy.example.com in it."
        replaced_content = self.url_replacer.process_response(content, content_type, content_disposition, encoding)

        self.assertEqual(replaced_content, expected_replaced_content)
