from datetime import date
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, text
from typing import List

from ..models import Appointment, AppointmentState, AppointmentHistory, Customer, MedspaService, Procedure
from ..dependencies import SessionDep


router = APIRouter(
  prefix="/appointments",
  tags=["appointments"]
)

# This method is not very RESTFull-y. The problem here seems to be
# That the first get with a parameter stablish the hierarchy of
# the whole API. So having two different routes with id and state
# seems not to be possible within FASTApi.
@router.get("/state")
async def find_appointments_on_state(session: SessionDep, state: AppointmentState):
  # Using a ORM might not have been the best decision. SQLModel made some things really hard
  raw_sql = text("""
    SELECT a.*
    FROM appointment a
    JOIN (
      SELECT DISTINCT ON (appointment_id) appointment_id, state
        FROM appointmenthistory
        ORDER BY appointment_id, created_at DESC
    ) ah ON a.id = ah.appointment_id
    WHERE ah.state = :state
  """)
  result = session.execute(raw_sql, {"state": state})
  appointments = [Appointment(**row._mapping) for row in result]
  return appointments


@router.get("/by_date")
async def find_appointments_by_date(session: SessionDep, date: date):
  appointments = session.exec(select(Appointment).where(Appointment.start_time >= date))
  return appointments.all()


@router.get("/{appointment_id}")
async def appointment(session: SessionDep, appointment_id: int):
  appmnt = session.get(Appointment, appointment_id)
  if not appmnt:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
  procedures = appmnt.services
  return {
    "total_duration": sum(proc.duration for proc in procedures),
    "total_price": sum(proc.price for proc in procedures),
  } | vars(appmnt)


@router.post("/")
async def schedule(session: SessionDep, appointment: Appointment, customer: Customer, services: List[MedspaService]):
  existing_customer = session.exec(select(Customer).where(Customer.email == customer.email).limit(1)).all()
  if not existing_customer:
    session.add(customer)
    session.commit()
    existing_customer = customer
  else:
    existing_customer = existing_customer[0]
  appointment.customer_id = existing_customer.id
  session.add(appointment)
  session.commit()
  appmnt_history = AppointmentHistory(appointment_id=appointment.id, state=AppointmentState.SCHEDULED)
  session.add(appmnt_history)
  session.commit()
  # There's a N+1 query issue. We can optimize this later on
  for medspa_service in services:
    existing_service = session.get(MedspaService, medspa_service.id)
    if not existing_service:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Service {medspa_service.id} not found')
    procedure = Procedure(medspaservice_id=medspa_service.id, appointment_id=appointment.id)
    session.add(procedure)
  session.commit()


@router.put("/{appointment_id}/procedures")
async def add_procedures(session: SessionDep, appointment_id: int, services: List[MedspaService]):
  appointment = session.get(Appointment, appointment_id)
  if not appointment:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
  for service in services:
    existing_service = session.get(MedspaService, service.id)
    if not existing_service:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Service {service.id} not found')
    procedure = Procedure(medspaservice_id=service.id, appointment_id=appointment.id)
    session.add(procedure)


@router.get("/{appointment_id}/procedures")
async def appointment_procedures(session: SessionDep, appointment_id: int):
  appmnt = session.get(Appointment, appointment_id)
  if not appmnt:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
  return session.exec(select(Procedure).where(Procedure.appointment_id == appmnt.id)).all()


# We assume the state can change to anything.
@router.put("/{appointment_id}/update_state")
async def update_appointment_state(session: SessionDep, appointment_id: int, state: AppointmentState, notes: str):
  appmnt = session.get(Appointment, appointment_id)
  if not appmnt:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
  appmnt_history = AppointmentHistory(appointment_id=appmnt.id, state=state, notes=notes)
  session.add(appmnt_history)
  session.commit()
