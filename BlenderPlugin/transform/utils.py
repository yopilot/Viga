def build_server_url(base_url, endpoint):
    """Constructs the full URL for a given endpoint."""
    if not base_url.endswith('/'):
        base_url += '/'
    return f"{base_url}{endpoint}"
