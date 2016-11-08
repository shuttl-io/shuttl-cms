from jinja2 import nodes
from jinja2.ext import Extension
from flask import g
import re

from shuttl import app

class TagNameConflictError(Exception): pass


## base class of all tags.
#
class BaseTagExtension(Extension):

    ## the end tag of the tag, if applicable
    endTag = None

    ## Sets the render so that only one can be rendered
    onlyOneRender = True

    def __init__(self, environment):
        super(BaseTagExtension, self).__init__(environment)
        g.previous = set()
        pass

    ## parses the  arguments
    # \param context the context for this render
    # \parser the current parser
    # \return args the arguments for the action
    def _parseArgs(self, context, parser):
        args = [context, parser.parse_expression()]
        while parser.stream.skip_if('comma'):
            args.append(parser.parse_expression())
            pass
        return args

    ## Parse the tag.
    # \param parser the parser that is parsing the Template
    # \return a node
    def parse(self, parser):
        lineno = next(parser.stream).lineno
        context = nodes.ContextReference()
        args = self._parseArgs(context, parser)
        self.body = self._getBody(parser)
        self.template = self._compileInside()
        return nodes.CallBlock(self.call_method('_preAction', args),
                               [], [], []).set_lineno(lineno)

    ## called before any other actions are taken, just pops caller for now.
    #
    # \disc this method can be overridden but you usually want to override _action
    def _preAction(self, context,  *args, **kwargs):
        caller = kwargs.pop("caller")
        if self.endTag:
            pass
        if self.onlyOneRender:
            if not hasattr(g, "previous"):
                g.previous = set()
                pass
            name = args[0]
            if name in g.previous:
                raise TagNameConflictError("Tag with name {0} was already rendered".format(name))

            g.previous.add(name)
            pass
        self._loadInfo(context)
        return self._action(context, *args, **kwargs)

    def _loadInfo(self, context):
        self.page      = context.get("page")
        self.website   = context.get("website") 
        self.publisher = context.get("publisher")
        pass

    ## The action of the tag
    # \param context the context of the rendering template
    # \return the html of the tag
    # \raise NotImplementedError
    def _action(self, context, name, *args, **kwargs):
        raise NotImplementedError

    # ## Gets the Body of the tag, this is for tags with an end tag
    # # \param parser the parser parsing the template.
    def _getBody(self, parser):
        if self.endTag is not None:
            return parser.parse_statements(['name:{0}'.format(self.endTag)], drop_needle=True)
        return []

    ## Takes the AST generated by the parser and builds the template so that we can render the template.
    # \return a template object. 
    def _compileInside(self):
        if self.endTag is None:
            return None
        template_node = nodes.Template(self.body)
        fileName = "<{0}>".format(self.__class__.__name__)
        generator = app.jinja_env.code_generator_class(app.jinja_env, 
            "<{0}>".format(self.__class__.__name__), 
            fileName
        )
        generator.visit(template_node)
        self.template_code = generator.stream.getvalue()
        template_code = compile(self.template_code, fileName, "exec")
        return app.jinja_env.template_class.from_code(app.jinja_env, template_code, app.jinja_env.globals)