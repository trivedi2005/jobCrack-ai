from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth import get_current_active_user
from app.models.connection import Connection
from app.models.user import User

router = APIRouter()


class ConnectionRequest(BaseModel):
    user_id: int


def person(user: User) -> dict:
    return {"id": user.id, "email": user.email, "role": user.role.value}


@router.get("/people")
async def people(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    users = db.query(User).filter(User.id != current_user.id, User.is_active == True).order_by(User.created_at.desc()).limit(50).all()
    existing = db.query(Connection).filter(
        (Connection.requester_id == current_user.id) | (Connection.recipient_id == current_user.id)
    ).all()
    statuses = {}
    for connection in existing:
        other_id = connection.recipient_id if connection.requester_id == current_user.id else connection.requester_id
        statuses[other_id] = connection.status
    return [{**person(user), "connection_status": statuses.get(user.id)} for user in users]


@router.get("/connections")
async def connections(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    rows = db.query(Connection).filter(
        ((Connection.requester_id == current_user.id) | (Connection.recipient_id == current_user.id)),
        Connection.status.in_(["pending", "accepted"]),
    ).all()
    result = []
    for row in rows:
        other_id = row.recipient_id if row.requester_id == current_user.id else row.requester_id
        other = db.query(User).filter(User.id == other_id).first()
        result.append({"id": row.id, "status": row.status, "direction": "sent" if row.requester_id == current_user.id else "received", "user": person(other)})
    return result


@router.post("/connections")
async def send_connection(
    request: ConnectionRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if request.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot connect with yourself")
    recipient = db.query(User).filter(User.id == request.user_id, User.is_active == True).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.query(Connection).filter(
        ((Connection.requester_id == current_user.id) & (Connection.recipient_id == request.user_id)) |
        ((Connection.requester_id == request.user_id) & (Connection.recipient_id == current_user.id))
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Connection is already {existing.status}")
    connection = Connection(requester_id=current_user.id, recipient_id=request.user_id)
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return {"id": connection.id, "status": connection.status}


@router.post("/connections/{connection_id}/accept")
async def accept_connection(
    connection_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    connection = db.query(Connection).filter(Connection.id == connection_id, Connection.recipient_id == current_user.id, Connection.status == "pending").first()
    if not connection:
        raise HTTPException(status_code=404, detail="Pending connection not found")
    connection.status = "accepted"
    db.commit()
    return {"id": connection.id, "status": connection.status}