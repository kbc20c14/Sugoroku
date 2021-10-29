import abc
import pygame
from pygame.locals import *

import sys

# 初期化
pygame.init()
# global
screen = pygame.display.set_mode((1280, 640))
clock = pygame.time.Clock()
backImg = pygame.image.load('Grass2_5_32bit.png')  # 座標(0,128,32,32)

# エフェクト表示用のGroup
effect_group = pygame.sprite.Group()

# スクリーン切り替え用変数
ScreenNum = 0

# Set Up Colors
Aqua = (0, 255, 255)
Black = (0, 0, 0)
Blue = (0, 0, 255)
Fuchsia = (255, 0, 255)
Gray = (128, 128, 128)
Green = (0, 128, 0)
Lime = (0, 255, 0)
Maroon = (128, 0, 0)
Navy_Blue = (0, 0, 128)
Olive = (128, 128, 0)
Purple = (128, 0, 128)
Red = (255, 0, 0)
Silver = (192, 192, 192)
Teal = (0, 128, 128)
White = (255, 255, 255)
Yellow = (255, 255, 0)


class ScreenAbc(metaclass=abc.ABCMeta):
    def __init__(self):
        grid = [[0 for j in range(20)] for i in range(40)]
        for i in range(40):
            for j in range(20):
                grid[i][j] = (i * 32, j * 32)
        self.grid = tuple(grid)

        self.Font_L = 'hg創英角ﾎﾟｯﾌﾟ体hgp創英角ﾎﾟｯﾌﾟ体hgs創英角ﾎﾟｯﾌﾟ体'
        self.Font_M = 'yugothicyugothicuisemiboldyugothicuibold'
        self.Font_S = 'simsunnsimsun'
        
        #text_sliceを利用するための変数
        self.slice_number = 0
        self.stringlist_object = ''

        #新規追加effect_group = pygame.sprite.Group()のインスタンス
        self.effect_group = pygame.sprite.Group()

    @abc.abstractmethod
    def display(self):
        pass

    @abc.abstractmethod
    def get_event(self): #get_event
        pass

    def update(self, tick=10):
        self.__draw_effect()
        pygame.display.update()
        clock.tick(tick)

    def __draw_effect(self):
        """
        effect_groupにあるエフェクトクラスのエフェクトを表示する
        privateメソッド
        """
        effect_group.draw(screen)
        effect_group.update()

    def set_background_tile(self, imag, imagePosi=(0, 0, 32, 32)):
        for i in self.grid:
            for j in i:
                screen.blit(imag, j, imagePosi)

    # 1280 640以上のサイズの画像を背景にする
    def set_background_pic(self, imag):
        screen.blit(imag, (0, 0))

    # game_managementで実際に使用する
    def reflect_display(self):
        self.display()
        self.get_event()

    def set_text_l(self, text, position, size, color=White):
        font = pygame.font.SysFont(self.Font_L, size)
        message = font.render(text, False, color)
        screen.blit(message, position)

    def set_text_m(self, text, position, size, color=White):
        font = pygame.font.SysFont(self.Font_M, size)
        message = font.render(text, False, color)
        screen.blit(message, position)

    def set_text_s(self, text, position, size=25, color=White):
        font = pygame.font.SysFont(self.Font_S, size)
        message = font.render(text, False, color)
        screen.blit(message, position)

    # posi:左上の座標(タプル)、widht:boxの横幅,height:boxの高さ,bold：boxの線の太さ
    def set_box(self, color, posi, width, height, bold=1):
        # screenオブジェクト、左上の座標、図形の形(x,y,width,height)
        leftY = posi[1] + height
        rightX = posi[0] + width
        pygame.draw.rect(screen, color, posi + (width, bold))
        pygame.draw.rect(screen, color, posi + (bold, height))
        pygame.draw.rect(screen, color, (rightX, posi[1]) + (bold, height))
        pygame.draw.rect(screen, color, (posi[0], leftY) + (width, bold))

    def set_textbox_s(self, text, textColor, boxColor, posi, width, height, bold=1, size=25, puddingX=10, puddingY=10):
        """
        :param text: text:[文字]
        :param textColor:
        :param boxColor:
        :param posi: (左上の座標)
        :param width:
        :param height:
        :param bold: boxの線の太さ
        :param size:
        :param puddingX: boxの線と一行目の余白 x
        :param puddingY: boxの線と一行目の余白 y
        """
        self.set_box(boxColor, posi, width, height, bold)
        charPosi = (posi[0] + puddingX, posi[1] + puddingY)
        count = 1
        for char in text:
            self.set_text_s(char, charPosi, size, textColor)
            charPosi = (charPosi[0], charPosi[1] + size)
            count += 1

    def add_effect(self, effect_instance: pygame.sprite.Sprite):
        effect_group.add(effect_instance)

    #追加したテキストを一文字ずつ表示する為のメソッド
    def text_slice(self, stringlist):
        #引数がストリングを要素としたリストかどうかを判別、違った場合はExceptionをスローする
        if type(stringlist) == list:

            #第二引数移行に他の型オブジェクトがあった場合エラーが起こる、要修正
            if type(stringlist[0]) == str:

                pass
            
            else:

                raise Exception
        
        else:

            raise Exception
        
        stringlist_tmp = ','.join(stringlist)

        if self.stringlist_object != stringlist_tmp:

            self.stringlist_object = stringlist_tmp

            self.slice_number = 0
        
        retrun_stringlist = self.stringlist_object[0 : self.slice_number].split(',')

        if self.slice_number < len(self.stringlist_object):

            self.slice_number = self.slice_number + 1

        return retrun_stringlist

    #全てのスクリーンに実装すべきイベント
    def get_regular_event(self):

        for event in pygame.event.get():

            if event.type == QUIT:

                pygame.quit()
                sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:

                pygame.quit()
                sys.exit()
            
            pygame.event.post()