from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wikimirror.models import Article
from wikimirror import wikidump_dir
import os
import re
import glob
import shlex
import shutil
import subprocess

class Command(BaseCommand):
    args = '<dump_file dump_file ...>'
    help = 'Imports the specified wiki dumps to be used with wikimirror.'

    @transaction.commit_manually
    def handle(self, *args, **kwargs):
        for dump_file in args:
            dump_file = os.path.abspath(dump_file)
            dump = os.path.basename(dump_file)
            source = dump.split('-')[0]
            if source == "enwiki":
                source = "wikipedia"
            else:
                source = re.sub('^en', '', source)

            dump_dir = os.path.join(wikidump_dir, source)
            if os.path.isdir(dump_dir):
                shutil.rmtree(dump_dir)
            os.makedirs(dump_dir)
            os.chdir(dump_dir)
            shutil.copyfile(dump_file, os.path.join(dump_dir, dump))
            dump_file = os.path.join(dump_dir, dump)
            subprocess.call('bzip2recover {dump_file}'.format(dump_dir=dump_dir, dump_file=dump_file), shell=True)
            os.remove(dump_file)

            for archive in glob.iglob(os.path.join(dump_dir, 'rec*.bz2')):
                p = subprocess.Popen("bzcat '{archive}' | grep '<title' | perl -ne 'm/<title>([^<]+)<\/title>/ && print $1.\"\\n\";'".format(archive=archive), shell=True, stdout=subprocess.PIPE)
                stdout, stderr = p.communicate()
                processed = 0
                for title in stdout.splitlines():
                    article = Article(title=title, archive=os.path.abspath(archive), source=source)
                    article.save()
            transaction.commit()

