import requests
from django.http import HttpResponse
import sys
sys.path.append("/Users/ketanwani/projects/github/flipflop/flipflop")
from ffproxy.flipflop_config import FlipFlopConfig
from ffproxy.flipflop_proxy_handler import FlipFlopProxyHandler

def reverse_proxy_view(request, rest_of_path=''):
    config = FlipFlopConfig("localhost:8080", "www.python.org")
    proxy = FlipFlopProxyHandler(config)
    return proxy.handle_request(request, rest_of_path)
