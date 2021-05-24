import time

from network import Network
from datetime import datetime

import pygame

from objects.button import Button
from objects.corpse import Corpse
from objects.votingbutton import VotingButton
from objects.portal import Portal
from objects.parameters import Parameters
from objects.background import Background
from objects.task import Task
from objects.report_button import ReportButton
from objects.wall import Wall

pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (255, 255, 0)

font = pygame.font.SysFont("arial", 50)
menu_img = pygame.image.load("../assets/menu.png")
lobby_img = pygame.image.load("../assets/menu.png")
voting_img = pygame.image.load("../assets/voting.png")
task_img = pygame.image.load("../assets/task.png")
report_btn_img = pygame.image.load("../assets/report_button.png")
portal_img = pygame.image.load("../assets/portal.png")
display_width = 1200
display_height = 900
size = (display_width, display_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("AMONGUS3")

parameters = Parameters(player_speed=5, crewmate_vision=500, impostor_vision=750, impaired_vision=50, vote_time=180,
                        kill_cooldown=30,
                        kill_distance='short', common_tasks=1, long_tasks=2, short_tasks=5)

impostor_vision = parameters.impostor_vision
crewmate_vision = parameters.crewmate_vision

lobby_buttons = pygame.sprite.Group()
voting_buttons = pygame.sprite.Group()

start_btn = Button([500, 600], "../assets/startbutton.PNG", 250, 100)
lobby_buttons.add(start_btn)

skip_btn = Button([100, 550], "../assets/skipbutton.png", 150, 75)
voting_buttons.add(skip_btn)
voting_players_buttons = []

tasks_sprites = pygame.sprite.Group()
tasks_no = 10
tasks = []
tasks_positions = [[100, 200], [500, 200], [1100, 200],
                   [100, 600], [500, 600], [1100, 600],
                   [100, 1000], [500, 1000], [1100, 1000],
                   [100, 1400]]

trap_positions = [
    [-100, 300], [100, 300]
]

radius = 50

report_btn = ReportButton([600, 200], 50, 39, radius)
tasks_sprites.add(report_btn)

portal1 = Portal([800, 400], 200, 200, radius, [1700, 700])
portal2 = Portal([1500, 700], 200, 200, radius, [800, 400])
portals = [portal1, portal2]

corpses_sprites = pygame.sprite.Group()
corpses_list = []
corpses_positions_list = []
death_positions_list = []

game_map = Background("../assets/mapp.png", display_width, display_height)
backgrounds = pygame.sprite.Group()
backgrounds.add(game_map)

walls = [
    Wall([-10, 240], [290, 420]),
    Wall([200, 420], [260, 630]),
    Wall([200, 630], [530, 990]),
    Wall([470, 870], [830, 1500]),
    Wall([-700, -120], [260, 120]),
    Wall([260, -300], [470, -30]),
    Wall([470, -330], [1280, -210]),
    Wall([1250, -300], [1550, 60]),
    Wall([1550, 60], [2180, 270]),
    Wall([2180, 270], [2960, 780]),
    Wall([2960, 750], [3170, 1230]),
    Wall([2420, 750], [2690, 930]),
    Wall([2180, 1230], [3500, 1980]),
    Wall([1640, 1860], [1790, 2040]),
    Wall([1730, 2040], [1820, 2580]),
    Wall([1100, 2310], [1730, 2580]),
    Wall([1100, 1890], [1430, 2010]),
    Wall([1100, 1950], [1190, 2340]),
    Wall([620, 2400], [1100, 2610]),
    Wall([350, 2160], [620, 2430]),
    Wall([-460, 2160], [380, 2430]),
    Wall([-700, 1770], [-460, 2130]),
    Wall([-1090, 2040], [-670, 2190]),
    Wall([-1150, 1980], [-1060, 2160]),
    Wall([-1330, 1230], [-1150, 2100]),
    Wall([-1150, 1050], [-1000, 1440]),
    Wall([-790, 1050], [-640, 1410]),
    Wall([-700, 1230], [-190, 1680]),
    Wall([-250, 1620], [-190, 2010]),
    Wall([20, 1860], [350, 2040]),
    Wall([200, 1770], [350, 1890]),
    Wall([290, 1500], [350, 1770]),
    Wall([290, 1020], [440, 1530]),
    Wall([-340, 960], [440, 1230]),
    Wall([-790, 510], [-610, 960]),
    Wall([-700, 240], [-280, 780]),
    Wall([-370, 780], [-160, 990]),
    Wall([-280, 240], [-190, 360]),
    Wall([-1720, 1380], [-1330, 1530]),
    Wall([-1720, 480], [-1510, 1470]),
    Wall([-1510, -150], [-1270, 540]),
    Wall([-1330, 540], [-970, 690]),
    Wall([-1180, 690], [-1000, 930]),
    Wall([-1270, -120], [-1090, 390]),
    Wall([-1090, -240], [-730, -30]),
    Wall([1010, 870], [1460, 1170]),
    Wall([1250, 750], [1460, 990]),
    Wall([1460, 600], [1640, 840]),
    Wall([1550, 330], [1790, 630]),
    Wall([1790, 420], [1910, 630]),
    Wall([1910, 510], [1970, 690]),
    Wall([1400, 960], [1970, 1170]),
    Wall([1910, 870], [2240, 1050]),
    Wall([1820, 1050], [1970, 1620]),
    Wall([1010, 1320], [1250, 1440]),
    Wall([1100, 1440], [1250, 1710]),
    Wall([1100, 1590], [1880, 1740]),
    Wall([1730, 1500], [1820, 1620])
         ]

# tymczasowe cialo martwego gracza
dead_image = pygame.Surface([50, 50])
dead_image.fill((0, 0, 0))
dead_img = pygame.image.load("../assets/dead_img.png")

# tymczasowy duszek martwego gracza
ghost_image = pygame.Surface([50, 50])
ghost_image.fill((0, 0, 255))

# tymczasowy impo
impostor_image = pygame.Surface([50, 50])
impostor_image.fill((255, 0, 0))


def set_tasks(p):
    if p.role == "crewmate":
        for i in range(tasks_no):
            task = Task(tasks_positions[i], 50, 75, radius, "task")
            tasks.append(task)
            tasks_sprites.add(task)
    else:
        for trap_pos in trap_positions:
            trap = Task(trap_pos, 50, 75, radius, "trap")
            tasks.append(trap)
            tasks_sprites.add(trap)
    p.add_tasks(tasks)


def create_voting_buttons(players_list):
    voting_buttons.add(skip_btn)

    x, y, x_diff, y_diff = 150, 125, 500, 85
    voting_buttons_positions = [[x + (i * x_diff), y + (j * y_diff)] for i in range(2) for j in range(5)]

    for i in range(10):
        if not players_list[i].is_dead:
            voting_btn = VotingButton(voting_buttons_positions[i], "../assets/votingbutton.png", 400, 75, players_list[i].name, i)
            voting_players_buttons.append(voting_btn)
            voting_buttons.add(voting_btn)


def clear_voting_buttons():
    voting_buttons.empty()
    voting_players_buttons.clear()


def count_alive_players(players_list):
    counter = 0
    for player in players_list:
        if not player.is_dead:
            counter += 1
    return counter


def count_impostor_bodies(player):
    global death_positions_list
    death_positions_list.extend(player.dead_bodies_positions)
    death_positions_list = remove_duplicates(death_positions_list)
    if len(death_positions_list) > len(corpses_positions_list):
        new_bodies_positions = [x for x in death_positions_list if x not in corpses_positions_list]
        for new in new_bodies_positions:
            corpse = Corpse(new, 50, 50, radius)
            corpses_sprites.add(corpse)
            corpses_list.append(corpse)
            corpses_positions_list.append(new)


def remove_duplicates(my_list):
    res = []
    [res.append(x) for x in my_list if x not in res]
    return res


def remove_corpses():
    corpses_sprites.empty()
    corpses_list.clear()


class GameState:
    def __init__(self, state):
        self.state = state

    def menu(self):
        input_box = pygame.Rect(350, 700, 500, 50)
        color_inactive = pygame.Color('white')
        color_active = pygame.Color('black')
        color = color_inactive
        active = False
        text = ''

        while True:
            p = n.p
            players_list = n.send(p)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if input_box.collidepoint(mouse_pos):
                        active = not active
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

            screen.blit(menu_img, (0, 0))

            txt_surface = font.render(text, True, color)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y - 4))
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.update()

    def lobby(self):
        while True:
            p = n.p
            players_list = n.send(p)
            for player in players_list:
                if player.in_game:
                    p.role = players_list[p.id].role
                    p.kill_distance = players_list[p.id].kill_distance
                    p.kill_cooldown = players_list[p.id].kill_cooldown
                    p.in_game = True
                    set_tasks(p)
                    self.state = 'main_game'
                    self.state_manager()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_btn.pressed(mouse_pos):
                        p.in_game = True

            screen.blit(lobby_img, (0, 0))
            lobby_buttons.draw(screen)
            pygame.display.update()

    def voting(self):
        p = n.p
        p.voted_for = -1
        players_list = n.send(p)
        clear_voting_buttons()
        create_voting_buttons(players_list)

        alive_players = count_alive_players(players_list)

        time.sleep(2)

        while True:
            p = n.p
            players_list = n.send(p)

            votes_dict = {}
            for i in range(len(players_list)):
                votes_dict[i] = 0
            counter = 0

            loser = -1
            max_votes = 0
            only_one_loser = True

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

            if(counter == alive_players):
                if only_one_loser:
                    print("bye bye", loser)
                    if p.role == "impostor":
                        p.dead_bodies.append(loser)
                else:
                    print("remis")

                p.in_meeting = False
                p.position = [800, 300]
                remove_corpses()
                p = n.p
                players_list = n.send(p)
                time.sleep(2)
                self.state = 'main_game'
                self.state_manager()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if skip_btn.pressed(mouse_pos):
                        if not p.is_dead:
                            p.voted_for = -2  # "SKIP"
                            print("skipujemy!")
                        else:
                            print("Martwi nie glosuja")
                    for btn in voting_players_buttons:
                        if btn.pressed(mouse_pos):
                            if not p.is_dead:
                                p.voted_for = btn.id
                                print("go", btn.id)
                            else:
                                print("Martwi nie glosuja")

            screen.blit(voting_img, (0, 0))
            voting_buttons.draw(screen)
            pygame.display.update()

    def main_game(self):
        while True:
            global crewmate_vision  # TO MA WYLECIEC POZNIEJ
            global impostor_vision
            p = n.p
            players_list = n.send(p)
            for player in players_list:
                # czy jestem martwy
                if not p.is_dead:
                    if p.id in player.dead_bodies:
                        p.is_dead = True
                # czy start zebranie
                if player.in_meeting:
                    p.break_task()
                    p.in_meeting = True
                    if p.role == "impostor":
                        p.set_traps = []  # podczas zebrania gracze orientuja sie o pulapce i przestaja w nia wpadac
                        # (pulapke juz nie jest aktywna)
                    self.state = 'voting'
                    self.state_manager()
                # zliczanie cial
                if player.role == "impostor":
                    count_impostor_bodies(player)

            # czy gracz wszedl w pulapke
            if p.role != "impostor":
                for player in players_list:
                    if player.role == "impostor":
                        for trap_pos in player.set_traps:
                            position_diff = [trap_pos[0] - p.position[0],
                                             trap_pos[1] - p.position[1]]
                            if abs(position_diff[0]) <= radius and abs(position_diff[1]) <= radius:
                                p.is_dead = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        p.x_change -= p.velocity
                        game_map.x_change += p.velocity
                    elif event.key == pygame.K_RIGHT:
                        p.x_change += p.velocity
                        game_map.x_change -= p.velocity
                    elif event.key == pygame.K_DOWN:
                        p.y_change += p.velocity
                        game_map.y_change -= p.velocity
                    elif event.key == pygame.K_UP:
                        p.y_change -= p.velocity
                        game_map.y_change += p.velocity
                    elif event.key == pygame.K_SPACE:  # chce robic taska
                        p.y_change = 0  # zatrzymanie gracza
                        game_map.y_change = 0
                        p.x_change = 0
                        game_map.x_change = 0

                        for t in p.tasks:
                            if t.is_near(p.position):  # czy jest w okolicy taska
                                pygame.display.update()
                                p.start_task(t)
                                break
                    elif event.key == pygame.K_q:  # kill

                        if not p.is_dead and p.role == "impostor" and p.cant_kill_until <= datetime.now():
                            for other_player in players_list:
                                if other_player.id != p.id and not other_player.is_dead and other_player.role == "crewmate":
                                    if p.am_i_near(other_player.position):
                                        p.start_kill_cooldown()
                                        print("I killed", other_player.id)
                                        p.dead_bodies.append(other_player.id)
                                        p.dead_bodies_positions.append(other_player.position)
                                        break

                    elif event.key == pygame.K_r:  # report
                        if not p.is_dead:
                            for corpse in corpses_list:
                                if corpse.is_near(p.position):
                                    p.in_meeting = True
                            if report_btn.is_near(p.position):
                                p.in_meeting = True

                    elif event.key == pygame.K_p:  # portal
                        if p.role == "impostor":
                            p.y_change = 0  # zatrzymanie gracza
                            game_map.y_change = 0
                            p.x_change = 0
                            game_map.x_change = 0

                            for portal in portals:
                                if portal.is_near(p.position):  # czy jest w okolicy portalu
                                    game_map.x_offset -= portal.where_teleports[0] - p.position[0]
                                    game_map.y_offset -= portal.where_teleports[1] - p.position[1]
                                    p.position[0] = portal.where_teleports[0]
                                    p.position[1] = portal.where_teleports[1]

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        p.y_change = 0
                        game_map.y_change = 0

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        p.x_change = 0
                        game_map.x_change = 0

            p.move()
            tasks_sprites.update()  # +report_button
            corpses_sprites.update()
            backgrounds.update()
            game_map.move()  # przesuwanie mapy
            if p.collides(walls):
                p.unmove()
                game_map.unmove()
            game_map.show(screen)

            if p.in_task:  # czy gracz skonczyl taska
                if p.task_until <= datetime.now():
                    if p.task.task_type == "lights":  # czy gracz naprawil swiatla
                        crewmate_vision = parameters.crewmate_vision
                        for player in players_list:
                            if player != p:
                                player.remove_lights()
                    if p.task.task_type == "trap":  # zastawiona pulapka
                        for player in players_list:
                            if player.role != "impostor":
                                p.set_traps.append(p.task.position)
                    p.end_task()

            for i in range(len(players_list)):  # wyswietlanie graczy
                if players_list[i].id == p.id:
                    if p.is_dead:
                        players_list[i].show(screen, ghost_image, p.screen_pos)
                    else:
                        if p.role == "impostor":
                            players_list[i].show(screen, impostor_image, p.screen_pos)
                        else:
                            players_list[i].show(screen, images[i], p.screen_pos)

                else:
                    if p.role == "impostor":
                        vision = impostor_vision
                    else:
                        vision = crewmate_vision
                    position_diff = [players_list[i].position[0] - p.position[0],
                                     players_list[i].position[1] - p.position[1]]
                    if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                        tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                        if p.is_dead:
                            if players_list[i].is_dead:
                                players_list[i].show(screen, ghost_image, tmp_screen_pos)
                            elif players_list[i].role == "impostor":
                                players_list[i].show(screen, impostor_image, tmp_screen_pos)
                            else:
                                players_list[i].show(screen, images[i], tmp_screen_pos)
                        else:
                            if not players_list[i].is_dead:
                                if players_list[i].role == "impostor" and p.role == "impostor":
                                    players_list[i].show(screen, impostor_image, tmp_screen_pos)
                                else:
                                    players_list[i].show(screen, images[i], tmp_screen_pos)

            for corpse in corpses_list:  # wyswietlanie cial
                if p.role != "impostor":
                    vision = crewmate_vision
                    position_diff = [corpse.position[0] - p.position[0],
                                     corpse.position[1] - p.position[1]]
                    if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                        tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                        corpse.show(screen, dead_image, tmp_screen_pos)
                else:
                    vision = impostor_vision
                    position_diff = [corpse.position[0] - p.position[0],
                                     corpse.position[1] - p.position[1]]
                    if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                        tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                        corpse.show(screen, dead_image, tmp_screen_pos)

            for t in p.tasks:  # wyswietlanie taskow, pulapek
                if p.role == "impostor":
                    vision = impostor_vision
                else:
                    vision = crewmate_vision
                position_diff = [t.position[0] - p.position[0],
                            t.position[1] - p.position[1]]
                if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                    tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                    t.show(screen, task_img, tmp_screen_pos)

            for portal in portals:  # wyswietlanie portali
                if p.role == "impostor":
                    vision = impostor_vision
                else:
                    vision = crewmate_vision
                position_diff = [portal.position[0] - p.position[0],
                            portal.position[1] - p.position[1]]
                if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                    tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                    portal.show(screen, portal_img, tmp_screen_pos)

            if p.role != "impostor":  # wyswietlanie przycisku glosowania
                vision = crewmate_vision
                position_diff = [report_btn.position[0] - p.position[0],
                                 report_btn.position[1] - p.position[1]]
                if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                    tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                    report_btn.show(screen, report_btn_img,  tmp_screen_pos)
            else:
                vision = impostor_vision
                position_diff = [report_btn.position[0] - p.position[0],
                                 report_btn.position[1] - p.position[1]]
                if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                    tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                    report_btn.show(screen, report_btn_img,  tmp_screen_pos)

            # players.draw(screen)
            pygame.display.update()
            n.p = p

    def endgame(self):
        pass

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


if __name__ == "__main__":
    n = Network()
    clock = pygame.time.Clock()
    p1_image = pygame.Surface([50, 50])
    p1_image.fill((255, 0, 255))
    images = [p1_image] * 10  # TODO: ladowac obrazki normalnie

    game_state = GameState('menu')
    players = pygame.sprite.Group()

    game_state.state_manager()
