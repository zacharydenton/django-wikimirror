from django.core.management.base import BaseCommand, CommandError
from wikimirror.models import Article
from wikimirror import renderer
import os
import hashlib

class Command(BaseCommand):
    args = ''
    help = 'Renders all templates.'

    def handle(self, *args, **kwargs):
        templates = Article.objects.filter(title__contains="Template:")
        template_dir = os.path.join(renderer, 'templates')
        for template in templates:
            if 'doc' in template.title.lower():
                continue
            md5 = hashlib.md5()
            title = template.title.replace('Template:', '')
            title = title.lower()
            md5.update(title)
            name = '{hash}.mwt'.format(hash=md5.hexdigest())
            filename = os.path.join(template_dir, template.source, name) 
            if not os.path.isdir(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            if not os.path.exists(filename):
                f = open(filename, 'w')
                f.write(template.content)
                f.close()
