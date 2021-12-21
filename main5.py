import pygame
import numpy as np

pygame.init()

##color definitions
white = (255,255,255)
black = (0,0,0)
dark_grey = (60,60,60)
grey = (128, 128, 128)
light_grey = (200, 200, 200)

#Tile construction

class Tile:
    def __init__(
        self,
        walkable: bool,
        transparent: bool,
        color_notseen: (int, int, int),
        color_seen: (int,int,int),
        color_fade: (int,int,int),
        contains: [] ##<--BUGSPOT
        ):

        self.walkable = walkable
        self.transparent = transparent
        self.color_notseen = color_notseen
        self.color_seen = color_seen
        self.color_fade = color_fade
        self.contains = []

def new_tile(tile_type):
    if tile_type == "floor":
        tile = Tile(
            walkable = True,
            transparent = True,
            color_notseen = black,
            color_seen = light_grey,
            color_fade = (128,128,200),
            contains = []
            )
        return tile
    elif tile_type == "wall":
        tile = Tile(
            walkable = False,
            transparent = False,
            color_notseen = black,
            color_seen = grey,
            color_fade = (200,200,255),
            contains = []
            )
        return tile

class Game_Map:
    def __init__(self, tilewidth: int, tileheight: int, width: int, height: int, view_x: int, view_y: int):
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.mapwidth = width
        self.mapheight = height
        self.view_x = view_x
        self.view_y = view_y

        self.tiles = np.full((width, height), fill_value = new_tile("floor"), order = "F")

        self.tiles[5:8, 10] = new_tile("wall")

    def in_bounds(self, x:int, y:int) -> bool:
        return 0 <= x < self.width and o <= y < self.height

    def render(self, screen, x_start, y_start):
        xstep = -self.tilewidth
        ystep = 0
        for x in (self.tiles):
            ystep = -self.tileheight
            xstep += self.tilewidth
            for y in x:
                ystep += self.tileheight
                salsa = pygame.Rect(
                    ((x_start + xstep),
                    (y_start + ystep)),
                    (self.tilewidth - 1,
                    self.tileheight - 1)
                    )
                pygame.draw.rect(
                    surface = screen,
                    color = y.color_seen,
                    rect = salsa
                    )
                if y.contains is not []:
                    for contained_object in y.contains:
                        contained_object.draw(screen, salsa)
                
class Actor:
    def __init__(
        self,
        actor_color: (int, int, int),
        start_location: (int, int),
        game_map
        ):
        
        self.color = actor_color
        self.location = start_location
        x, y = self.location
        game_map.tiles[x,y].contains.append(self)

### draw function is now fed rectangle object from the game_map render function
    def draw(self,screen,rectangle):
        pygame.draw.rect(
            surface = screen,
            color = self.color,
            rect = rectangle)

    def move(self, dx: int, dy: int, game_map):
#        self.actor_rect = self.actor_rect.move(dx, dy)
        x,y = self.location

        game_map.tiles[self.location].contains.remove(self)
        self.location = (x+dx, y+dy)
        print(self.location)
        game_map.tiles[self.location].contains.append(self)

                    
def main():
    running = True
    screen = pygame.display.set_mode((600,300))
    screen.fill(white)
    width, height = 20, 20
    view_radius = 10
    tilewidth, tileheight = 10, 10 #pixel size for tiles
    game_map = Game_Map(
        tilewidth = tilewidth,
        tileheight = tileheight,
        width = width,
        height = height,
        view_x = view_radius,
        view_y = view_radius
        )
    player = Actor((255,0,0), (5,5), game_map)
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, 1, game_map)
                if event.key == pygame.K_DOWN:
                    player.move(0, -1, game_map)
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0, game_map)
                if event.key == pygame.K_RIGHT:
                    player.move(1,0, game_map)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    running = False
            screen.fill(white)
            game_map.render(screen, 10, 10)
            pygame.display.flip()

if __name__ == "__main__":
    main()


#blankspace for comfort viewing






























    
    
