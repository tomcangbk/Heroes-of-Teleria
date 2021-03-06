import pygame, hero, human, party, button, imagebutton, random, battlescene, time
from globalvars import *
from pygame.locals import *
class HeroCreationScreen():
    def __init__(self, surface):
        self.textColor = (0,0,0)
        self.backgroundColor = (128,128,128)
        self.surface = surface
        self.keysPressed = []
        self.ismain = True
        self.heroes = 1
        self.drawtoolTip = False
        self.tooltipPos = (0,0)
        self.initVariables()
        self.mainLoop()
    def initVariables(self):
        self.spriteIndex = 0
        self.lastTime = 0
        self.party = party.Party(1)
        self.party.addHero(self.makeHero())
        self.bgimage = pygame.transform.scale2x(pygame.image.load("images/panel_blue.png"))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.addHeroButton = button.Button(self.makeText("Add Hero"), self.addHero, tooltipName="Add Hero", tooltipText="Add a new hero to the grid above. Maximum 6 heroes.")
        self.addHeroButton.setRect(pygame.Rect(self.surface.get_rect().width - 100, self.surface.get_rect().height - 50, 100, 50))
        self.toBattleButton = button.Button(self.makeText("To Battle!"), tooltipName="Go to Battle", tooltipText="Bring the heroes above into battle against the AI.")
        self.toBattleButton.setRect(pygame.Rect(self.surface.get_rect().width - 200,self.surface.get_rect().height - 50,100,50))
    def addHero(self):
        if self.heroes <= 6:
            self.party.addHero(self.makeHero())
    def makeText(self, text):
        return self.font.render(text, True, self.textColor)
    def makeHero(self):
        h = hero.Hero(self.heroes, random.choice(NAMES), heroclass = random.choice(CLASSES), race = random.choice(RACES))
        self.heroes = self.heroes + 1
        return h
    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                for x in self.nameButtons + [self.toBattleButton, self.addHeroButton] + self.levelUpButtons:
                    if x.collidepoint(event.pos):
                        self.drawtoolTip = True
                        self.tooltipPos = event.pos
                        break
                    self.drawtoolTip = False
            if event.type == MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                if len(self.keysPressed)> 0:
                    self.keysPressed.pop()
                if self.addHeroButton.getRect().collidepoint(event.pos):
                    self.addHeroButton.callBack()
                elif self.toBattleButton.getRect().collidepoint(event.pos):
                    b = battlescene.BattleScene(self.surface, self.party)
                else:
                    for x in range(len(self.nameButtons)):
                        if self.nameButtons[x].getRect().collidepoint((mx,my)) and not self.levelUpButtons[x].getRect().collidepoint((mx,my)):
                            self.nameButtons[x].callBack()
                        elif self.levelUpButtons[x].getRect().collidepoint((mx,my)):
                            self.levelUpButtons[x].callBack()
            if event.type == QUIT:
                pygame.quit()
    def mainLoop(self):
        while self.ismain == True:
            self.createUI()
            self.update()
            self.draw(self.surface)
            self.eventHandler()
            pygame.display.update()
    def update(self):
        pass
                        
    def createUI(self):
        self.bgImages = []
        self.nameButtons = []
        self.hpLabels = []
        self.raceLabels = []
        self.activeClassLabels = []
        self.levelLabels = []
        self.strLabels = []
        self.agiLabels = []
        self.conLabels = []
        self.intLabels = []
        self.wisLabels = []
        self.levelUpButtons = []
        self.manaLabels = []
        self.sprites = []
        for hero in self.party.getHeroes():
            self.bgImages.append(imagebutton.ImageButton(self.bgimage, None))
            b = button.Button(self.makeText(hero.getName()),hero.makeConfigScreen, [self.surface], tooltipName="Hero Configuration", tooltipText="Edit this hero's class and equipped items.")
            b.setRect(pygame.Rect(0,0, 100, 20))
            self.nameButtons.append(b)
            self.manaLabels.append(self.makeText("Max Mana: " + str(hero.getMaxMana())))
            self.hpLabels.append(self.makeText("Max HP: " + str(hero.getMaxHp())))
            self.raceLabels.append(self.makeText("Race: " + hero.getRace().getName()))
            self.activeClassLabels.append(self.makeText("Profession: " + hero.getActiveHeroClass().getName()))
            self.levelLabels.append(self.makeText("Lvl: " + str(hero.getLevel())))
            self.strLabels.append(self.makeText("Str: " + str(hero.getStr())))
            self.agiLabels.append(self.makeText("Agi: " + str(hero.getAgi())))
            self.conLabels.append(self.makeText("Con: " + str(hero.getCon())))
            self.intLabels.append(self.makeText("Int: " + str(hero.getInt())))
            self.wisLabels.append(self.makeText("Wis: " + str(hero.getWis())))
            self.sprites.append(hero.getActiveHeroClass().getD3Sprites())
            self.levelUpButtons.append(button.Button(self.makeText("Level Up"), callBack = hero.levelUp, tooltipName="Level Up!", tooltipText="Level up this hero. The HP and stats will increase. Maximum level of 50."))
    def drawUI(self, surface):
        row = 0
        self.curTime = time.clock()


        for x in range(len(self.nameButtons)):
            if x != 0  and self.surface.get_rect().width / (x - (row * 4)) <= 200:
                row = row + 1
            self.levelUpButtons[x].setRect(pygame.Rect((x - (row * 4)) * 200 + 100, row * 200 + 145, 75, 40))
            self.bgImages[x].setRect(pygame.Rect((x - (row * 4)) * 200, row * 200, 200, 200))
            for e in self.keysPressed:
                if self.bgImages[x].getRect().collidepoint(e.pos) and not self.levelUpButtons[x].getRect().collidepoint(e.pos):
                    self.bgImages[x].image = pygame.transform.scale(pygame.image.load("images\panelInset_blue.png"), (200,200))
            self.bgImages[x].draw(surface)
            self.nameButtons[x].setRect(pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 10, 75, 20))
            self.nameButtons[x].draw(surface)
            surface.blit(self.raceLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 35, 150, 20))
            surface.blit(self.activeClassLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 50, 150, 20))
            surface.blit(self.hpLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 70, 150, 20))
            surface.blit(self.manaLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 85, 150, 20))
            surface.blit(self.levelLabels[x], pygame.Rect((x - (row * 4)) * 200 + 140, row * 200 + 10, 150, 20))
            surface.blit(self.strLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 100, 150, 20))
            surface.blit(self.agiLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 115, 150, 20))
            surface.blit(self.conLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 130, 150, 20))
            surface.blit(self.intLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 145, 150, 20))
            surface.blit(self.wisLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 160, 150, 20))
            self.levelUpButtons[x].draw(surface)
            surface.blit(self.sprites[x][self.spriteIndex], pygame.Rect((x - (row * 4)) * 200 + 120, row * 200 + 30, 60, 60))
            if self.curTime - self.lastTime > .125:
                if self.spriteIndex >= 5:
                    self.spriteIndex = 0
                else:
                    self.spriteIndex += 1
                self.lastTime = time.clock()
        self.addHeroButton.draw(surface)
        self.toBattleButton.draw(surface)
        if self.drawtoolTip:
            for x in self.nameButtons + self.levelUpButtons + [self.toBattleButton, self.addHeroButton]:
                if x.collidepoint(self.tooltipPos):
                    x.drawToolTip(surface, self.tooltipPos)
    def draw(self, surface):
        surface.fill(self.backgroundColor)
        self.drawUI(surface)
if __name__ == "__main__":
    pygame.init()
    h = HeroCreationScreen(pygame.display.set_mode((800,600)))
