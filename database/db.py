import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config import DATABASE_URL


def fix_db_url(url: str) -> str:
    # 1. Scheme fix
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    # 2. SAARE query params hatao (sslmode, channel_binding, etc.)
    if "?" in url:
        url = url.split("?")[0]
    return url


FIXED_URL = fix_db_url(DATABASE_URL)
print(f"[DB] Connecting to: {FIXED_URL.split('@')[-1]}")  # debug

# Neon ke liye SSL zaruri hai
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

Base = declarative_base()

engine = create_async_engine(
    FIXED_URL,
    echo=False,
    connect_args={"ssl": ssl_ctx},
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
