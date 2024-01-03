import asyncio
from sqlalchemy import insert, select, update, delete
from models import Order
from database import async_session_maker
from datetime import datetime
async def create_order(
    quantity: int,
    price: float,
    customer_id: int,
    notes: str = None
) -> tuple:
    async with async_session_maker() as session:
        query = insert(Order).values(
            quantity=quantity,
            price=price,
            customer=customer_id,
            created_at=datetime.utcnow(),
            notes=notes,
        ).returning(Order.id, Order.created_at, Order.customer)
        data = await session.execute(query)
        await session.commit()
        return tuple(data)[0]
async def fetch_orders(skip: int = 0, limit: int = 10) -> list[Order]:
    async with async_session_maker() as session:
        query = select(Order).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

async def get_order_by_id(order_id: int) -> Order | None:
    async with async_session_maker() as session:
        query = select(Order).filter_by(id=order_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def update_order(order_id: int, values: dict):
    if not values:
        return
    async with async_session_maker() as session:
        query = update(Order).where(Order.id == order_id).values(**values)
        result = await session.execute(query)
        await session.commit()

async def delete_order(order_id: int):
    async with async_session_maker() as session:
        query = delete(Order).where(Order.id == order_id)
        await session.execute(query)
        await session.commit()

async def main():
    await asyncio.gather(
        create_order(
            quantity=10,
            price=25.99,
            customer_id=12,
            notes='Order notes'
        ),
        get_order_by_id(1),
        fetch_orders(skip=0, limit=5),
    )

asyncio.run(main())