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
        self.view_func = None
        self.content = None
        
    def title(self):
        return 'Profile'

    def url(self):
        return ''
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        logging.debug('Processing view')
        if request.REQUEST.has_key('prof'):
            self.view_func = view_func
            logging.debug('Profiler key found in request')
            self.profiler = profile.Profile()
            self.profiler.runcall(view_func, request, *view_args, **view_kwargs)
            
    def process_response(self, request, response):
        logging.debug('Processing response')
        if request.REQUEST.has_key('prof') and self.view_func is None:
            logging.debug('Profiler disabled - No view function to profile')
            self.content = '<p>This view cannot be profiled.</p>'
            
    def content(self):
        if self.profiler is not None:
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
        
            self.tmpfile = tempfile.mktemp()
            self.profiler.dump_stats(self.tmpfile)
            stats = pstats.Stats(self.tmpfile)
        
            stats.sort_stats('time')
            stats.print_stats(.1)
        
            sys.stdout = old_stdout
            self.content = '<pre>%s</pre>' % out.getvalue()
        return render_to_string('debug_toolbar/panels/profile.html', {'content': self.content})
        
        
    
        