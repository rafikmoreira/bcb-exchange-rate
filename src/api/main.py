from fastapi import FastAPI
from src.api.routes import router

from fastapi.responses import RedirectResponse

app = FastAPI(
    title="BCB PTAX API",
    description="API que acessa e retorna cotações de Dólar de forma automatizada via site do Banco Central.",
    version="0.1.0"
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
