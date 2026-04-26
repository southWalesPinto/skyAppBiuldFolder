from django.conf import settings
from django.shortcuts import redirect


class RequireLoginMiddleware:
    public_exact_paths = {
        "/signup/success/",
        "/redirecting/",
        "/signed-out/",
        "/favicon.ico",
    }
    public_prefixes = (
        "/admin/",
        "/login/",
        "/admin-login/",
        "/signup/",
        "/password-reset/",
        "/static/",
        "/media/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated or self._is_public_path(request.path_info):
            return self.get_response(request)

        login_url = settings.LOGIN_URL or "/login/"
        return redirect(f"{login_url}?next={request.get_full_path()}")

    def _is_public_path(self, path):
        if path in self.public_exact_paths:
            return True
        return any(path.startswith(prefix) for prefix in self.public_prefixes)
