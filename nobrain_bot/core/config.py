from dataclasses import dataclass
from dotenv import load_dotenv
import os


load_dotenv()


@dataclass
class Settings:
    bot_token: str
    admin_id: int
    site_url: str
    blog_url: str
    manager_url: str
    database_url: str


def get_settings() -> Settings:
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", ""),
        admin_id=int(os.getenv("ADMIN_ID", "0")),
        site_url=os.getenv("SITE_URL", ""),
        blog_url=os.getenv("BLOG_URL", ""),
        manager_url=os.getenv("MANAGER_URL", ""),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/nobrain"
        ),
    )
