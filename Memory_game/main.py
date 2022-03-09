"""
Memory Game by Adam Bigos
Made with PyGame
I know the code is terrible but time was pressing
"""
import time

import pygame, sys
from config import BaseSettings, game_window
import random
from utils import draw_text, tile_coordinates, possible_choices, word_coordinates

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f"[!] Had {check_errors[1]} errors when initialising game, exiting...")
    sys.exit(-1)
else:
    print("[+] Game successfully initialised")

pygame.display.set_caption("Memory Game - recruitment task performed by Adam Bigos")

# defining logo path
logo = pygame.image.load("logo.png")

# importing a database from a text file
txt_file = open("Words.txt", "r")

words_pool = []
for x in txt_file:
    words_pool.append(x.replace("\n", ""))


class MemoryGame:
    def start_menu(self, difficulty_lvl):

        selected = 0

        while True:
            game_window.fill(BaseSettings.WHITE)
            selected = selected % 2
            draw_text("Press ESC to quit", 20, BaseSettings.BLACK, None, 560, 0, "topleft")
            draw_text("Navigate with arrow keys", 20, BaseSettings.BLACK, None, 560, 17, "topleft")
            game_window.blit(logo, (15, BaseSettings.HEIGHT / 2 - logo.get_height() / 2))
            if selected == 0:
                draw_text("START GAME", 60, BaseSettings.RED, None, 350, 140, "topleft")
                draw_text("DIFFICULTY: ", 60, BaseSettings.BLACK, None, 350, 250, "topleft")
                draw_text(difficulty_lvl, 60, BaseSettings.BLACK, None, 350, 290, "topleft")
            elif selected == 1:
                draw_text("START GAME", 60, BaseSettings.BLACK, None, 350, 140, "topleft")
                draw_text("DIFFICULTY:", 60, BaseSettings.RED, None, 350, 250, "topleft")
                draw_text(difficulty_lvl, 60, BaseSettings.RED, None, 350, 290, "topleft")

            # iterate over the list of Event objects
            # that was returned by pygame.event.get() method.
            for event in pygame.event.get():

                # if event object type is QUIT then quitting the pygame and program both.
                if event.type == pygame.QUIT:
                    # deactivates the pygame library
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        selected -= 1
                    elif event.key == pygame.K_DOWN:
                        selected += 1
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.start_game(difficulty_lvl)
                        elif selected == 1:
                            self.difficulty_menu()

            # Draws the surface object to the screen.
            pygame.display.update()
            BaseSettings.fps_controller.tick(60)

    def difficulty_menu(self):
        sequence = [BaseSettings.BLUE, BaseSettings.BLUE, BaseSettings.BLUE, BaseSettings.BLUE, BaseSettings.BLUE]
        selected = 0
        while True:
            game_window.fill(BaseSettings.BLUE)
            draw_text(
                "EASY", 60, BaseSettings.BLACK, sequence[0], BaseSettings.WIDTH / 2, 119, "center"
            ),
            draw_text(
                "HARD", 60, BaseSettings.BLACK, sequence[1], BaseSettings.WIDTH / 2, 219, "center"
            ),
            draw_text(
                "BONUS STAGE: IMPOSSIBLE", 60, BaseSettings.BLUE, sequence[2], BaseSettings.WIDTH / 2, 319, "center",
            )

            for event in pygame.event.get():

                # if event object type is QUIT then quitting the pygame and program both.
                if event.type == pygame.QUIT:
                    # deactivates the pygame library
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        selected -= 1
                    elif event.key == pygame.K_DOWN:
                        selected += 1
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.start_menu("EASY")
                        elif selected == 1:
                            self.start_menu("HARD")
                        elif selected == 2:
                            self.start_menu("IMPOSSIBLE")

            selected = selected % 3
            sequence = [BaseSettings.BLUE, BaseSettings.BLUE, BaseSettings.BLUE]
            sequence[selected] = BaseSettings.RED

            # Draws the surface object to the screen.
            pygame.display.update()
            BaseSettings.fps_controller.tick(60)

    # Main logic
    def start_game(self, difficulty):
        running = True
        tries_left = 0
        word_to_guess = 0
        player_selection = ""
        player_selection_storage = []
        tiles_location = []
        words_location = []
        possibilities = possible_choices()
        bad_player = False
        tiles_flipped = []
        delay = 0

        if difficulty == "EASY":
            tries_left = 8
            word_to_guess = 4
            tiles_location = tile_coordinates(2)
            words_location = word_coordinates(2)
            del possibilities[8:16]
        elif difficulty == "HARD":
            tries_left = 15
            word_to_guess = 8
            tiles_location = tile_coordinates(4)
            words_location = word_coordinates(4)
        elif difficulty == "IMPOSSIBLE":
            tries_left = 1
            word_to_guess = 8
            tiles_location = tile_coordinates(4)
            words_location = word_coordinates(4)

        words_flipped_or_guessed = []
        game_word_pool = random.choices(words_pool, k=word_to_guess)
        game_word_pool += game_word_pool
        random.shuffle(game_word_pool)
        word_location_dictionary = {possibilities[i]: [game_word_pool[i], tiles_location[i], words_location[i]] for i in range(len(game_word_pool)) }

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Whenever a key is pressed down
                if event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_selection.lower() not in possibilities:
                            bad_player = True
                            player_selection = ""
                        else:
                            bad_player = False
                            if len(player_selection_storage) > 0:
                                if player_selection != player_selection_storage[0]:
                                    tiles_flipped.append(word_location_dictionary[player_selection][1])
                                    words_flipped_or_guessed.append([word_location_dictionary[player_selection][0],
                                                                     word_location_dictionary[player_selection][2]])
                                    tiles_location.remove(word_location_dictionary[player_selection][1])
                                    possibilities.remove(player_selection)
                                    player_selection_storage.append(player_selection)
                            else:
                                tiles_flipped.append(word_location_dictionary[player_selection][1])
                                words_flipped_or_guessed.append([word_location_dictionary[player_selection][0],
                                                                 word_location_dictionary[player_selection][2]])
                                tiles_location.remove(word_location_dictionary[player_selection][1])
                                possibilities.remove(player_selection)
                                player_selection_storage.append(player_selection)
                            player_selection = ""
                    elif event.unicode.isprintable():
                        if len(player_selection) < 2:
                            player_selection += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        player_selection = player_selection[:-1]

                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # GFX
            game_window.fill(BaseSettings.WHITE)

            draw_text("Please type your guess (example: 'A1')", 30, BaseSettings.BLACK, None, 360, 5, "center")
            pygame.draw.rect(game_window, BaseSettings.RED, pygame.Rect(340, 65, 40, 25), 2)
            draw_text(player_selection, 30, BaseSettings.BLACK, None, 360, 70, "center")
            draw_text("tries left: " + str(tries_left), 30, BaseSettings.BLACK, None, 470, 100, "topleft")
            draw_text("A", 30, BaseSettings.BLACK, None, 182, 135, "center")
            draw_text("B", 30, BaseSettings.BLACK, None, 302, 135, "center")
            draw_text("C", 30, BaseSettings.BLACK, None, 422, 135, "center")
            draw_text("D", 30, BaseSettings.BLACK, None, 542, 135, "center")
            draw_text("1", 30, BaseSettings.BLACK, None, 100, 173, "center")
            draw_text("2", 30, BaseSettings.BLACK, None, 100, 228, "center")

            if difficulty != "EASY":
                draw_text("3", 30, BaseSettings.BLACK, None, 100, 283, "center")
                draw_text("4", 30, BaseSettings.BLACK, None, 100, 338, "center")
            if bad_player:
                draw_text("WRONG try again", 30, BaseSettings.RED, None, 360, 35, "center")

            for i in range(len(tiles_location)):
                pygame.draw.rect(game_window, BaseSettings.SNAKE_GREEN, pygame.Rect(tiles_location[i][0], tiles_location[i][1], 115, 50))

            for i in range(len(words_flipped_or_guessed)):
                draw_text(words_flipped_or_guessed[i][0], 30, BaseSettings.RED, None, words_flipped_or_guessed[i][1][0], words_flipped_or_guessed[i][1][1], "center")

            # Game conditions
            if tries_left == 0:
                self.game_over("I'm sorry you lost")

            if len(tiles_location) == 0:
                self.game_over("CONGRATULATIONS YOU WON")

            if len(player_selection_storage) > 1:
                delay +=1

            if delay > 30:
                if word_location_dictionary[player_selection_storage[0]][0] == word_location_dictionary[player_selection_storage[1]][0]:
                    tiles_flipped.clear()
                    player_selection_storage.clear()
                    delay = 0

                else:
                    tiles_location.extend(tiles_flipped)
                    words_flipped_or_guessed.remove(
                        [word_location_dictionary[player_selection_storage[0]][0],
                         word_location_dictionary[player_selection_storage[0]][2]])
                    words_flipped_or_guessed.remove(
                        [word_location_dictionary[player_selection_storage[1]][0],
                         word_location_dictionary[player_selection_storage[1]][2]])
                    tiles_flipped.clear()
                    possibilities.extend(player_selection_storage)
                    player_selection_storage.clear()
                    tries_left -= 1
                    delay = 0

            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            BaseSettings.fps_controller.tick(60)

    def game_over(self, final_score):
        running = True
        player_name = ""
        while running:
            game_window.fill(BaseSettings.BLACK)

            draw_text(
                "WELL DONE!", 70, BaseSettings.BLUE, None, BaseSettings.WIDTH / 2, 60, "center"
            )
            draw_text(
                "Enter your name:",
                40,
                BaseSettings.WHITE,
                None,
                BaseSettings.WIDTH / 2,
                226,
                "center",
            )
            draw_text(
                player_name, 45, BaseSettings.WHITE, None, BaseSettings.WIDTH / 2, 260, "center"
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        self.end_game_screen(final_score, player_name)
                    elif event.unicode.isalpha():
                        player_name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]

            # Refresh game screen
            pygame.display.update()
            BaseSettings.fps_controller.tick(60)

    # Game Over with option to start again with the same difficulty level
    def end_game_screen(self, final_score, player_name):
        running = True
        player = player_name
        while running:
            game_window.fill(BaseSettings.BLACK)

            draw_text(
                "Memory Game",
                100,
                BaseSettings.SNAKE_GREEN,
                None,
                BaseSettings.WIDTH / 2,
                70,
                "center",
            )
            draw_text(
                player, 70, BaseSettings.BLUE, None, BaseSettings.WIDTH / 2, 160, "center"
            )
            draw_text(
                final_score,
                50,
                BaseSettings.SNAKE_GREEN,
                None,
                BaseSettings.WIDTH / 2,
                265,
                "center",
            )
            draw_text(
                "Press ENTER to PLAY AGAIN", 30, BaseSettings.BLUE, None, 219, 380, "topleft"
            )

            pygame.draw.rect(game_window, BaseSettings.BLUE, (189, 355, 342, 70), 10, 19)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        self.start_menu("EASY")

            # Refresh game screen
            pygame.display.update()
            BaseSettings.fps_controller.tick(60)


MemoryGame().start_menu("EASY")
