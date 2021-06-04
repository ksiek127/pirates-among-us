from datetime import datetime

import pygame
from assets import Assets
from objects.parameters import Parameters
from objects.button import Button
from objects.task import Task
from objects.report_button import ReportButton
from objects.corpse import Corpse
from objects.votingbutton import VotingButton
from objects.background import Background
from objects.portal import Portal
from network import Network
import time


def init_portals(radius):
    portal1 = Portal(position=[800, 400], width=200, height=200, radius=radius, where_teleports=[1700, 700])
    portal2 = Portal(position=[1500, 700], width=200, height=200, radius=radius, where_teleports=[800, 400])
    return [portal1, portal2]


def count_alive_players(players_list):
    counter = 0
    for player in players_list:
        if not player.is_dead:
            counter += 1
    return counter


def remove_duplicates(my_list):
    res = []
    [res.append(x) for x in my_list if x not in res]
    return res


def quit_handler(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()


def kill_handler(p, event, players_list):
    if event.key == pygame.K_q:  # kill
        if not p.is_dead and p.role == "impostor" and p.cant_kill_until <= datetime.now():
            for other_player in players_list:
                if other_player.id != p.id and not other_player.is_dead and other_player.role == "crewmate":
                    if p.am_i_near(other_player.position):
                        p.start_kill_cooldown()
                        print("I killed", other_player.id)
                        p.dead_bodies.append(other_player.id)
                        p.dead_bodies_positions.append(other_player.position)
                        break


def check_is_dead(p, player):
    if not p.is_dead:
        if p.id in player.dead_bodies:
            p.is_dead = True


def check_task(p, players_list):
    if p.in_task:  # czy gracz skonczyl taska
        if p.task_until <= datetime.now():
            if p.task.task_type == "trap":  # zastawiona pulapka
                for player in players_list:
                    if player.role != "impostor":
                        p.set_traps.append(p.task.position)
            p.end_task()


class GameState:
    def __init__(self, state):
        self.state = state
        self.who_won = "nobody"
        self.a = Assets()
        self.size = (self.a.display_width, self.a.display_height)
        self.screen = pygame.display.set_mode(self.size)
        self.parameters = Parameters(player_speed=5, crewmate_vision=500, impostor_vision=750, impaired_vision=50,
                                     vote_time=180, kill_distance=300, radius=50)
        self.lobby_buttons = pygame.sprite.Group()
        self.voting_buttons = pygame.sprite.Group()
        self.start_btn = Button(position=[500, 800], img="../assets/startbutton.PNG", width=250, height=100)
        self.lobby_buttons.add(self.start_btn)
        self.skip_btn = Button(position=[525, 860], img="../assets/skipbutton.png", width=150, height=75)
        self.voting_buttons.add(self.skip_btn)
        self.voting_players_buttons = []
        self.tasks_sprites = pygame.sprite.Group()
        self.tasks_no = 10
        self.tasks = []
        self.radius = self.parameters.radius
        self.portals = init_portals(self.radius)
        self.report_btn = ReportButton(position=[600, 200], width=50, height=39, radius=self.radius)
        self.tasks_sprites.add(self.report_btn)
        self.corpses_sprites = pygame.sprite.Group()
        self.corpses_list = []
        self.corpses_positions_list = []
        self.death_positions_list = []
        self.game_map = Background(filepath="../assets/mapp.png", width=self.a.display_width, height=self.a.display_height)
        self.backgrounds = pygame.sprite.Group()
        self.backgrounds.add(self.game_map)
        self.n = Network()
        self.clock = pygame.time.Clock()
        self.images = self.a.images
        self.impostor_images = self.a.impostor_images

    def set_tasks(self, p):
        if p.role == "crewmate":
            for i in range(self.tasks_no):
                task = Task(position=self.a.tasks_positions[i], width=50, height=75, radius=self.radius, task_type="task")
                self.tasks.append(task)
                self.tasks_sprites.add(task)
        else:
            for trap_pos in self.a.trap_positions:
                trap = Task(position=trap_pos, width=50, height=75, radius=self.radius, task_type="trap")
                self.tasks.append(trap)
                self.tasks_sprites.add(trap)
        p.add_tasks(self.tasks)

    def create_voting_buttons(self, players_list):
        self.voting_buttons.add(self.skip_btn)

        x, y, x_diff, y_diff = 150, 190, 500, 130
        voting_buttons_positions = [[x + (i * x_diff), y + (j * y_diff)] for i in range(2) for j in range(5)]

        for i in range(10):
            if not players_list[i].is_dead:
                voting_btn = VotingButton(position=voting_buttons_positions[i], img="../assets/votingbutton.png",
                                          width=400, height=125, name=players_list[i].name, id=i,
                                          color=self.a.crewmate_colors[i])
                self.voting_players_buttons.append(voting_btn)
                self.voting_buttons.add(voting_btn)

    def clear_voting_buttons(self):
        self.voting_buttons.empty()
        self.voting_players_buttons.clear()

    def count_impostor_bodies(self, player):
        self.death_positions_list.extend(player.dead_bodies_positions)
        death_positions_list = remove_duplicates(self.death_positions_list)
        if len(death_positions_list) > len(self.corpses_positions_list):
            new_bodies_positions = [x for x in death_positions_list if x not in self.corpses_positions_list]
            for new in new_bodies_positions:
                corpse = Corpse(position=new, width=50, height=50, radius=self.radius)
                self.corpses_sprites.add(corpse)
                self.corpses_list.append(corpse)
                self.corpses_positions_list.append(new)

    def remove_corpses(self):
        self.corpses_sprites.empty()
        self.corpses_list.clear()

    def vote(self, p, event):
        mouse_pos = event.pos
        if p.voted_for != -1:
            print("już zagłosowałem na", p.voted_for)
        elif self.skip_btn.pressed(mouse_pos):
            if not p.is_dead:
                p.voted_for = -2  # "SKIP"
                print("skipujemy!")
            else:
                print("Martwi nie glosuja")
        else:
            for btn in self.voting_players_buttons:
                if btn.pressed(mouse_pos):
                    if not p.is_dead:
                        p.voted_for = btn.id
                        print("go", btn.id)
                    else:
                        print("Martwi nie glosuja")

    def check_if_endgame(self, players_list):
        impostors_alive = 0
        crewmates_alive = 0
        for player in players_list:
            if not player.is_dead:
                if player.role == "impostor":
                    impostors_alive += 1
                else:
                    crewmates_alive += 1
        if impostors_alive == 0:
            self.who_won = "crewmates"
            self.state = "endgame"
            self.state_manager()
        if crewmates_alive == 0 or impostors_alive == crewmates_alive:
            self.who_won = "impostors"
            self.state = "endgame"
            self.state_manager()

    def move_handler(self, p, event):
        if event.key == pygame.K_LEFT:
            p.x_change -= p.velocity
            self.game_map.x_change += p.velocity
        elif event.key == pygame.K_RIGHT:
            p.x_change += p.velocity
            self.game_map.x_change -= p.velocity
        elif event.key == pygame.K_DOWN:
            p.y_change += p.velocity
            self.game_map.y_change -= p.velocity
        elif event.key == pygame.K_UP:
            p.y_change -= p.velocity
            self.game_map.y_change += p.velocity

    def task_handler(self, p, event):
        if event.key == pygame.K_SPACE:  # chce robic taska
            p.y_change = 0  # zatrzymanie gracza
            self.game_map.y_change = 0
            p.x_change = 0
            self.game_map.x_change = 0

            for t in p.tasks:
                if t.is_near(p.position):  # czy jest w okolicy taska
                    pygame.display.update()
                    p.start_task(t)
                    break

    def report_handler(self, p, event):
        if event.key == pygame.K_r:  # report
            if not p.is_dead:
                for corpse in self.corpses_list:
                    if corpse.is_near(p.position):
                        p.in_meeting = True
                if self.report_btn.is_near(p.position):
                    p.in_meeting = True

    def portal_handler(self, p, event):
        if event.key == pygame.K_p:  # portal
            if p.role == "impostor":
                p.y_change = 0  # zatrzymanie gracza
                self.game_map.y_change = 0
                p.x_change = 0
                self.game_map.x_change = 0

                for portal in self.portals:
                    if portal.is_near(p.position):  # czy jest w okolicy portalu
                        self.game_map.x_offset -= portal.where_teleports[0] - p.position[0]
                        self.game_map.y_offset -= portal.where_teleports[1] - p.position[1]
                        p.position[0] = portal.where_teleports[0]
                        p.position[1] = portal.where_teleports[1]

    def stop_moving_handler(self, p, event):
        if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
            p.y_change = 0
            self.game_map.y_change = 0

        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            p.x_change = 0
            self.game_map.x_change = 0

    def check_traps(self, p, players_list):  # czy gracz wszedl w pulapke
        if p.role != "impostor":
            for player in players_list:
                if player.role == "impostor":
                    for trap_pos in player.set_traps:
                        position_diff = [trap_pos[0] - p.position[0],
                                         trap_pos[1] - p.position[1]]
                        if abs(position_diff[0]) <= self.radius and abs(position_diff[1]) <= self.radius:
                            p.is_dead = True

    def check_if_meeting(self, player, p):
        # czy start zebranie
        if player.in_meeting:
            p.break_task()
            p.in_meeting = True
            if p.role == "impostor":
                p.set_traps = []  # podczas zebrania gracze orientuja sie o pulapce i przestaja w nia wpadac
                # (pulapke juz nie jest aktywna)
            self.state = 'voting'
            self.state_manager()

    def show_players(self, p, players_list):
        for i in range(len(players_list)):  # wyswietlanie graczy
            if players_list[i].id == p.id:
                if p.is_dead:
                    players_list[i].show(self.screen, self.a.ghost_image, p.screen_pos)
                else:
                    if p.role == "impostor":
                        players_list[i].show(self.screen, self.impostor_images[i], p.screen_pos)
                    else:
                        players_list[i].show(self.screen, self.images[i], p.screen_pos)

            else:
                if p.role == "impostor":
                    vision = self.parameters.impostor_vision
                else:
                    vision = self.parameters.crewmate_vision
                position_diff = [players_list[i].position[0] - p.position[0],
                                 players_list[i].position[1] - p.position[1]]
                if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                    tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                    if p.is_dead:
                        if players_list[i].is_dead:
                            players_list[i].show(self.screen, self.a.ghost_image, tmp_screen_pos)
                        elif players_list[i].role == "impostor":
                            players_list[i].show(self.screen, self.impostor_images[i], tmp_screen_pos)
                        else:
                            players_list[i].show(self.screen, self.images[i], tmp_screen_pos)
                    else:
                        if not players_list[i].is_dead:
                            if players_list[i].role == "impostor" and p.role == "impostor":
                                players_list[i].show(self.screen, self.impostor_images[i], tmp_screen_pos)
                            else:
                                players_list[i].show(self.screen, self.images[i], tmp_screen_pos)

    def show_corpses(self, p):
        for corpse in self.corpses_list:  # wyswietlanie cial
            if p.role != "impostor":
                vision = self.parameters.crewmate_vision
                position_diff = [corpse.position[0] - p.position[0],
                                 corpse.position[1] - p.position[1]]
                if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                    tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                    corpse.show(self.screen, self.a.dead_image, tmp_screen_pos)
            else:
                vision = self.parameters.impostor_vision
                position_diff = [corpse.position[0] - p.position[0],
                                 corpse.position[1] - p.position[1]]
                if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                    tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                    corpse.show(self.screen, self.a.dead_image, tmp_screen_pos)

    def show_tasks(self, p):
        for t in p.tasks:  # wyswietlanie taskow, pulapek
            if p.role == "impostor":
                vision = self.parameters.impostor_vision
            else:
                vision = self.parameters.crewmate_vision
            position_diff = [t.position[0] - p.position[0],
                             t.position[1] - p.position[1]]
            if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                t.show(self.screen, self.a.task_img, tmp_screen_pos)

    def show_portals(self, p):
        for portal in self.portals:  # wyswietlanie portali
            if p.role == "impostor":
                vision = self.parameters.impostor_vision
            else:
                vision = self.parameters.crewmate_vision
            position_diff = [portal.position[0] - p.position[0],
                             portal.position[1] - p.position[1]]
            if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                portal.show(self.screen, self.a.portal_img, tmp_screen_pos)

    def show_report_button(self, p):
        if p.role != "impostor":  # wyswietlanie przycisku glosowania
            vision = self.parameters.crewmate_vision
            position_diff = [self.report_btn.position[0] - p.position[0],
                             self.report_btn.position[1] - p.position[1]]
            if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                self.report_btn.show(self.screen, self.a.report_btn_img, tmp_screen_pos)
        else:
            vision = self.parameters.impostor_vision
            position_diff = [self.report_btn.position[0] - p.position[0],
                             self.report_btn.position[1] - p.position[1]]
            if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                self.report_btn.show(self.screen, self.a.report_btn_img, tmp_screen_pos)

    def menu(self):
        input_box = pygame.Rect(350, 700, 500, 50)
        color_inactive = pygame.Color('white')
        color_active = pygame.Color('black')
        color = color_inactive
        active = False
        text = 'Tu wpisz swe imie, kamracie!'

        while True:
            p = self.n.p
            self.n.send(p)
            for event in pygame.event.get():
                quit_handler(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if input_box.collidepoint(mouse_pos):
                        active = not active
                        text = ''
                    else:
                        active = False
                    color = color_active if active else color_inactive

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            print("Name:", text)
                            p.name = text
                            self.state = 'lobby'
                            self.state_manager()
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.blit(self.a.menu_img, (0, 0))
            self.screen.blit(self.a.title_img, (150, 400))

            txt_surface = self.a.font.render(text, True, 'black')
            self.screen.blit(txt_surface, (input_box.x + 10, input_box.y + 15))
            pygame.draw.rect(self.screen, color, input_box, 4)

            pygame.display.update()

    def lobby(self):
        while True:
            p = self.n.p
            players_list = self.n.send(p)
            for player in players_list:
                if player.in_game:
                    p.role = players_list[p.id].role
                    p.kill_distance = self.parameters.kill_distance
                    p.kill_cooldown = players_list[p.id].kill_cooldown
                    p.in_game = True
                    self.set_tasks(p)
                    self.state = 'main_game'
                    self.state_manager()

            for event in pygame.event.get():
                quit_handler(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.start_btn.pressed(mouse_pos):
                        p.in_game = True

            self.screen.blit(self.a.lobby_img, (0, 0))
            self.screen.blit(self.a.instructions_img, (300, 300))
            self.lobby_buttons.draw(self.screen)
            pygame.display.update()

    def voting(self):
        p = self.n.p
        p.voted_for = -1
        players_list = self.n.send(p)
        self.clear_voting_buttons()
        self.create_voting_buttons(players_list)
        alive_players = count_alive_players(players_list)
        time.sleep(2)

        while True:
            p = self.n.p
            players_list = self.n.send(p)
            only_one_loser = True
            votes_dict = {}
            skips_counter = 0
            loser = -1
            max_votes = 0
            for i in range(len(players_list)):
                votes_dict[i] = 0
            counter = 0
            for player in players_list:
                if player.voted_for != -1 and player.voted_for != -2:
                    votes = votes_dict.pop(player.voted_for)
                    votes_dict[player.voted_for] = votes + 1
                    if loser == -1 or max_votes < votes_dict[player.voted_for]:
                        loser = player.voted_for
                        max_votes = votes_dict[loser]
                        only_one_loser = True
                    elif max_votes == votes_dict[player.voted_for]:
                        only_one_loser = False
                    counter += 1
                elif player.voted_for == -2:  # SKIP
                    counter += 1
                    skips_counter += 1
            if counter == alive_players:
                if skips_counter > max_votes:
                    print("Nikt nie został wygłosowany")
                elif only_one_loser:
                    print("bye bye", loser)
                    if p.role == "impostor":
                        p.dead_bodies.append(loser)
                else:
                    print("remis")

                p.in_meeting = False
                p.position = [800, 300]
                self.remove_corpses()
                p = self.n.p
                self.n.send(p)
                time.sleep(2)
                self.state = 'main_game'
                self.state_manager()

            for event in pygame.event.get():
                quit_handler(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.vote(p, event)

            self.screen.blit(self.a.voting_img, (0, 0))
            self.voting_buttons.draw(self.screen)
            pygame.display.update()

    def main_game(self):
        while True:
            p = self.n.p
            players_list = self.n.send(p)
            self.check_if_endgame(players_list)

            for player in players_list:
                check_is_dead(p, player)
                self.check_if_meeting(player, p)
                # zliczanie cial
                if player.role == "impostor":
                    self.count_impostor_bodies(player)
            self.check_traps(p, players_list)

            for event in pygame.event.get():
                quit_handler(event)
                if event.type == pygame.KEYDOWN:
                    self.move_handler(p, event)
                    self.task_handler(p, event)
                    kill_handler(p, event, players_list)
                    self.report_handler(p, event)
                    self.portal_handler(p, event)
                elif event.type == pygame.KEYUP:
                    self.stop_moving_handler(p, event)
            check_task(p, players_list)
            p.move()
            self.tasks_sprites.update()  # +report_button ---> to nie moze byc razem, SINGLE RESPONSIBILITY
            self.corpses_sprites.update()
            self.backgrounds.update()
            self.game_map.move()  # przesuwanie mapy
            if p.collides(self.a.walls):
                p.unmove()
                self.game_map.unmove()
            self.game_map.show(self.screen)
            self.show_players(p, players_list)
            self.show_corpses(p)
            self.show_portals(p)
            self.show_report_button(p)
            pygame.display.update()
            self.n.p = p

    def endgame(self):
        if self.who_won == "crewmates":
            self.screen.blit(self.a.crewmates_won, (0, 0))
        else:
            self.screen.blit(self.a.impostors_won, (0, 0))

    def state_manager(self):
        if self.state == 'menu':
            self.menu()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'lobby':
            self.lobby()
        if self.state == 'voting':
            self.voting()
        if self.state == 'endgame':
            self.endgame()
