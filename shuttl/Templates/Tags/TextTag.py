from .Base import BaseTagExtension
from shuttl.Models.ContentBlocks.Text import TextBlock


## The class for Wysiwyg tags
class TextBlockExtension(BaseTagExtension):

    ## What tags trigger this extension
    tags = {'text'}

    ## Creates a Wysiwyg Block if it is needed, and returns the rendered block
    # \param context the context rendering the content
    # \param name the name of the block
    # \param default the default content
    # \return the rendered content for the block
    def _action(self, context, name, default=""):
        page = context["page"]
        publishing = context.get("publishing", False)
        block = TextBlock.GetOrCreate(page, name, default)
        return block.renderContent(context, publishing)

