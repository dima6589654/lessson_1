from django.urls import path
from salad.views import IndexSlView

urlpatterns = [
    path('', IndexSlView.as_view(), name='index1'),

]
