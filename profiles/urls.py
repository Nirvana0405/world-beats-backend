from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
]


from django.urls import path
from .views import ProfileDetailView

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile-detail'),
]


# profiles/urls.py
from django.urls import path
from .views import ProfileRetrieveUpdateView

urlpatterns = [
    path('profile/', ProfileRetrieveUpdateView.as_view(), name='profile-detail'),
]


from django.urls import path
from .views import ProfileDetailView

urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
]







from django.urls import path
from .views import OtherUserProfileView

urlpatterns = [
    path('<int:user_id>/', OtherUserProfileView.as_view(), name='other_user_profile'),
]






# profiles/urls.py

from django.urls import path
from .views import OtherUserProfileView

urlpatterns = [
    path('<int:user_id>/', OtherUserProfileView.as_view(), name='other_user_profile'),
]




# profiles/urls.py

from django.urls import path
from .views import PublicProfileView

urlpatterns = [
    path('<int:user__id>/', PublicProfileView.as_view(), name='public-profile'),
]





# profiles/urls.py
from django.urls import path
from .views import OtherUserProfilesView

urlpatterns = [
    path('others/', OtherUserProfilesView.as_view(), name='other-profiles'),
]




