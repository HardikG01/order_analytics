from fastapi import FastAPI
import routes

app = FastAPI(title="Order Stats API")
app.include_router(routes.router)
