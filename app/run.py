import logging

import uvicorn

from app.core.config import config

logging.basicConfig(
    format=config.logging.log_format,
    level=config.logging.log_level_value,
)

if __name__ == "__main__":
    uvicorn.run(
        app="app.presentation.api.main:main_app",
        host=config.run.run_host,
        port=config.run.run_port,
        reload=config.run.debug,
    )
