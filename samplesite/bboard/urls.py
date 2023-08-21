import bbs as bbs
from django.urls import path
from django.views.generic import WeekArchiveView

from bboard.models import Bb
from bboard.views import index, detail, BbByRubricView, BbDetailView, BbAddView, BbMonthArchiveView, BbRedirectView,rubrics,bbs

urlpatterns = [
    path('', index, name='index'),
    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),
    path('page1/<int:page>/', index, name='page1'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('<int:rubric_id>/page/<int:page>/', BbByRubricView.as_view(), name='rubric_page'),
    path('read/<int:rec_id>/', detail, name='read'),
    path('add/', BbAddView.as_view(), name='add'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('<int:year>/<int:month>/', BbMonthArchiveView.as_view()),
    path('<int:year>/week/<int:week>/',
         WeekArchiveView.as_view(model=Bb, date_field="published", context_object_name='bbs')),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old.detail'),

]
