# from fastapi import FastAPI
# import importlib.util
# import os

# # Import routes dynamically from local path to avoid name collisions with similarly named modules
# spec = importlib.util.spec_from_file_location("local_routes_support", os.path.join(os.path.dirname(__file__), "routes", "support.py"))
# support = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(support)

# app = FastAPI(title="Support PoC")

# app.include_router(support.router)

# @app.get("/")
# def root():
#     return {"message": "Support PoC running"}

from fastapi import FastAPI
from src.app.routes.support import router as support_router

app = FastAPI(title="Support PoC")

app.include_router(support_router)


@app.get("/")
def root():
    return {"status": "ok"}
