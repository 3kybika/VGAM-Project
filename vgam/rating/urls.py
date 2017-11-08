from django.conf.urls import url

from rating.views import *

urlpatterns = [
    url(r'^$', 		  	  indexPage, 		name='index_page'      ),
    url(r'simpleScript/', simpleWSGIScript, name='simpleWSGIScript'),
    url(r'registration/', registerUser,     name='register_page'   ),
    url(r'login/',		  loginUser,        name='login_page'      ),
    url(r'logout/',		  logoutUser,       name='log-out'     	   ),
    url(r'main/', 		  ratingPage, 		name='rating_page'     ),
    url(r'profile/', 	  profilePage, 		name='profile_page'    ),
]
