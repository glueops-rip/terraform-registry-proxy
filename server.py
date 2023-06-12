import os
import uvicorn

if __name__ == "__main__":
    LOCAL_DEV_MODE = os.getenv("LOCAL_DEV_MODE", "FALSE")
    if LOCAL_DEV_MODE == "FALSE":
        print("Running in PRODUCTION mode")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
        )
    else:
        print("Running in DEVELOPMENT mode")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            ssl_keyfile="./key.pem",
            ssl_certfile="./cert.pem",
        )
