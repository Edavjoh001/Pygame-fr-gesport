import logging
import pygame
import sys
import random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 60
SCREEN_SIZE = (800, 600)
CAPTION = "Pygame Example"

COLOR = {'car': pygame.Color('#DD3333'),
        'bg_pause': pygame.Color('#DD3333'),
        'bg': pygame.Color('#333333'),
        'bg_pause': pygame.Color('#DD3333'),
        'thruster': pygame.Color('#7799FF'),
        'text_color': pygame.Color('#000000'),
}


# Game states
STATE_PREGAME = 1
STATE_RUNNING = 2
STATE_PAUS = 3
STATE_GAMEOVER = 4
STATE_WON = 5



class Controller():
    """Game controller."""

    def __init__(self):
        """Initialize game controller."""
        self.fps = FPS

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self._time = pygame.time.get_ticks()

        self.player = Player(self.screen)
        self.blocks = [Block(self)]
        self.time_to_next_block = 100
        self.time_to_next_level = self.fps * 20
        self.level = 1
        self.a = 1


        # Initialize game state
        self.game_state = STATE_PREGAME
        self.next_state = None

        self.large_text = pygame.font.SysFont("comicsansms",110)


    def run(self):
        """Main game loop."""
        while True:
            if self.next_state:
                self.game_state = self.next_state
                self.next_state = None
                logger.info('Changning state to {}'.format(self.game_state))

            # Hantera event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 or icon in upper right corner.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape key pressed.
                    self.quit()


                # -- Game state PREGAME --------------------------------------
                if self.game_state == STATE_PREGAME:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.next_state = STATE_RUNNING


                # -- Game state RUNNING --------------------------------------
                if self.game_state == STATE_RUNNING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.next_state = STATE_PAUS
                        logger.debug('Pausing')
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.player.turn_right_on()

                if event.type == pygame.KEYUP and event.key == pygame.K_d:
                    self.player.turn_right_off()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    self.player.turn_left_on()

                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    self.player.turn_left_off()

                # -- Game state won ------------------------------------------
                if self.game_state == STATE_WON:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            self.player.reset_car()
                            self.block.reset_blocks()
                            logger.info('Reseting,after winning')


                # -- Game state PAUS -----------------------------------------
                if self.game_state == STATE_PAUS:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.next_state = STATE_RUNNING
                        logger.debug('Unpausing')

                # -- Game state GAMEOVER -------------------------------------
                if self.game_state == STATE_GAMEOVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            self.next_state = STATE_RUNNING
                            self.player.reset_car()
#                            self.block.reset_blocks()
                            self.time_to_next_block = 100
                            self.time_to_next_level = self.fps * 20
                            self.level = 1
                            self.a = 1

                    logger.info('Reseting')



            # Hantera speltillstånd
            if self.game_state == STATE_PREGAME:
                self.screen.fill(COLOR['bg_pause'])
                text = self.large_text.render("Press here to start", True, COLOR['text_color'] )
                pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                        SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                self.screen.blit(text, pos)



            if self.game_state == STATE_RUNNING:
                self.player.tick()
                for block in self.blocks:
                    block.tick()
                self.time_to_next_level -= 1
                if self.time_to_next_level == 0:
                    self.time_to_next_level = self.fps * 30
                    logger.info('Level up')
                    self.level = self.level + 1
                    if self.level == 4:
                        self.game_state = STATE_WON
                    self.a = self.a + 2

                self.time_to_next_block -= 1
                b = -self.a**2 + 90
                if self.time_to_next_block == 0:
                    self.blocks.append(Block(self))


                    self.time_to_next_block = random.randint(self.a, b)


                if self.player.car_y > SCREEN_SIZE[1] - 10 or self.player.car_y < 10:
#                    logger.debug('OUT OF BOUNDS!')
                        self.game_state = STATE_GAMEOVER
                if self.player.car_x > SCREEN_SIZE[0] - 5 or self.player.car_x < 5:
