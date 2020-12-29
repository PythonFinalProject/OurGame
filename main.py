import pygame
import random
from random import choice 
from character import Player, Enemy, Explosion

win_width = 480
win_height = 480
pygame.init()

win = pygame.display.set_mode((win_width,win_height)) # 遊戲視窗
pygame.display.set_caption("First Game") # 给視窗取名
clock = pygame.time.Clock() # 遊戲更新速度

start_bg = pygame.image.load("./materials/startphoto(480).png")
start_bg.convert()
win.blit(start_bg, (0, 0))

font4 = pygame.font.SysFont("simhei", 50) # 按鈕字體、大小

button1_ps = (int(win_width/7*1), int(win_height/7*5.5)) # 按鈕位置修改處
button2_ps = (int(win_width/7*3), int(win_height/7*5.5))
button3_ps = (int(win_width/7*5), int(win_height/7*5.5))
button4_ps = (0, 0)

# 建立按鈕並檢查是否按下滑鼠
to_run = True
n1 = True
while to_run: 
    while n1:  
        clock.tick(30)
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        
        str1 = "PLAY"
        str2 = "QUIT"
        str3 = "SET"

        button1_off = font4.render(str1, True, (170,0,0),(0,0,0)) 
        button1_on = font4.render(str1, True, (255,0,0),(0,0,0))
        button2_off = font4.render(str2, True, (170,0,0),(0,0,0))
        button2_on = font4.render(str2, True, (255,0,0),(0,0,0))
        button3_off = font4.render(str3, True, (170,0,0),(0,0,0))
        button3_on = font4.render(str3, True, (255,0,0),(0,0,0))
        button_size = []

        button_size.append([button1_off.get_size()[0], button1_off.get_size()[1]])
        button_size.append([button2_off.get_size()[0], button2_off.get_size()[1]])
        button_size.append([button3_off.get_size()[0], button3_off.get_size()[1]])

        win.blit(start_bg,(0,0))
        win.blit(button1_off, button1_ps)
        win.blit(button2_off, button2_ps)
        win.blit(button3_off, button3_ps)
             
        if x1 >= button1_ps[0] and x1 <= button1_ps[0]+button_size[0][0] and y1 >= button1_ps[1] and y1 <=button1_ps[1]+button_size[0][1]:
            win.blit(button1_on, button1_ps)
            if buttons[0]:  #若按下 進入
                n1 = False
        if x1 >= button2_ps[0] and x1 <= button2_ps[0]+button_size[1][0] and y1 >= button2_ps[1] and y1 <=button2_ps[1]+button_size[1][1]:
            win.blit(button2_on, button2_ps)         
            if buttons[0]:  #若按下 退出
                print("exiting...")
                to_run = False
                break
        if x1 >= button3_ps[0] and x1 <= button3_ps[0]+button_size[2][0] and y1 >= button3_ps[1] and y1 <=button3_ps[1]+button_size[2][1]:
            win.blit(button3_on, button3_ps)
           
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting")
                pygame.quit()
    
    if to_run == False:
        break

    """""" #遊戲畫面
    font2 = pygame.font.SysFont("simhei", 20)   #score 

    CREATE_ENEMY_EVENT = pygame.USEREVENT

    # Initialize player
    # player = Player(300, 410, 591//9, 261//4)
    player_list = []
    target_player = []  #敵方目標清單
    for i in range(2):
        player_list.append(Player(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 591//9, 261//4))
        target_player.append(i)
    # Initialize enemy
    N = 1
    enemy_list = []
    for i in range(N):
        enemy_list.append(Enemy(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 576//9, 256//4))
        enemy_list[i].target = random.randrange(0, len(player_list), 1)

    bg = pygame.image.load('./materials/bg.jpg')
    bg.convert()

    def redrawGameWindow(win):
        win.blit(bg, (0, 0))
        for player in player_list:
            player.draw(win)
            if player.health > 0:  #生命歸零時不畫出角色血量 
                health_bg1 = pygame.Surface((40,5))  #血條大小
                health_bg1.convert()
                health_bg1.fill((255,0,0))
                win.blit(health_bg1, (player.x+10, player.y))

                health_bg2 = pygame.Surface((int(40*player.health/player.healthmax),5))  #血條大小
                health_bg2.convert()
                health_bg2.fill((0,255,0))
                win.blit(health_bg2, (player.x+10, player.y))
                #win.blit(health_bg, (player.x+10, player.y))
                #pygame.draw.rect(health_bg, (0,255,0), [0,0,100,100], 20)   #打不出來...
                #pygame.draw.circle(health_bg,(0,255,0),(30,30),20,0)
            for bullet in player.bullet_list:
                bullet.draw(win)
            # print(player.explode_list)
            for explosion in player.explode_list:
                explosion.draw(win,player)
                if explosion.remove == True:
                    player.explode_list.pop(player.explode_list.index(explosion))
        for enemy in enemy_list:
            enemy.draw(win)
        
        text2 = font2.render("score:%d" %score, True, (0,0,0),(255,255,255))  #畫出分數
        win.blit(text2, (0, 0))   
        
        pygame.display.update()

    def checkPlayerEnemyCollision(player):
        global cold_time   # 受傷忍卻時間
        player_hb_0 = player.hitbox[0]
        player_hb_1 = player.hitbox[1]
        player_hb_2 = player.hitbox[2]
        player_hb_3 = player.hitbox[3]
        for enemy in enemy_list:
            enemy_hb_0 = enemy.hitbox[0]
            enemy_hb_1 = enemy.hitbox[1]
            enemy_hb_2 = enemy.hitbox[2]
            enemy_hb_3 = enemy.hitbox[3]
            if player_hb_1 + player_hb_3 > enemy_hb_1 and player_hb_1 < enemy_hb_1 + enemy_hb_3 and player_hb_0 + player_hb_2 > enemy_hb_0 and player_hb_0 < enemy_hb_0 + enemy_hb_2:
                if player.cold_time >130: # 受傷忍卻時間
                    player.cold_time = 0 # 重新計時
                    player.hit()
                    

    def checkEnemyEnemyCollision():
        for i in range(len(enemy_list)-1, -1, -1):
            collision = False
            first = enemy_list[i]
            first_hb_0 = first.hitbox[0]
            first_hb_1 = first.hitbox[1]
            first_hb_2 = first.hitbox[2]
            first_hb_3 = first.hitbox[3]
            for j in range(i-1, -1, -1):
                # if i == j:
                #     continue
                second = enemy_list[j]
                second_hb_0 = second.hitbox[0]
                second_hb_1 = second.hitbox[1]
                second_hb_2 = second.hitbox[2]
                second_hb_3 = second.hitbox[3]
                if first_hb_1 + first_hb_3 > second_hb_1 and first_hb_1 < second_hb_1 + second_hb_3 and first_hb_0 + first_hb_2 > second_hb_0 and first_hb_0 < second_hb_0 + second_hb_2:
                    collision = True
                    # print("collision")
                    break
            if collision == False:
                if first.target not in target_player:
                    first.target = choice(target_player)
                first.chase(player_list[first.target])


    def playerUpdate(player_list):
        for player in player_list:
            player.shootLoop += 1
            player.switchLoop += 1 
            if player.shootLoop >= player.shootCoolDown:
                player.shootLoop = 0
            if player.switchLoop >= player.switchGap:
                player.switchLoop =0 

    run = [True]
    score = 0 # 分數

    player_selection = ["1P", "2P"]
    while run[0]:
        clock.tick(60) # Set FPS
           
        # Pygame event control, including (1) check running status, (2) appending enemy in a specific time period
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run[0] = False 
                to_run = False
                pygame.quit()
            elif event.type == CREATE_ENEMY_EVENT:
                # This will create enemy every 0.2 sec
                enemy_list.append(Enemy(random.randrange(1, win_width, 1), random.randrange(1, win_height, 1), 576//9, 256//4))
                enemy_list[-1].target = random.randrange(0, len(player_list), 1)
        if len(target_player) == 0: # 如果沒有目標 退出遊戲
            run[0] = False
            pygame.time.wait(1000) # 短暫暫停
            break
        checkEnemyEnemyCollision()
        #print("new")
        # Moving the player with "WASD"
        for i, player in enumerate(player_list):
            checkPlayerEnemyCollision(player)
            
            if (player.health <= 0) and i in target_player: # 生命歸零時 移出目標清單
                target_player.remove(i)  

            player.control(run, win_width, win_height, player_selection[i])
            for bullet in player.bullet_list:
                bullet.fly()
                if bullet.out(win_width, win_height):
                    player.bullet_list.pop(player.bullet_list.index(bullet))
                    continue

                for enemy in enemy_list:
                    enemy_hb_0 = enemy.hitbox[0]
                    enemy_hb_1 = enemy.hitbox[1]
                    enemy_hb_2 = enemy.hitbox[2]
                    enemy_hb_3 = enemy.hitbox[3]
                    if bullet.x > enemy_hb_0 and bullet.x < enemy_hb_0 + enemy_hb_2 and bullet.y > enemy_hb_1 and bullet.y < enemy_hb_1 + enemy_hb_3:
                        x = enemy_hb_0
                        y = enemy_hb_1
                        exp = Explosion(x,y) 
                        player.explode_list.append(exp)
                        player.bullet_list.pop(player.bullet_list.index(bullet))
                        enemy_list.pop(enemy_list.index(enemy))
                        score += 1 # 打死敵人後分數加1
                        break
            player.cold_time += 1 # 計算受傷忍卻時間

        # print(len(player_list))
            # print(len(player.bullet_list))
        playerUpdate(player_list)
        redrawGameWindow(win)
        
    """"""  #結束畫面
    bg_over = pygame.image.load('./materials/overphoto.png')
    bg_over.convert()

    n2 = True
    while n2:
        clock.tick(30)
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        
        win.blit(bg_over, (0, 0))
        font3 = pygame.font.SysFont("simhei", 40)
        text3 = font3.render("GameOver", True, (0,0,0),(255,255,255))  #GameOver文字
        win.blit(text3, (int(win_width/2-100), int(win_height/2)))   #
        text4 = font3.render("score: %d" %score, True, (0,0,0),(255,255,255))  #score文字
        win.blit(text4, (int(win_width/2-100), int(win_height/2+50)))
        
        str1 = "AGAIN"
        str2 = "SCORE"
        str3 = "QUIT"

        button1_off = font4.render(str1, True, (170,0,0),(0,0,0)) 
        button1_on = font4.render(str1, True, (255,0,0),(0,0,0))
        button2_off = font4.render(str2, True, (170,0,0),(0,0,0))
        button2_on = font4.render(str2, True, (255,0,0),(0,0,0))
        button3_off = font4.render(str3, True, (170,0,0),(0,0,0))
        button3_on = font4.render(str3, True, (255,0,0),(0,0,0))
        button_size = []
        button_size.append([button1_off.get_size()[0], button1_off.get_size()[1]])
        button_size.append([button2_off.get_size()[0], button2_off.get_size()[1]])
        button_size.append([button3_off.get_size()[0], button3_off.get_size()[1]])
        
        str4 = "BACK"
        button4_off = font4.render(str4, True, (170,0,0),(0,0,0))
        button4_on = font4.render(str4, True, (255,0,0),(0,0,0))
        button_size.append([button4_off.get_size()[0], button4_off.get_size()[1]])
        
        win.blit(button1_off, button1_ps)
        win.blit(button2_off, button2_ps)
        win.blit(button3_off, button3_ps)
        win.blit(button4_off, button4_ps)
        if x1 >= button1_ps[0] and x1 <= button1_ps[0]+button_size[0][0] and y1 >= button1_ps[1] and y1 <=button1_ps[1]+button_size[0][1]:
            win.blit(button1_on, button1_ps)
            if buttons[0]: # 若按下 進入                
                break
        if x1 >= button2_ps[0] and x1 <= button2_ps[0]+button_size[1][0] and y1 >= button2_ps[1] and y1 <=button2_ps[1]+button_size[1][1]:
            win.blit(button2_on, button2_ps)
                       
        if x1 >= button3_ps[0] and x1 <= button3_ps[0]+button_size[2][0] and y1 >= button3_ps[1] and y1 <=button3_ps[1]+button_size[2][1]:
            win.blit(button3_on, button3_ps)
            if buttons[0]: # 若按下 退出
                to_run = False
                break
        if x1 >= button4_ps[0] and x1 <= button4_ps[0]+button_size[3][0] and y1 >= button4_ps[1] and y1 <=button4_ps[1]+button_size[3][1]:
            win.blit(button4_on, button4_ps)
            if buttons[0]: # 若按下 退出
                n1 = True
                break       
                
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting")
                n2 = False
                to_run = False
                pygame.quit()
         
    if to_run == False:
        break
        
pygame.quit()