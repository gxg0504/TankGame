import pygame, sys
from pygame.locals import *  # 全局常量

# 初始化
pygame.init()

# 屏幕对象
screen = pygame.display.set_mode((400, 270))  # 尺寸

# Surface对象
surf = pygame.Surface((50, 50))  # 长、宽
surf.fill((255, 255, 255))  # 颜色

# Surface对象的矩形区域
rect = surf.get_rect()

# 窗口主循环
while True:
    # 遍历事件队列
    for event in pygame.event.get():
        if event.type == QUIT:  # 点击右上角的'X'，终止主循环
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # 按下'ESC'键，终止主循环
                pygame.quit()
                sys.exit()

                # 放置Surface对象
    screen.blit(surf, ((400 - 50) // 2, (270 - 50) // 2))  # 窗口正中
    # screen.blit(surf, rect)                      # surf的左上角

    # 重绘界面
    pygame.display.flip()