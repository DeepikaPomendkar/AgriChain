from django.urls import path,include
from . import views

urlpatterns = [
    #path('',views.home,name='user-home'),
    path('',views.home,name='user-home'),
    path('signIn/',views.signIn,name='user-signIn'),
    path('postsignIn/',views.postsign,name='user-postsignIn'),
    path('signUp/',views.signUp,name='user-signup'),
    path('logout/',views.logout,name='user-logout'),
    path('postsignUp/',views.postsignUp,name='user-postsignUp'),
    path('farmer/',views.farmer,name='farmer'),
    path('processor/',views.processor,name='processor'),
     path('retailer/',views.retailer,name='retailer'),
    path('qualityChecker/',views.qualityChecker,name='qualityChecker'),
    path('payments/',views.payments,name='payments'),
    path('farmer/getData/',views.getData,name='getData'),
]