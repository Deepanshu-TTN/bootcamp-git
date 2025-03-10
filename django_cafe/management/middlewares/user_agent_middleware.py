class UserAgentMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT")
        print(user_agent)
        response = self.get_response(request)
        return response
