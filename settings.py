from random import randrange
from random import choice


class Board:
    def __init__(self, size):
        self.size = size
        self.map = [['O' for _ in range(size)] for _ in range(size)]
        self.radar = [['O' for _ in range(size)] for _ in range(size)]
    def get_board_type(self, hid):
        if hid == False:
            return self.map
        if hid == True:
            return self.radar
    # отрисовка поля
    def draw_board(self, hid):
        board = self.get_board_type(hid)

        for x in range(-1, self.size):
            for y in range(-1, self.size):
                if x == -1 and y == -1:
                    print("   ", end="  ")
                    continue
                if x == -1 and y >= 0:
                    print(y + 1, end="   ")
                    continue
                if x >= 0 and y == -1:
                    print('', Game.title[x], '|', end='')
                    continue
                print('', str(board[x][y]), '|', end='')
            print("")

    print("")

    # проверка входит ли кобаль в поле
    def check_ship_fits(self, ship, hid):
        board = self.get_board_type(hid)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or \
                ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False

        for i_x in range(x, x + height):
            for i_y in range(y, y + width):
                if str(board[i_x][i_y]) == 'T':
                    return False

        for i_x in range(x - 1, x + height + 1):
            for i_y in range(y - 1, y + width + 1):
                if i_x < 0 or i_x >= len(board) or i_y < 0 or i_y >= len(board):
                    continue
                if str(board[i_x][i_y]) in ('■', 'X'):
                    return False

        return True

    # разметка поля вокруг подбитого корабля согласно правилам
    def mark_destroyed_ship(self, ship, hid):
        board = self.get_board_type(hid)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for i_x in range(x - 1, x + height + 1):
            for i_y in range(y - 1, y + width + 1):
                if i_x < 0 or i_x >= len(board) or i_y < 0 or i_y >= len(board):
                    continue
                board[i_x][i_y] = 'T'

        for i_x in range(x, x + height):
            for i_y in range(y, y + width):
                board[i_x][i_y] = 'X'

    # добавление корабля, параметр hid для скрытия или отражаения кораблей на доске
    def add_ship(self, ship, hid):
        board = self.get_board_type(hid)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for i_x in range(x, x + height):
            for i_y in range(y, y + width):
                board[i_x][i_y] = ship


class Game:
    title = ("1", "2", "3", "4", "5", "6")
    ships_rules = [1, 1, 1, 1, 2, 2, 3]
    board_size = len(title)

    def __init__(self):
        self.players = []
        self.current_player = None
        self.next_player = None
        self.status = 'prepare'

    # при старте игры назначаем текущего и следующего игрока
    def start_game(self):
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    # функция переключения статусов
    def status_check(self):
        # переключаем с prepare на in game если в игру добавлено два игрока.
        # далее стартуем игру
        if self.status == 'prepare' and len(self.players) >= 2:
            self.status = 'in game'
            self.start_game()
            return True
        #  game over если у следующего игрока осталось 0 кораблей.
        if self.status == 'in game' and len(self.next_player.ships) == 0:
            self.status = 'game over'
            return True

    def add_player(self, player):
        # при добавлении игрока создаем для него поле
        player.board = Board(Game.board_size)
        player.enemy_ships = list(Game.ships_rules)
        # расставляем корабли
        self.random_board(player)
        self.players.append(player)

    def random_board(self, player):
        # делаем расстановку кораблей
        for ship_size in Game.ships_rules:
            retry_count = 30
            ship = Ship(ship_size, 0, 0, 0)

            while True:
                x, y, d = player.get_input('ship_setup')
                ship.set_position(x, y, d)
                # если корабль помещается, добавляем игроку на поле корабль, добавляем корабль в список кораблей игрока.
                # и продолжаем расстановку кораблей по списку
                if player.board.check_ship_fits(ship, False):
                    player.board.add_ship(ship, False)
                    player.ships.append(ship)
                    break

                # если корабль не поместился отнимаем попытку на расстановку и пробуем еще
                retry_count -= 1
                if retry_count < 0:
                    # после заданного количества неудачных попыток - обнуляем карту игрока
                    # убираем у него все корабли и начинаем расстановку по новой
                    player.board.map = [['O' for _ in range(Game.board_size)] for _ in
                                        range(Game.board_size)]
                    player.ships = []
                    self.random_board(player)
                    return True

    def draw(self):
        if not self.current_player.is_ai:
            self.current_player.board.draw_board(False)
            self.current_player.board.draw_board(True)

        for line in self.current_player.message:
            print(line)

    # смена игроков
    def switch_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player


class Player:
    def __init__(self, name, is_ai):
        self.name = name
        self.is_ai = is_ai
        self.message = []
        self.ships = []
        self.enemy_ships = []
        self.board = None

    # Ход игрока:расстановка кораблей,либо совершения выстрела
    def get_input(self, input_type):
        if input_type == "ship_setup":
            x = str(randrange(0, self.board.size))
            y = str(randrange(0, self.board.size))
            d = choice(["H", "V"])
            return int(x) - 1, int(y) - 1, 0 if d == 'H' else 1

        if input_type == "shot":
            if self.is_ai:
                x, y = randrange(0, self.board.size), randrange(0, self.board.size)
            else:
                user_input = input().replace(" ", "")
                x, y = user_input[0], user_input[1:]
                if not x.isdigit() or int(x) not in range(1, Game.board_size + 1) or not y.isdigit() or \
                        int(y) not in range(1, Game.board_size + 1):
                    self.message.append('Приказ непонятен, ошибка формата данных')
                    return 100, 0
                x = int(x) - 1
                y = int(y) - 1
            return x, y

    def make_shot(self, target_player):
        s_x, s_y = self.get_input('shot')
        if s_x + s_y == 100 or self.board.radar[s_x][s_y] != 'O':
            return 'retry'
        shot_res = target_player.receive_shot((s_x, s_y))

        if shot_res == 'miss':
            self.board.radar[s_x][s_y] = 'T'

        if shot_res == 'get':
            self.board.radar[s_x][s_y] = '□'

        if type(shot_res) == Ship:
            destroyed_ship = shot_res
            self.board.mark_destroyed_ship(destroyed_ship, True)
            self.enemy_ships.remove(destroyed_ship.size)
            shot_res = 'kill'

        return shot_res

    # возврат результата выстрела
    def receive_shot(self, shot):
        s_x, s_y = shot
        if type(self.board.map[s_x][s_y]) == Ship:
            ship = self.board.map[s_x][s_y]
            ship.hp -= 1
            if ship.hp <= 0:
                self.board.mark_destroyed_ship(ship, False)
                self.ships.remove(ship)
                return ship
            self.board.map[s_x][s_y] = '□'
            return 'get'
        else:
            self.board.map[s_x][s_y] = 'T'
            return 'miss'

class Ship:
    def __init__(self, size, x, y, direction):
        self.size = size
        self.hp = size
        self.x = x
        self.y = y
        self.direction = direction
        self.set_direction(direction)

    def __str__(self):
        return '■'
    def set_position(self, x, y, d):
        self.x = x
        self.y = y
        self.set_direction(d)
    def set_direction(self, d):
        self.direction = d
        if self.direction == 0:
            self.width = self.size
            self.height = 1
        elif self.direction == 1:
            self.width = 1
            self.height = self.size