#importing all the neccessary modules and other py files
import time
import random
from turtle import title
from pictures import *
from ship import Ship, Player, Enemy, Laser, collide

#initalize font and name of the game
pygame.font.init()
pygame.display.set_caption("Space Invaders")



def main():
    #declargin all used variables
    run = True
    lost = False
    lost_count = 0
    FPS = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 5
    player_vel = 5

    #create player object at x = 300, y = 500
    player = Player(300, 500)

    #creating clock object
    clock = pygame.time.Clock()

    #defining function for drawing the game
    def redraw_window():
        #drawing the window
        WIN.blit(BG, (0, 0))
        
        #drawing lives and level label at top right and top left corners which display lives and level variable counts
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, ((WIDTH - level_label.get_width() - 10), 10))


        #drawing enemies
        for enemy in enemies:
            enemy.draw(WIN)

        #drawing player
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Game Over", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width() / 2, 350))


        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()
        #game over message if player health reaches 0 or lives reaches zero

        if lives <= 0  or player.health <= 0:
            lost = True
            lost_count += 1


        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        #if level successfully completed increasing level and and number of enemies that are randomly chosen from red blue or green
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #declaring key listeners for movevemt, shooting and starting the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w]  and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        #enemies shooting lasers with 1 in 2 probability
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(0, 120) == 1:
                enemy.shoot()

            #if enemy touches the players player looses 30 health from total of 100
            if collide(enemy, player):
                player.health -= 30
                enemies.remove(enemy)
            #if enemy goes behind the screen player looses 1 live from total of 3
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            

        player.move_lasers(-laser_vel, enemies)


#creating main menu, clicking anywhere on the screen with mouse will make the game starts
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press mouse to begin", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()