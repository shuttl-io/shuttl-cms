from .Base import BaseTagExtension
from shuttl.Models.ContentBlocks.GlobalBlock import GlobalBlock
from shuttl.Models.FileTree.FileObjects.Template import Template


## The class for Obtain tags
class ObtainTagExtension(BaseTagExtension):

    ## What tags trigger this extension
    tags = {'obtain'}

    ## Obtain is like include but obtain is in the global scope
    # \param context the context rendering the content
    # \param path the path of the template to include
    # \return the rendered content for the block
    def _action(self, context, path):
        website = context["website"]
        context = dict(**context)
        template = Template.GetFileFromPath(path, website)
        block = GlobalBlock.GetOrCreate(template)
        return block.renderContent(context)