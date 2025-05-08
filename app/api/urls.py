from django.urls import path
from .views import HelloWorld, Student
from .views import ContactListView
from .exam_views import ChatView

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('students/', Student.as_view(), name='list_student'),
    path('chat/',ChatView.as_view(), name='chat_view'),
]
