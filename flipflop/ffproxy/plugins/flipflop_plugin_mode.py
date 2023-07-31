from enum import Enum

class FlipFlopPluginMode(Enum):
    """
    Enumeration representing the mode of operation for FlipFlop plugins.

    The `FlipFlopPluginMode` enum defines three possible modes of operation for FlipFlop plugins: ENABLED, DISABLED, and
    LOGGING_ONLY. These modes determine how the plugins will be processed during the reverse proxy request and response
    flow.

    Enum Values:
        ENABLED (str): The plugin is enabled and will actively process the request/response data.
        DISABLED (str): The plugin is disabled and will not modify the request/response data.
        LOGGING_ONLY (str): The plugin is in logging-only mode and will only log data without modifying the response.

    Note:
        - Plugins can be registered with one of these modes to control their behavior during the reverse proxy flow.
    """

    ENABLED = 'enabled'
    DISABLED = 'disabled'
    LOGGING_ONLY = 'logging_only'
