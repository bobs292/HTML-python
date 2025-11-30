class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        if not self.props:
            return ""
        s = ""
        for x in self.props:
            s = s + f' {x}="{self.props[x]}"'
        return s
    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props})"
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    @property
    def children(self):
        return None

    @children.setter
    def children(self, value):
        if value not in (None, [], ()):
            raise ValueError("LeafNode cannot have children")
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        # Self-closing tags like img don't need closing tags
        if self.tag == "img":
            return f"<{self.tag}{props_html}>"
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props = None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        s = ""
        if not self.tag:
            raise ValueError("ParentNode requires a value")
        if not self.children:
            raise ValueError("ParentNode requires a child")
        props_html = self.props_to_html()
        for child in self.children:
            s = f"{s}{child.to_html()}"
        return f"<{self.tag}{props_html}>{s}</{self.tag}>"