from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('st/', include('st.urls')),
    path('admin/', admin.site.urls),
]