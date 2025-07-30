
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, contracts # 👈 Import the new contracts router

app = FastAPI(title="ContractIQ API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the ContractIQ backend!"}

# Include the API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(contracts.router, prefix="/api/contracts", tags=["Contracts"])
