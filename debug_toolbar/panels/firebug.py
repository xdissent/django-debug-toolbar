from debug_toolbar.panels import DebugPanel
from django.template.loader import render_to_string

class FirebugPanel(DebugPanel):
    has_content = True
    name = 'Firebug'
        
    def title(self):
        return 'Firebug'

    def url(self):
        return ''
            
    def content(self):
        return render_to_string('debug_toolbar/panels/firebug.html')
        
        
    
        