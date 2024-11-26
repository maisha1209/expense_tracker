# myproject/urls.py

from django.contrib import admin
from django.urls import path, include



app_name = 'project-url'
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('expense_tracker.urls')),  # This includes the app-level URLs
    path('expense_tracker/', include('expense_tracker.urls', namespace='expense_tracker')),


    # path('', include(('expense_tracker.urls', 'expense_tracker'), namespace='expense_tracker')),
]
