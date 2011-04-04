from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
        url(r'^(?P<source>\w+)/(?P<article_slug>.+)/$', 'wikimirror.views.article', name='wikimirror-article'),
        )
