import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect，または，爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def check_direct(obj_direct:list) -> list[bool, bool]:
    """
    移動する方向からこうか㌧の向いている方向を決定する関数
    引数：こうか㌧が移動する値のリスト
    戻り値：反転するか、方向
    """
    dir = [0, 0]
    if obj_direct[0]==5 and obj_direct[1]==5:
        dir = [1,1]
    if obj_direct[0]==5 and obj_direct[1]==0:
        dir = [1,0]
    if obj_direct[0]==5 and obj_direct[1]==-5:
        dir = [1,7]
    if obj_direct[0]==0 and obj_direct[1]==-5:
        dir = [1,6]
    if obj_direct[0]==-5 and obj_direct[1]==-5:
        dir = [0,7]
    if obj_direct[0]==-5 and obj_direct[1]==0:
        dir = [0,0]
    if obj_direct[0]==-5 and obj_direct[1]==5:
        dir = [0,1]
    if obj_direct[0]==0 and obj_direct[1]==5:
        dir = [1,2]
    return dir


def end():
    """
    ゲームオーバーになった時の処理を行う関数
    未完成なので以下略です
    """ 
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    screen.fill((0, 0, 0))
    bg_img.set_alpha(128)
    screen.blit(bg_img)
    print("Game Over")
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center = [WIDTH/2, HEIGHT/2])
    screen.blit(txt, txt_rct)
    
    pg.display.update()
    time.sleep(5)
    return


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #ここからこうかとん
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    kk_direct = 0   
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), kk_direct, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    #ここから爆弾
    bomb_size = 10
    bomb_img = pg.Surface((bomb_size*2, bomb_size*2))
    bomb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_img, (255, 0, 0), (bomb_size, bomb_size), bomb_size)
    bomb_rct = bomb_img.get_rect()
    bomb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    vx, vy = 5, 5
    direct = [0, 45, 90, 135, 180, 225, 270, 315]
    saccs = [a for a in range(1, 11)]
    

    clock = pg.time.Clock()
    tmr = 0
    move_dic = {  #移動量辞書
        pg.K_w:(0, -5), 
        pg.K_s:(0, 5), 
        pg.K_a:(-5, 0), 
        pg.K_d:(5, 0)
    }
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            


        if kk_rct.colliderect(bomb_rct):  # こうか㌧がぶつかったら

            end()
            return
        


        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in move_dic.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_direct = direct[check_direct(sum_mv)[1]]
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), kk_direct, 2.0)
        if check_direct(sum_mv)[0] == 1:
            kk_img = pg.transform.flip(kk_img,True,False)
        screen.blit(kk_img, kk_rct)
        #爆弾の処理
        bomb_img = pg.Surface((bomb_size*2, bomb_size*2))
        pg.draw.circle(bomb_img, (255, 0, 0), (bomb_size, bomb_size), bomb_size)
        bomb_img.set_colorkey((0, 0, 0))
        bomb_rct.move_ip(vx,vy)
        screen.blit(bomb_img,bomb_rct)
        yoko, tate = check_bound(bomb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
