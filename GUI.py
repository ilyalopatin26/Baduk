import pygame
import numpy as np
from BadukLogic import *
from BadukGameSession import *

pygame.init()

screen_width = 1200
screen_height = 800
delta_wh =screen_width - screen_height
screen = pygame.display.set_mode((screen_width, screen_height))

lsquare = int(screen_height / 10 )
Rstone = int( lsquare / 2 )
Stone_size = (  lsquare , lsquare  ) 
Goban_size = ( screen_height , screen_height)
y0, x0 = lsquare, lsquare



Pass_width = 200
Pass_height = 50
Pass_x = screen_height + (delta_wh // 2 ) - (Pass_width //2)
Pass_y = 100
pygame.draw.rect(screen, (255, 255, 255), (Pass_x, Pass_y, Pass_width, Pass_height))
button_font = pygame.font.Font(None, 36)
button_text_surface = button_font.render('Pass', True, (255, 0, 0))
button_text_rect = button_text_surface.get_rect(center=(Pass_x + Pass_width // 2, Pass_y + Pass_height // 2))
screen.blit(button_text_surface, button_text_rect)

Resign_width = 200
Resign_height = 50
Resign_x = screen_height + (delta_wh // 2 ) - (Resign_width //2)
Resign_y = 200
pygame.draw.rect(screen, (255, 255, 255), (Resign_x, Resign_y, Resign_width, Resign_height))
button_font = pygame.font.Font(None, 36)
button_text_surface = button_font.render('Resign', True, (255, 0, 0))
button_text_rect = button_text_surface.get_rect(center=(Resign_x + Resign_width // 2, Resign_y + Resign_height // 2))
screen.blit(button_text_surface, button_text_rect)

# Update the screen
pygame.display.flip()




def draw_sharp() :
    for n in range(9):
        xb, yb = x0 + n*lsquare, y0
        xe, ye = xb, y0 + 8*lsquare
        pygame.draw.line( screen, (0, 0, 0), (yb, xb), (ye, xe) )
    for n in range(9):
        xb, yb = x0, y0 + n*lsquare
        xe, ye = x0 + 8 *lsquare, yb   
        pygame.draw.line( screen, (0, 0, 0), (yb, xb), (ye, xe) )




Goban_image = pygame.image.load('src/Goban-texture.jpeg')
Bstone_image = pygame.image.load('src/black-stone.png')
Wstone_image = pygame.image.load('src/white-stone.png')

Goban_image = pygame.transform.scale(  Goban_image , Goban_size )
Bstone_image = pygame.transform.scale( Bstone_image , Stone_size )
Wstone_image = pygame.transform.scale( Wstone_image , Stone_size )


GoBoard = BadukGame()
flagContinue = True


def checkEndGame() :
    a = 10
    if not GoBoard.GameEnd():
        return False,  0
    
    BlackMarker, WhiteMarker, res = GoBoard.calculateResult()
    for x in range(9):
        for y in range(9):
            if GoBoard.currBoard.Neutral[x , y] == 0 :
                continue
            if BlackMarker[x ,y] == 1:
                pygame.draw.circle( screen, (0, 0, 0), (y0 + y*lsquare , x0+ x*lsquare  ), a )
            if WhiteMarker[x, y] == 1:
                pygame.draw.circle( screen, (255, 255, 255), (y0 + y*lsquare , x0+ x*lsquare  ), a )
    pygame.display.flip()
    return True, res

while True:
    if flagContinue:
        screen.blit( Goban_image, (0, 0) )
        draw_sharp()
        for x in range(9):
            for y in range(9):
                if GoBoard.currBoard.get_color( x, y) == 1:
                    screen.blit( Bstone_image, ( y0 + y*lsquare - Rstone  , x0+ x*lsquare - Rstone) )
                if GoBoard.currBoard.get_color( x, y ) == 2 :
                    screen.blit( Wstone_image, ( y0 + y*lsquare - Rstone  , x0+ x*lsquare - Rstone) )
    
        if GoBoard.currPlayer == 1:
            pygame.draw.circle( screen, (0, 0, 0), (screen_height-15, screen_height-15), 10 )
        else:
            pygame.draw.circle( screen, (255, 255, 255), (screen_height-15, screen_height-15), 10 )

        pygame.display.flip()

        flag, res= checkEndGame()
        if flag:
            flagContinue = False
            font = pygame.font.Font(None, 36)
            text = None
            if res > 0:
                text = font.render( f'Black win +{abs(res)}', True, (255, 0, 0 ))
            else:
                text = font.render( f'White win +{abs(res)}', True, (255, 0, 0 ))
            screen.blit( text, (Pass_x, 700 ) )
            pygame.display.flip()
            break
    else:
        break        



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if not flagContinue:
            break        

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_y, mouse_x = pygame.mouse.get_pos()

            if Pass_x <= mouse_y <= Pass_x + Pass_width and Pass_y <= mouse_x <= Pass_y + Pass_height:
                GoBoard.makeMove( -1, -1, True )
                break
            
            if Resign_x <= mouse_y <= Resign_x + Resign_width and Resign_y <= mouse_x <= Resign_y + Resign_height:
                flagContinue = False
                font = pygame.font.Font(None, 36)
                text = None
                if GoBoard.currPlayer == 1:
                    text = font.render('White win by resign', True, (255, 0, 0 ))
                else:
                    text = font.render('Black win by resign', True, (255, 0, 0 ))
                screen.blit( text, (Pass_x, 700 ) )
                pygame.display.flip()
                break

            if mouse_x < x0 or mouse_x > x0 + 8*lsquare or mouse_y < y0 or mouse_y > y0 + 8*lsquare:
                continue
            pos_y =  round( (mouse_y - y0) / lsquare )
            pos_x =  round( (mouse_x - x0) / lsquare )
            flag = GoBoard.makeMove( pos_x, pos_y )
            break
        
            

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()