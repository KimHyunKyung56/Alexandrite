import pygame
import sys
  
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = (255,255,0)
darkgreen = (0,80,80)
lightgray = (220,220,220)




Alexandrite=pygame.image.load('main_char.png')
pygame.display.set_icon(Alexandrite)

#음악 추가
# pygame.mixer.init()
# pygame.mixer.music.load('alexandrite_bg.mp3')
# pygame.mixer.music.play(-1, 0.0)


# 플레이어 컨트롤
class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, color):
        pygame.sprite.Sprite.__init__(self)
  
        # 벽 만들기
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# 벽 생성
def setupRoomOne(all_sprites_list):
    wall_list=pygame.sprite.RenderPlain()
     
    # 벽 리스트
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # 리스트 반복. 벽 만들고 리스트에 추가
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],darkgreen)
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    return wall_list

def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,darkgreen))
      all_sprites_list.add(gate)
      return gate

# 보석 클래스      
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
 
        # 보석 이미지 파일 생성
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('alexandrite2.png')
 
        # 직사각형 객체 가져오기
        self.rect = self.image.get_rect() 

# 플레이어 조작
class Player(pygame.sprite.Sprite):
  
    #속도 지정
    change_x=0
    change_y=0
  
    def __init__(self,x,y, filename):
        pygame.sprite.Sprite.__init__(self)
   
        self.image = pygame.image.load(filename).convert_alpha()
  
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # 속도 초기화
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # 속도 변경
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    def update(self,walls,gate):
        # 전의 위치 가져오기
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # 벽 부딛쳤는지 확인하기
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # 벽과 충돌 시 전의 위치로 이동 
            self.rect.left=old_x
        else:

            self.rect.top = new_y

            # 벽 부딛쳤는지 확인하기
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # 벽과 충돌 시 전의 위치로 이동
                self.rect.top=old_y

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y

class Enemy(Player):
    # 적의 속도
    def changespeed(self,list,enemy,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif enemy == "ememy4":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]

Enemy1_directions = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Enemy2_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Enemy3_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Enemy4_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pl = len(Enemy1_directions)-1
bl = len(Enemy2_directions)-1
il = len(Enemy3_directions)-1
cl = len(Enemy4_directions)-1

pygame.init()

#화면 크기
screen = pygame.display.set_mode([606, 606])


#제목
pygame.display.set_caption('Alexandrite')

# 백그라운드 지면 생성
background = pygame.Surface(screen.get_size())

bg_img = pygame.image.load('last_bg.png')
bg_img = pygame.transform.scale(bg_img ,(606,606))

#시간 지연
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

#캐릭터들 기본 위치
w = 303-16 #가로
ch_h = (7*60)+19 #캐릭터 높이
e1_h = (4*60)+19 #Enemy1 높이
e2_h = (3*60)+19 #Enemy2 높이
e3_w = 303-16-32 #Enemy3 가로
e4_w = 303+(32-16) #Enemy4 가로

