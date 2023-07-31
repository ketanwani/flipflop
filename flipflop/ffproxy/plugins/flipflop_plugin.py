from ffproxy.plugins.flipflop_plugin_mode import FlipFlopPluginMode
from ffproxy.flipflop_config import FlipFlopConfig
from typing import Awaitable, Dict

class FlipFlopPlugin:

    def __init__(self, name:str, config: FlipFlopConfig, mode = FlipFlopPluginMode.ENABLED):
        self._name = name
        self._mode = mode
        self._config = config

    def get_mode(self):
        return self._mode

    def set_mode(self, mode: FlipFlopPluginMode):
        self._mode = mode

    def get_name(self) -> str:
        return self._name


    def set_config(self,
        config: FlipFlopConfig,
    ):
        pass


    def process_request_headers(
        self,
        headers: dict[str, str],
        request_method: str,
    ) -> dict[str, str]:
        pass


    def process_response(
        self,
        chunk: bytes,
        content_type: str,
        content_disposition: str,
        encoding: str,
    ) -> bytes:
        pass


    def can_stream_response(self) -> bool:
        pass
