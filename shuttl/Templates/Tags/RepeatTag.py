from .Base import BaseTagExtension
from shuttl.Models.ContentBlocks.MultipleBlock import MultipleBlock
from shuttl.Models.FileTree.FileObjects.Template import Template

## The class for Obtain tags
class RepeatTagExtension(BaseTagExtension):

    ## What tags trigger this extension
    tags = {'repeat'}
    endTag = "endrepeat"

    ## Obtain is like include but obtain is in the global scope
    # \param context the context rendering the content
    # \param path the path of the template to include
    # \return the rendered content for the block
    def _action(self, context, name):
        context = dict(**context)
        block = MultipleBlock.GetOrCreate(name, self.page, self.template_code)
        return block.renderContent(context, template=self.template)