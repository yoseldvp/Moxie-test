from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..dependencies import SessionDep
from ..models import Medspa, MedspaService, Service, ServiceDetails


router = APIRouter(
  prefix="/medspas",
  tags=["medspas"],
)


@router.get("/")
async def medspas(session: SessionDep):
  return session.exec(select(Medspa)).all()


@router.get("/{medspa_id}")
async def medspa(session: SessionDep, medspa_id: int):
  medspa = session.get(Medspa, medspa_id)
  if not medspa:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medspa not found")
  return medspa


@router.get("/{medspa_id}/services")
async def medspa_services(session: SessionDep, medspa_id: int):
  medspa = session.get(Medspa, medspa_id)
  if not medspa:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medspa not found")
  return session.exec(select(MedspaService).where(MedspaService.medspa_id == medspa.id)).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(session: SessionDep, medspa: Medspa):
  session.add(medspa)
  session.commit()


@router.put("/{medspa_id}")
async def update(session: SessionDep, medspa_id: int, medspa: Medspa):
  old_spa = session.get(Medspa, medspa_id)
  if not old_spa:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
  old_spa.name = medspa.name
  old_spa.phone = medspa.phone
  old_spa.address = medspa.address
  session.add(old_spa)
  session.commit()
  return True


# This method is an upsert. We are allowing users to either create a new association or update an existing one
@router.put("/{medspa_id}/services/{service_id}", status_code=status.HTTP_201_CREATED)
async def associate_service(session: SessionDep, medspa_id: int, service_id: int, details: ServiceDetails):
  service = session.get(Service, service_id)
  medspa = session.get(Medspa, medspa_id)
  if not service or not medspa:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service or Medspa not found")
  existing_services = session.exec(select(MedspaService).where(MedspaService.medspa_id == medspa.id, MedspaService.service_id == service.id))
  for service in existing_services:
    service.price = details.price
    service.duration = details.duration
    session.add(service)
  else:
    medspa_service = MedspaService(medspa_id=medspa.id, service_id=service.id, price=details.price, duration=details.duration)
    session.add(medspa_service)
  session.commit()


@router.delete("/{medspa_id}")
async def delete(session: SessionDep, medspa_id: int):
  medspa = session.get(Medspa, medspa_id)
  if not medspa:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
  session.delete(medspa)
  session.commit


@router.get("/{medspa_id}/appointments")
async def appointments(session: SessionDep, medspa_id: int):
  medspa = session.get(Medspa, medspa_id)
  if not medspa:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
  return medspa.appointments
