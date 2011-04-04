import os
import settings
load_path = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))

try:
    wikidump_dir = settings.WIKIDUMP_DIR
except:
    import os
    wikidump_dir = os.path.expanduser("~/wikidumps")

parser_script = load_path('show.pl')
