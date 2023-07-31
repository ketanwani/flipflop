class FlipFlopConfig:
    def __init__(self, source_url: str, target_url: str, plugins = {}):
        self._source_url = source_url
        self._target_url = target_url
        self._plugins = plugins

    def get_source_url(self):
        return self._source_url

    def get_target_url(self):
        return self._target_url

    def get_plugins(self):
        return self._plugins
