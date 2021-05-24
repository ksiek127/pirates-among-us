class Wall:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def player_collides(self, player_pos):
        return self.top_left[0] <= player_pos[0] <= self.bottom_right[0] and self.top_left[1] <= player_pos[1] <= self.bottom_right[1]