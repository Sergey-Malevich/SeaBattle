from settings import *


if __name__ == '__main__':
    # делаем список из двух игроков и задаем им основные параметры
    players = []
    players.append(Player(name='User', is_ai=False))
    players.append(Player(name='AI', is_ai=True))

    # создаем саму игру и начинаем
    game = Game()

    while True:
        # каждое начало хода проверяем статус и дальше уже действуем исходя из статуса игры
        game.status_check()

        if game.status == 'prepare':
            game.add_player(players.pop(0))

        if game.status == 'in game':
            game.current_player.message.append("Ход игрока, введите x y через пробел: ")
            game.draw()
            game.current_player.message.clear()
            shot_result = game.current_player.make_shot(game.next_player)

            if shot_result == 'miss':
                game.next_player.message.append('AI, промахнулся! '.format(game.current_player.name))
                game.switch_players()
                continue

            elif shot_result == 'retry':
                game.current_player.message.append('Что то пошло не так, попробуй еще раз!')
                continue

            elif shot_result == 'get':
                game.current_player.message.append('Попал, стреляй еще!')
                game.next_player.message.append('Ваш корабль подбит!')
                continue

            elif shot_result == 'kill':
                game.current_player.message.append('Поздравляю, корабль врага уничтожен!')
                game.next_player.message.append('Вы лишились одного судна :```(')
                continue

        if game.status == 'game over':
            game.next_player.board.draw_board(False)
            game.current_player.board.draw_board(False)
            print('Все корабли противника {} уничтожены!'.format(game.next_player.name))
            print('{} выиграл!'.format(game.current_player.name))
            break

    input('')