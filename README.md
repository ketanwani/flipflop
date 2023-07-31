# flipflop
Reverse Proxy for Django
# FlipFlop Reverse Proxy Library

FlipFlop is a flexible and customizable reverse proxy library for Django web applications. It allows you to easily create a reverse proxy server that can handle incoming requests and forward them to backend servers, performing various actions and modifications along the way using plugins.

## Usage

1. Create a Django project or use an existing one.

2. Create your custom plugin classes by deriving them from the `FlipFlopPlugin` base class. You can implement various methods to process request headers, response content, and control streaming behavior.

3. Instantiate a `FlipFlopProxyHandler` object in your Django view, passing it a `FlipFlopConfig` object that specifies the source and target URLs, and any desired plugins.

4. Call the `handle_request` method on the `FlipFlopProxyHandler` object in your Django view to process incoming requests and forward them to the backend server.

## Plugin Development

You can create your own custom plugins by deriving them from the `FlipFlopPlugin` base class. Implement the necessary methods to control the behavior of your plugin. The plugin architecture allows you to modify request headers, process response content, and control streaming behavior.

## Testing

FlipFlop comes with a test suite that includes unit tests for various components of the library. You can run the tests using the following command:

```bash
python -m unittest discover tests
