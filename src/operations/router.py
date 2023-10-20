import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationResponse, Operation

router = APIRouter(
    prefix="/operations",
    tags=["operation"],
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много-много данных, которые вычислялись сто лет!"


@router.get("/", response_model=OperationResponse)
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        # x = 1 / 0
        return {
            "status": "success",
            "data": result.all(),
            "details": None,
        }
    except ZeroDivisionError:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Делишь на ноль? Фатальная ошибка!",
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": str(e),
            }
        )


@router.post("/")
async def add_specific_operations(new_operation: Operation, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
