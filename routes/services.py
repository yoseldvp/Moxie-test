from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..dependencies import SessionDep
from ..models import Service


router = APIRouter(
  prefix="/services",
  tags=["services"]
)


@router.get("/")
async def services(session: SessionDep):
  return session.exec(select(Service)).all()


@router.get("/{service_id}")
async def service(session: SessionDep, service_id: int):
  service = session.get(Service, service_id)
  if not service:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
  return service


@router.put("/{service_id}", status_code=status.HTTP_200_OK)
async def update(session: SessionDep, service_id: int, service: Service):
  old_service = session.get(Service, service_id)
  if not old_service:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
  old_service.description = service.description or old_service.description
  old_service.name = service.name or old_service.name
  old_service.category_id = service.category_id or old_service.category_id
  session.add(old_service)
  session.commit()
  return True
