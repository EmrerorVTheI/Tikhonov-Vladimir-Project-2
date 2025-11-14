import os
import shutil
import pygame
import sys
import pyperclip
pygame.init()

width, height = 1600, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Файловый Менеджер 1.0")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
button_x, button_y = 650, 350
button_width, button_height = 300, 100
font = pygame.font.Font(None, 40)
btn1 = True

text_x, text_y = 100, 350
text_width, text_height = 1400, 50
user_text = "Введите путь к файлу без кавычек и нажмите RShift"
text1 = False

folder1 = False
files_count = 0
move_type = -1
chosen_file = ''
search1 = False
search2 = False
search_text = 'Введите ключевое слово и нажмите RShift'
found_files = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if btn1 == True:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (button_x <= mouse_x <= button_x + button_width and
                    button_y <= mouse_y <= button_y + button_height):
                    btn1 = False
                    text1 = True
            elif folder1 == True:
                search2 = False
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (20 <= mouse_x <= 1580 and
                    20 <= mouse_y <= y_position):
                    if move_type == -1:
                        chosen_file = files[(mouse_y - 20) // 50]
                        move_type = 0
                    elif move_type == 0:
                        if files[(mouse_y - 20) // 50] == chosen_file:
                            move_type = -1
                            os.remove(user_text+'/'+chosen_file)   
                        else:
                            move_type = -1
                            shutil.copy(user_text+'/'+chosen_file, user_text+'/'+files[(mouse_y - 20) // 50])   
                if (20 <= mouse_x <= 1580 and
                    y_position + 50 <= mouse_y <= y_position + 100):  
                    search1 = True                  
        elif event.type == pygame.KEYDOWN:
            if text1 == True:
                if event.key == pygame.K_DELETE:
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RSHIFT:
                    text1 = False
                    folder_path = user_text
                    folder1 = True
                elif event.key == pygame.K_LCTRL:
                    user_text = user_text + pyperclip.paste()
                else:
                    user_text += event.unicode
            elif search1 == True:
                if event.key == pygame.K_DELETE:
                    search_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                elif event.key == pygame.K_RSHIFT:
                    if search_text == '/exit':
                        search1 = False
                        search2 = False
                    else:
                        search1 = False
                        found_files = []
                        for file in files:
                            if search_text in file:
                                found_files.append(file)
                        search2 = True                                  
                elif event.key == pygame.K_LCTRL:
                    search_text = search_text + pyperclip.paste()
                else:
                    search_text += event.unicode         

    screen.fill(WHITE)
    if btn1 == True:
        button_color = LIGHT_BLUE if pygame.mouse.get_pos()[0] in range(button_x, button_x + button_width) and \
                                      pygame.mouse.get_pos()[1] in range(button_y, button_y + button_height) else BLUE
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    if btn1 == True:
        text = font.render("Начать работу", True, WHITE)
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(text, text_rect)
    if text1 == True:
        pygame.draw.rect(screen, BLACK, (text_x, text_y, text_width, text_height), 2)
    if text1 == True:
        text_surface = font.render(user_text, True, BLACK)
        screen.blit(text_surface, (text_x + 5, text_y + 10))
        add_text = font.render('удалить этот текст можно нажав Delete', True, BLACK)
        screen.blit(add_text, (text_x + 5, text_y + 50))
        add2_text = font.render('можно вставить текст нажав LCtrl', True, BLACK)
        screen.blit(add2_text, (text_x + 5, text_y + 100))
    elif search1 == True:
        text_surface = font.render(search_text, True, BLACK)
        screen.blit(text_surface, (25, y_position + 60))
        add_text = font.render('удалить этот текст можно нажав Delete', True, BLACK)
        screen.blit(add_text, (25, y_position + 110))
        add2_text = font.render('можно вставить текст нажав LCtrl', True, BLACK)
        screen.blit(add2_text, (25, y_position + 160))
    if folder1 == True:
        if search2 == False:
            files = os.listdir(folder_path)
            y_position = 20
            for file in files:
                text_surface = font.render(file, True, BLACK)
                screen.blit(text_surface, (20, y_position))
                y_position += 50
            files_count = y_position // 50
            files_text = font.render('Количество файлов в папке: '+str(files_count), True, BLACK)
            screen.blit(files_text, (20, y_position))
            pygame.draw.rect(screen, BLACK, (20, y_position + 50, 1560, 50), 2)
        else:
            files = found_files
            y_position = 20
            for file in files:
                text_surface = font.render(file, True, BLACK)
                screen.blit(text_surface, (20, y_position))
                y_position += 50
            files_count = y_position // 50
            files_text = font.render('Найденное количество файлов: '+str(files_count), True, BLACK)
            screen.blit(files_text, (20, y_position))
            pygame.draw.rect(screen, BLACK, (20, y_position + 50, 1560, 50), 2)
    pygame.display.flip()

pygame.quit()
sys.exit()