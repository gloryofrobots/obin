from obin.compile.parse import token_type as tt
from obin.compile.parse import nodes
from obin.compile.parse import tokens
from obin.types import api, space, plist, root


class InvalidIndentationError(Exception):
    def __init__(self, msg, position, line, column):
        self.position = position
        self.line = line
        self.column = column
        self.msg = msg


class Block(root.W_Root):
    def __init__(self, parent_level, level, push_end_on_dedent, push_end_of_expression_on_new_line, ignore_new_lines):
        self.parent_level = parent_level
        self.level = level
        self.push_end_on_dedent = push_end_on_dedent
        self.push_end_of_expression_on_new_line = push_end_of_expression_on_new_line
        self.ignore_new_lines = ignore_new_lines


def newblock_level(pl, l):
    return Block(pl, l, False, False, False)


def newblock(pl):
    return Block(pl, -1, False, False, False)


def newblock_code(pl):
    return Block(pl, -1, True, True, False)


def newblock_expression(pl):
    return Block(pl, -1, False, True, False)


def newblock_free(pl):
    return Block(pl, -1, False, False, True)


def newblock_top_level():
    return newblock_level(-1, 0)


def indentation_error(msg, token):
    raise InvalidIndentationError(msg, tokens.token_position(token),
                                  tokens.token_line(token),
                                  tokens.token_column(token))


class IndentationTokenStream:
    def __init__(self, _tokens, src):
        self.tokens = [token for token in _tokens]
        self.index = 0
        self.length = len(self.tokens)
        self.node = None
        self.token = None
        self.src = src
        self.generated_tokens = []
        self.blocks = plist.plist([newblock_top_level()])

    def current_block(self):
        return plist.head(self.blocks)

    def add_code_block(self):
        cur = self.current_block()
        self.blocks = plist.cons(newblock_code(cur.level), self.blocks)

    def add_expression_block(self):
        cur = self.current_block()
        self.blocks = plist.cons(newblock_expression(cur.level), self.blocks)

    def add_free_block(self):
        cur = self.current_block()
        self.blocks = plist.cons(newblock_free(cur.level), self.blocks)

    def add_to_generated(self, token):
        self.generated_tokens.append(token)

    def next_generated(self):
        t = self.generated_tokens.pop()
        return t

    def has_generated(self):
        return len(self.generated_tokens) != 0

    def _next(self):
        token = self.tokens[self.index]
        print "NEXT TOKEN", token
        self.index += 1
        return token

    def _on_newline(self):
        next_token = self._next()
        if next_token != tt.TT_SPACES:
            self.index += 1
            level = 0
        else:
            level = len(tokens.token_value_s(next_token))

        block = self.current_block()
        # new uninitialized block
        # FIXME IT WILL BROKE COMBINED APPROACH when if x == 1 -> somecode \n somecode
        if block.level == -1:
            if level < block.parent_level:
                return indentation_error(u"Indentation level is too small", next_token)
            block.level = level
            return self._next()

        # new free block
        if block.ignore_new_lines is True:
            if level <= block.parent_level:
                return indentation_error(u"Indentation level of free block must be lesser then of parent block",
                                         next_token)
            return self._next()

        if level > block.level:
            return indentation_error(u"Invalid indentation level", next_token)

        # dedent
        blocks = self.blocks
        while True:
            block = plist.head(blocks)
            blocks = plist.tail(blocks)
            if space.isvoid(block):
                return indentation_error(u"Indentation does not match with any of previous levels", next_token)

            if block.level < level:
                return indentation_error(u"Invalid indentation level", next_token)
            elif block.level > level:
                if block.push_end_of_expression_on_new_line is True:
                    self.add_to_generated(tokens.create_end_expression_token(next_token))
                if block.push_end_on_dedent is True:
                    self.add_to_generated(tokens.create_end_token(next_token))
            elif block.level == level:
                if block.push_end_of_expression_on_new_line is True:
                    self.add_to_generated(tokens.create_end_expression_token(next_token))

                if self.has_generated():
                    return self.next_generated()
                return self.next()
            self.blocks = blocks

    def next(self):
        if self.has_generated():
            return self.next_generated()

        if self.index >= self.length:
            return self.node

        token = self._next()
        if tokens.token_type(token) == tt.TT_NEWLINE:
            return self._on_newline()

        self.token = token
        self.node = nodes.node_blank(self.token)
        return self.node
