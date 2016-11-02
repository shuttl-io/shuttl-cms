from shuttl import db
from shuttl.database import BaseModel
from sqlalchemy.exc import IntegrityError

## An Abstract Base Class to represent Content blocks
class ContentBase(db.Model, BaseModel):

    ##ID of object
    id = db.Column(db.Integer, primary_key=True)

    ## The webpage this object belongs to
    webpage_id = db.Column(db.Integer, db.ForeignKey('webpage.id'), nullable=False)

    ## The webpage this object belongs to
    webpage = db.relationship("Webpage", back_populates='contentBlocks')

    #name of the block
    name = db.Column(db.String, nullable=False)

    ## Type of the inherited class, this is used for polymorphic behavior
    type = db.Column(db.String(50))

    content = ""

    ## The arguments for the polymorphic behavior. SQLAlchemy link: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
    __mapper_args__ = {
        'polymorphic_identity': 'content_base',
        'polymorphic_on': type
    }

    __table_args__ = (
        db.UniqueConstraint('name', 'webpage_id', name='_name_webpage_uc'),
    )

    ## Get the content of this content block
    # \param context the context that is being used to render the webpage
    # \param publishing indicates if the block is being published
    # \return a string representing the content block
    def renderContent(self, context, publishing=False):
        raise NotImplementedError

    ## Gets the content block. If it doesn't exist, this function creates it with optional content
    # \param webpage, the webpage that this block should belong to
    # \param name the name of this block
    # \param defaultContent the content this object has by default
    # \return a content block
    # \disc maybe this should return a tuple with a second position indicating if this object was created or not
    @classmethod
    def GetOrCreate(cls, webpage, name, defaultContent=""):
        content = cls.polyQuery().filter(cls.name==name).filter(cls.webpage_id==webpage.id).first()
        if content is None:
            content = cls.Create(webpage=webpage, name=name)
            content.setContent(defaultContent)
            pass
        return content

    ## Sets the context if applicable
    # \param content the content to give to this block
    def setContent(self, content):
        pass

        ## Make a polymorphic Query, this will automatically cast objects to their inherited classes
        # \param cls_or_all defualts to ("*") this is the classes that we should cast to

    @classmethod
    def polyQuery(cls, cls_or_all=("*")):
        return cls.query.with_polymorphic(*cls_or_all)

    pass

class ContentMock(ContentBase):
    id = db.Column(db.Integer, db.ForeignKey('content_base.id'), primary_key=True)

    content = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'content_mock',
    }

    ##Get the content of this content block
    # \param context the context that is being used to render the webpage
    # \param publishing indicates if the block is being published
    # \return a string representing the content block
    def renderContent(self, context, publishing=False):
        if not publishing:
            return "<div class='testing'>{0}</div>".format(self.content)
        return self.content

    ## Sets the context if applicable
    # \param content the content to give to this block
    def setContent(self, content):
        self.content = content
        self.save()
        pass