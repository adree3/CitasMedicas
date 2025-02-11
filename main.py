from fastapi import FastAPI, Request
import uvicorn
from app import models
from app.routers import usuario, cita, medico
from app.db.database import *
from fastapi.responses import JSONResponse
from app.exceptions import NotFoundException, UnauthorizedException, ForbiddenException, BadRequestException, InternalServerErrorException




app = FastAPI(
    title="API de citas medicas",
    description="API para gestionar citas medicas.",
)

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(InternalServerErrorException)
async def internal_server_error_exception_handler(request: Request, exc: InternalServerErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    db.close()

app.include_router(usuario.router)
app.include_router(cita.router)
app.include_router(medico.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
