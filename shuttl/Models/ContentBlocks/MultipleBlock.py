import tempfile
from werkzeug.datastructures import FileStorage
import os

from .ContentBase import ContentBase
from shuttl import db, app
from .MultipleContent import MultipleContent


class NoTemplateException(Exception): pass

## Multiple Content block. This acts as a list
class MultipleBlock(ContentBase):


    id = db.Column(db.Integer, db.ForeignKey('content_base.id'), primary_key=True)

    ## id of the first multiContentNode in the list
    multipleBlock_id = db.Column(db.Integer, db.ForeignKey('multiple_content.id'))

    ## template associated with the multipleBlock
    templateCompiled = db.Column(db.String)

    ## the current multinode while being iterated over.
    currentMulti = None

    __mapper_args__ = {
        'polymorphic_identity': 'multiple_block',
    }

    ## Loads the first object of the list
    @property
    def firstContent(self):
        return MultipleContent.query.filter(MultipleContent.id == self.multipleBlock_id).first()

    ## Gets the content block. If it doesn't exist, this function creates it with optional content
    # \param webpage, the webpage that this block should belong to
    # \param name the name of this block
    # \param defaultContent the content this object has by default
    # \return a content block
    # \disc maybe this should return a tuple with a second position indicating if this object was created or not
    @classmethod
    def GetOrCreate(cls, name, webpage, compiledTemplate=""):
        block = cls.polyQuery().filter(cls.name==name).filter(cls.webpage_id==webpage.id).first()
        if block is None:
            firstMutiContent = MultipleContent.Create(
                name='multipleblockcontent_{0}_{1}_0'.format(name, webpage.id), 
                parent=webpage.website.hidden,
                website=webpage.website,
            )
            block = cls.Create(multipleBlock_id=firstMutiContent.id, webpage=webpage, name=name)
            firstMutiContent.owner_id = block.id
            firstMutiContent.save()
            pass
        block.templateCompiled = compiledTemplate
        block.save()
        return block

    ## Sets the content for the the block
    # \param content the content to be updated
    def setContent(self, content):
        # item = self[content["index"]]
        # del content["index"]
        for ndx, value in enumerate(content):
            self[ndx].updateContent(value)
            pass
        pass

    ## Gets the item at the index. This is basically just gets the correct MultiContent with the index like so Multiblock[ndx]
    # \param ndx the index that the object is at
    # \returns the object at index
    # \raises IndexError if the object doesn't exist at ndx
    def __getitem__(self, ndx):
        ndx = self._adjustIndex(ndx)
        obj = MultipleContent.query.filter(MultipleContent.owner_id == self.id).filter(MultipleContent.index == ndx).first()
        if obj is None:
            raise IndexError
        return obj

    ## Allows to perform a for loop over the MultiBlock like so `for i in self`
    # This sets the currentMulti to the firstContent
    # \returns self
    def __iter__(self):
        self.currentMulti = self.firstContent
        return self

    ## Gets the next Multicontent in the collection. Also sets currentMulti to the next object in the array
    # \returns the next object in the collection
    # \raises StopIteration when done
    def __next__(self):
        if self.currentMulti is None:
            raise StopIteration
        old = self.currentMulti
        try:
            self.currentMulti = next(self.currentMulti)
            pass
        except StopIteration:
            self.currentMulti = None
            pass
        return old

    ## Returns the legnth of the collection.
    def __len__(self):
        return MultipleContent.query.filter(MultipleContent.owner_id==self.id).count()

    ## iterates over the collection as well
    @property
    def content(self):
        multiBlock = []
        for i in self:
            multiBlock.append(i.content)
            pass
        return multiBlock

    ## Appends an MultipleContent to the collection at ndx
    # \param ndx the index to append to.
    # \returns the block that was created
    def append(self, ndx=-1):
        block = self[ndx]
        return block.addNext()

    def _build(self):
        template_code = compile(self.templateCompiled, self.__class__.__name__, "exec")
        return app.jinja_env.template_class.from_code(app.jinja_env, template_code, app.jinja_env.globals)

    ## Renders the block
    # \param context the context to publish
    # \param publishing indicates if this is being published
    # \return the html for the block
    def renderContent(self, context, template=None, publishing=False):
        template = template or self._build()
        multiBlocks = []
        for i in self:
            multiBlocks.append(i.renderContent(template, context, publishing))
            pass
        completeBlock = "".join(multiBlocks)
        if not publishing:
            completeBlock = """
            <shuttl-multiblock page="{page}" block="{block}" id="{name}">{content}</shuttl-multiblock>
            """.format(page = self.webpage_id, name=self.id, block=self.name, content="".join(multiBlocks))
            pass
        return completeBlock

    ## Removes and returns the object. But it doesn't delete the object from the DB.
    # \param ndx the index of the object to pop
    # \return obj the object at index
    def pop(self, ndx=0):
        ndx = self._adjustIndex(ndx)
        obj = self[ndx].pop()
        if obj is None:
            return
        self.fixIndex()
        return obj

    ## removes and deletes the object at ndx
    # \param ndx the index to get removed
    def remove(self, ndx=-1):
        obj = self.pop(ndx)
        if obj is None:
            return
        obj.delete()
        pass

    ## adjusts the index so that we can use negative indexes for example -1
    # will access the last object in the collection
    # \param ndx the index to adjust
    # \returns ndx if ndx >= 0 otherwise returns the legnth minus the index.
    def _adjustIndex(self, ndx):
        return ndx if ndx >= 0 else len(self) + ndx

    ## Iterates over the multiple contents and then fix the index for the block
    def fixIndex(self):
        index = 0
        for i in self:
            i.index = index
            index += 1
            i.save()
            pass
        pass

    ## Moves the the object at index from to index to
    # \param fro move the index of the object to move
    # \param to move the index to move the object to
    def move(self, fro, to):
        old = self[fro]
        new = self[to]
        old.appendBefore(new)
        self.fixIndex()
        pass