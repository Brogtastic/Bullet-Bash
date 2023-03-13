'''
Bullet Bash
Author: Michael Brogdon

TODO:
1.) Main Menu Art
2.) Music and Sound Effects
3.) Pause Screen Draw
4.) Controls Menu
5.) Auto-Aiming Choice
6.) SFX: Bullet Hit, Player Hurt, Player Dead
7.) Shift = speed or invincibility

'''

import pygame
import sys
import math
import random
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init(44100, -16, 2, 64)
pygame.init()
pygame.font.init()

size = width, height = 800, 600
display = pygame.display.set_mode(size)
pygame.display.set_caption('Bullet Bash')

backgroundColor = (26, 32, 64, 25)

class Game:
    def main(self, ammunition_init, ammunition1_init, score_init, health_init, enemy_track_init, player_x_init, player_y_init, ammo_track_init, health_kit_track_init, player_bullets_click_track_init, player_bullets_track_init, music_seconds_init):
        mixer.music.load('Gameplay.wav')
        mixer.music.play(-1, int(music_seconds_init)/1000.0)

        red_bullet_sound = mixer.Sound('red bullet.wav')
        red_bullet_sound.set_volume(0.2)
        yellow_bullet_sound = mixer.Sound('yellow bullet.wav')
        yellow_bullet_sound.set_volume(0.2)
        red_die_sound = mixer.Sound('red enemy die.wav')
        red_die_sound.set_volume(0.3)
        yellow_die_sound = mixer.Sound('yellow enemy die.wav')
        yellow_die_sound.set_volume(0.3)
        red_ammo_sound = mixer.Sound('red ammo pickup.wav')
        red_ammo_sound.set_volume(0.2)
        yellow_ammo_sound = mixer.Sound('yellow ammo pickup.wav')
        yellow_ammo_sound.set_volume(0.2)
        health_kit_sound = mixer.Sound('health kit pickup.wav')
        health_kit_sound.set_volume(0.3)

        size = width, height = 800, 600
        display = pygame.display.set_mode((size))
        pygame.display.set_caption('Bullet Bash')
        clock = pygame.time.Clock()
        timer = 0
        full_health = 100
        enemy_full_health = 6
        enemy_damage = 10
        ammo_plus = 4
        global score_to_add
        score_to_add = 0
        score = score_init
        enemy_colors = ["red", "yellow"]
        bullet_colors = ["red", "yellow"]
        enemy_track = enemy_track_init
        ammo_track = ammo_track_init
        player_bullets_click_track = player_bullets_click_track_init
        player_bullets_track = player_bullets_track_init
        health_kit_track = health_kit_track_init

        '''
        OG COLORS
        bulletColor = (119, 131, 166, 65)
        backgroundColor = (26, 32, 64, 25)
        playerColor = (119, 131, 166, 65)
        enemyColor = (166, 65, 65, 65)
        enemyColor2 = (166, 0, 0, 65)
        '''

        bulletColor = (245, 122, 113, 96)
        bulletColor2 = (245, 178, 64, 96)
        backgroundColor = (26, 32, 64, 25)
        playerColor = (60, 168, 166, 66)
        enemyColor = (168, 76, 69, 66)
        enemyColor2 = (168, 125, 52, 66)
        healthBarColor = playerColor
        healthBarBGColor = (50, 138, 178, 70)

        class Player:
            def __init__(self, x, y, width, height, full_health, player_color):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.speed = 6
                self.target_x = x
                self.target_y = y
                self.easing = 0.2
                self.timer = 0
                self.health = full_health
                self.color = "blue"
                self.dead = False

            def update(self, dt):
                dx = self.target_x - self.x
                dy = self.target_y - self.y

                self.x += dx * self.easing
                self.y += dy * self.easing

                if self.x < 0:
                    self.x = 0
                    self.target_x = self.x
                elif self.x > width - self.width:
                    self.x = width - self.width
                    self.target_x = self.x

                if self.y < 0:
                    self.y = 0
                    self.target_y = self.y
                elif self.y > height - self.height:
                    self.y = height - self.height
                    self.target_y = self.y

                player_rect = self.get_rect()
                self.timer -= 1

            def main(self, display):
                if((self.timer <= 0) or ((((self.timer % 2 == 0) and (self.timer < 20)) or (((self.timer % 3 == 0) and (self.timer > 20)))) and (self.timer > 0))) and (self.health > 0):
                    pygame.draw.rect(display, playerColor, (self.x, self.y, self.width, self.height))

            def get_rect(self):
                return pygame.Rect(self.x, self.y, self.width, self.height)

            def bullet_recoil_click(self, mouse_x, mouse_y, direction, factor):
                if((mouse_x > self.x) and (((mouse_y - self.y) >= 0) and (mouse_y - self.y) <= 50)):
                    direction = "right"
                if ((mouse_x < self.x) and (((mouse_y - self.y) >= 0) and (mouse_y - self.y) <= 50)):
                    direction = "left"
                if ((mouse_y < self.y) and (((mouse_x - self.x) >= 0) and (mouse_x - self.x) <= 30)):
                    direction = "up"
                if ((mouse_y > self.y) and (((mouse_x - self.x) >= 0) and (mouse_x - self.x) <= 30)):
                    direction = "down"
                if (((mouse_x - self.x) <= -30) and (mouse_y < self.y)):
                    direction = "upleft"
                if (((mouse_x - self.x) >= 30) and (mouse_y < self.y)):
                    direction = "upright"
                if (((mouse_x - self.x) <= -30) and ((mouse_y - self.y) >= 40)):
                    direction = "downleft"
                if (((mouse_x - self.x) >= 30) and ((mouse_y - self.y) >= 40)):
                    direction = "downright"

                if (direction == "left"):
                    self.target_x += self.speed * factor
                elif (direction == "right"):
                    self.target_x -= self.speed * factor
                elif (direction == "up"):
                    self.target_y += self.speed * factor
                elif (direction == "down"):
                    self.target_y -= self.speed * factor
                elif (direction == "upleft"):
                    self.target_y += self.speed * factor / 1.9
                    self.target_x += self.speed * factor / 1.9
                elif (direction == "upright"):
                    self.target_y += self.speed * factor / 1.9
                    self.target_x -= self.speed * factor / 1.9
                elif (direction == "downleft"):
                    self.target_y -= self.speed * factor / 1.9
                    self.target_x += self.speed * factor / 1.9
                elif (direction == "downright"):
                    self.target_y -= self.speed * factor / 1.9
                    self.target_x -= self.speed * factor / 1.9

            def damageKB(self, enemyx, enemyy):
                if(self.health > 0):
                    red_die_sound.play()
                    pygame.draw.rect(display, (255, 255, 255), (self.x, self.y, self.width, self.height))
                    if (enemyx > self.x):
                        self.target_x -= self.speed * 20
                    else:
                        self.target_x += self.speed * 20
                    if (enemyy > self.y):
                        self.target_y -= self.speed * 20
                    else:
                        self.target_y += self.speed * 20
                
                    
            def terminate(self, enemyx, enemyy):
                if(self.dead == False):
                    red_die_sound.play()
                    yellow_die_sound.play()
                    self.dead = True
                    for i in range(15):
                        death_particles.append(deathParticles(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 7, 7, self.color, enemyx, enemyy))
                    del self

            def dash(self, direction, factor):

                if (direction == "left"):
                    self.target_x -= self.speed * factor
                elif (direction == "right"):
                    self.target_x += self.speed * factor
                elif (direction == "up"):
                    self.target_y -= self.speed * factor
                elif (direction == "down"):
                    self.target_y += self.speed * factor
                elif (direction == "upleft"):
                    self.target_y -= self.speed * factor / 1.5
                    self.target_x -= self.speed * factor / 1.5
                elif (direction == "upright"):
                    self.target_y -= self.speed * factor / 1.5
                    self.target_x += self.speed * factor / 1.5
                elif (direction == "downleft"):
                    self.target_y += self.speed * factor / 1.5
                    self.target_x -= self.speed * factor / 1.5
                elif (direction == "downright"):
                    self.target_y += self.speed * factor / 1.5
                    self.target_x += self.speed * factor / 1.5

            def move_left(self):
                self.target_x -= self.speed

            def move_left_up(self):
                self.target_x -= self.speed
                self.target_y -= self.speed / 1.7

            def move_right(self):
                self.target_x += self.speed

            def move_right_up(self):
                self.target_x += self.speed
                self.target_y -= self.speed / 1.7

            def move_up(self):
                self.target_y -= self.speed

            def move_down(self):
                self.target_y += self.speed

            def move_left_down(self):
                self.target_x -= self.speed
                self.target_y += self.speed / 1.7

            def move_right_down(self):
                self.target_x += self.speed
                self.target_y += self.speed / 1.7

        class PlayerBullet:
            def __init__(self, x, y, closest_enemy_x, closest_enemy_y, direction, color, track, alive, exploded, angle, x_vel, y_vel):
                if (color == bulletColor):
                    red_bullet_sound.play()
                else:
                    yellow_bullet_sound.play()
                self.x = x
                self.y = y
                self.enemy_x = closest_enemy_x
                self.enemy_y = closest_enemy_y
                if ((self.enemy_x > self.x) and (((self.enemy_y - self.y) >= 0) and (self.enemy_y - self.y) <= 50)):
                    #"right"
                    self.x = x + 30
                    self.y = y + 20
                if ((self.enemy_x < self.x) and (((self.enemy_y - self.y) >= 0) and (self.enemy_y - self.y) <= 50)):
                    #"left"
                    self.x = x - 10
                    self.y = y + 20
                if ((self.enemy_y < self.y) and (((self.enemy_x - self.x) >= 0) and (self.enemy_x - self.x) <= 30)):
                    #"up"
                    self.x = x + 15
                    self.y = y - 5
                if ((self.enemy_y > self.y) and (((self.enemy_x - self.x) >= 0) and (self.enemy_x - self.x) <= 30)):
                    #"down"
                    self.x = x + 15
                    self.y = y + 40
                if (((self.enemy_x - self.x) <= -30) and (self.enemy_y < self.y)):
                    #"upleft"
                    self.x = x
                    self.y = y
                if (((self.enemy_x - self.x) >= 30) and (self.enemy_y < self.y)):
                    #"upright"
                    self.x = x + 40
                    self.y = y
                if (((self.enemy_x - self.x) <= -30) and ((self.enemy_y - self.y) >= 40)):
                    #"downleft"
                    self.x = x - 2
                    self.y = y + 45
                if (((self.enemy_x - self.x) >= 30) and ((self.enemy_y - self.y) >= 40)):
                    #"downright"
                    self.x = x + 40
                    self.y = y + 45
                self.speed = 15
                if (angle == 0 and x_vel == 0 and y_vel == 0):
                    self.angle = math.atan2(y - self.enemy_y, x - self.enemy_x)
                    self.x_vel = math.cos(self.angle) * self.speed
                    self.y_vel = math.sin(self.angle) * self.speed
                else:
                    self.angle = angle
                    self.x_vel = x_vel
                    self.y_vel = y_vel

                self.color = color
                self.is_alive = alive
                self.placement = track
                self.direction = direction
                self.exploded = exploded
                self.direction = direction
                self.speed = 15
                self.is_alive = True
                self.color = color


            def main(self, display):
                self.x -= int(self.x_vel)
                self.y -= int(self.y_vel)
                bullet_rect = pygame.Rect(self.x - 7, self.y - 7, 10, 10)
                if (self.is_alive == True) and (player.dead == False):
                    pygame.draw.circle(display, self.color, (self.x, self.y), 7)
                else:
                    if (self.exploded == False) and (player.dead == False):
                        for i in range(7):
                            bullet_particles.append(bulletParticles(self.x + random.randint(2, 6), self.y + random.randint(-4, 4),random.randint(1, 4), self.color))
                        self.exploded = True
                    player_bullets.remove(self)
                    self.is_alive = False
                player_bullets_track[self.placement - 1] = ((self.x, self.y, self.enemy_x, self.enemy_y, self.direction, self.color, self.placement, self.is_alive, self.exploded, self.angle, self.x_vel, self.y_vel))
                return bullet_rect

            def update(self):
                player_bullets_track[self.placement - 1] = ((self.x, self.y, self.enemy_x, self.enemy_y, self.direction, self.color, self.placement, self.is_alive, self.exploded, self.angle, self.x_vel, self.y_vel))
                if((self.x < 0) or (self.x > 800) or (self.y < 0) or (self.y > 600)):
                    self.is_alive = False

        class PlayerBulletClick:
            def __init__(self, x, y, mouse_x, mouse_y, direction, color, track, alive, exploded, angle, x_vel, y_vel):
                if(color == bulletColor):
                    red_bullet_sound.play()
                else:
                    yellow_bullet_sound.play()
                self.x = x
                self.y = y
                if ((mouse_x > self.x) and (((mouse_y - self.y) >= 0) and (mouse_y - self.y) <= 50)):
                    #"right"
                    self.x = x + 30
                    self.y = y + 20
                if ((mouse_x < self.x) and (((mouse_y - self.y) >= 0) and (mouse_y - self.y) <= 50)):
                    #"left"
                    self.x = x - 10
                    self.y = y + 20
                if ((mouse_y < self.y) and (((mouse_x - self.x) >= 0) and (mouse_x - self.x) <= 30)):
                    #"up"
                    self.x = x + 15
                    self.y = y - 5
                if ((mouse_y > self.y) and (((mouse_x - self.x) >= 0) and (mouse_x - self.x) <= 30)):
                    #"down"
                    self.x = x + 15
                    self.y = y + 40
                if (((mouse_x - self.x) <= -30) and (mouse_y < self.y)):
                    #"upleft"
                    self.x = x
                    self.y = y
                if (((mouse_x - self.x) >= 30) and (mouse_y < self.y)):
                    #"upright"
                    self.x = x + 40
                    self.y = y
                if (((mouse_x - self.x) <= -30) and ((mouse_y - self.y) >= 40)):
                    #"downleft"
                    self.x = x - 2
                    self.y = y + 45
                if (((mouse_x - self.x) >= 30) and ((mouse_y - self.y) >= 40)):
                    #"downright"
                    self.x = x + 40
                    self.y = y + 45
                self.mouse_x = mouse_x
                self.mouse_y = mouse_y
                self.speed = 15
                if(angle == 0 and x_vel == 0 and y_vel == 0):
                    self.angle = math.atan2(y-mouse_y, x-mouse_x)
                    self.x_vel = math.cos(self.angle) * self.speed
                    self.y_vel = math.sin(self.angle) * self.speed
                else:
                    self.angle = angle
                    self.x_vel = x_vel
                    self.y_vel = y_vel
                self.color = color
                self.is_alive = alive
                self.placement = track
                self.direction = direction
                self.exploded = exploded

            def main(self, display):
                self.x -= int(self.x_vel)
                self.y -= int(self.y_vel)
                bullet_rect = pygame.Rect(self.x - 7, self.y - 7, 10, 10)
                if (self.is_alive == True) and (player.dead == False):
                    pygame.draw.circle(display, self.color, (self.x, self.y), 7)
                else:
                    if(self.exploded == False) and (player.dead == False):
                        for i in range(7):
                            bullet_particles.append(bulletParticles(self.x + random.randint(2, 6), self.y + random.randint(-4, 4), random.randint(1, 4), self.color))
                        self.exploded = True
                    player_bullets_click.remove(self)
                    self.is_alive = False
                player_bullets_click_track[self.placement - 1] = ((self.x, self.y, self.mouse_x, self.mouse_y, self.direction, self.color, self.placement, self.is_alive, self.exploded, self.angle, self.x_vel, self.y_vel))
                return bullet_rect

            def update(self):
                player_bullets_click_track[self.placement - 1] = ((self.x, self.y, self.mouse_x, self.mouse_y, self.direction, self.color, self.placement, self.is_alive, self.exploded, self.angle, self.x_vel, self.y_vel))
                if((self.x < 0) or (self.x > 800) or (self.y < 0) or (self.y > 600)):
                    self.is_alive = False

        class Enemy:
            def __init__ (self, x, y, width, height, health, speed, track, color):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.health = health
                self.speed = speed
                self.color = color
                self.drop_chance = random.randint(0, 100)
                self.placement = track
                self.isAlive = True

            def main(self, display):
                if(self.health > 0) and (self.color == "red"):
                    pygame.draw.rect(display, enemyColor, (self.x, self.y, self.width, self.height))
                    self.move_towards_player()
                elif(self.health > 0) and (self.color == "yellow"):
                    pygame.draw.rect(display, enemyColor2, (self.x, self.y, self.width, self.height))
                    self.move_towards_player()
                enemy_track[self.placement-1] = ((self.x, self.y, self.width, self.height, self.health, self.speed, self.placement, self.color))
                return self.get_rect()

            def move_towards_player(self):
                if(player.dead == False):
                    # calculate angle between enemy and player
                    moveangle = math.atan2(player.y - self.y, player.x - self.x)
                    dx = math.cos(moveangle)
                    dy = math.sin(moveangle)
                    self.x += dx * self.speed
                    self.y += dy * self.speed

            def get_rect(self):
                return pygame.Rect(self.x, self.y, self.width, self.height)

            def was_hit(self, bulletx, bullety, damage):
                if(self.health > 0):
                    # calculate angle between bullet and enemy
                    angle = math.atan2(player.y - (self.y + 21), player.x - (self.x + 16))
                    pygame.draw.rect(display, (255, 255, 255), (self.x, self.y, self.width + 3, self.height + 5))
                    # calculate x and y components of recoil movement
                    recoil_distance = 10
                    recoil_x = recoil_distance * math.cos(angle)
                    recoil_y = recoil_distance * math.sin(angle)
                    # move enemy in opposite direction of bullet
                    self.x -= int(recoil_x)
                    self.y -= int(recoil_y)
                    self.health -= damage
                    if(self.health <= 0):
                        if(self.color == "red"):
                            red_die_sound.play()
                        else:
                            yellow_die_sound.play()

                        for i in range(15):
                            death_particles.append(deathParticles(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 10, 10, self.color, self.x, self.y))

                        if(ammunition < 2):
                            ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "red", len(ammo_track), False, 15))
                            ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10,"red", 0, False, 15))
                        if(ammunition1 < 2):
                            ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "yellow", len(ammo_track), False, 15))
                            ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10,"yellow", 0, False, 15))
                        if(self.drop_chance < 75):
                            if (((ammunition - ammunition1) > 25) and (self.drop_chance < 50)) or (ammunition1 < 7):
                                ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "yellow", 0, False, 15))
                                ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "yellow", len(ammo_track), False, 15))
                            elif (((ammunition1 - ammunition) > 25) and (self.drop_chance < 50)) or (ammunition < 7):
                                ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "red", 0, False, 15))
                                ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "red", len(ammo_track), False, 15))
                            elif(ammunition < 7) and (ammunition < 7):
                                ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "red", 0, False, 15))
                                ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "red", len(ammo_track), False, 15))
                                ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "yellow", 0, False, 15))
                                ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, "yellow", len(ammo_track), False, 15))
                            elif (self.drop_chance < 7):
                                ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, " ", 0, False, 15))
                                ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, random.choice(bullet_colors), len(ammo_track), False, 15))
                                ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, " ", 0, False, 15))
                                ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, random.choice(bullet_colors), len(ammo_track), False, 15))
                            else:
                                ammo_track.append((self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, " ", 0, False, 15))
                                ammo_item.append(Ammo_Item(self.x + random.randint(0, 100), self.y + random.randint(0, 100), 20, 10, random.choice(bullet_colors), len(ammo_track), False, 15))
                        if(self.drop_chance < 15) and (player.health <= 10):
                            health_kit_track.append((self.x, self.y, 45, 25, 0, False))
                            health_kit.append(Health_Kit(self.x, self.y, 45, 25, len(health_kit_track), False))
                        elif(self.drop_chance < 3) and (player.health < full_health):
                            health_kit_track.append((self.x, self.y, 45, 25, 0, False))
                            health_kit.append(Health_Kit(self.x, self.y, 45, 25, len(health_kit_track), False))


                        if(self == closest_enemy):
                            self.x = 10000
                            self.y = 10000
                        global score_to_add
                        score_to_add += 100
                        #enemies.remove(self)
                else:
                    del self

        class deathParticles:
            def __init__(self, x, y, height, width, color, enemyx, enemyy):
                self.x = x + random.randint(0, 4)
                self.y = y + random.randint(0, 4)
                self.height = height
                self.width = width
                self.speed = random.randint(2, 6)
                self.target_x = x
                self.target_y = y
                self.timer = 30
                self.color = color
                self.enemyx = enemyx
                self.enemyy = enemyy

            def main(self):
                if(self.color != "blue"):
                    if(self.timer > 20):
                        if (player.x < self.x):
                            self.x += self.speed
                        else:
                            self.x -= self.speed

                        if(player.y > self.y):
                            self.y -= self.speed
                        else:
                            self.y += self.speed
                    elif(self.timer > 0):
                        if (player.x < self.x):
                            self.x += self.speed / self.timer
                        else:
                            self.x -= self.speed / self.timer

                        if(player.y > self.y):
                            self.y -= self.speed / self.timer
                        else:
                            self.y += self.speed / self.timer
                else:
                    if (self.timer > 20):
                        if (self.enemyx < self.x):
                            self.x += self.speed
                        else:
                            self.x -= self.speed

                        if (self.enemyy > self.y):
                            self.y -= self.speed
                        else:
                            self.y += self.speed
                    elif (self.timer > 0):
                        if (self.enemyx < self.x):
                            self.x += self.speed / self.timer
                        else:
                            self.x -= self.speed / self.timer

                        if (self.enemyy > self.y):
                            self.y -= self.speed / self.timer
                        else:
                            self.y += self.speed / self.timer

            def update(self, dt):
                self.timer -= 1
                if(self.timer > 0) and (self.color == "red"):
                    pygame.draw.rect(display, enemyColor, (self.x, self.y, self.width * self.timer/15, self.height * self.timer/15))
                elif (self.timer > 0) and (self.color == "yellow"):
                    pygame.draw.rect(display, enemyColor2, (self.x, self.y, self.width * self.timer / 15, self.height * self.timer / 15))
                elif (self.timer > 0) and (self.color == "blue"):
                    pygame.draw.rect(display, playerColor, (self.x, self.y, self.width * self.timer / 15, self.height * self.timer / 15))

        class Ammo_Item:
            def __init__(self, x, y, height, width, color, track, dead, timer):
                self.x = x + random.randint(0, 4)
                self.y = y + random.randint(0, 4)
                self.height = height
                self.width = width
                self.speed = random.randint(2, 6)
                self.target_x = x
                self.target_y = y
                self.timer = timer
                self.dead = dead
                self.pickedup = False
                self.color = color
                self.placement = track

            def main(self, display):
                if self.x < 0:
                    self.x = 3
                    self.target_x = self.x
                elif self.x > width - self.width:
                    self.x = (width - 10) - self.width
                    self.target_x = self.x

                if self.y < 0:
                    self.y = 3
                    self.target_y = self.y
                elif self.y > height - self.height:
                    self.y = height - self.height
                    self.target_y = self.y


                if(self.timer > 5):
                    if (player.x < self.x):
                        self.x += self.speed
                    else:
                        self.x -= self.speed

                    if(player.y > self.y):
                        self.y -= self.speed
                    else:
                        self.y += self.speed
                elif(self.timer > 0):
                    if (player.x < self.x):
                        self.x += self.speed / self.timer
                    else:
                        self.x -= self.speed / self.timer

                    if(player.y > self.y):
                        self.y -= self.speed / self.timer
                    else:
                        self.y += self.speed / self.timer

                ammo_track[self.placement - 1] = ((self.x, self.y, self.height, self.width, self.color, self.placement, self.dead, self.timer))
                return pygame.Rect(self.x, self.y, self.width * 3, self.height)

            def update(self, dt, display):
                if(self.dead == False):
                    self.timer -= 1
                    if(self.color == "red"):
                        for i in range(3):
                            pygame.draw.rect(display, bulletColor, (self.x + i * 15, self.y, self.width, self.height), 10, 3)
                    else:
                        for i in range(3):
                            pygame.draw.rect(display, bulletColor2, (self.x + i * 15, self.y, self.width, self.height), 10, 3)

            def terminate(self):
                self.dead = True
                #del self

        class Cursor_Circle:
            def __init__(self, mouse_x, mouse_y):
                self.x = mouse_x
                self.y = mouse_y
                self.visible = True

            def main(self, display, mouse_x, mouse_y):
                self.x = mouse_x
                self.y = mouse_y
                if self.visible:
                    pygame.draw.circle(display, (0, 255, 0), (self.x, self.y), 10, 3)

        class Ammo_Count_Display:
            def __init__(self, width, height):
                self.x = 60
                self.y = 545
                self.width = width
                self.height = height

            def main(self):
                for i in range(int(ammunition)):
                    pygame.draw.rect(display, bulletColor, (self.x + i * 15, self.y, self.width, self.height), 10, 3)
                for j in range(int(full_ammunition - ammunition)):
                    pygame.draw.rect(display, bulletColor, (self.x + ((full_ammunition-1) * 15) - j*15, self.y, self.width, self.height), 2, 4)

        class Ammo_Count_Display1:
            def __init__(self, width, height):
                self.x = 60
                self.y = 570
                self.width = width
                self.height = height

            def main(self):
                for i in range(int(ammunition1)):
                    pygame.draw.rect(display, bulletColor2, (self.x + i * 15, self.y, self.width, self.height), 10, 3)
                for j in range(int(full_ammunition1 - ammunition1)):
                    pygame.draw.rect(display, bulletColor2, (self.x + ((full_ammunition1-1) * 15) - j*15, self.y, self.width, self.height), 2, 4)

        class Health_Bar_BG:
            def __init__(self, x, y, height, width):
                self.x, self.y = x, y
                self.height = height
                self.width = width * full_health

            def main(self):
                pygame.draw.rect(display, healthBarBGColor, (self.x, self.y, self.width, self.height), 3)

        class Health_Bar:
            def __init__(self, x, y, height, width):
                self.x, self.y = x, y
                self.height, self.width = height, width

            def main(self):
                for i in range(player.health):
                    pygame.draw.rect(display, healthBarColor, ((self.x + i * self.width), self.y, self.width, self.height))

        class Health_Kit:
            def __init__(self, x, y, width, height, track, dead):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.rect = pygame.Rect(x, y, width, height)
                self.pickedup = False
                self.dead = dead
                self.placement = track

            def main(self, display):
                if(self.dead == False):
                    pygame.draw.rect(display, (200, 200, 200), self.rect, 20, 5)
                    pygame.draw.rect(display, (0, 200, 0), (self.x + 21, self.y + 3, self.width - 40, self.height - 6))
                    pygame.draw.rect(display, (0, 200, 0), (self.x + 14, self.y + 10, self.height - 6, self.width - 40))
                health_kit_track[self.placement - 1] = ((self.x, self.y, self.width, self.height, self.placement, self.dead))
                return pygame.Rect(self.x, self.y, self.width, self.height)

            def terminate(self):
                self.dead = True
                del self

        class bulletParticles:
            def __init__(self, x, y, size, color):
                self.x = x + random.randint(0, 2)
                self.y = y + random.randint(0, 2)
                self.size = size
                self.speed = random.randint(3, 5)
                self.target_x = x
                self.target_y = y
                self.timer = 15
                self.color = color

            def main(self):
                if(self.timer > 10):
                    if (player.x > self.x):
                        self.x += self.speed
                    else:
                        self.x -= self.speed

                    if(player.y < self.y):
                        self.y -= self.speed
                    else:
                        self.y += self.speed
                elif (self.timer > 0):
                    if (player.x > self.x):
                        self.x += self.speed / self.timer
                    else:
                        self.x -= self.speed / self.timer

                    if (player.y < self.y):
                        self.y -= self.speed / self.timer
                    else:
                        self.y += self.speed / self.timer

            def update(self, dt):
                self.timer -= 1
                if(self.timer > 0) and (self.color == bulletColor):
                    pygame.draw.circle(display, self.color, (self.x, self.y), self.size * self.timer / 7)
                elif (self.timer > 0) and (self.color == bulletColor2):
                    pygame.draw.circle(display, self.color, (self.x, self.y), self.size * self.timer / 7)



        #Health_Kit(300, 300, 45, 25)

        #Initialize Player position and size
        player = Player(player_x_init, player_y_init, 32, 42, health_init, playerColor)
        cursor_circle = Cursor_Circle(0, 0)
        health_bar = Health_Bar(30, 28, 20, 2)
        health_bar_bg = Health_Bar_BG(30, 28, 20, 2)
        enemies = []
        enemyset = (0, 0, 32, 42, 5)
        player_bullets = []
        player_bullets_click = []
        death_particles = []
        bullet_particles = []
        ammo_item = []
        health_kit = []
        closest_distance = 1000
        closest_enemy = None
        closest_red_enemy_x = 0
        closest_red_enemy_y = 0
        closest_yellow_enemy_x = 0
        closest_yellow_enemy_y = 0
        closest_enemy_direction = "right"
        ammo_count_display = Ammo_Count_Display(10, 20)
        ammo_count_display1 = Ammo_Count_Display1(10, 20)
        ammunition = ammunition_init
        full_ammunition = 45
        ammunition1 = ammunition1_init
        full_ammunition1 = 45
        bullet_damage, bullet_click_damage = 1, 1

        lastDirection = "right"
        movementEnabled = True
        dashTimeCool = 0
        shootAgain = True
        hurtAgain = True

        #width is 800, height is 600
        enemy_spawn_points_x = [-50, 400, 800]
        enemy_spawn_points_y = [-50, 300, 600]

        #respawn_time = 2000
        respawn_time = 2000
        invincibility_time = 1500

        BULLET_SPRAY_DELAY = pygame.USEREVENT + 1
        ENEMY_RESPAWN = pygame.USEREVENT + 2
        BULLET_ADD = pygame.USEREVENT + 3
        SCORE_ADD = pygame.USEREVENT + 4
        INVINCIBILITY = pygame.USEREVENT + 5
        pygame.time.set_timer(ENEMY_RESPAWN, respawn_time)
        pygame.time.set_timer(BULLET_ADD, 25)
        pygame.time.set_timer(SCORE_ADD, 5)
        pygame.time.set_timer(INVINCIBILITY, invincibility_time)

        bullets_to_add = 0
        bullets_to_add_1 = 0
        health_to_add = player.health

        for i in range(len(enemy_track)):
            if(enemy_track[i][4] > 0):
                enemies.append(Enemy(*enemy_track[i]))

        for i in range(len(ammo_track)):
            ammo_item.append(Ammo_Item(*ammo_track[i]))

        for i in range(len(health_kit_track)):
            health_kit.append(Health_Kit(*health_kit_track[i]))

        for i in range(len(player_bullets_click_track)):
            player_bullets_click.append(PlayerBulletClick(*player_bullets_click_track[i]))

        for i in range(len(player_bullets_track)):
            player_bullets.append(PlayerBullet(*player_bullets_track[i]))

        replaycolor = backgroundColor
        mainmenucolor = backgroundColor
        highlightcolor = (255, 100, 100, 0)

        scorefont = pygame.font.SysFont("monospace", 40)
        diedfont = pygame.font.SysFont("monospace", 100)
        textfont = pygame.font.SysFont("monospace", 60)
        replay_rect = pygame.Rect(195, 277, 226, 60)
        main_menu_rect = pygame.Rect(195, 352, 335, 60)

        on_replay = False
        on_main_menu = False
        replay_click = False
        main_menu_click = False

        while True:
            score_string=("0" * (7-len(str(score)))) + str(score)

            textSCORE = scorefont.render(score_string, 1, (255, 255, 255))
            textDIED = diedfont.render("YOU DIED", 1, (255, 255, 255))
            textREPLAY = textfont.render("REPLAY", 1, (255, 255, 255))
            textMAINMENU = textfont.render("MAIN MENU", 1, (255, 255, 255))
            display.blit(textSCORE, (325, 15))
            if(player.health <= 0):
                mixer.music.stop()
                pygame.draw.rect(display, replaycolor, (replay_rect))
                pygame.draw.rect(display, mainmenucolor, (main_menu_rect))
                display.blit(textDIED, (175, 100))
                display.blit(textREPLAY, (200, 275))
                display.blit(textMAINMENU, (200, 350))
                if replay_rect.collidepoint(mouse_x, mouse_y):
                    replaycolor = highlightcolor
                    on_replay = True
                else:
                    replaycolor = backgroundColor
                    on_replay = False
                if main_menu_rect.collidepoint(mouse_x, mouse_y):
                    mainmenucolor = highlightcolor
                    on_main_menu = True
                else:
                    mainmenucolor = backgroundColor
                    on_main_menu = False
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)

            pygame.display.update()

            music_seconds = pygame.mixer.music.get_pos()

            display.fill((backgroundColor))

            mouse_x, mouse_y = pygame.mouse.get_pos()

            dt = clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if(on_main_menu == True) and (main_menu_click == True):
                            MainMenu.main(MainMenu(), False)
                        if(on_replay == True) and (replay_click == True):
                            MainMenu.main(MainMenu(), True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if(on_replay == True):
                            replay_click = True
                        elif(on_main_menu == True):
                            main_menu_click = True
                        else:
                            replay_click = False
                            main_menu_click = False
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                # Handle the timer event
                if event.type == BULLET_SPRAY_DELAY:
                    shootAgain = True
                if event.type == INVINCIBILITY:
                    hurtAgain = True
                if(event.type == BULLET_ADD) and (bullets_to_add > 0):
                    if(ammunition < full_ammunition):
                        ammunition += 1
                    bullets_to_add -= 1
                if (event.type == BULLET_ADD) and (bullets_to_add_1 > 0):
                    if (ammunition1 < full_ammunition1):
                        ammunition1 += 1
                    bullets_to_add_1 -= 1
                if(score_to_add > 0):
                    score += 1
                    score_to_add -= 1
                if event.type == ENEMY_RESPAWN:
                    spawnx = random.choice(enemy_spawn_points_x)
                    spawny = random.choice(enemy_spawn_points_y)
                    good = False
                    while(good == False):
                        if(spawnx == 400 and spawny == 300):
                            spawnx = random.choice(enemy_spawn_points_x)
                            spawny = random.choice(enemy_spawn_points_y)
                        else:
                            good = True
                    if(player.health > 0):
                        enemy_track.append((spawnx, spawny, 50, 60, enemy_full_health, 2, 0, "red"))
                        enemies.append(Enemy(spawnx, spawny, 50, 60, enemy_full_health, 2, len(enemy_track), random.choice(enemy_colors)))
                    if(respawn_time > 1000):
                        respawn_time -= 7
                    pygame.time.set_timer(ENEMY_RESPAWN, respawn_time)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if(lastDirection == "upleft"):
                            lastDirection = "upright"
                        if (lastDirection == "downleft"):
                            lastDirection = "downright"
                        if(lastDirection == "left"):
                            lastDirection = "right"
                    if event.key == pygame.K_LEFT:
                        if(lastDirection == "upright"):
                            lastDirection = "upleft"
                        if (lastDirection == "downright"):
                            lastDirection = "downleft"
                        if (lastDirection == "right"):
                            lastDirection = "left"
                    if (event.key == pygame.K_p) and (player.health > 0):
                        PauseGame.main(PauseGame(), ammunition, ammunition1, score, player.health, enemy_track, player.x, player.y, ammo_track, health_kit_track, player_bullets_click_track, player_bullets_track, music_seconds)

            keys = pygame.key.get_pressed()

            movementEnabled = True


            if (movementEnabled == True):
                if (pygame.mouse.get_pressed()[0]):
                    if (shootAgain == True):
                        if(ammunition > 0) and (player.dead == False):
                            player_bullets_click_track.append((player.x, player.y, mouse_x, mouse_y, lastDirection, bulletColor, 0, True, False, 0, 0, 0))
                            player_bullets_click.append(PlayerBulletClick(player.x, player.y, mouse_x, mouse_y, lastDirection, bulletColor, len(player_bullets_click_track), True, False, 0, 0, 0))
                            ammunition -= 1
                        player.bullet_recoil_click(mouse_x, mouse_y, lastDirection, 2)
                        shootAgain = False
                        pygame.time.set_timer(BULLET_SPRAY_DELAY, 100)
                if (pygame.mouse.get_pressed()[2]):
                    if (shootAgain == True):
                        if(ammunition1 > 0) and (player.dead == False):
                            player_bullets_click_track.append((player.x, player.y, mouse_x, mouse_y, lastDirection, bulletColor2, 0, True, False, 0, 0, 0))
                            player_bullets_click.append(PlayerBulletClick(player.x, player.y, mouse_x, mouse_y, lastDirection, bulletColor2, len(player_bullets_click_track), True, False, 0, 0, 0))
                            ammunition1 -= 1
                        player.bullet_recoil_click(mouse_x, mouse_y, lastDirection, 2)
                        shootAgain = False
                        pygame.time.set_timer(BULLET_SPRAY_DELAY, 100)
                if ((keys[pygame.K_UP] or keys[pygame.K_w]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not(keys[pygame.K_DOWN] or keys[pygame.K_s]))):
                    player.move_up()
                    lastDirection = "up"
                if ((keys[pygame.K_UP] or keys[pygame.K_w]) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not(keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not(keys[pygame.K_DOWN] or keys[pygame.K_s])))):
                    player.move_left_up()
                    lastDirection = "upleft"
                if ((keys[pygame.K_UP] or keys[pygame.K_w]) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not(keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not(keys[pygame.K_DOWN] or keys[pygame.K_s])))):
                    player.move_right_up()
                    lastDirection = "upright"
                if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not(keys[pygame.K_UP] or keys[pygame.K_w]))):
                    player.move_down()
                    lastDirection = "down"
                if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not(keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not(keys[pygame.K_UP] or keys[pygame.K_w])))):
                    player.move_left_down()
                    lastDirection = "downleft"
                if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not(keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not(keys[pygame.K_UP] or keys[pygame.K_w])))):
                    player.move_right_down()
                    lastDirection = "downright"
                if ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not (keys[pygame.K_UP] or keys[pygame.K_w])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s])) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d]))):
                    player.move_left()
                    lastDirection = "left"
                if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not (keys[pygame.K_UP] or keys[pygame.K_w])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s])) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a]))):
                    player.move_right()
                    lastDirection = "right"
                if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                    if (lastDirection == "right"):
                        player.move_right()
                    if (lastDirection == "left"):
                        player.move_left()
                    if (lastDirection == "up"):
                        player.move_up()
                    if (lastDirection == "down"):
                        player.move_down()
                    if (lastDirection == "downleft"):
                        player.move_left_down()
                    if (lastDirection == "downright"):
                        player.move_right_down()
                    if (lastDirection == "upleft"):
                        player.move_left_up()
                    if (lastDirection == "upright"):
                        player.move_right_up()
                if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s]))):
                    if (lastDirection == "right"):
                        player.move_right()
                    if (lastDirection == "left"):
                        player.move_left()
                    if (lastDirection == "up"):
                        player.move_up()
                    if (lastDirection == "down"):
                        player.move_down()
                    if (lastDirection == "downleft"):
                        player.move_left_down()
                    if (lastDirection == "downright"):
                        player.move_right_down()
                    if (lastDirection == "upleft"):
                        player.move_left_up()
                    if (lastDirection == "upright"):
                        player.move_right_up()
                if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not (keys[pygame.K_UP] or keys[pygame.K_w])) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                    if (lastDirection == "right"):
                        player.move_right()
                    if (lastDirection == "left"):
                        player.move_left()
                    if (lastDirection == "up"):
                        player.move_up()
                    if (lastDirection == "down"):
                        player.move_down()
                    if (lastDirection == "downleft"):
                        player.move_left_down()
                    if (lastDirection == "downright"):
                        player.move_right_down()
                    if (lastDirection == "upleft"):
                        player.move_left_up()
                    if (lastDirection == "upright"):
                        player.move_right_up()
                if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                    if (lastDirection == "right"):
                        player.move_right()
                    if (lastDirection == "left"):
                        player.move_left()
                    if (lastDirection == "up"):
                        player.move_up()
                    if (lastDirection == "down"):
                        player.move_down()
                    if (lastDirection == "downleft"):
                        player.move_left_down()
                    if (lastDirection == "downright"):
                        player.move_right_down()
                    if (lastDirection == "upleft"):
                        player.move_left_up()
                    if (lastDirection == "upright"):
                        player.move_right_up()
                if ((not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                    if (lastDirection == "right"):
                        player.move_right()
                    if (lastDirection == "left"):
                        player.move_left()
                    if (lastDirection == "up"):
                        player.move_up()
                    if (lastDirection == "down"):
                        player.move_down()
                    if (lastDirection == "downleft"):
                        player.move_left_down()
                    if (lastDirection == "downright"):
                        player.move_right_down()
                    if (lastDirection == "upleft"):
                        player.move_left_up()
                    if (lastDirection == "upright"):
                        player.move_right_up()
                if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not(keys[pygame.K_UP] or keys[pygame.K_w])) and (not(keys[pygame.K_DOWN] or keys[pygame.K_s]))):
                    if (lastDirection == "right"):
                        player.move_right()
                    if (lastDirection == "left"):
                        player.move_left()
                if (keys[pygame.K_z]):
                    cursor_circle.visible = False
                    if (shootAgain == True) and (ammunition > 0) and (player.dead == False):
                        player_bullets_track.append((player.x, player.y, closest_red_enemy_x, closest_red_enemy_y, lastDirection,bulletColor, 0, True, False, 0, 0, 0))
                        player_bullets.append(PlayerBullet(player.x, player.y, closest_red_enemy_x, closest_red_enemy_y, closest_enemy_direction, bulletColor, len(player_bullets_track), True, False, 0, 0, 0))
                        player.bullet_recoil_click(closest_red_enemy_x, closest_red_enemy_y, lastDirection, 2)
                        ammunition -= 1
                        shootAgain = False
                        pygame.time.set_timer(BULLET_SPRAY_DELAY, 100)
                if (keys[pygame.K_x]):
                    cursor_circle.visible = False
                    if (shootAgain == True) and (ammunition1 > 0) and (player.dead == False):
                        player_bullets_track.append((player.x, player.y, closest_yellow_enemy_x, closest_yellow_enemy_y, lastDirection, bulletColor2, 0, True, False, 0, 0, 0))
                        player_bullets.append(PlayerBullet(player.x, player.y, closest_yellow_enemy_x, closest_yellow_enemy_y, closest_enemy_direction, bulletColor2, len(player_bullets_track), True, False, 0, 0, 0))
                        player.bullet_recoil_click(closest_yellow_enemy_x, closest_yellow_enemy_y, lastDirection, 2)
                        ammunition1 -= 1
                        shootAgain = False
                        pygame.time.set_timer(BULLET_SPRAY_DELAY, 100)

            player.update(dt)
            player.main(display)

            if pygame.mouse.get_rel()[0] > 0:
                cursor_circle.visible = True

            for particle in death_particles:
                particle.main()
                particle.update(dt)
                if(particle.timer < 0):
                    death_particles.remove(particle)

            for particle in bullet_particles:
                particle.main()
                particle.update(dt)
                if(particle.timer < 0):
                    bullet_particles.remove(particle)

            for kit in health_kit:
                kit.main(display)
                kit_rect = kit.main(display)
                if kit_rect.colliderect(player.get_rect()):
                    if kit.pickedup == False:
                        health_kit_sound.play()
                        kit.pickedup = True
                        if(player.health >= 90):
                            for i in range(full_health - player.health):
                                player.health += 1
                                score_to_add += 4
                        else:
                            for i in range(10):
                                player.health += 1
                                score_to_add += 2
                    kit.terminate()

            for ammo in ammo_item:
                ammo.update(dt, display)
                ammo_rect = ammo.main(display)
                if ammo_rect.colliderect(player.get_rect()):
                    if (ammo.pickedup == False) and (ammo.dead == False):
                        ammo.pickedup = True
                        if(ammo.color == bulletColor):
                            red_ammo_sound.play()
                        else:
                            yellow_ammo_sound.play()
                        if(ammo.color == "red"):
                            for i in range(ammo_plus):
                                if(full_ammunition - ammunition) > 0:
                                    bullets_to_add += 1
                                    score_to_add += 1
                                else:
                                    score_to_add += 5
                        else:
                            for i in range(ammo_plus):
                                if(full_ammunition1 - ammunition1) > 0:
                                    bullets_to_add_1 += 1
                                    score_to_add += 1
                                else:
                                    score_to_add += 5
                    ammo.terminate()

            for bullet in player_bullets:
                bullet.update()

            for bullet in player_bullets_click:
                bullet.update()

            for bullet in player_bullets_click:
                bullet_rect = bullet.main(display)
                for enemy in enemies:
                    if bullet_rect.colliderect(enemy.get_rect()):
                        if(enemy.health > 0) and ((enemy.color == "red") and ((bullet.color == bulletColor)) or ((enemy.color == "yellow") and (bullet.color == bulletColor2))):
                            score_to_add += 1
                            enemy.was_hit(bullet.x, bullet.y, bullet_click_damage)
                            bullet.is_alive = False

            for bullet in player_bullets:
                bullet_rect = bullet.main(display)
                for enemy in enemies:
                    if bullet_rect.colliderect(enemy.get_rect()):
                        if (enemy.health > 0) and ((enemy.color == "red") and ((bullet.color == bulletColor)) or ((enemy.color == "yellow") and (bullet.color == bulletColor2))):
                            score_to_add += 1
                            enemy.was_hit(bullet.x, bullet.y, bullet_damage)
                            bullet.is_alive = False


            def get_distance(pos1, pos2):
                x1, y1 = pos1
                x2, y2 = pos2
                return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            closest_distance = float('inf')

            for enemy in enemies:
                enemy_rect = enemy.main(display)
                if enemy_rect.colliderect(player.get_rect()):
                    if(enemy.health > 0) and (hurtAgain == True):
                        player.damageKB(enemy.x, enemy.y)
                        player.timer = int(invincibility_time / 18.75)
                        for i in range(enemy_damage):
                            player.health -= 1
                        if(player.health <= 0):
                            player.terminate(enemy.x, enemy.y)
                        hurtAgain = False
                        pygame.time.set_timer(INVINCIBILITY, 1500)


                if(enemy.health > 0):
                    distance = get_distance((enemy.x, enemy.y), (player.x, player.y))
                    if (distance < closest_distance) and (enemy.color == "red"):
                        closest_red_enemy = enemy
                        closest_red_enemy_x = enemy.x # +25
                        closest_red_enemy_y = enemy.y # +30
                        closest_distance = distance

                if (enemy.health > 0):
                    distance = get_distance((enemy.x, enemy.y), (player.x, player.y))
                    if (distance < closest_distance) and (enemy.color == "yellow"):
                        closest_yellow_enemy = enemy
                        closest_yellow_enemy_x = enemy.x
                        closest_yellow_enemy_y = enemy.y
                        closest_distance = distance

            ammo_count_display.main()
            ammo_count_display1.main()
            health_bar.main()
            health_bar_bg.main()
            if(player.health > 0):
                cursor_circle.main(display, mouse_x, mouse_y)

