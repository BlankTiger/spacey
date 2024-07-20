class Hitbox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update_pos(self, x_offset, y_offset):
        self.x += x_offset
        self.y += y_offset

    def overlaps(self, other):
        if self.x + self.width < other.x:
            return False
        if self.x > other.x + other.width:
            return False
        if self.y + self.height < other.y:
            return False
        if self.y > other.y + other.height:
            return False
        return True
