"""
Development server startup script.

This script starts the FastAPI development server with proper configuration
for Windows environments, excluding problematic directories from file watching.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_excludes=[
            "venv/*",
            "*.db",
            "*.db-journal",
            "alembic/versions/*",
            "__pycache__/*",
            "*.pyc",
            ".pytest_cache/*",
        ],
        log_level="info",
    )
