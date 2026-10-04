from django.urls import path

from .views import (
    SkillListCreateView,
    UserSkillListCreateView,
    UserSkillDetailView,
)


urlpatterns = [

    path(
        "",
        SkillListCreateView.as_view(),
        name="skill-list-create"
    ),

    path(
        "my-skills/",
        UserSkillListCreateView.as_view(),
        name="my-skills"
    ),

    path(
        "my-skills/<int:pk>/",
        UserSkillDetailView.as_view(),
        name="my-skill-detail"
    ),

]