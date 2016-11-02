from shuttl.Models.FileTree.Webpage import Webpage
from shuttl import db

##Block for global scope. Must be like a web page.
class GlobalBlock(Webpage):

    id = db.Column(db.Integer, db.ForeignKey('webpage.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'global_block',
    }

    def _internalRender(self, data):
        return data

    ## Gets the content block. If it doesn't exist, this function creates it with optional content
    # \param webpage, the webpage that this block should belong to
    # \param name the name of this block
    # \param defaultContent the content this object has by default
    # \return a content block
    # \disc maybe this should return a tuple with a second position indicating if this object was created or not
    @classmethod
    def GetOrCreate(cls, template):
        content = cls.polyQuery().filter(cls.template_id==template.id).first()
        if content is None:
            content = cls.Create(template_id = template.id, website_id=template.website_id)
            pass
        return content

    ## Get the content of this content block
    # \param context the context that is being used to render the webpage
    # \param publishing indicates if the block is being published
    # \return a string representing the content block
    def renderContent(self, context, publishing=False):
        content = self.buildContent(context["publisher"])
        if not context["publishing"]:
            content = """
            <shuttl-obtain self_id="{id}">{content}</shuttl-obtain>
            """.format(id = self.id, content = content )
            pass
        return content

    ## The sys_name of the file, just the name with the space replaced with underscores
    # \return the name with underscores
    @property
    def sys_name(self):
        return "global.global"