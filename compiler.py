import re
import os
import six

class Compiler(object):
    RE_INTERPOLATE = re.compile(r'(\\)?([#!]){(.*?)}')
    selfClosing = [
        'meta'
      , 'img'
      , 'link'
      , 'input'
      , 'area'
      , 'base'
      , 'col'
      , 'br'
      , 'hr'
    ]
    autocloseCode = 'if,for,block,filter,autoescape,with,trans,spaceless,comment,cache,macro,localize,compress,raw'.split(',')

    filters = {}

    def __init__(self, node, **options):
        self.options = options
        self.node = node
        self.hasCompiledDoctype = False
        self.hasCompiledTag = False
        self.debug = False
        self.filters.update(options.get('filters', {}))
        self.selfClosing.extend(options.get('selfClosing', []))
        self.autocloseCode.extend(options.get('autocloseCode', []))
        self.useRuntime = options.get('useRuntime', True)
        self.indents = 0
        self.terse = False
        self.xml = False
        self.mixing = 0
        self.variable_start_string = '{{'
        self.variable_end_string = '}}'
        self.instring = False

    def compile(self):
        self.buf = ['']
        self.lastBufferedIdx = -1
        self.visit(self.node)
        compiled = u''.join(self.buf)
        if isinstance(compiled, six.binary_type):
            compiled = six.text_type(compiled, 'utf8')
        return compiled

    def var_processor(self, var):
        if isinstance(var,six.string_types) and var.startswith('_ '):
            var = '_("%s")'%var[2:]
        return var

    def buffer(self, str):
        if self.lastBufferedIdx == len(self.buf):
            self.lastBuffered += str
            self.buf[self.lastBufferedIdx - 1] = self.lastBuffered
        else:
            self.buf.append(str)
            self.lastBuffered = str;
            self.lastBufferedIdx = len(self.buf)

    def visit(self, node, *args, **kwargs):
        # debug = self.debug
        # if debug:
        #     self.buf.append('__jade.unshift({ lineno: %d, filename: %s });' % (node.line,('"%s"'%node.filename) if node.filename else '__jade[0].filename'));

        # if node.debug==False and self.debug:
        #     self.buf.pop()
        #     self.buf.pop()

        self.visitNode(node, *args, **kwargs)
        # if debug: self.buf.append('__jade.shift();')

    def visitNode (self, node, *args, **kwargs):
        name = node.__class__.__name__
        print('visiting {}'.format(name))
        if self.instring and name != 'Tag':
            self.buffer('\n')
            self.instring = False
        return getattr(self, 'visit%s' % name)(node, *args, **kwargs)

    def visitLiteral(self, node):
        self.buffer(node.str)

    def visitBlock(self, block):
        for node in block.nodes:
            self.visit(node)

    def visitTag(self,tag):
        self.indents += 1
        name = tag.name
        if not self.hasCompiledTag:
            if not self.hasCompiledDoctype and 'html' == name:
                self.visitDoctype()
            self.hasCompiledTag = True

        closed = name in self.selfClosing and not self.xml
        self.buffer('<%s' % name)
        self.visitAttributes(tag.attrs)
        self.buffer('/>' if not self.terse and closed else '>')

        if not closed:
            if tag.text: self.buffer(self.interpolate(tag.text.nodes[0].lstrip()))
            self.escape = 'pre' == tag.name
            # empirically check if we only contain text
            textOnly = tag.textOnly or not bool(len(tag.block.nodes))
            self.instring = False
            self.visit(tag.block)

            self.buffer('</%s>' % name)
        self.indents -= 1


    def _interpolate(self, attr, repl):
        return self.RE_INTERPOLATE.sub(lambda matchobj:repl(matchobj.group(3)),
                                       attr)

    def interpolate(self, text, escape=True):
        if escape:
            return self._interpolate(text,lambda x:'%s%s|escape%s' % (self.variable_start_string, x, self.variable_end_string))
        return self._interpolate(text,lambda x:'%s%s%s' % (self.variable_start_string, x, self.variable_end_string))


    def visitText(self,text):
        script = text.parent and text.parent.name == 'script'
        text = ''.join(text.nodes)
        text = self.interpolate(text, script)
        self.buffer(text)

    def visitString(self,text):
        instring = not text.inline
        text = ''.join(text.nodes)
        text = self.interpolate(text)
        self.buffer(text)
        self.instring = instring

    def visitAssignment(self,assignment):
        self.buffer('{%% set %s = %s %%}' % (assignment.name, assignment.val))

    def visitConditional(self, conditional):
        TYPE_CODE = {
            'if': lambda x: 'if %s'%x,
            'unless': lambda x: 'if not %s'%x,
            'elif': lambda x: 'elif %s'%x,
            'else': lambda x: 'else'
        }
        self.buf.append('{%% %s %%}' % TYPE_CODE[conditional.type](conditional.sentence))
        if conditional.block:
            self.visit(conditional.block)
            for next in conditional.next:
              self.visitConditional(next)
        if conditional.type in ['if','unless']:
            self.buf.append('{% endif %}')


    def visitVar(self, var, escape=False):
        var = self.var_processor(var)
        return ('%s%s%s%s' % (self.variable_start_string, var,
                              '|escape' if escape else '', self.variable_end_string))

    def visitEach(self,each):
        self.buf.append('{%% for %s in %s|__pyjade_iter:%d %%}' % (','.join(each.keys), each.obj, len(each.keys)))
        self.visit(each.block)
        self.buf.append('{% endfor %}')

    def attributes(self,attrs):
        return "%s__pyjade_attrs(%s)%s" % (self.variable_start_string, attrs, self.variable_end_string)

    def visitDynamicAttributes(self, attrs):
        buf, classes, params = [], [], {}
        terse='terse=True' if self.terse else ''
        for attr in attrs:
            if attr['name'] == 'class':
                classes.append('(%s)' % attr['val'])
            else:
                pair = "('%s',(%s))" % (attr['name'], attr['val'])
                buf.append(pair)

        if classes:
            classes = " , ".join(classes)
            buf.append("('class', (%s))" % classes)

        buf = ', '.join(buf)
        if self.terse: params['terse'] = 'True'
        if buf: params['attrs'] = '[%s]' % buf
        param_string = ', '.join(['%s=%s' % (n, v) for n, v in six.iteritems(params)])
        if buf or terse:
            self.buf.append(self.attributes(param_string))

    def visitAttributes(self, attrs):
        temp_attrs = []
        for attr in attrs:
            if (not self.useRuntime and not attr['name']=='class') or attr['static']: #
                if temp_attrs:
                    self.visitDynamicAttributes(temp_attrs)
                    temp_attrs = []
                n, v = attr['name'], attr['val']
                if isinstance(v, six.string_types):
                    if self.useRuntime or attr['static']:
                        self.buf.append(' %s=%s' % (n, v))
                    else:
                        self.buf.append(' %s="%s"' % (n, self.visitVar(v)))
                elif v is True:
                    if self.terse:
                        self.buf.append(' %s' % (n,))
                    else:
                        self.buf.append(' %s="%s"' % (n, n))
            else:
                temp_attrs.append(attr)

        if temp_attrs: self.visitDynamicAttributes(temp_attrs)

    ##################################################################

    def visitAssignment(self,assignment):
        self.buffer('{%% set %s = %s %%}'%(assignment.name,assignment.val))

    def visitEach(self,each):
        self.buf.append("{%% for %s in %s(%s,%d) %%}"%(','.join(each.keys),ITER_FUNC,each.obj,len(each.keys)))
        self.visit(each.block)
        self.buf.append('{% endfor %}')

    def attributes(self,attrs):
        return "%s%s(%s)%s" % (self.variable_start_string, ATTRS_FUNC,attrs, self.variable_end_string)

    ##################################################################

    @classmethod
    def register_autoclosecode(cls, name):
        cls.autocloseCode.append(name)
