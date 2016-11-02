from flask import g

from shuttl import db
from shuttl.Models.FileTree.Webpage import Webpage

##Block for global scope. Must be like a web page.
class NodeLinkedException(Exception): pass

## the actual object in the collection
class MultipleContent(Webpage):

    id = db.Column(db.Integer, db.ForeignKey('webpage.id'), primary_key=True)

    ## The id of the next Node
    next_id = db.Column(db.Integer, db.ForeignKey('multiple_content.id'))

    ##The id of the previous Node
    previous_id = db.Column(db.Integer, db.ForeignKey('multiple_content.id'))

    ## The index of the node
    index = db.Column(db.Integer, default=0)

    ## The id of the MultipleBlock that this node belongs to
    owner_id = db.Column(db.Integer, db.ForeignKey('multiple_block.id'), )

    ## The actual owner object
    owner = db.relationship("MultipleBlock", foreign_keys=[owner_id])

    __mapper_args__ = {
        'polymorphic_identity': 'multiple_content',
    }

    ## Loads the actual next node of the collection
    # \returns the next node
    @property
    def next(self):
        return MultipleContent.query.filter(MultipleContent.id == self.next_id).first()

    ## Sets the next node
    # \param newNext the new next node
    @next.setter
    def next(self, newNext):
        self.next_id = newNext.id if newNext else None
        self.save()
        pass

    ## Loads the actual previous node of the collection
    # \returns the previous node
    @property
    def previous(self):
        return MultipleContent.query.filter(MultipleContent.id == self.previous_id).first()

    ## Sets the previous node
    # \param newprevious the new previous node
    @previous.setter
    def previous(self, newprevious):
        self.previous_id = newprevious.id if newprevious else None
        self.save()
        pass

    ## removes this node from the collection
    # \return this node
    def pop(self):
        if len(self.owner) == 1:
            return
        prev = self.previous
        nxt = self.next
        if prev is not None:
            prev.next = nxt
            pass
        if nxt is not None:
            nxt.previous = prev
            pass
        if self.id == self.owner.multipleBlock_id:
            self.owner.multipleBlock_id = self.next.id
            self.owner.save()
            pass
        self.owner_id = None
        self.next, self.previous = None, None
        return self

    ## Appends this node before block
    # \param the block to append this object before
    def appendBefore(self, block):
        if block is None:
            self.next = None
            return
        self.owner_id = block.owner_id
        prev = block.previous
        if self.previous is not None:
            raise NodeLinkedException
        self.previous = prev
        if prev is not None:
            prev.next = self
            prev.save()
            pass
        block.previous = self
        self.next = block
        self.save()
        block.save()
        pass

    ## Appends this node after block
    # \param the block to append this object after
    def appendAfter(self, block):
        if block is None:
            self.previous = None
            return 
        self.owner_id = block.owner_id
        nxt = block.next
        if self.next is not None:
            raise NodeLinkedException
        self.next = nxt
        if nxt is not None:
            nxt.previous = self
            nxt.save()
            pass
        block.next = self
        self.previous = block
        self.save()
        block.save()
        pass

    ## indicates if the block is adjecent to this
    # \returns 1 if block is before this node, -1 if block is after this node
    # and 0 for all other cases
    def isAdjacent(self, block):
        if self.next == block:
            return 1
        if self.previous == block:
            return -1
        return 0

    ## Moves the block up one
    # \sa _move
    def moveUp(self):
        self._move(self.previous, self.appendBefore)
        pass

    ## Moves the object down One.
    # \sa _move
    def moveDown(self):
        self._move(self.next, self.appendAfter)
        pass

    ## Moves the object either up or down and reasigns the index of the two
    # blocks.
    # \note This is what moveUp and MoveDown call. This is what actually does
    # the moving. This is basically a cheapo swap function
    # \param obj the other object to move with this object Should be either
    #   self.next or self.previous
    # \param func the operation to perfom on the two objects. Either appendBefore
    #   or appendAfter
    def _move(self, obj, func):
        owner_id = self.owner_id
        if obj is not None:
            self.pop()
            func(obj)
            self.index, obj.index = obj.index, self.index
            self.save()
            obj.save()
            pass
        self.owner_id = owner_id
        self.save()
        pass

    ## Adds a new object to the collection and adds it after this object.
    # \returns the block that was added.
    def addNext(self):
        block = MultipleContent.Create(
            name='multipleblockcontent_{0}_{1}'.format(self.name, self.index+1), 
            template=self.template, 
            owner_id=self.owner_id,
            website=self.website
        )
        block.index = self.index + 1
        oldNext = self.next
        self.next = block
        block.previous = self
        block.next = oldNext
        if oldNext is not None:
            oldNext.previous = block
            pass
        try:
            obj = next(block)
            while obj is not None:
                obj.index += 1
                obj = next(obj)
                pass
            pass
        except StopIteration:
            pass
        return block

    ## Gets the next object in the list
    # \returns self.next
    # \raises StopIteration if self.next is None
    def __next__(self):
        nxt = self.next
        if nxt is None:
            raise StopIteration
        return nxt

    ## Get the content of this content block
    # \param context the context that is being used to render the webpage
    # \param publishing indicates if the block is being published
    # \return a string representing the content block
    def renderContent(self, template, context, publishing=False):
        g.previous = set()
        context["page"] = self
        content =  template.render(**context)
        if not context.get("publishing", False):
            content = """
            <shuttl-multiItem self_id="{id}" index="{index}" owner="{owner_name}">{content}</shuttl-multiItem>
            """.format(id = self.id, content = content, index=self.index, owner_name=self.owner.name)
            pass
        return content

    ## The sys_name of the file, just the name with the space replaced with underscores
    # \return the name with underscores
    @property
    def sys_name(self):
        return "multiblock.multiblock"

    # def delete(self):
        
    #         pass
    #     super(MultipleContent, self).delete()