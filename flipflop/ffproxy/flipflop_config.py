class FlipFlopConfig:
    """
    Class representing configuration settings for the FlipFlop reverse proxy.

    The `FlipFlopConfig` class allows users to specify configuration settings for the FlipFlop reverse proxy, including
    the source URL, target URL, and registered plugins.

    Note:
        - Users can create a `FlipFlopConfig` instance to provide essential configuration settings for the reverse proxy,
          such as source and target URLs.
        - Registered plugins can be specified during the initialization of the `FlipFlopConfig` instance.
    """

    def __init__(self, source_url: str, target_url: str, plugins: dict = {}):
        """
        Initialize the FlipFlopConfig instance with the specified source URL, target URL, and plugins.

        Args:
            source_url (str): The source URL to be replaced in the incoming response content.
            target_url (str): The target URL to replace the source URL in the incoming response content.
            plugins (dict, optional): A dictionary of registered plugins (default is an empty dictionary).
        """
        self._source_url = source_url
        self._target_url = target_url
        self._plugins = plugins

    def get_source_url(self) -> str:
        """
        Get the source URL for the reverse proxy.

        Returns:
            str: The source URL to be replaced in the incoming response content.
        """
        return self._source_url

    def get_target_url(self) -> str:
        """
        Get the target URL for the reverse proxy.

        Returns:
            str: The target URL to replace the source URL in the incoming response content.
        """
        return self._target_url

    def get_plugins(self) -> dict:
        """
        Get the dictionary of registered plugins.

        Returns:
            dict: A dictionary containing the registered plugins for the reverse proxy.
        """
        return self._plugins
