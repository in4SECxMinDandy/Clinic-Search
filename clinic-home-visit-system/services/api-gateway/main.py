"""
API Gateway - Main Application
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent))

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import httpx
from shared.config import get_settings

settings = get_settings()
structlog.configure(processors=[structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])
logger = structlog.get_logger()

SERVICE_URLS = {
    "auth": "http://auth-service:8003",
    "clinic": "http://clinic-service:8001",
    "booking": "http://booking-service:8002",
    "review": "http://review-service:8004",
    "notification": "http://notification-service:8005",
    "data-collector": "http://data-collector-service:8006",
}

# Phần đầu path sau /api/v1/ → service gateway (khớp với prefix router của từng microservice)
API_V1_ROUTE_PREFIX_TO_SERVICE = {
    "auth": "auth",
    "users": "auth",
    "locations": "auth",
    "clinics": "clinic",
    "doctors": "clinic",
    "gps": "clinic",
    "bookings": "booking",
    "reviews": "review",
    "notifications": "notification",
    "collectors": "data-collector",
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("api_gateway_starting", version=settings.APP_VERSION)
    yield
    logger.info("api_gateway_shutdown")

app = FastAPI(title="API Gateway", version=settings.APP_VERSION, description="Unified API Gateway", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"], expose_headers=["X-Request-ID"])
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.api_route("/api/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_v1(path: str, request: Request):
    """Chuyển tiếp /api/v1/... tới đúng microservice (path ví dụ: auth/register, clinics?...)"""
    prefix = path.split("/", 1)[0] if path else ""
    service = API_V1_ROUTE_PREFIX_TO_SERVICE.get(prefix)
    if not service or service not in SERVICE_URLS:
        return Response(content='{"error":"Service not found"}', status_code=404, media_type="application/json")

    target_url = f"{SERVICE_URLS[service]}/api/v1/{path}"
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ["host"]}
    headers["X-Forwarded-For"] = request.client.host if request.client else "unknown"

    try:
        body = await request.body()
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
            )
        out_headers = {
            k: v
            for k, v in response.headers.items()
            if k.lower() not in ("content-length", "transfer-encoding", "content-encoding")
        }
        ct = response.headers.get("content-type") or "application/json"
        if "application/json" in ct and "charset" not in ct.lower():
            ct = "application/json; charset=utf-8"
        out_headers["content-type"] = ct

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=out_headers,
            media_type=ct,
        )
    except httpx.RequestError as e:
        logger.error("proxy_error", service=service, error=str(e))
        return Response(content='{"error":"Service unavailable"}', status_code=503, media_type="application/json")


@app.get("/health")
async def health(): return {"status": "healthy", "service": "api-gateway", "version": settings.APP_VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
