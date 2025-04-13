from decimal import Decimal
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str = Field(index=True, unique=True)


class Product(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str =  Field(index=True)
  markup: Decimal = Field(default=0, decimal_places=3)
  supplier: str | None
  service_id : int | None = Field(default=0, foreign_key="service.id")


class Procedure(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  appointment_id: int | None = Field(default=None, foreign_key="appointment.id")
  medspaservice_id: int | None = Field(default=None, foreign_key="medspaservice.id")


# As services are common to the system, we need a way to track which
# services a Medspa can offer.
class MedspaService(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  # Hacky!
  medspa_id: int | None = Field(default=None, foreign_key="medspa.id")
  service_id: int | None = Field(default=None, foreign_key="service.id")
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  price: Decimal = Field(default=0, decimal_places=3)
  # Duration will be stored in minutes. UI Has to transform the value to a user readable amount.
  duration: int =  Field(default=0)

  appointments: list["Appointment"] = Relationship(back_populates="services", link_model=Procedure)


class Service(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str = Field(index=True, unique=True)
  description: str | None
  category_id: int | None = Field(default=None, foreign_key="category.id")

  medspas: list["Medspa"] = Relationship(back_populates="services", link_model=MedspaService)


class Medspa(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str = Field(index=True, unique=True)
  address: str | None = Field(default=None)
  phone: str | None = Field(default=None)
  email_address: str | None = Field(default=None)

  services: list["Service"] = Relationship(back_populates="medspas", link_model=MedspaService)
  appointments: list["Appointment"] = Relationship(back_populates="medspa")


class Appointment(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  start_time: datetime
  medspa_id: int | None = Field(default=None, foreign_key="medspa.id")
  medspa: Medspa | None = Relationship(back_populates="appointments")
  customer_id: int | None = Field(default=None, foreign_key="customer.id")

  services: list["MedspaService"] = Relationship(back_populates="appointments", link_model=Procedure)


class ServiceDetails(BaseModel):
  price: Decimal
  duration: int


class Customer(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str
  email: str = Field(index=True)


class AppointmentState(Enum):
  SCHEDULED = "scheduled"
  COMPLETED = "completed"
  CANCELED = "canceled"


# Appointment data is considered immutable.
# We will only insert new records here in case a state transition is required.
# This strategy allows to keep track to what happens to any appointment.
# It also eliminates the need to update data and deal with potential race conditions.
class AppointmentHistory(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  state: AppointmentState = Field(default=AppointmentState.SCHEDULED)
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  appointment_id: int | None = Field(default=None, foreign_key="appointment.id")
  notes: str | None = Field(default="")
