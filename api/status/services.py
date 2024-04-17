import dataclasses
import datetime
from user import services as user_service
from .models import Status
from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
@dataclasses.dataclass
class StatusDataClass():

    content: str
    id: int = None
    date_published: datetime.datetime = None
    user: user_service.UserDataClass = None

    @classmethod
    def from_instance(cls, status_model: "Status") -> "StatusDataClass":
        return cls(
            id=status_model.id,
            content=status_model.content,
            date_published=status_model.date_published,
            user=status_model.user
        )

def create_status(user, status: "StatusDataClass") -> "StatusDataClass": 
    status_create = Status.objects.create(
        content=status.content,
        user=user
    )

    return StatusDataClass.from_instance(status_model=status_create)

def get_user_statuses(user: "User"):
    user_status = Status.objects.filter(user=user).all()

    return [ StatusDataClass.from_instance(status) for status in user_status ]

def get_user_status_detail(status_id: int) -> "StatusDataClass":
    status = get_object_or_404(Status, pk=status_id)

    return StatusDataClass.from_instance(status_model=status)

def delete_user_status(user: "User", status_id: int) -> "StatusDataClass":
    status = get_object_or_404(Status, pk=status_id)

    if status.user.id != user.id:
        raise exceptions.PermissionDenied("You are not the user")
    
    status.delete()

def update_user_status(user: "User", status_id: int, status_data: "StatusDataClass") -> "StatusDataClass":
    status = get_object_or_404(Status, pk=status_id)

    if status.user.id != user.id:
        raise exceptions.PermissionDenied("You are not the user")
    
    status.content = status_data.content
    status.save()
    
    return StatusDataClass.from_instance(status_model=status)