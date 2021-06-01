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
from assets import Assets

pygame.init()
a = Assets()
size = (a.display_width, a.display_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("AMONGUS3")
parameters = Parameters(player_speed=5, crewmate_vision=500, impostor_vision=750, impaired_vision=50, vote_time=180,
                        kill_distance=300)
lobby_buttons = pygame.sprite.Group()
voting_buttons = pygame.sprite.Group()

start_btn = Button([500, 600], "../assets/startbutton.PNG", 250, 100)
lobby_buttons.add(start_btn)

skip_btn = Button([100, 700], "../assets/skipbutton.png", 150, 75)
voting_buttons.add(skip_btn)
voting_players_buttons = []

tasks_sprites = pygame.sprite.Group()
tasks_no = 10
tasks = []

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

game_map = Background("../assets/mapp.png", a.display_width, a.display_height)
backgrounds = pygame.sprite.Group()
backgrounds.add(game_map)
dead_image = pygame.Surface([50, 50])
dead_image.fill((0, 0, 0))
dead_img = pygame.image.load("../assets/dead_img.png")
ghost_image = pygame.Surface([50, 50])
ghost_image.fill((0, 0, 255))
impostor_image = pygame.Surface([50, 50])
impostor_image.fill((255, 0, 0))


def set_tasks(p):
    if p.role == "crewmate":
        for i in range(tasks_no):
            task = Task(a.tasks_positions[i], 50, 75, radius, "task")
            tasks.append(task)
            tasks_sprites.add(task)
    else:
        for trap_pos in a.trap_positions:
            trap = Task(trap_pos, 50, 75, radius, "trap")
            tasks.append(trap)
            tasks_sprites.add(trap)
    p.add_tasks(tasks)


def create_voting_buttons(players_list):
    voting_buttons.add(skip_btn)

    x, y, x_diff, y_diff = 150, 125, 500, 120
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


def quit_handler(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()


def vote(p, event):
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


def check_if_endgame(players_list, game_state):
    impostors_alive = 0
    crewmates_alive = 0
    for player in players_list:
        if not player.is_dead:
            if player.role == "impostor":
                impostors_alive += 1
            else:
                crewmates_alive += 1
    if impostors_alive == 0:
        game_state.who_won = "crewmates"
        game_state.state = "endgame"
        game_state.state_manager()
    if crewmates_alive == 0 or impostors_alive == crewmates_alive:
        game_state.who_won = "impostors"
        game_state.state = "endgame"
        game_state.state_manager()


def move_handler(p, event):
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


def task_handler(p, event):
    if event.key == pygame.K_SPACE:  # chce robic taska
        p.y_change = 0  # zatrzymanie gracza
        game_map.y_change = 0
        p.x_change = 0
        game_map.x_change = 0

        for t in p.tasks:
            if t.is_near(p.position):  # czy jest w okolicy taska
                pygame.display.update()
                p.start_task(t)
                break


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


def report_handler(p, event):
    if event.key == pygame.K_r:  # report
        if not p.is_dead:
            for corpse in corpses_list:
                if corpse.is_near(p.position):
                    p.in_meeting = True
            if report_btn.is_near(p.position):
                p.in_meeting = True


def portal_handler(p, event):
    if event.key == pygame.K_p:  # portal
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


def stop_moving_handler(p, event):
    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
        p.y_change = 0
        game_map.y_change = 0

    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        p.x_change = 0
        game_map.x_change = 0


def check_traps(p, players_list):  # czy gracz wszedl w pulapke
    if p.role != "impostor":
        for player in players_list:
            if player.role == "impostor":
                for trap_pos in player.set_traps:
                    position_diff = [trap_pos[0] - p.position[0],
                                     trap_pos[1] - p.position[1]]
                    if abs(position_diff[0]) <= radius and abs(position_diff[1]) <= radius:
                        p.is_dead = True


def check_is_dead(p, player):
    if not p.is_dead:
        if p.id in player.dead_bodies:
            p.is_dead = True


def check_if_meeting(player, p, game_state):
    # czy start zebranie
    if player.in_meeting:
        p.break_task()
        p.in_meeting = True
        if p.role == "impostor":
            p.set_traps = []  # podczas zebrania gracze orientuja sie o pulapce i przestaja w nia wpadac
            # (pulapke juz nie jest aktywna)
        game_state.state = 'voting'
        game_state.state_manager()


def check_task(p, players_list):
    if p.in_task:  # czy gracz skonczyl taska
        if p.task_until <= datetime.now():
            if p.task.task_type == "trap":  # zastawiona pulapka
                for player in players_list:
                    if player.role != "impostor":
                        p.set_traps.append(p.task.position)
            p.end_task()


def show_players(p, players_list):
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
                vision = parameters.impostor_vision
            else:
                vision = parameters.crewmate_vision
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


def show_corpses(p):
    for corpse in corpses_list:  # wyswietlanie cial
        if p.role != "impostor":
            vision = parameters.crewmate_vision
            position_diff = [corpse.position[0] - p.position[0],
                             corpse.position[1] - p.position[1]]
            if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                corpse.show(screen, dead_image, tmp_screen_pos)
        else:
            vision = parameters.impostor_vision
            position_diff = [corpse.position[0] - p.position[0],
                             corpse.position[1] - p.position[1]]
            if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
                tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
                corpse.show(screen, dead_image, tmp_screen_pos)


def show_tasks(p):
    for t in p.tasks:  # wyswietlanie taskow, pulapek
        if p.role == "impostor":
            vision = parameters.impostor_vision
        else:
            vision = parameters.crewmate_vision
        position_diff = [t.position[0] - p.position[0],
                         t.position[1] - p.position[1]]
        if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
            tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
            t.show(screen, a.task_img, tmp_screen_pos)


def show_portals(p):
    for portal in portals:  # wyswietlanie portali
        if p.role == "impostor":
            vision = parameters.impostor_vision
        else:
            vision = parameters.crewmate_vision
        position_diff = [portal.position[0] - p.position[0],
                         portal.position[1] - p.position[1]]
        if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
            tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
            portal.show(screen, a.portal_img, tmp_screen_pos)


def show_report_button(p):
    if p.role != "impostor":  # wyswietlanie przycisku glosowania
        vision = parameters.crewmate_vision
        position_diff = [report_btn.position[0] - p.position[0],
                         report_btn.position[1] - p.position[1]]
        if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
            tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
            report_btn.show(screen, a.report_btn_img, tmp_screen_pos)
    else:
        vision = parameters.impostor_vision
        position_diff = [report_btn.position[0] - p.position[0],
                         report_btn.position[1] - p.position[1]]
        if abs(position_diff[0]) <= vision and abs(position_diff[1]) <= vision:
            tmp_screen_pos = [p.screen_pos[0] + position_diff[0], p.screen_pos[1] + position_diff[1]]
            report_btn.show(screen, a.report_btn_img, tmp_screen_pos)


class GameState:
    def __init__(self, state):
        self.state = state
        self.who_won = "nobody"

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
                quit_handler(event)
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

            screen.blit(a.menu_img, (0, 0))

            txt_surface = a.font.render(text, True, color)
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
                    p.kill_distance = players_list[p.id].kill_distance  # czemu nie z parametrow?
                    p.kill_cooldown = players_list[p.id].kill_cooldown
                    p.in_game = True
                    set_tasks(p)
                    self.state = 'main_game'
                    self.state_manager()

            for event in pygame.event.get():
                quit_handler(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_btn.pressed(mouse_pos):
                        p.in_game = True

            screen.blit(a.lobby_img, (0, 0))
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
            only_one_loser = True
            votes_dict = {}
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
            if counter == alive_players:
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
                quit_handler(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    vote(p, event)

            screen.blit(a.voting_img, (0, 0))
            voting_buttons.draw(screen)
            pygame.display.update()

    def main_game(self):
        while True:
            p = n.p
            players_list = n.send(p)
            check_if_endgame(players_list, self)

            for player in players_list:
                check_is_dead(p, player)
                check_if_meeting(player, p, self)
                # zliczanie cial
                if player.role == "impostor":
                    count_impostor_bodies(player)
            check_traps(p, players_list)

            for event in pygame.event.get():
                quit_handler(event)
                if event.type == pygame.KEYDOWN:
                    move_handler(p, event)
                    task_handler(p, event)
                    kill_handler(p, event, players_list)
                    report_handler(p, event)
                    portal_handler(p, event)
                elif event.type == pygame.KEYUP:
                    stop_moving_handler(p, event)
            check_task(p, players_list)
            p.move()
            tasks_sprites.update()  # +report_button ---> to nie moze byc razem, SINGLE RESPONSIBILITY
            corpses_sprites.update()
            backgrounds.update()
            game_map.move()  # przesuwanie mapy
            if p.collides(a.walls):
                p.unmove()
                game_map.unmove()
            game_map.show(screen)
            show_players(p, players_list)
            show_corpses(p)
            show_portals(p)
            show_report_button(p)
            pygame.display.update()
            n.p = p

    def endgame(self):
        if self.who_won == "crewmates":
            screen.blit(a.crewmates_won, (0, 0))
        else:
            screen.blit(a.impostors_won, (0, 0))

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
    player_image = pygame.Surface([50, 50])
    player_image.fill((255, 0, 255))
    images = [player_image] * 10

    game_st = GameState('menu')
    players = pygame.sprite.Group()
    game_st.state_manager()
