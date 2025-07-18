import pygame
import sys

# 全局状态
_window = None
_screen = None
_clock = None
_key_state = set()
_quit = False
_update_func = None
_key_func = None

# 初始化窗口
def init(width=640, height=480, title="gameplus"):
    global _window, _screen, _clock, _key_state, _quit
    pygame.init()
    _window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    _screen = _window
    _clock = pygame.time.Clock()
    _key_state = set()
    _quit = False

# 事件驱动API
def on_update(func):
    global _update_func
    _update_func = func

def on_key(func):
    global _key_func
    _key_func = func

# 自动主循环
def run(width=640, height=480, title="gameplus", fps=60):
    init(width, height, title)
    global _quit
    while not _quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit = True
            elif event.type == pygame.KEYDOWN and _key_func:
                keyname = pygame.key.name(event.key)
                _key_func(keyname)
        if _update_func:
            _update_func()
        pygame.display.flip()
        _clock.tick(fps)

# 清屏
def clear(color=(0,0,0)):
    if _screen is None:
        return
    if isinstance(color, str):
        color = {
            'black': (0,0,0), 'white': (255,255,255), 'red': (255,0,0),
            'green': (0,255,0), 'blue': (0,0,255), 'yellow': (255,255,0),
            'gray': (128,128,128), 'grey': (128,128,128)
        }.get(color, (0,0,0))
    _screen.fill(color)

# 加载图片
def load_image(path):
    return pygame.image.load(path).convert_alpha()

# 绘制图片
def draw_image(img, x, y):
    if _screen is None:
        return
    _screen.blit(img, (x, y))

# 绘制矩形（简化名rect）
def draw_rect(x, y, w, h, color=(255,255,255), width=0):
    if _screen is None:
        return
    if isinstance(color, str):
        color = {
            'black': (0,0,0), 'white': (255,255,255), 'red': (255,0,0),
            'green': (0,255,0), 'blue': (0,0,255), 'yellow': (255,255,0),
            'gray': (128,128,128), 'grey': (128,128,128)
        }.get(color, (255,255,255))
    pygame.draw.rect(_screen, color, (x, y, w, h), width)

def rect(x, y, w, h, color=(255,255,255), width=0):
    draw_rect(x, y, w, h, color, width)

# 绘制圆
def draw_circle(x, y, r, color=(255,255,255), width=0):
    if _screen is None:
        return
    if isinstance(color, str):
        color = {
            'black': (0,0,0), 'white': (255,255,255), 'red': (255,0,0),
            'green': (0,255,0), 'blue': (0,0,255), 'yellow': (255,255,0),
            'gray': (128,128,128), 'grey': (128,128,128)
        }.get(color, (255,255,255))
    pygame.draw.circle(_screen, color, (x, y), r, width)

def circle(x, y, r, color=(255,255,255), width=0):
    draw_circle(x, y, r, color, width)

# 绘制线
def draw_line(x1, y1, x2, y2, color=(255,255,255), width=1):
    if _screen is None:
        return
    if isinstance(color, str):
        color = {
            'black': (0,0,0), 'white': (255,255,255), 'red': (255,0,0),
            'green': (0,255,0), 'blue': (0,0,255), 'yellow': (255,255,0),
            'gray': (128,128,128), 'grey': (128,128,128)
        }.get(color, (255,255,255))
    pygame.draw.line(_screen, color, (x1, y1), (x2, y2), width)

def line(x1, y1, x2, y2, color=(255,255,255), width=1):
    draw_line(x1, y1, x2, y2, color, width)

# 显示文本（简化名text）
def draw_text(text, x, y, size=24, color=(255,255,255)):
    if _screen is None:
        return
    if isinstance(color, str):
        color = {
            'black': (0,0,0), 'white': (255,255,255), 'red': (255,0,0),
            'green': (0,255,0), 'blue': (0,0,255), 'yellow': (255,255,0),
            'gray': (128,128,128), 'grey': (128,128,128)
        }.get(color, (255,255,255))
    font = pygame.font.SysFont(None, size)
    img = font.render(str(text), True, color)
    _screen.blit(img, (x, y))

def text(text, x, y, size=24, color=(255,255,255)):
    draw_text(text, x, y, size, color)

# 播放音效
def play_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.play()

# 键盘检测
def key_down(key):
    keys = pygame.key.get_pressed()
    keymap = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN,
        'space': pygame.K_SPACE, 'esc': pygame.K_ESCAPE, 'enter': pygame.K_RETURN
    }
    k = keymap.get(key, getattr(pygame, f'K_{key.upper()}', None))
    if k is not None:
        return keys[k]
    return False

# 鼠标检测
def mouse_pos():
    return pygame.mouse.get_pos()

def mouse_down():
    return pygame.mouse.get_pressed()[0]

# 帧率控制+刷新
def update(fps=60):
    if _clock is None:
        return
    pygame.display.flip()
    _clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global _quit
            _quit = True

# 退出检测
def quit():
    return _quit 