#                    logger.debug('OUT OF BOUNDS!')
                    self.game_state = STATE_GAMEOVER

                self.screen.fill(COLOR['bg'])
                self.player.draw()
                for block in self.blocks:
                    block.draw()

                    if self.player.car_x - block.block_width/2 - self.player.car_width/2 <= block.block_x <=  self.player.car_x + block.block_width/2 + self.player.car_width/2:
                        if self.player.car_y - block.block_length/2 - self.player.car_length/2 <= block.block_y <= self.player.car_y + block.block_length/2 + self.player.car_length/2:
                            #self.game_state = STATE_GAMEOVER
                            logger.info('collision: {}, {}'.format(self.player, block))

            if self.game_state == STATE_WON:
                self.screen.fill(COLOR['bg_pause'])
                text = self.large_text.render("Game won!!|r to reset", True, COLOR['text_color'] )
                pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                        SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                self.screen.blit(text, pos)




            if self.game_state == STATE_PAUS:
                self.screen.fill(COLOR['bg_pause'])
                text = self.large_text.render("Game paused", True, COLOR['text_color'] )
                pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                        SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                self.screen.blit(text, pos)


            if self.game_state == STATE_GAMEOVER:
                        self.screen.fill(COLOR['bg_pause'])
                        text = self.large_text.render("Game over|r to reset", True, COLOR['text_color'] )
                        pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                                SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                        self.screen.blit(text, pos)


                #self.quit()  # Gör nåplayer.car

            pygame.display.flip()

            self.clock.tick(self.fps)


    def quit(self):
        logging.info('Quitting... good bye!')
        pygame.quit()
        sys.exit()

    def paus(self):
        pass

#    def reset(self):
#            #--- resets the game when restarting
#            self.player.car_x = SCREEN_SIZE[0] / 2
#            self.player.car_y = SCREEN_SIZE[1] / 2
#            self.block.block_x = random.randint(0,800)
#            self.block.block_y = SCREEN_SIZE[1] - 620


class Player():
    def __init__(self, screen):
        self.car_x = SCREEN_SIZE[0] / 2
        self.car_y = SCREEN_SIZE[1] / 2
        self.screen = screen
        self.turn_right = 0
        self.turn_left = 0
        self.car_width = 30
        self.car_length = 65

    def draw(self):
        surface = pygame.Surface((30, 65))
        block = pygame.Surface((50, 10))
        screen = pygame.Surface((800, 600))
        surface.fill(COLOR['car'])
        pygame.draw.rect(surface, COLOR['car'],(self.car_width,self.car_length,self.car_width,self.car_length))


        self.screen.blit(surface, (self.car_x - 10, self.car_y - 20))
    def reset_car(self):
            #--- resets the game when restarting
            self.car_x = SCREEN_SIZE[0] / 2
            self.car_y = SCREEN_SIZE[1] / 2



    def tick(self):
        #-- turn x axel
        if self.turn_right:
            self.car_x += 5
        if self.turn_left:
            self.car_x -= 5
    def turn_right_on(self):
        self.turn_right = True
    def turn_right_off(self):
        self.turn_right = False
    def turn_left_on(self):
        self.turn_left = True
    def turn_left_off(self):
        self.turn_left = False

class Block():
    def __init__(self, controller):
        self.block_x = random.randint(0,800)
        self.block_y = SCREEN_SIZE[1] - 620
        self.controller = controller
        self.screen = controller.screen
        self.block_width = 100
        self.block_length = 20


    def draw(self):
        screen = pygame.Surface((800, 600))
        block = pygame.Surface((100, 20))
        pygame.draw.rect(block, COLOR['car'],(self.block_width,self.block_length,self.block_width,self.block_length))

        self.screen.blit(block, (self.block_x - 5, self.block_y - 5))

    def tick(self):
#        if  self.block_time > 1:
        self.block_y = self.block_y + 1

        if self.block_y > 600:
            self.controller.blocks.remove
    def reset_blocks(self):
        #--- resets the game when restarting
#        self.block_x = random.randint(0,800)
        self.block_y = SCREEN_SIZE[1] - 620



if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()
