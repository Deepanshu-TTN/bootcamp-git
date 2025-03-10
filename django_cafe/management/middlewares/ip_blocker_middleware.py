from django.http import HttpResponseForbidden

BLOCKED_IPS = [
    # '127.0.0.1'
]

def blocker_middleware(get_response):
    def middleware(request):
        ip_address = request.META.get("HTTP_HOST").split(":")[0]
        ip_address = request.META.get("REMOTE_ADDR")

        if ip_address in BLOCKED_IPS:
            return HttpResponseForbidden("<h1>FORBIDDEN<h1>", status=403)
        
        response = get_response(request)

        return response
    
    return middleware

