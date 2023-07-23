import re
import requests
from django.http import HttpResponse

def reverse_proxy_view(request, rest_of_path=''):
    # Get the CSRF token from the incoming request
    csrf_token = request.COOKIES.get('csrftoken')

    # Define the backend URL where the requests will be forwarded
    backend_url = 'https://www.python.org'

    # Construct the complete request URL for the backend
    request_url = f"{backend_url}/{rest_of_path}"
    print(request_url)

    # Preserve the original request method, body, and headers
    original_request_method = request.method
    original_request_body = request.body
    original_request_headers = {key: value for key, value in request.headers.items()}
    del original_request_headers['Host']
    # Remove the "Content-Length" header to avoid conflicts
    if 'Content-Length' in original_request_headers:
        del original_request_headers['Content-Length']

    # Construct the headers for the new request to the backend
    new_request_headers = {
        'X-CSRFToken': csrf_token,
        **original_request_headers,
    }

    # Make the request to the backend using requests library
    try:
        response = requests.request(
            method=original_request_method,
            url=request_url,
            data=original_request_body,
            headers=new_request_headers
        )
    except requests.exceptions.RequestException as e:
        return HttpResponse(str(e), status=500, content_type='text/plain')

    # Get the content type and status code from the response
    content_type = response.headers.get('Content-Type', 'text/plain')
    status_code = response.status_code
    if(content_type != "image/png"):
    # Modify the URLs in the response content to use the reverse proxy's domain
        if response.encoding:
            modified_content = re.sub(r'python\.org', 'localhost:8080', response.content.decode(response.encoding))
        else:
            modified_content = re.sub(r'python\.org', 'localhost:8080', response.content.decode('utf-8'))
    else:
        modified_content = response.content

    # Create the HttpResponse object with the correct content type and content
    return HttpResponse(modified_content, status=status_code, content_type=content_type)
