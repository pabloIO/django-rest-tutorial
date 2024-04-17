from django.urls import path
from .apis import StatusCreateListApi, StatusRetrieveUpdateDeleteApi

urlpatterns = [
    path("status/", StatusCreateListApi.as_view(), name="status"),
    path("status/<int:status_id>/", StatusRetrieveUpdateDeleteApi.as_view(), name="retrieve_status"),
]
