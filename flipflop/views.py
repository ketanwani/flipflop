import requests
from django.http import HttpResponse

def reverse_proxy_view(request, rest_of_path=''):
    # Get the CSRF token from the incoming request
    csrf_token = request.COOKIES.get('csrftoken')

    # Define the backend URL where the requests will be forwarded
    backend_url = 'http://localhost:8000'

    # Construct the complete request URL for the backend
    request_url = f"{backend_url}/admin/{rest_of_path}"

    # Get the request data from the client
    request_method = request.method
    request_headers = dict(request.headers)
    request_headers['X-CSRFToken'] = csrf_token  # Add the CSRF token to the headers
    request_body = request.body

    # Forward the request to the backend system
    response = requests.request(request_method, request_url, headers=request_headers, data=request_body)

    # Relay the backend response to the client
    return HttpResponse(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
