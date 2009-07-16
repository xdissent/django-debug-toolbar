from debug_toolbar.panels import DebugPanel
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import escape
import logging
import tidy


class ValidatorPanel(DebugPanel):
    has_content = True
    name = 'Validator'
    
    def __init__(self):
        self.errors = []
        self.source = None
        
    def title(self):
        return 'Validator (%d)' % len(self.errors)

    def url(self):
        return ''
            
    def process_response(self, request, response):
        self.source = response.content
        parsed = tidy.parseString(self.source, { 'input_encoding': 'utf8' })
        self.errors = parsed.errors
        
        try:
            from pygments import highlight
            from pygments.lexers import HtmlLexer
            from pygments.formatters import HtmlFormatter
            
            formatter = HtmlFormatter(linenos='inline', lineanchors='validator')
            self.source = highlight(self.source, HtmlLexer(), formatter)
            
        except ImportError:
            self.source = '<pre>%s</pre>' % escape(self.source)
            
        self.source = mark_safe(self.source)
            
    def content(self):
        context = { 'errors': self.errors, 'source': self.source }
        return render_to_string('debug_toolbar/panels/validator.html', context)
        
        
    
        