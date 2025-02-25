import logging
import structlog
import json
from pathlib import Path
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter
from typing import Optional
from dataclasses import dataclass
from enum import Enum

class Environment(Enum):
    DEV = "dev"
    PROD = "prod"

@dataclass
class LogConfig:
    env: Environment = Environment.DEV
    log_level: int = logging.DEBUG
    log_dir: str = "vva_logs"
    log_filename: str = "voice_agent.log"
    max_bytes: int = 5 * 1024 * 1024
    backup_count: int = 3

def configure_logging(config: LogConfig):        
    log_dir = Path(config.log_dir)
    log_dir.mkdir(exist_ok=True)
    log_file_path = log_dir / config.log_filename

    handlers = []

    console_handler = logging.StreamHandler()
    if config.env == Environment.DEV:
        console_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    else:
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)

    # Main file handler
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=config.max_bytes,
        backupCount=config.backup_count,
        encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    handlers.append(file_handler)

    # Configure root logger first
    root_logger = logging.getLogger()
    root_logger.setLevel(config.log_level)
    for handler in handlers:
        root_logger.addHandler(handler)

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    processor_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer() if config.env == Environment.PROD
        else structlog.dev.ConsoleRenderer(colors=True),
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
        ],
    )

    console_handler.setFormatter(processor_formatter)
    file_handler.setFormatter(processor_formatter)

    third_party_levels = {
        "urllib3": logging.ERROR,
        "openai": logging.DEBUG,
        "deepgram": logging.ERROR,
        "silero": logging.ERROR,
        "livekit": logging.DEBUG,
        "httpcore": logging.ERROR,
        "httpx": logging.ERROR,
        "msal": logging.ERROR
    }
    
    for logger_name, level in third_party_levels.items():
        logging.getLogger(logger_name).setLevel(level)