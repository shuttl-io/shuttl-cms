from jinja2 import nodes
from flask import render_template_string

from .Base import BaseTagExtension
from shuttl.Models.ContentBlocks.GlobalBlock import GlobalBlock
from shuttl.Models.FileTree.FileObjects.Template import Template
from shuttl.Models.FileTree.Directory import Directory

## The class for Obtain tags
class ForEachTag(BaseTagExtension):
    ## What tags trigger this extension
    tags = {'foreach'}
    endTag = "endforeach"

    ## Parse the arguments
    # \param context the current context
    # \param parser the parser that is parsing the template
    def _parseArgs(self, context, parser):
        target = parser.parse_assign_target(extra_end_rules=('name:in',))
        parser.stream.expect('name:in')
        directory = parser.parse_tuple(with_condexpr=False)
        args = [context, nodes.Const(target.name), directory]
        return args

    ## Obtain is like include but obtain is in the global scope
    # \param context the context rendering the content
    # \param path the path of the template to include
    # \return the rendered content for the block
    def _action(self, context, target, path, depth=1):
        pagesHTML = []
        directory = self.website.getDirectoryFromPath(path)
        if directory is None:
            return "<p>Directory doesn't exist</p>" if not context["publishing"] else ""
        childrenElements = self.getChildren(directory, depth-1)
        prior = context.get(target)
        context = dict(**context)
        for i in childrenElements:
            context[target] = i
            i.setContext(context)
            pagesHTML.append(self.template.render(**context))
            pass
        return "".join(pagesHTML)

    ## Recursively get the children
    # \root the node to get the child of
    # \param depth the depth of the crawl
    # \note if depth == 0 it will not look at the children.
    def getChildren(self, root, depth):
        children = []
        for child in root.children:
            if child.isHidden:
                continue
            if type(child) == Directory:
                if depth != 0:
                    children.append(self.getChildren(child, depth-1))
                    pass
                else:
                    children.append(child.render())
                    pass
                pass
            else:
                children.append(child)
                pass
            pass
        return children