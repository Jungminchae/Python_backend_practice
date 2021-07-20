from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet

router = DefaultRouter()
router.register("", QuestionViewSet)
app_name = "questions"

urlpatterns = router.urls

