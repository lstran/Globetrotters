#!/usr/bin/env python


import pygame
import sys
import math

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def is_long(val):
    try:
        int(round(float(val)))
    except (ValueError, TypeError) as e:
        return False
    return True

def control(command, state, prevDestination):
    nextState = state
    if is_long(command):
        destination = float(command)
        if math.floor(destination) % 3 == 0:
            destination = int(math.floor(destination))
        elif math.ceil(destination) % 3 == 0:
            destination = int(math.ceil(destination))
        elif round(destination) + 1 % 3 == 0:
            destination = int(round(destination) + 1)
        else:
            destination = int(round(destination) - 1)

        if destination < 0 and destination > -180:
            destination =  (0 - destination)/3
            nextState = 'rotateToDestination'
        elif destination >= 0 and destination < 181:
            destination = (360 - destination)/3
            nextState = 'rotateToDestination'
        else:
            destination = prevDestination

    else:
        cmdStr = str(command).lower()
        destination = prevDestination
        if cmdStr == 'stop':
            nextState = 'stop'
        elif cmdStr == 'left' or cmdStr == 'west':
            nextState = 'sRotateCW'
        elif cmdStr == 'right' or cmdStr == 'east':
            nextState = 'idle'
        elif cmdStr == 'fast':
            if state == 'idle':
                nextState = 'fRotateCCW'
            elif state == 'sRotateCW':
                nextState = 'fRotateCW'
        elif cmdStr == 'slow':
            if state == 'fRotateCCW' or state == 'ffRotateCCW':
                nextState = 'idle'
            elif state == 'fRotateCW' or state == 'ffRotateCW':
                nextState = 'sRotateCW'
        elif cmdStr == 'faster':
            if state == 'idle':
                nextState = 'fRotateCCW'
            elif state == 'fRotateCCW':
                nextState = 'ffRotateCCW'
            elif state == 'sRotateCW':
                nextState = 'fRotateCW'
            elif state == 'fRotateCW':
                nextState = 'ffRotateCW'
        elif cmdStr == 'slower':
            if state == 'ffRotateCCW':
                nextState = 'fRotateCCW'
            elif state == 'fRotateCCW':
                nextState = 'sRotateCCW'
            elif state == 'ffRotateCW':
                nextState = 'fRotateCW'
            elif state == 'fRotateCW':
                nextState = 'sRotateCW'
    return (nextState, destination)



pygame.init()
screen = pygame.display.set_mode((900,900))
done = False
clock = pygame.time.Clock()

origCenter = screen.get_rect().center
charImage = pygame.image.load('globe1.jpg')
charImage = pygame.transform.scale(charImage, screen.get_size())
charImage = charImage.convert()
screen_rect = screen.get_rect()
image_rect = charImage.get_rect()
image_rect.center = screen_rect.center
displayImage = pygame.transform.rotate(charImage, 0)
degree = 0

state = 'idle'
destination = 0

imageList = []
for i in xrange(120):
    imageList.append(rot_center(charImage, i*3))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    try:
        with open('commands', 'r+') as commandFile:
            command = commandFile.readline()
            if len(command) > 0:
                newState = control(command, state, destination)
                state = newState[0]
                destination = newState[1]
            commandFile.seek(0)
            commandFile.truncate()
    except IOError:
        pass


    ##############################################
    # Idle state keeps rotating counter clockwise
    if state == 'idle':
        degree += 1
        if degree > 119:
            degree = 0
        displayImage = imageList[degree]

    ######################################
    # sRotateCW rotates clockwise slowly
    elif state == 'sRotateCW':
        degree -= 1
        if degree < 0:
            degree = 119
        displayImage = imageList[degree]

    #####################################
    # fRotateCCW rotates counter clockwise fast
    elif state == 'fRotateCCW':
        degree += 2
        if degree > 119:
            degree = 0
        displayImage = imageList[degree]

    ####################################
    # fRotateCW rotates clockwise fast
    elif state == 'fRotateCW':
        degree -= 2
        if degree < 0:
            degree = 119
        displayImage = imageList[degree]

    ###################################
    #  ffRotateCCW rotates counter clockwise very fast
    elif state == 'ffRotateCCW':
        degree += 3
        if degree > 119:
            degree = 0
        displayImage = imageList[degree]

    ###################################
    # ffRotateCW rotates clockwise very fast
    elif state == 'ffRotateCW':
        degree -= 3
        if degree < 0:
            degree = 119
        displayImage = imageList[degree]

    ##################################
    # rotateToDestination takes shortest path to rotate towards a certain degree
    elif state == 'rotateToDestination':
        if degree == destination:
            state = 'stop'
        elif destination - degree < (180 + degree) - destination:
            degree += 1
            if degree > 119:
                degree = 0
            displayImage = imageList[degree]
        else:
            degree -= 1
            if degree < 0:
                degree = 119
            displayImage = imageList[degree]





    screen.fill((255,255,255))
    #screen.blit(image, (20,20))


    screen.blit(displayImage, (0,0))

    pygame.display.flip()
    clock.tick(60)
    #print clock.get_fps()


