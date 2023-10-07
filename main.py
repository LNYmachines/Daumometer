import pygame
import math
from flask import Flask, request, abort
app = Flask(__name__)
import threading
pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

def get_angle_from_percentage(percentage):
    angle =  180 + percentage * 180 / 100 
    return angle 


def blitRotate(surf, image, pos, originPos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)


def blitRotate2(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    #pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)


image = pygame.image.load('thumb.png')
target = 180

    #image.blit(text, (1, 1))
w, h = image.get_size()
gauge = pygame.image.load("gauge.jpg")
angle = -180
mass = 1
damping = 0.1
spring = 0.5
target_angle = 0
start_angle = 0

def dynamic_anlge(target_angle, start_angle, t, damping):
    new_angle = target_angle + math.exp(-0.3* t * damping) * 0.5* (target_angle -start_angle) *  math.cos(3*t)
    return new_angle

done = False
t=0

my_thread = threading.Thread(target=app.run, args=["0.0.0.0"], daemon=True)
my_thread.start()

@app.route("/percentage")
def get_percentage():
    global target_angle
    global damping
    global t
    percentage = request.args.get("percentage")
    print(percentage)
    try:
        percentage_float = float(percentage)
        target_angle = get_angle_from_percentage(percentage_float)
        damping = 1
        t=0
    except TypeError:

        abort(400)
    return "ok"

while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                t = 0
                damping = 0
                target_angle = 360
                start_angle = 0
            if event.key == pygame.K_DOWN:
                print("pressed up")
                target_angle = 180
                start_angle = -180
                damping = 1
                t=0
            if event.key == pygame.K_UP:
                print("pressed up")
                target_angle = 360
                start_angle = -0
                damping = 1
                t=0
            if event.key == pygame.K_LEFT:
                target_angle = 270
                start_angle = -0
                damping = 1
                t=0
            if event.key == pygame.K_RIGHT:
                target_angle = 90
                start_angle = -0
                damping = 1
                t=0



    pos = (screen.get_width() / 2, screen.get_height() / 2)

    screen.fill(0)
    screen.blit(gauge, (0, 0))
    blitRotate(screen, image, pos, (w / 2, h / 2), angle)
    # blitRotate2(screen, image, pos, angle)
    angle = dynamic_anlge(target_angle, start_angle=start_angle, t=t, damping=damping)

    # pygame.draw.line(screen, (0, 255, 0), (pos[0] - 20, pos[1]), (pos[0] + 20, pos[1]), 3)
    # pygame.draw.line(screen, (0, 255, 0), (pos[0], pos[1] - 20), (pos[0], pos[1] + 20), 3)
    # pygame.draw.circle(screen, (0, 255, 0), pos, 7, 0)
    t += 0.06
    pygame.display.flip()

pygame.quit()
exit()