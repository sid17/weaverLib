from django.conf.urls import patterns, url
import views as vp

urlpatterns = patterns('',
    url(r'execFn/', vp.execFn, name='execFn'),
    
)
