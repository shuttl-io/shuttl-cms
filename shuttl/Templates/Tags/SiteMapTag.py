from .Base import BaseTagExtension
from shuttl.Models.ContentBlocks.Wysiwyg import WysiwygBlock

class BaseVisitor:
    def __init__(self, isPublishing, site, root, context):
        self.isPublishing = isPublishing
        self.site = site
        self.content = self.buildContent(root, context)
        pass

    def buildContent(self, root, level=0):
        raise NotImplemented

class HtmlVisitor (BaseVisitor):

    def buildContent(self, root, context, level=0):
        htmlFormat = """
<ul class="directoryContainer {id} {root}" id="dirContainer-{id}">{content}</ul>
        """
        liFormat = """
<li class="{type}" id="{type}-{id}">
    <a href="{href}" class="{type}">{name}</a>
    {content}
</li>
        """
        liFormat2 = """
<li class="{type}" id="{type}-{id}">
    {content}
</li>
        """
        aFormat = """
<a href="{href}" class="{type} {name}">{name}</a>
{content}
        """
        highlightedFormat = """ 
        <li class="{type}" id="{type}-{id}">
            <div class="highlighted"></div>
            <a href="{href}" class="{type}">{name}</a>
            {content}
        </li>
        """
        lis = []
        for child in root.children:
            child = child.cast()
            currPage = context.get("page")
            _liFormat = liFormat if currPage is  None or currPage != child else highlightedFormat
            if child.isHidden:
                continue
            if child.fileType == "dir":
                content = self.buildContent(child, context, level + 1)
                liStr = liFormat2.format(type=child.fileType, href="#", id=child.id, name=child.name, content=content)
                lis.append(liStr)
                pass
            else:
                href = "/show/{website_id}/{page_id}".format(website_id=self.site.id, page_id=child.id)
                if self.isPublishing:
                    href = child.fullPath
                    pass
                liStr = _liFormat.format(type=child.fileType, href=href, id=child.id, name=child.name, content="")
                lis.append(liStr)
                pass
        content = "".join(lis)
        isRoot = "root" if level == 0 else ""
        content = htmlFormat.format(id=root.id, root=isRoot, content = content)
        aStr = aFormat.format(type="dir", id=root.id, href="#", name=root.name, content=content)
        return aStr

## The class for Wysiwyg tags
class SiteMapExtension(BaseTagExtension):

    ## What tags trigger this extension
    tags = {'SiteMap'}

    ## Creates a Wysiwyg Block if it is needed, and returns the rendered block
    # \param context the context rendering the content
    # \param name the name of the block
    # \param default the default content
    # \return the rendered content for the block
    def _action(self, context, mapFormat="html"):
        mapFormat = mapFormat.lower()
        site = context["website"]
        if mapFormat == "html":
            klass = HtmlVisitor
            pass
        visitor = klass(isPublishing=context.get("publishing", False), site=site, root=site.root, context=context)
        return visitor.content
