from objects.wall import Wall
import pygame


class Assets:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 50)
        self.menu_img = pygame.image.load("../assets/menu.png")
        self.lobby_img = pygame.image.load("../assets/menu.png")
        self.instructions_img = pygame.image.load("../assets/instructions.png")
        self.voting_img = pygame.image.load("../assets/voting.jpg")
        self.task_img = pygame.image.load("../assets/task.png")
        self.report_btn_img = pygame.image.load("../assets/report_button.png")
        self.portal_img = pygame.image.load("../assets/portal.png")
        self.impostors_won = pygame.image.load("../assets/impostors_won.png")
        self.crewmates_won = pygame.image.load("../assets/crewmates_won.png")
        self.dead_image = pygame.Surface([50, 50])
        self.dead_image.fill((0, 0, 0))
        self.dead_img = pygame.image.load("../assets/dead_img.png")
        self.ghost_image = pygame.Surface([50, 50])
        self.ghost_image.fill((255, 255, 255))
        self.crewmate_colors = [(250, 100, 75), (250, 150, 50), (250, 250, 50), (150, 230, 50), (0, 200, 50),
                                (0, 250, 250), (0, 50, 250), (150, 50, 250), (250, 0, 250), (150, 150, 150)]
        self.images = []
        self.impostor_images = []
        for i in range(10):
            player_image = pygame.Surface([50, 50])
            player_image.fill(self.crewmate_colors[i])
            self.images.append(player_image)
            impostor_image = pygame.Surface([50, 50])
            impostor_image.fill(self.crewmate_colors[i])
            impostor_image.subsurface((10, 10), (30, 30)).fill((255, 0, 0))
            self.impostor_images.append(impostor_image)

        self.display_width = 1200
        self.display_height = 1200
        self.tasks_positions = [[100, 200], [500, 200], [1100, 200],
                           [100, 600], [500, 600], [1100, 600],
                           [100, 1000], [500, 1000], [1100, 1000],
                           [100, 1400]]

        self.trap_positions = [
            [-100, 300], [100, 300]
        ]

        self.walls = [
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
