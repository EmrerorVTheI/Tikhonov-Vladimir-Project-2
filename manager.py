import os
import shutil
import pygame
import sys
import pyperclip
from Config import width, height, WHITE, BLUE, LIGHT_BLUE, BLACK, button_x, button_y, button_width, button_height, text_x, text_y, text_width, text_height, move_type

pygame.init()

font = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Файловый Менеджер 1.0")

btn1 = True
user_text = ''
text1 = False 
folder1 = False
files_count = 0
chosen_file = ''
search1 = False
search2 = False
search_text = ''
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
                if (20 <= mouse_x <= width - 20 and
                    20 <= mouse_y <= y_position):
                    if move_type == -1:
                        chosen_file = files[(mouse_y - 20) // text_height]
                        move_type = 0
                    elif move_type == 0:
                        if files[(mouse_y - 20) // text_height] == chosen_file:
                            move_type = -1
                            os.remove(user_text+'/'+chosen_file)   
                        else:
                            move_type = -1
                            shutil.copy(user_text+'/'+chosen_file, user_text+'/'+files[(mouse_y - 20) // text_height])   
                if (20 <= mouse_x <= width - 20 and
                    y_position + text_height <= mouse_y <= y_position + 2 * text_height):  
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
        add_text = font.render('Введите путь к файлу без кавычек и нажмите RShift', True, BLACK) 
        screen.blit(add_text, (text_x + 5, text_y + text_height + 10))
        add2_text = font.render('Удалить этот текст можно нажав Delete', True, BLACK)
        screen.blit(add2_text, (text_x + 5, text_y + 2 * text_height + 10))
        add3_text = font.render('Можно вставить текст нажав LCtrl', True, BLACK)
        screen.blit(add3_text, (text_x + 5, text_y + 3 * text_height + 10))
    elif search1 == True:
        text_surface = font.render(search_text, True, BLACK)
        screen.blit(text_surface, (25, y_position + text_height + 10))
        add_text = font.render('Введите ключевое слово и нажмите RShift', True, BLACK)
        screen.blit(add_text, (25, y_position + 2 * text_height + 10))
        add2_text = font.render('Удалить этот текст можно нажав Delete', True, BLACK)
        screen.blit(add2_text, (25, y_position + 3 * text_height + 10))
        add3_text = font.render('Можно вставить текст нажав LCtrl', True, BLACK)
        screen.blit(add3_text, (25, y_position + 4 * text_height + 10))
    if folder1 == True:
        if search2 == False:
            files = os.listdir(folder_path)
            y_position = 20
            for file in files:
                text_surface = font.render(file, True, BLACK)
                screen.blit(text_surface, (20, y_position))
                y_position += text_height
            files_count = y_position // text_height
            files_text = font.render('Количество файлов в папке: '+str(files_count), True, BLACK)
            screen.blit(files_text, (20, y_position))
            pygame.draw.rect(screen, BLACK, (20, y_position + text_height, width - 40, text_height), 2)
        else:
            files = found_files
            y_position = 20
            for file in files:
                text_surface = font.render(file, True, BLACK)
                screen.blit(text_surface, (20, y_position))
                y_position += text_height
            files_count = y_position // text_height
            files_text = font.render('Найденное количество файлов: ' + str(files_count), True, BLACK)
            screen.blit(files_text, (20, y_position))
            pygame.draw.rect(screen, BLACK, (20, y_position + text_height, width - 40, text_height), 2)
    pygame.display.flip()

pygame.quit()
sys.exit()
