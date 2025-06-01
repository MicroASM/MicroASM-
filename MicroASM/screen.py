import numpy as np
import pygame
import time
from multiprocessing import shared_memory

# Output buffer memory layout (memory[384–511] → shm.buf[0–127])
R_ADDR = 0
G_ADDR = 1
B_ADDR = 2
X_ADDR = 3
Y_ADDR = 4
SET_ADDR = 5
FLIP_ADDR = 6

SHM_NAME = 'MicroASMsharedmemory_main_output_abv'

# Setup
pygame.init()
screen = pygame.display.set_mode((256, 256))
surface = pygame.Surface((256, 256))
image = np.zeros((256, 256, 3), dtype=np.uint8)

# Shared memory
shm = shared_memory.SharedMemory(name=SHM_NAME)
mem = shm.buf[:128]

last_set = -1

running = True
while running:
    mem = shm.buf[:128]
    r = mem[R_ADDR]
    g = mem[G_ADDR]
    b = mem[B_ADDR]
    x = mem[X_ADDR]
    y = mem[Y_ADDR]
    set_val = mem[SET_ADDR]
    print(r,g,b,x,y,set_val)
    # If SET changed, write pixel
    if set_val != last_set:
        if 0 <= x < 256 and 0 <= y < 256:
            image[y, x] = [r, g, b]
        last_set = set_val

    # Always refresh screen
    pygame.surfarray.blit_array(surface, image)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
shm.close()
