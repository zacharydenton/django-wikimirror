from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, render_to_response
from models import Article
# Create your views here.

@cache_page(60 * 60 * 24 * 30)
def article(request, source, article_slug=""):
    if article_slug == "":
        article_slug = "Main_Page"
    article_slug = article_slug.encode('utf-8')
    if article_slug.endswith("/"):
        article_slug = title[:-1]
    try:
        article = get_object_or_404(Article, source=source, title__exact=article_slug.replace('_', ' '))
    except Article.MultipleObjectsReturned:
        article = Article.objects.filter(source=source, title__exact=article_slug.replace('_', ' '))[0]
    return render_to_response('wikimirror/article.html', {'article': article}, context_instance=RequestContext(request)) 
