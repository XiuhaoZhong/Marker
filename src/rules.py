__author__ = 'Zhongxh'

class Rule:
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    """
    Header is a string which length is less than 70 and isn't ending with ":"
    """
    type = 'heading'
    def condition(self,block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ":"

class TitleRule(HeadingRule):
    """
    Title is a document's fist block, which acts as the topic.
    """
    type = 'title'
    first = True

    def condition(self, block):
        if not self.fitst:
            return False
        self.first = False
        return HeadingRule.condition(self, block)

class ListItemRule(Rule):
    """
    List Item starts with an en dash, which is part of format, and will be deleted in the end.
    """
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        handler.start(self, type)
        print "here is in listitem rule" + block
        handler.feed(block[1:].strip())
        handler.end(self, type)
        return True

class ListRule(ListItemRule):
    """
    When a listitem start beteewn a non-listitem and a listitem, ending with the last listitem
    """
    type = 'list'
    inside = False
    def condition(self, block):
        return True
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self, type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self, type)
            self.inside = False
        return False

class ParagraphRule(Rule):
    """
    Paragraph doesn't according with others' rule
    """
    type = 'paragraph'
    def condition(self, block):
        return True