from debug_toolbar.panels import DebugPanel
from django.template.loader import render_to_string
import sys, tempfile, pstats
from cStringIO import StringIO
import logging
try:
    import cProfile as profile
except:
    import profile

class ProfileDebugPanel(DebugPanel):
    has_content = True
    name = 'Profile'
    
    def __init__(self):
        self.profiler = None
        
    def title(self):
        return 'Profile'

    def url(self):
        return ''
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        logging.debug("Processing view")
        if request.REQUEST.has_key('prof'):
            logging.debug("Profiler key found in request")
            self.profiler = profile.Profile()
            return self.profiler.runcall(view_func, request, *view_args, **view_kwargs)
            
    def content(self):
        content = None
        if self.profiler is not None:
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
        
            self.tmpfile = tempfile.mktemp()
            self.profiler.dump_stats(self.tmpfile)
            stats = pstats.Stats(self.tmpfile)
        
            stats.sort_stats('time')
            stats.print_stats(.1)
        
            sys.stdout = old_stdout
            content = '<pre>%s</pre>' % out.getvalue()
        return render_to_string('debug_toolbar/panels/profile.html', {'content':content})
        
        
    
        