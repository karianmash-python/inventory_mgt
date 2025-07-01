from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Optional, Callable


class UtmParams:
    def __init__(
            self,
            utm_source: Optional[str] = None,
            utm_medium: Optional[str] = None,
            utm_campaign: Optional[str] = None,
            utm_term: Optional[str] = None,
            utm_content: Optional[str] = None,
    ):
        self.utm_source = utm_source
        self.utm_medium = utm_medium
        self.utm_campaign = utm_campaign
        self.utm_term = utm_term
        self.utm_content = utm_content


class UtmTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        utm_params = UtmParams(
            utm_source=request.query_params.get("utm_source"),
            utm_medium=request.query_params.get("utm_medium"),
            utm_campaign=request.query_params.get("utm_campaign"),
            utm_term=request.query_params.get("utm_term"),
            utm_content=request.query_params.get("utm_content"),
        )
        request.state.utm_params = utm_params
        response = await call_next(request)
        return response