def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monster_list = pygame.sprite.RenderPlain()

  Ch_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)


  e1_turn = 0
  e1_steps = 0

  e2_turn = 0
  e2_steps = 0

  e3_turn = 0
  e3_steps = 0

  e4_turn = 0
  e4_steps = 0


  # 이미지 삽입 리스트에 추가
  Ch = Player( w, ch_h, "main_char.png" )
  all_sprites_list.add(Ch)
  Ch_collide.add(Ch)
   
  Enemy2=Enemy( w, e2_h, "monster1.png" )
  monster_list.add(Enemy2)
  all_sprites_list.add(Enemy2)

  Enemy1=Enemy( w, e1_h, "monster2.png" )
  monster_list.add(Enemy1)
  all_sprites_list.add(Enemy1)
   
  Enemy3=Enemy( e3_w, e1_h, "monster3.png" )
  monster_list.add(Enemy3)
  all_sprites_list.add(Enemy3)
   
  Enemy4=Enemy( e4_w, e1_h, "monster4.png" )
  monster_list.add(Enemy4)
  all_sprites_list.add(Enemy4)

  # 보석 그리기
  for row in range(19):  #가로
      for column in range(19):  #세로
          if ( row == 1 or row == 2 or row == 3 or row == 4 or row == 5 or row == 6 or row == 7 or row == 8
          or row==9 or row==10 or row ==11 or row==12 or row == 13 or row ==14 or row == 15 or row == 16 
          or row == 17) or (  column ==1 or column == 2 or column == 3 or column == 4 or column ==5 or column == 6 
          or column ==7 or column == 8 or column == 9 or column == 10 or column ==11 or column ==12 or column ==13
          or column ==14 or column ==15 or column ==16 or column == 17 ):
              continue
          else:
            block = Block(red, 11, 18)

            # 보석 임의 위치 설정
            block.rect.x = (30*column-6)+26
            block.rect.y = (30*row-6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, Ch_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # 리스트에 보석 추가
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  jewel = 0

  done = False

  i = 0

  while done == False:
      # 이동
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Ch.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Ch.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Ch.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Ch.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Ch.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Ch.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Ch.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Ch.changespeed(0,-30)
          
   
      # 적의 움직임
      Ch.update(wall_list,gate)

      returned = Enemy1.changespeed(Enemy1_directions,False,e1_turn,e1_steps,pl)
      e1_turn = returned[0]
      e1_steps = returned[1]
      Enemy1.changespeed(Enemy1_directions,False,e1_turn,e1_steps,pl)
      Enemy1.update(wall_list,False)

      returned = Enemy2.changespeed(Enemy2_directions,False,e2_turn,e2_steps,bl)
      e2_turn = returned[0]
      e2_steps = returned[1]
      Enemy2.changespeed(Enemy2_directions,False,e2_turn,e2_steps,bl)
      Enemy2.update(wall_list,False)

      returned = Enemy3.changespeed(Enemy3_directions,False,e3_turn,e3_steps,il)
      e3_turn = returned[0]
      e3_steps = returned[1]
      Enemy3.changespeed(Enemy3_directions,False,e3_turn,e3_steps,il)
      Enemy3.update(wall_list,False)

      returned = Enemy4.changespeed(Enemy4_directions,"ememy4",e4_turn,e4_steps,cl)
      e4_turn = returned[0]
      e4_steps = returned[1]
      Enemy4.changespeed(Enemy4_directions,"ememy4",e4_turn,e4_steps,cl)
      Enemy4.update(wall_list,False)

      # 캐릭터 벽 또는 적과 부딛쳤는지 확인
      blocks_hit_list = pygame.sprite.spritecollide(Ch, block_list, True)
       
      # 점수
      if len(blocks_hit_list) > 0:
          jewel +=len(blocks_hit_list)
      
      
      screen.fill(black)

      screen.blit(bg_img, (0, 0))
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monster_list.draw(screen)

      text=font.render("Jewel: "+str(jewel)+"/"+str(bll), True, white)
      screen.blit(text, [10, 10])

      if jewel == bll:
        doNext("Game Win!",235,all_sprites_list,block_list,monster_list,Ch_collide,wall_list,gate)

      monster_hit_list = pygame.sprite.spritecollide(Ch, monster_list, False)

      if monster_hit_list:
        doNext("Game Over",235,all_sprites_list,block_list,monster_list,Ch_collide,wall_list,gate)

      
      pygame.display.flip()
    
      clock.tick(10)

def doNext(message,left,all_sprites_list,block_list,monster_list,Ch_collide,wall_list,gate):
  while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monster_list
            del Ch_collide
            del wall_list
            del gate
            startGame()

      #게임 종료시 뜨는 배경
      w = pygame.Surface((500,300)) 
      w = pygame.image.load('box3.png')
      w = pygame.transform.scale(w ,(500,300))
      
      w.set_alpha(100)        #서서히 등장효과        
      # w.fill((0,0,0))         
      screen.blit(w, (50,150))    

      #이겼을때와 졌을때
      text1=font.render(message, True, lightgray)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, lightgray)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, lightgray)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
      return pygame.font.Font("Bettafield.otf", size)

def main_menu():
      while True:
            screen.blit(bg_img, (0,0))
            
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            
            MENU_TEXT = get_font(80).render("ALEXANDRITE", True, lightgray)
            MENU_RECT = MENU_TEXT.get_rect(center=(303, 100))
            
            PLAY_BUTTON = Button(image=pygame.image.load("buttonex3.png"), pos=(303, 250), text_input="START", font=get_font(60), base_color="#d7fcd4", hovering_color="black")
            QUIT_BUTTON = Button(image=pygame.image.load("buttonex3.png"), pos=(303, 450), text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="black")
            
            screen.blit(MENU_TEXT, MENU_RECT)
            
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                  button.changeColor(MENU_MOUSE_POS)
                  button.update(screen)
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                              startGame()
                        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                              pygame.quit()
                              sys.exit()
            pygame.display.update()

main_menu()

pygame.quit()