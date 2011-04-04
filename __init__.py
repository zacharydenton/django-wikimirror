import settings
try:
    wikidump_dir = settings.WIKIDUMP_DIR
except:
    import os
    wikidump_dir = os.path.expanduser("~/wikidumps")
