# app/logger.py
import logging
from pathlib import Path

def setup_logger(name: str = "ixora_bot") -> logging.Logger:
    logs_dir = Path("storage") / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    # важно: чтобы хендлеры не плодились при повторных импортах
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    fh = logging.FileHandler(logs_dir / "bot.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger

logger = setup_logger()