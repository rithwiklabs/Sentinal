# # pyrefly: ignore [missing-import]
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware


# # ============================================================
# # SENTINEL — PAYMENT RISK INTELLIGENCE
# # Backend Application
# # ============================================================

# app = FastAPI(
#     title="Sentinel — Payment Risk Intelligence API",
#     description="Backend API for analyzing payment risk",
#     version="1.0.0"
# )


# # ============================================================
# # CORS CONFIGURATION
# # Allows our HTML/CSS/JavaScript frontend
# # to communicate with the FastAPI backend.
# # ============================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ============================================================
# # ROOT ENDPOINT
# # ============================================================

# @app.get("/")
# def root():
#     return {
#         "message": "Sentinel Backend is running",
#         "status": "online",
#         "version": "1.0.0"
#     }


# # ============================================================
# # HEALTH CHECK
# # ============================================================

# @app.get("/api/health")
# def health_check():
#     return {
#         "status": "healthy",
#         "service": "Sentinel Risk Intelligence API"
#     }