class PauseGame:
    def main(self, ammunition_cont, ammunition1_cont, score_cont, health_cont, enemy_track_cont, player_x_cont, player_y_cont, ammo_track_cont, health_kit_track_cont, player_bullet_click_track_cont, player_bullet_track_cont, music_seconds_cont):
        textfont = pygame.font.SysFont("Verdana", 50)
        titlefont = pygame.font.SysFont("Verdana", 80)
        resume_rect = pygame.Rect(247, 303, 225, 60)
        main_menu_rect = pygame.Rect(247, 405, 310, 60)
        mainmenucolor = (26, 100, 64, 25)
        resumecolor = backgroundColor
        on_resume = False
        on_main_menu = False
        clickdown = 0

        HOVER_TIME = pygame.USEREVENT + 1
        pygame.time.set_timer(HOVER_TIME, 3)

        while True:
            pauseText = titlefont.render("PAUSE", 1, (255, 255, 255))
            resumeText = textfont.render("RESUME", 1, (255, 255, 255))
            mainMenuText = textfont.render("MAIN MENU", 1, (255, 255, 255))
            pygame.draw.rect(display, resumecolor, (resume_rect))
            pygame.draw.rect(display, mainmenucolor, (main_menu_rect))
            display.blit(pauseText, (135, 40))
            display.blit(resumeText, (250, 300))
            display.blit(mainMenuText, (250, 400))

            mouse_x, mouse_y = pygame.mouse.get_pos()

            pygame.mouse.set_visible(True)

            if resume_rect.collidepoint(mouse_x, mouse_y):
                resumecolor = (255, 100, 100, 0)
                on_resume = True
            else:
                resumecolor = backgroundColor
                on_resume = False

            if main_menu_rect.collidepoint(mouse_x, mouse_y):
                mainmenucolor = (255, 100, 100, 0)
                on_main_menu = True
            else:
                mainmenucolor = backgroundColor
                on_main_menu = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if (on_resume == True) and (clickdown == 1):
                            Game.main(Game(), ammunition_cont, ammunition1_cont, score_cont, health_cont, enemy_track_cont, player_x_cont, player_y_cont, ammo_track_cont, health_kit_track_cont, player_bullet_click_track_cont, player_bullet_track_cont, music_seconds_cont)
                        if (on_main_menu == True) and (clickdown == 2):
                            MainMenu.main(MainMenu(), False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (on_resume == True):
                            clickdown = 1
                        elif (on_main_menu == True):
                            clickdown = 2
                        else:
                            clickdown = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        Game.main(Game(), ammunition_cont, ammunition1_cont, score_cont, health_cont, enemy_track_cont, player_x_cont, player_y_cont, ammo_track_cont, health_kit_track_cont, player_bullet_click_track_cont, player_bullet_track_cont, music_seconds_cont)
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

class MainMenu:
    def main(self, myreplay):
        mixer.music.load('Menu.wav')
        #mixer.music.play(-1)
        #
        #
        textfont = pygame.font.SysFont("Verdana", 50)
        titlefont = pygame.font.SysFont("Verdana", 80)
        play_rect = pygame.Rect(247, 303, 130, 60)
        option_rect = pygame.Rect(247, 403, 290, 60)
        highlightcolor = (255, 100, 100, 0)
        on_play = False
        on_options = False
        optioncolor = backgroundColor
        playcolor = backgroundColor
        playclicked = False
        optionsclicked = False

        HOVER_TIME = pygame.USEREVENT + 1
        pygame.time.set_timer(HOVER_TIME, 3)

        enemy_track = []
        ammo_track = []
        health_kit_track = []
        player_bullet_click_track = []
        player_bullet_track = []

        while True:
            if (myreplay == True):
                Game.main(Game(), 45, 45, 0, 100, enemy_track, 400, 300, ammo_track, health_kit_track, player_bullet_click_track, player_bullet_track, 0)

            pygame.mouse.set_visible(True)

            display.fill(backgroundColor)

            titleText = titlefont.render("BULLET BASH", 1, (255, 255, 255))
            playText = textfont.render("PLAY", 1, (255, 255, 255))
            controlsText = textfont.render("CONTROLS", 1, (255, 255, 255))
            pygame.draw.rect(display, playcolor, (play_rect))
            pygame.draw.rect(display, optioncolor, (option_rect))
            display.blit(titleText, (135, 40))
            display.blit(playText, (250, 300))
            display.blit(controlsText, (250, 400))

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if play_rect.collidepoint(mouse_x, mouse_y):
                playcolor = highlightcolor
                on_play = True
            else:
                playcolor = backgroundColor
                on_play = False
            if option_rect.collidepoint(mouse_x, mouse_y):
                optioncolor = highlightcolor
                on_options = True
            else:
                optioncolor = backgroundColor
                on_options = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if(on_play == True) and (playclicked == True):
                            #ammunition, ammunition1, score, health, enmies, centerx, centery, ammo, health kits, clickbullets, bullets, music seconds,
                            Game.main(Game(), 45, 45, 0, 100, enemy_track, 400, 300, ammo_track, health_kit_track, player_bullet_click_track, player_bullet_track, 0)
                        if (on_options == True) and (optionsclicked == True):
                            Controls.main(Controls())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if(on_play == True):
                            playclicked = True
                        elif(on_options == True):
                            optionsclicked = True
                        else:
                            playclicked = False
                            optionsclicked = False
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

class Controls:
    def main(self):
        playerColor = (119, 131, 225, 65)
        clock = pygame.time.Clock()
        dt = clock.tick(60) / 1000
        timer = 0
        lastDirection = "right"

        class Player:
            def __init__(self, x, y, width, height, full_health, player_color):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.speed = 0.3
                self.target_x = x
                self.target_y = y
                self.easing = 1
                self.timer = 0
                self.health = full_health
                self.color = "blue"
                self.dead = False

            def update(self, dt):
                dx = self.target_x - self.x
                dy = self.target_y - self.y

                self.x += dx * self.easing
                self.y += dy * self.easing

                if self.x < 0:
                    self.x = 0
                    self.target_x = self.x
                elif self.x > width - self.width:
                    self.x = width - self.width
                    self.target_x = self.x

                if self.y < 0:
                    self.y = 0
                    self.target_y = self.y
                elif self.y > 280:
                    self.y = 280
                    self.target_y = self.y

                player_rect = self.get_rect()
                self.timer -= 1

            def main(self, display):
                if ((self.timer <= 0) or ((((self.timer % 2 == 0) and (self.timer < 20)) or (((self.timer % 3 == 0) and (self.timer > 20)))) and (self.timer > 0))) and (self.health > 0):
                    pygame.draw.rect(display, playerColor, (self.x, self.y, self.width, self.height))

            def get_rect(self):
                return pygame.Rect(self.x, self.y, self.width, self.height)

            def bullet_recoil_click(self, mouse_x, mouse_y, direction, factor):
                if ((mouse_x > self.x) and (((mouse_y - self.y) >= 0) and (mouse_y - self.y) <= 50)):
                    direction = "right"
                if ((mouse_x < self.x) and (((mouse_y - self.y) >= 0) and (mouse_y - self.y) <= 50)):
                    direction = "left"
                if ((mouse_y < self.y) and (((mouse_x - self.x) >= 0) and (mouse_x - self.x) <= 30)):
                    direction = "up"
                if ((mouse_y > self.y) and (((mouse_x - self.x) >= 0) and (mouse_x - self.x) <= 30)):
                    direction = "down"
                if (((mouse_x - self.x) <= -30) and (mouse_y < self.y)):
                    direction = "upleft"
                if (((mouse_x - self.x) >= 30) and (mouse_y < self.y)):
                    direction = "upright"
                if (((mouse_x - self.x) <= -30) and ((mouse_y - self.y) >= 40)):
                    direction = "downleft"
                if (((mouse_x - self.x) >= 30) and ((mouse_y - self.y) >= 40)):
                    direction = "downright"

                if (direction == "left"):
                    self.target_x += self.speed * factor
                elif (direction == "right"):
                    self.target_x -= self.speed * factor
                elif (direction == "up"):
                    self.target_y += self.speed * factor
                elif (direction == "down"):
                    self.target_y -= self.speed * factor
                elif (direction == "upleft"):
                    self.target_y += self.speed * factor / 1.9
                    self.target_x += self.speed * factor / 1.9
                elif (direction == "upright"):
                    self.target_y += self.speed * factor / 1.9
                    self.target_x -= self.speed * factor / 1.9
                elif (direction == "downleft"):
                    self.target_y -= self.speed * factor / 1.9
                    self.target_x += self.speed * factor / 1.9
                elif (direction == "downright"):
                    self.target_y -= self.speed * factor / 1.9
                    self.target_x -= self.speed * factor / 1.9

            def move_left(self):
                self.target_x -= self.speed

            def move_left_up(self):
                self.target_x -= self.speed
                self.target_y -= self.speed / 1.7

            def move_right(self):
                self.target_x += self.speed

            def move_right_up(self):
                self.target_x += self.speed
                self.target_y -= self.speed / 1.7

            def move_up(self):
                self.target_y -= self.speed

            def move_down(self):
                self.target_y += self.speed

            def move_left_down(self):
                self.target_x -= self.speed
                self.target_y += self.speed / 1.7

            def move_right_down(self):
                self.target_x += self.speed
                self.target_y += self.speed / 1.7

        player = Player(380, 162, 32, 42, 100, playerColor)


        arrowx = 50
        arrowy = 0

        wasdx = 410
        wasdy = 0

        keyfont = pygame.font.SysFont("Verdana", 65)
        titlefont = pygame.font.SysFont("Verdana", 80)
        #x, y, width, height
        left_box_rect_fill = pygame.Rect(58 + arrowx, 502 + arrowy, 65, 65)
        left_box_rect = pygame.Rect(58 + arrowx, 502 + arrowy, 65, 65)
        center_box_rect_fill = pygame.Rect(135 + arrowx, 502 + arrowy, 65, 65)
        center_box_rect = pygame.Rect(135 + arrowx, 502 + arrowy, 65, 65)
        top_center_box_rect_fill = pygame.Rect(135 + arrowx, 422 + arrowy, 65, 65)
        top_center_box_rect = pygame.Rect(135 + arrowx, 422 + arrowy, 65, 65)
        right_box_rect_fill = pygame.Rect(212 + arrowx, 502 + arrowy, 65, 65)
        right_box_rect = pygame.Rect(212 + arrowx, 502 + arrowy, 65, 65)
        z_box_rect_fill = pygame.Rect(0 + arrowx, 340 + arrowy, 65, 65)
        z_box_rect = pygame.Rect(0 + arrowx, 340 + arrowy, 65, 65)
        x_box_rect_fill = pygame.Rect(75 + arrowx, 340 + arrowy, 65, 65)
        x_box_rect = pygame.Rect(75 + arrowx, 340 + arrowy, 65, 65)

        left_box_rect_fill1 = pygame.Rect(58 + wasdx, 502 + wasdy, 65, 65)
        left_box_rect1 = pygame.Rect(58 + wasdx, 502 + wasdy, 65, 65)
        center_box_rect_fill1 = pygame.Rect(135 + wasdx, 502 + wasdy, 65, 65)
        center_box_rect1 = pygame.Rect(135 + wasdx, 502 + wasdy, 65, 65)
        top_center_box_rect_fill1 = pygame.Rect(135 + wasdx, 422 + wasdy, 65, 65)
        top_center_box_rect1 = pygame.Rect(135 + wasdx, 422 + wasdy, 65, 65)
        right_box_rect_fill1 = pygame.Rect(212 + wasdx, 502 + wasdy, 65, 65)
        right_box_rect1 = pygame.Rect(212 + wasdx, 502 + wasdy, 65, 65)
        mouse_rect = pygame.Rect(275 + wasdx, 340 + wasdy, 65, 100)
        mouse_rect_hor = pygame.Rect(275 + wasdx, 375 + wasdy, 65, 5)
        mouse_rect_vert = pygame.Rect(306 + wasdx, 340 + wasdy, 5, 37)

        mainmenucolor = (26, 100, 64, 25)
        resumecolor = backgroundColor
        buttonPressColorLeft = backgroundColor
        buttonPressColorRight = backgroundColor
        buttonPressColorUp = backgroundColor
        buttonPressColorDown = backgroundColor
        buttonPressColorZ = backgroundColor
        buttonPressColorX = backgroundColor

        buttonPressColorA = backgroundColor
        buttonPressColorD = backgroundColor
        buttonPressColorW = backgroundColor
        buttonPressColorS = backgroundColor

        HOVER_TIME = pygame.USEREVENT + 1
        pygame.time.set_timer(HOVER_TIME, 3)

        while True:

            display.fill(backgroundColor)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            pygame.draw.rect(display, buttonPressColorLeft, (left_box_rect_fill), 0, 5)
            pygame.draw.rect(display, buttonPressColorDown, (center_box_rect_fill), 0, 5)
            pygame.draw.rect(display, buttonPressColorRight, (right_box_rect_fill), 0, 5)
            pygame.draw.rect(display, buttonPressColorUp, (top_center_box_rect_fill), 0, 5)
            pygame.draw.rect(display, buttonPressColorZ, (z_box_rect_fill), 0, 5)
            pygame.draw.rect(display, buttonPressColorX, (x_box_rect_fill), 0, 5)

            pygame.draw.rect(display, buttonPressColorA, (left_box_rect_fill1), 0, 5)
            pygame.draw.rect(display, buttonPressColorS, (center_box_rect_fill1), 0, 5)
            pygame.draw.rect(display, buttonPressColorD, (right_box_rect_fill1), 0, 5)
            pygame.draw.rect(display, buttonPressColorW, (top_center_box_rect_fill1), 0, 5)


            upArrow = keyfont.render("^", 1, (255, 255, 255))
            downArrow = keyfont.render("v", 1, (255, 255, 255))
            rightArrow = keyfont.render(">", 1, (255, 255, 255))
            leftArrow = keyfont.render("<", 1, (255, 255, 255))
            zKey = keyfont.render("z", 1, (255, 255, 255))
            xKey = keyfont.render("x", 1, (255, 255, 255))
            display.blit(upArrow, (141 + arrowx, 420 + arrowy))
            display.blit(downArrow, (149 + arrowx, 485 + arrowy))
            display.blit(rightArrow, (219 + arrowx, 490 + arrowy))
            display.blit(leftArrow, (62 + arrowx, 490 + arrowy))
            display.blit(zKey, (15 + arrowx, 325 + arrowy))
            display.blit(xKey, (89 + arrowx, 325 + arrowy))

            pygame.draw.rect(display, (255, 255, 255), (left_box_rect), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (center_box_rect), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (right_box_rect), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (top_center_box_rect), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (z_box_rect), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (x_box_rect), 5, 5)

            wKey = keyfont.render("w", 1, (255, 255, 255))
            sKey = keyfont.render("s", 1, (255, 255, 255))
            dKey = keyfont.render("d", 1, (255, 255, 255))
            aKey = keyfont.render("a", 1, (255, 255, 255))

            display.blit(wKey, (140 + wasdx, 407 + wasdy))
            display.blit(sKey, (149 + wasdx, 487 + wasdy))
            display.blit(dKey, (222 + wasdx, 490 + wasdy))
            display.blit(aKey, (70 + wasdx, 487 + wasdy))
            pygame.draw.rect(display, (255, 255, 255), (mouse_rect), 5, 50)
            pygame.draw.rect(display, (255, 255, 255), (mouse_rect_hor))
            pygame.draw.rect(display, (255, 255, 255), (mouse_rect_vert))

            pygame.draw.rect(display, (255, 255, 255), (left_box_rect1), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (center_box_rect1), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (right_box_rect1), 5, 5)
            pygame.draw.rect(display, (255, 255, 255), (top_center_box_rect1), 5, 5)

            player.main(display)
            player.update(dt)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("X POS: " + str(mouse_x))
                        print("Y POS: " + str(mouse_y))
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_LEFT]):
                buttonPressColorLeft = (28, 52, 151)
            else:
                buttonPressColorLeft = backgroundColor
            if (keys[pygame.K_RIGHT]):
                buttonPressColorRight = (28, 52, 151)
            else:
                buttonPressColorRight = backgroundColor
            if (keys[pygame.K_DOWN]):
                buttonPressColorDown = (28, 52, 151)
            else:
                buttonPressColorDown = backgroundColor
            if (keys[pygame.K_UP]):
                buttonPressColorUp = (28, 52, 151)
            else:
                buttonPressColorUp = backgroundColor
            if (keys[pygame.K_z]):
                buttonPressColorZ = (28, 52, 151)
            else:
                buttonPressColorZ = backgroundColor
            if (keys[pygame.K_x]):
                buttonPressColorX = (28, 52, 151)
            else:
                buttonPressColorX = backgroundColor
            if (keys[pygame.K_w]):
                buttonPressColorW = (28, 52, 151)
            else:
                buttonPressColorW = backgroundColor
            if (keys[pygame.K_a]):
                buttonPressColorA = (28, 52, 151)
            else:
                buttonPressColorA = backgroundColor
            if (keys[pygame.K_s]):
                buttonPressColorS = (28, 52, 151)
            else:
                buttonPressColorS = backgroundColor
            if (keys[pygame.K_d]):
                buttonPressColorD = (28, 52, 151)
            else:
                buttonPressColorD = backgroundColor

            if ((keys[pygame.K_UP] or keys[pygame.K_w]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s]))):
                player.move_up()
                lastDirection = "up"
            if ((keys[pygame.K_UP] or keys[pygame.K_w]) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s])))):
                player.move_left_up()
                lastDirection = "upleft"
            if ((keys[pygame.K_UP] or keys[pygame.K_w]) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s])))):
                player.move_right_up()
                lastDirection = "upright"
            if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not (keys[pygame.K_UP] or keys[pygame.K_w]))):
                player.move_down()
                lastDirection = "down"
            if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (not (keys[pygame.K_UP] or keys[pygame.K_w])))):
                player.move_left_down()
                lastDirection = "downleft"
            if ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (not (keys[pygame.K_UP] or keys[pygame.K_w])))):
                player.move_right_down()
                lastDirection = "downright"
            if ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not (keys[pygame.K_UP] or keys[pygame.K_w])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s])) and (not (keys[pygame.K_RIGHT] or keys[pygame.K_d]))):
                player.move_left()
                lastDirection = "left"
            if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not (keys[pygame.K_UP] or keys[pygame.K_w])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s])) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a]))):
                player.move_right()
                lastDirection = "right"
            if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                if (lastDirection == "right"):
                    player.move_right()
                if (lastDirection == "left"):
                    player.move_left()
                if (lastDirection == "up"):
                    player.move_up()
                if (lastDirection == "down"):
                    player.move_down()
                if (lastDirection == "downleft"):
                    player.move_left_down()
                if (lastDirection == "downright"):
                    player.move_right_down()
                if (lastDirection == "upleft"):
                    player.move_left_up()
                if (lastDirection == "upright"):
                    player.move_right_up()
            if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s]))):
                if (lastDirection == "right"):
                    player.move_right()
                if (lastDirection == "left"):
                    player.move_left()
                if (lastDirection == "up"):
                    player.move_up()
                if (lastDirection == "down"):
                    player.move_down()
                if (lastDirection == "downleft"):
                    player.move_left_down()
                if (lastDirection == "downright"):
                    player.move_right_down()
                if (lastDirection == "upleft"):
                    player.move_left_up()
                if (lastDirection == "upright"):
                    player.move_right_up()
            if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not (keys[pygame.K_UP] or keys[pygame.K_w])) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                if (lastDirection == "right"):
                    player.move_right()
                if (lastDirection == "left"):
                    player.move_left()
                if (lastDirection == "up"):
                    player.move_up()
                if (lastDirection == "down"):
                    player.move_down()
                if (lastDirection == "downleft"):
                    player.move_left_down()
                if (lastDirection == "downright"):
                    player.move_right_down()
                if (lastDirection == "upleft"):
                    player.move_left_up()
                if (lastDirection == "upright"):
                    player.move_right_up()
            if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (not (keys[pygame.K_LEFT] or keys[pygame.K_a])) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                if (lastDirection == "right"):
                    player.move_right()
                if (lastDirection == "left"):
                    player.move_left()
                if (lastDirection == "up"):
                    player.move_up()
                if (lastDirection == "down"):
                    player.move_down()
                if (lastDirection == "downleft"):
                    player.move_left_down()
                if (lastDirection == "downright"):
                    player.move_right_down()
                if (lastDirection == "upleft"):
                    player.move_left_up()
                if (lastDirection == "upright"):
                    player.move_right_up()
            if ((not (keys[pygame.K_RIGHT] or keys[pygame.K_d])) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s])):
                if (lastDirection == "right"):
                    player.move_right()
                if (lastDirection == "left"):
                    player.move_left()
                if (lastDirection == "up"):
                    player.move_up()
                if (lastDirection == "down"):
                    player.move_down()
                if (lastDirection == "downleft"):
                    player.move_left_down()
                if (lastDirection == "downright"):
                    player.move_right_down()
                if (lastDirection == "upleft"):
                    player.move_left_up()
                if (lastDirection == "upright"):
                    player.move_right_up()
            if ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (not (keys[pygame.K_UP] or keys[pygame.K_w])) and (not (keys[pygame.K_DOWN] or keys[pygame.K_s]))):
                if (lastDirection == "right"):
                    player.move_right()
                if (lastDirection == "left"):
                    player.move_left()





MainMenu.main(MainMenu(), False)
