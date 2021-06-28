from rest_framework import routers

from apps.photo_manager.api import PhotoViewSet

app_name = 'photo_manager'

router = routers.SimpleRouter()
router.register('photos', PhotoViewSet)
urlpatterns = router.urls
