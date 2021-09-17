from pathlib import Path
from typing import Union, Optional, Dict, Any

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    BASE_DIR: Optional[Path] = Path("data/")

    @validator("BASE_DIR", pre=True)
    def assemble_base_dir(
        cls, v: Union[str, Path], values: Dict[str, Any]
    ) -> Path:
        if isinstance(v, str):
            return Path(v)
        return v


settings = Settings()

# Create the directories
for dir in ["cij", "email", "external", "PDFs", "db"]:
    p = settings.BASE_DIR / dir
    p.mkdir(parents=True, exist_ok=True)
