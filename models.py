from django.db import models
from wikimirror import wikidump_dir, parser_script
import re
import shlex
import subprocess
import HTMLParser

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500, help_text="The title of the article.")
    archive = models.FilePathField(path=wikidump_dir, match="rec*.bz2", recursive=True, help_text="The archive in which this article is located.")
    source = models.CharField(max_length=100, help_text="The wiki where the original article is located (e.g. wikibooks).")

    @property
    def content(self):
        p = subprocess.Popen(shlex.split('perl {script} "{archive}" "{title}"'.format(script=parser_script, archive=self.archive, title=self.title)), stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return open(stdout.strip()).read()

    def __unicode__(self):
        return self.title
