import pygame
import random
from random import choice 
from character import Player, Enemy, Explosion, Coconut, Button
from datetime import *
from tilemap import *
import pandas as pd 
import csv


win_width = 480
win_height = 480
map_width = 896 
map_height = 896
pygame.init()

win = pygame.display.set_mode((win_width,win_height)) # 遊戲視窗
pygame.display.set_caption("First Game") # 给視窗取名
clock = pygame.time.Clock() # 遊戲更新速度

start_bg = pygame.image.load("./materials/startphoto(480).png")
start_bg.convert()
win.blit(start_bg, (0, 0))
gamename = pygame.image.load("./materials/gamename.png")
gamename.convert()

#預設值
to_run = True
n1 = True
player_selection = ["1P"]
while to_run: 
    run = [True]
    n2 = True
    while n1:
        n1_set = False
        clock.tick(30)
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        win.blit(start_bg,(0,0))
        win.blit(gamename, (90, 100))
        button1 = Button(int(win_width/7*1), int(win_height/7*5.5), "PLAY")  # 按鈕位置、文字修改處
        button2 = Button(int(win_width/7*2.8), int(win_height/7*5.5), "QUIT")# 2.8 --> 比較對齊
        button3 = Button(int(win_width/7*5), int(win_height/7*5.5), "SET")
        win.blit(button1.off, button1.ps)
        win.blit(button2.off, button2.ps)
        win.blit(button3.off, button3.ps)            
        if button1.range(x1,y1):
            win.blit(button1.on, button1.ps)
            if buttons[0]:  #若按下 進入
                n1 = False
        if button2.range(x1,y1):
            win.blit(button2.on, button2.ps)         
            if buttons[0]:  #若按下 退出
                print("exiting...")
                to_run = False
                break
        if button3.range(x1,y1):
            win.blit(button3.on, button3.ps)
            if buttons[0]:                
                print("set")
                n1_set = True
                break
                
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting")
                to_run = False
                n1 = False
                n1_set = False
                run = [False]
                n2 = False 
                pygame.quit()
    help = False
    while n1_set:    #set model    
        clock.tick(30)
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos() 
        
        if help == False:  
            win.blit(start_bg,(0,0))
            button1 = Button(int(win_width/7*1.65), int(win_height/7*2), "SINGLE PLAY") #1.65 --> 比較置中
            button2 = Button(int(win_width/7*1.5), int(win_height/7*4), "COOPERATIVE")
            button3 = Button(int(win_width/7*3), int(win_height/7*6), "HELP")        
            win.blit(button1.off, button1.ps)
            win.blit(button2.off, button2.ps)  
            win.blit(button3.off, button3.ps)        
            if button1.range(x1,y1):
                win.blit(button1.on, button1.ps)
                if buttons[0]:  #若按下 進入
                    player_selection = ["1P"]   #從下面移到這裡，設定模式
                    print("SINGLE PLAY")
                    n1_set = False
                    run = [False]
                    n2 = False    
            if button2.range(x1,y1):
                win.blit(button2.on, button2.ps)
                if buttons[0]:  #若按下 進入
                    player_selection = ["1P","2P"]   #從下面移到這裡，設定模式
                    print("COOPERATIVE")
                    n1_set = False
                    run = [False]
                    n2 = False
            if button3.range(x1,y1):
                win.blit(button3.on, button3.ps)
                if buttons[0]:  #若按下 進入
                    help = True
                    continue
        else:         
            help_bg = pygame.image.load("./materials/help.png")
            help_bg.convert()
            win.blit(help_bg,(0,0))
            button3 = Button(350, 380, "BACK")
            win.blit(button3.off, button3.ps) 
            if button3.range(x1,y1):
                win.blit(button3.on, button3.ps)
                if buttons[0]:  #若按下 進入
                    help = False
                    continue
  
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting")
                to_run = False
                n1 = False
                n1_set = False
                run = [False]
                n2 = False   
                pygame.quit()
                
    if to_run == False:
        break

    """""" #遊戲畫面

    score = 0
    oldscore = score
    font2 = pygame.font.SysFont("comicsansms", 15)   #score 

    CREATE_ENEMY_EVENT = pygame.USEREVENT
    CREATE_COCONUT_EVENT = pygame.USEREVENT + 1

    # Initialize player
    # player = Player(300, 410, 591//9, 261//4)
    
    player_list = []
    # target_player = []  #敵方目標清單
    for i in range(len(player_selection)):
        player_list.append(Player(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 591//9, 261//4, player_selection[i]))  #新增player_selection[i]，區別兩隻角色
        # target_player.append(i)
    # Initialize enemy
    N = 1
    enemy_list = []
    enemy_nest = [(272,272),(720,656)]
    enemy_spawn_x, enemy_spawn_y= random.choice(enemy_nest)
    for i in range(N):
        enemy_list.append(Enemy(enemy_spawn_x, enemy_spawn_y, 576//9, 256//4, oldscore))
        # enemy_list[i].target = random.randrange(0, len(player_list), 1)
        enemy_list[i].target = random.choice(player_list)

    coconut_list = []
    coconut_list.append(Coconut(222, 222))
    #bg = pygame.image.load('./materials/bg.jpg')
    #bg.convert()
    map = TiledMap('./materials/Level 1.tmx')
    map_img = map.draw()
    clear_map = map_img.copy() 
    camera = Camera(win_width, win_height)


    obstacle_list = []
    proof_list = []
    stone = Obstacle(896,896,64,64) # generate this to use obstacle.function
    tree = Proof(896,896,64,64) # generate this to use Proof.function
    for tile_object in map.tmxdata.objects:
        if tile_object.name == 'stone':
            obstacle_list.append(Obstacle(tile_object.x, tile_object.y, 64, 64))
        elif tile_object.name == 'block':
            pass
        elif tile_object.name == 'proof':
            proof_list.append(Proof(tile_object.x, tile_object.y, 64, 64))
  
    """
    All the events happen on the map_img surface
    then we use camera.show surface to track the movements of player
    last, win.blit(camera.show, (0,0))
    """
    def redrawGameWindow(win, map_img, camera):
        #win.blit(bg, (0, 0))
        map_img.blit(clear_map, (0,0))

        for coconut in coconut_list:
            coconut.draw(map_img)

        for player in player_list:
            player.draw(map_img)
            if player.health > 0:  #生命歸零時不畫出角色血量 
                health_bg1 = pygame.Surface((40,5))  #血條大小
                health_bg1.convert()
                health_bg1.fill((255,0,0))
                map_img.blit(health_bg1, (player.x+10, player.y))
                health_bg2 = pygame.Surface((int(40*player.health/player.healthmax),5))  #血條大小
                health_bg2.convert()
                health_bg2.fill((0,255,0))
                map_img.blit(health_bg2, (player.x+10, player.y))
                #win.blit(health_bg, (player.x+10, player.y))
                #pygame.draw.rect(health_bg, (0,255,0), [0,0,100,100], 20)   #打不出來...
                #pygame.draw.circle(health_bg,(0,255,0),(30,30),20,0)
                
                if len(player.status) == 1:
                    player_status = player.status[0]
                else:
                    player_status = player.status[0]
                    for i in range(1,len(player.status)):
                        player_status += "+%s" %player.status[i]
               
                global text3, ps, text3s, pss
                if player.name == "1P":    #畫出角色編號(1P or 2P)
                    img = pygame.image.load('./materials/1P.png')
                    text3 = font2.render(f"{player.name}:{player.weapon}/{player_status}", True, (255,255,255), (0,0,0))  #畫出武器
                    ps = (90,0)

                    #text4 = font2.render(f"{player.name}:{str(player.weapon_list)}", True, (255,255,255), (0,0,0))
                    #ps2 = (0,40)  
                        
                elif player.name == "2P":                   
                    img = pygame.image.load('./materials/2P.png')
                    text3s = font2.render(f"{player.name}:{player.weapon}/{player_status}", True, (255,255,255), (0,0,0))  #畫出武器
                    pss = (90, 20)   

                map_img.blit(img,(player.x+20, player.y+60))
                win.blit(text3, ps)

                #win.blit(text4, ps2)
                
                  
                
            for bullet in player.bullet_list:
                bullet.draw(map_img)
            # print(player.explode_list)
            for explosion in player.explode_list:
                explosion.draw(map_img)
                if explosion.remove == True:
                    player.explode_list.pop(player.explode_list.index(explosion))
        
        for enemy in enemy_list:
            enemy.draw(map_img)
        
        status = pygame.Surface((win_width, 45))  #the status row on top
        status.convert()
        status.fill((0,0,0))
        camera.show.blit(status,(0, 0))
        text2 = font2.render("score:%d" %score, True,(255,255,255), (0,0,0))  #畫出分數
        
        if len(enemy_list)<25:
            text4 = font2.render("enemy:%d/30" %len(enemy_list), True,(255,255,255), (0,0,0))  #畫出敵人數
            text4_1 = font2.render("" , True,(255,255,255), (0,0,0))  #畫出敵人數     
            #camera.show.blit(text4, (win_width-text4.get_width(), 0))
        else:
            text4 = font2.render("enemy:%d/30" %len(enemy_list), True,(255,255,255), (0,0,0))  #畫出敵人數
            font4_1 = pygame.font.SysFont("comicsansms", 40) 
            text4_1 = font4_1.render("warn!!!" , True,(255,0,0), (0,0,0))  #警告            
        
        #print(text4.get_width())
        # first track the position, then showing on the camera.show surface 
        camera.update(player_list)
        camera.show.blit(map_img, camera.tracking)
        # remember that these text are always on the window --> camera.show surface
        # and be careful with the concept of layer
        camera.show.blit(text2, (0, 0))
        camera.show.blit(text4, (win_width-text4.get_width(), 0))      #畫出敵人數
        camera.show.blit(text4_1, (win_width-text4_1.get_width(), 20)) #警告
        camera.show.blit(text3, ps)

        if len(player_selection) == 2:
            camera.show.blit(text3s,pss)

        win.blit(camera.show, (0,0)) 
        

        pygame.display.update()


    def checkPlayerEnemyCollision(player):
        global cold_time, score   # 受傷冷卻時間和分數
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
                if player.is_super_man == False:
                    if player.cold_time > 130: # 受傷冷卻時間
                        player.cold_time = 0 # 重新計時
                        player.hit()
                elif player.is_super_man == True:
                    enemy_list.pop(enemy_list.index(enemy))
                    score += 1 # 撞死敵人後分數加1
                    
    
    def checkPlayerCoconutCollision(player, enemy_list):
        player_hb_0 = player.hitbox[0]
        player_hb_1 = player.hitbox[1]
        player_hb_2 = player.hitbox[2]
        player_hb_3 = player.hitbox[3]
        for coconut in coconut_list:
            coconut_hb_0 = coconut.hitbox[0]
            coconut_hb_1 = coconut.hitbox[1]
            coconut_hb_2 = coconut.hitbox[2]
            coconut_hb_3 = coconut.hitbox[3]
            if not coconut.ignited and player_hb_1 + player_hb_3 > coconut_hb_1 and player_hb_1 < coconut_hb_1 + coconut_hb_3 and player_hb_0 + player_hb_2 > coconut_hb_0 and player_hb_0 < coconut_hb_0 + coconut_hb_2:
                coconut.create_surprise(player, enemy_list)
                


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
            #if collision == False:
                # if first.target not in target_player:
                #     first.target = choice(target_player)
            if first.target not in player_list:
                first.target = choice(player_list)
            if len(player_list) != 0:
                # first.chase(player_list[first.target])
                first.chase(first.target)

    def playerUpdate(player_list):
        for player in player_list:
            if player.shootAvailabe == False:
                player.shootLoop += 1
            if player.switchAvailabe == False:
                player.switchLoop += 1 
            if player.shootLoop >= player.shootCoolDown:
                player.shootLoop = 0
                player.shootAvailabe = True
            if player.switchLoop >= player.switchCoolDown:
                player.switchLoop =0 
                player.switchAvailabe = True
            player.cold_time += 1 # 計算受傷冷卻時間
            # if player.is_enlarged:
            #     player.enlarge()
            # elif not player.is_enlarged:
            #     player.medium()
    def coconutUpdate(coconut_list, enemy_list):
        for coconut in coconut_list:
            if coconut.ignited == True:
                #print(coconut.surprise)
                coconut.update_surprise(enemy_list)
                #print(coconut.surprise_count , coconut.SURPRISE_TIME_TICK)
                if coconut.surprise_count > coconut.SURPRISE_TIME_TICK:
                    coconut.remove_surprise(enemy_list)
                    coconut_list.pop(coconut_list.index(coconut))

    p_time = 0  #暫停按下次數
    p_cool = 0  #暫停冷卻時間
    pause = False
    level = 1
    
    while run[0]:
        # print(player_list)
        # print(target_player)
        # for player in player_list:
            # print(id(player.walk_sheet[0]))
        clock.tick(60) # Set FPS
        if score<100 and score-oldscore>=10:
            oldscore = score
        # Pygame event control, including (1) check running status, (2) appending enemy in a specific time period
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                to_run = False
                n1 = False
                n1_set = False
                run = [False]
                n2 = False   
                break
                pygame.quit()
            elif event.type == CREATE_ENEMY_EVENT and pause == False:
                # This will create enemy every 1-score*5/1000 sec
                enemy_spawn_x, enemy_spawn_y= random.choice(enemy_nest)
                enemy_list.append(Enemy( enemy_spawn_x, enemy_spawn_y, 576//9, 256//4, oldscore))                
                enemy_list[-1].target = choice(player_list)
                # enemy_list[-1].target = random.randrange(0, len(player_list), 1)
            elif event.type == CREATE_COCONUT_EVENT and pause == False:
                coconut_list.append(Coconut(random.randrange(64, map_width-64, 1), random.randrange(64, map_height-64, 1)))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p] and p_time%2 == 0 and p_cool>60:
                p_time+=1
                p_cool = 0
                print(p_time)
                pause = True
            elif keys[pygame.K_p] and p_time%2 == 1 and p_cool>60:
                p_time+=1
                p_cool = 0
                pause = False
        p_cool += 1
        if pause == False:        
            if len(player_list) == 0: # 如果沒有目標 退出遊戲
                run[0] = False
                pygame.time.wait(1000) # 短暫暫停
                break

            # Update enemy
            checkEnemyEnemyCollision()
            for enemy in enemy_list:
                stone.checkEnemyStoneCollision(enemy, obstacle_list)
            
            # Moving the player with "WASD"
            for i, player in enumerate(player_list):
                # print(player.shootLoop)
                checkPlayerEnemyCollision(player)
                checkPlayerCoconutCollision(player, enemy_list)
                stone.checkPlayerStoneCollision(player, obstacle_list)
                
                if len(enemy_list)>=30:
                    player.health = 0                    

                if (player.health <= 0):
                #  and i in target_player: # 生命歸零時 移出目標清單
                    player_list.pop(player_list.index(player))
                    # target_player.remove(i)
                    player_status = "dead"
                    if player.name == "1P":
                        text3 = font2.render(f"{player.name}:{player_status}", True, (255,255,255), (0,0,0)) 
                    else:
                        text3s = font2.render(f"{player.name}:{player_status}", True, (255,255,255), (0,0,0)) 
                    #if len(player_list) == 2:
                        #player_list.remove(player) 

                player.control(run, map_width, map_height, player.name)
                for bullet in player.bullet_list:
                    bullet.fly() 
                    if bullet.out(map_width, map_height): 
                        player.bullet_list.pop(player.bullet_list.index(bullet))
                        continue
                    if tree.checkBulletProofCollision(bullet, proof_list) == True:
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
                # player.cold_time += 1 # 計算受傷冷卻時間

            # print(len(player_list))
                # print(len(player.bullet_list))
            # checkEnemyEnemyCollision()
            playerUpdate(player_list)
            coconutUpdate(coconut_list, enemy_list)
            camera.update(player_list)
            redrawGameWindow(win, map_img, camera)
    """"""  #處理分數
    with open('./score.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(score), str(datetime.today())[:19]])        
    df = pd.read_csv('./score.csv')  
    select_df = pd.DataFrame(df.sort_values(by=['score']))
    score_list = select_df["score"].values.tolist()
    score_lists = [x for x in score_list if str(x) != 'nan']
    time_list = select_df["time"].values.tolist()
    time_lists = [x for x in time_list if str(x) != 'nan']
    s = score_lists[::-1]
    t = time_lists[::-1]
    with open('./score.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['score', 'time'])
        writer.writerow(["", ""])
        for i in range(min(10,len(s))):
            writer.writerow([s[i],t[i]])
    """"""  #結束畫面
    bg_over = pygame.image.load('./materials/overphoto.png')
    bg_over.convert()
    bg_score = pygame.image.load('./materials/score.png')
    bg_score.convert()

    n2_score = False
    while n2:        
        clock.tick(30)
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        if n2_score == False:    
            win.blit(bg_over, (0, 0))
            font3 = pygame.font.SysFont("comicsansms", 25)
            text3 = font3.render("GameOver", True, (0,0,0),(255,255,255))  #GameOver文字
            win.blit(text3, (int(win_width/2-60), int(win_height/2 +50)))   #
            text4 = font3.render("score: %d" %score, True, (0,0,0),(255,255,255))  #score文字
            win.blit(text4, (int(win_width/2-50), int(win_height/2+90)))
            
            button1 = Button(int(win_width/7*0.5), int(win_height/7*5.5), "AGAIN")
            button2 = Button(int(win_width/7*2.8), int(win_height/7*5.5), "SCORE")
            button3 = Button(int(win_width/7*5), int(win_height/7*5.5), "QUIT")
            button4 = Button(0, 0, "BACK")
            win.blit(button1.off, button1.ps)
            win.blit(button2.off, button2.ps)
            win.blit(button3.off, button3.ps)
            win.blit(button4.off, button4.ps)
            
            if button1.range(x1,y1):
                win.blit(button1.on, button1.ps)
                if buttons[0]: # 若按下 進入                
                    break
            if button2.range(x1,y1):
                win.blit(button2.on, button2.ps)
                if buttons[0]:                
                    print("score")
                    n2_score = True
                    continue           
            if button3.range(x1,y1):
                win.blit(button3.on, button3.ps)
                if buttons[0]: # 若按下 退出
                    to_run = False
                    break
            if button4.range(x1,y1):
                win.blit(button4.on, button4.ps)
                if buttons[0]: # 若按下 退出
                    n1 = True
                    break                       
            pygame.display.update()

        else:   #score     
            win.blit(bg_score,(0,0))
            font3 = pygame.font.SysFont("simhei",25)  #配合字體大小 用simhei
            df = pd.read_csv('./score.csv')  
            select_df = pd.DataFrame(df)
            s = str(select_df[1:11]).split("\n")
            for i in range(len(s)):
                text3 = font3.render(s[i], True, (0,0,0),(100,200,200))  
                win.blit(text3, (int(win_width/10), int(win_height/7*1+i*25)))
                       
            button1 = Button(int(win_width/7*2), int(win_height/7*5+90), "BACK")       
            button2 = Button(int(win_width/7*4), int(win_height/7*5+90), "CLEAR") 
            win.blit(button1.off, button1.ps)  
            win.blit(button2.off, button2.ps)     
            if button1.range(x1,y1):
                win.blit(button1.on, button1.ps)
                if buttons[0]:  #若按下 進入
                    print("BACK")
                    n2_score = False
            if button2.range(x1,y1):
                win.blit(button2.on, button2.ps)
                if buttons[0]:  #若按下 進入
                    print("clear")
                    with open('./score.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['score', 'time'])
                        writer.writerow(["", ""])
  
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting")
                to_run = False
                n1 = False
                n1_set = False
                run = [False]
                n2 = False   
                pygame.quit()
            
    if to_run == False:
        break
        
pygame.quit()