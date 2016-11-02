from .ContentBase import ContentBase
from shuttl import db

class WysiwygBlock(ContentBase):

    ## The ID of the ContentBase
    id = db.Column(db.Integer, db.ForeignKey('content_base.id'), primary_key=True)

    content = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'wysiwyg',
    }

    ##Get the content of this content block
    # \param context the context that is being used to render the webpage
    # \param publishing indicates if the block is being published
    # \return a string representing the content block
    def renderContent(self, context, publishing=False):
        if not publishing:
            return """
                <shuttl-wysiwyg id='{page}_{block}' page='{page}' block='{block}' self_id='{id}'>{content}</shuttl-wysiwyg>
            """.format(page=self.webpage_id, block=self.name, id=self.id, content=self.content)
        return self.content

    ## Sets the context if applicable
    # \param content the content to give to this block
    def setContent(self, content):
        self.content = content
        self.save()
        pass