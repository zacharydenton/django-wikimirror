from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, render_to_response
from models import Article
# Create your views here.

@cache_page(60 * 60 * 24 * 30)
def article(request, article_slug):
    article_slug = article_slug.encode('utf-8')
    if article_slug.endswith("/"):
        article_slug = title[:-1]
    article = get_object_or_404(Article, title=article_slug.replace('_', ' '))
    return render_to_response('wikimirror/article.html', {'article': article}, context_instance=RequestContext(request)) 
