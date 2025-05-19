from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.upload     import router as upload_router
from .routes.summary    import router as summary_router
from .routes.tasks      import router as tasks_router
from .routes.history    import router as history_router
from .routes.train_ws   import router as train_ws_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(summary_router)
app.include_router(tasks_router)
app.include_router(history_router)
app.include_router(train_ws_router)
