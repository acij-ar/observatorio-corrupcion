from pathlib import Path
from typing import Union, Optional, Dict, Any, List

from pydantic import AnyHttpUrl, EmailStr, validator #, BaseSettings
from pydantic_settings import BaseSettings # NEW


class Settings(BaseSettings):
    BASE_DIR: Optional[Path] = Path("data/")

    @validator("BASE_DIR", pre=True)
    def assemble_base_dir(
        cls, v: Union[str, Path], values: Dict[str, Any]
    ) -> Path:
        if isinstance(v, str):
            return Path(v)
        return v

    ARANGO_HOST: AnyHttpUrl
    ARANGO_DB: str
    ARANGO_USERNAME: str
    ARANGO_PASSWORD: str

    BOT_EMAIL_USER: EmailStr
    BOT_EMAIL_PASSWORD: str
    BOT_EMAILS_TO_NOTIFY: List[EmailStr]

    @validator("BOT_EMAILS_TO_NOTIFY", pre=True)
    def assemble_emails_to_notify(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()

# Create the output directories
for dir in ["cij", "email", "external", "PDFs", "db"]:
    p = settings.BASE_DIR / dir
    p.mkdir(parents=True, exist_ok=True)
