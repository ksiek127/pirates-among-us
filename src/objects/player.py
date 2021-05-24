from datetime import datetime, timedelta
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_pos, position, role, cooldown, kill_distance, id):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.width = 50
        self.height = 50
        self.screen_pos = screen_pos  # pozycja na ekranie
        self.rect = pygame.Rect(position, (self.width, self.height))
        self.position = position  # faktyczna pozycja
        self.x_change = 0
        self.y_change = 0
        self.velocity = 30
        self.standard_velocity = self.velocity
        self.tasks = []
        self.is_dead = False
        self.kill_distance = kill_distance
        self.kill_cooldown = timedelta(seconds=cooldown)
        self.cant_kill_until = datetime.now() + self.kill_cooldown
        self.sabotage_cooldown = timedelta(seconds=cooldown)
        self.role = role
        self.name = ""
        self.in_task = False
        self.task_until = -1
        self.task = None
        self.in_game = False
        self.in_meeting = False
        self.voted_for = -1  # -1 brak glosu, -2 SKIP
        self.set_traps = []
        self.dead_bodies = []
        self.dead_bodies_positions = []

    def move_right(self):
        self.position[0] += self.velocity

    def move_left(self):
        self.position[0] -= self.velocity

    def move_up(self):
        self.position[1] -= self.velocity

    def move_down(self):
        self.position[1] += self.velocity

    def move(self):
        self.position[0] += self.x_change
        self.position[1] += self.y_change

    def unmove(self):
        self.position[0] -= self.x_change
        self.position[1] -= self.y_change

    def show(self, screen, img, where):
        screen.blit(img, where)

    def add_tasks(self, tasks):  # tasks - all tasks
        for i in range(len(tasks)):
            self.tasks.append(tasks[i])

    def start_task(self, task):
        self.task = task
        self.x_change = 0
        self.y_change = 0
        self.velocity = 0
        self.in_task = True
        now = datetime.now()
        delta = timedelta(seconds=5)
        self.task_until = now + delta

    def break_task(self):
        self.task = None
        self.velocity = self.standard_velocity
        self.in_task = False
        self.task_until = -1

    def end_task(self):
        self.tasks.remove(self.task)
        self.velocity = self.standard_velocity
        self.in_task = False
        self.task = None

    def am_i_near(self, other_player_position):
        position_diff = [self.position[0] - other_player_position[0],
                         self.position[1] - other_player_position[1]]
        if abs(position_diff[0]) <= self.kill_distance and abs(position_diff[1]) <= self.kill_distance:
            return True
        else:
            return False

    def start_kill_cooldown(self):
        now = datetime.now()
        delta = self.kill_cooldown
        self.cant_kill_until = now + delta

    def end_kill_cooldown(self):
        self.cant_kill_until = -1

    def remove_lights(self):
        for t in self.tasks:
            if t.task_type == "lights":
                self.tasks.remove(t)

    def collides(self, walls):
        for wall in walls:
            if wall.player_collides(self.position):
                return True
        return False
