import pygame
import sys
pygame.init()


my_s = pygame.mixer.Sound("sound/bolt.wav")

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

my_s.play()