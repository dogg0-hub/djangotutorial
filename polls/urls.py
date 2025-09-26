from django.urls import path

from . import views

#path("URLのパターン", 実行するビュー関数, name="名前")
app_name ="polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

]