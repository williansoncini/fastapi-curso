from typing import Generator, final
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session() -> Generator:
  session: AsyncSession = Session()
  
  try:
    yield session
  finally:
    await session.close()