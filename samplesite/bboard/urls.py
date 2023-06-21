from django.urls import path

from bboard.views import BbCreateView, add_and_save, BbBuRubricView, IndexView, BbDetailView

vals = {
    'name': 'by_index',
    'beaver': 'beaver – это бобёр!'
}

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:rubric_id>/', BbBuRubricView.as_view(), name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    # path('add/', add_and_save, name='add'),
    path('read/<int:rec_id>/', BbDetailView.as_view(), name='read')




    # path('<int:rubric_id>/', by_rubric, vals, name='by_rubric'),
    # path('read/<int:rec_id>/', detail, name='read'),
    # path('add/save/', add_save, name='add_save'),
]
