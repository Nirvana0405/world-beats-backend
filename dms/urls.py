# dms/urls.py

from django.urls import path

urlpatterns = [
    # 今は空でもOK。あとでAPIを追加できます。
]




# dms/urls.py
from django.urls import path
from .views import DirectMessageListCreateView

urlpatterns = [
    path('', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),
]



# dms/urls.py

from django.urls import path
from .views import DirectMessageListCreateView

urlpatterns = [
    path('', DirectMessageListCreateView.as_view(), name='dm-list-create'),
]





from django.urls import path
from .views import DirectMessageListCreateView

urlpatterns = [
    path('', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),
]
