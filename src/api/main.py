from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from src.api.routes import router

app = FastAPI(
    title="BCB Exchange Rate API",
    description="API que acessa e retorna cotações de Dólar de forma automatizada via site do Banco Central.",
    version="0.1.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        location = error.get("loc", [])
        field = location[-1] if location else "campo desconhecido"
        msg_type = error.get("type", "")

        if msg_type == "missing":
            message = f"O parâmetro '{field}' é obrigatório."
        elif msg_type in ("float_parsing", "int_parsing", "decimal_parsing"):
            message = f"O parâmetro '{field}' deve ser um número válido."
        else:
            message = f"Valor inválido para o parâmetro '{field}'."

        errors.append({"campo": field, "erro": message})

    return JSONResponse(status_code=422, content={"detail": errors})

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
