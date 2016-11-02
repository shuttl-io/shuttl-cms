import jinja2

from .ContentBase import ContentBase
from shuttl import db


class TextBlock(ContentBase):

    ## The ID of the ContentBase
    id = db.Column(db.Integer, db.ForeignKey('content_base.id'), primary_key=True)

    content = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'text',
    }

    ##Get the content of this content block
    # \param context the context that is being used to render the webpage
    # \param publishing indicates if the block is being published
    # \return a string representing the content block
    def renderContent(self, context, publishing=False):
        if not publishing:
            return """
                <shuttl-text id='{page}_{block}_{id}' page='{page}' block='{block}' self_id="{id}">{content}</shuttl-text>
            """.format(page=self.webpage_id, block=self.name, id=self.id, content=jinja2.escape(self.content))
        return jinja2.escape(self.content)

    ## Sets the context if applicable
    # \param content the content to give to this block
    def setContent(self, content):
        self.content = content
        self.save()
        pass