# def input(self):
#     keys = pg.key.get_pressed()
#     self.direction.x = 0
#     self.direction.y = 0
#
#     if keys[Keyboard.UP[0]] or keys[Keyboard.UP[1]]:
#         self.direction.y = -1
#         self.direction_state = DirEnum.UP
#
#     if keys[Keyboard.DOWN[0]] or keys[Keyboard.DOWN[1]]:
#         self.direction.y = 1
#         self.direction_state = DirEnum.DOWN
#
#     if keys[Keyboard.LEFT[0]] or keys[Keyboard.LEFT[1]]:
#         self.direction.x = -1
#         self.direction_state = DirEnum.LEFT
#
#     if keys[Keyboard.RIGHT[0]] or keys[Keyboard.RIGHT[1]]:
#         self.direction.x = 1
#         self.direction_state = DirEnum.RIGHT
#
# def c_s(self, sprite: pg.sprite.Sprite):
#     length, angel = 2, 0.2
#     sprite_mask = pg.mask.from_surface(pg.transform.flip(sprite.image, False, True)).outline()
#     points = np.array([(x + y * length * angel + sprite.rect.x - self.offset.x,
#                         y - y * length + sprite.rect.bottomleft[1] - 6 - self.offset.y) for x, y in sprite_mask])
#     pygame.gfxdraw.filled_polygon(self.display_surface, points, (10, 0, 60, 50))
#
# def create_shadow(sprite: pg.sprite.Sprite):
#     length, angel = 2, 0.2
#     sprite_mask = pg.mask.from_surface(pg.transform.flip(sprite.image, False, True)).outline()
#     points = [(x + y * length * angel + sprite.rect.x,
#                y - y * length + sprite.rect.bottomleft[1] - 6) for x, y in sprite_mask]
#     lx, ly = zip(*points)
#     min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
#     target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
#     shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
#     pg.draw.polygon(shape_surf, (10, 0, 40, 50), [(x - min_x, y - min_y) for x, y in points])
#     return target_rect, shape_surf
#
# def create_shadow_1(self, sprite: pg.sprite.Sprite):
#     length, angel = 2, 0.2
#     sprite_mask = pg.mask.from_surface(pg.transform.flip(sprite.image, False, True)).outline()
#     points = [(x + y * length * angel + sprite.rect.x - self.offset.x,
#                y - y * length + sprite.rect.bottomleft[1] - self.offset.y - 6) for x, y in sprite_mask]
#     return points
#
# def draw_shadow_1(self, points):
#     lx, ly = zip(*points)
#     min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
#     target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
#     shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
#     pg.draw.polygon(shape_surf, (10, 0, 40, 50), [(x - min_x, y - min_y) for x, y in points])
#     self.display_surface.blit(shape_surf, target_rect)
#
# def create_shadow_2(self, sprite: pg.sprite.Sprite):
#     color_key = sprite.image.get_colorkey()
#     transparent = color_key if color_key else (0, 0, 0, 0)
#     shadow_strips = []
#     multiply = sprite.rect.height // Config.TITLE_SIZE
#
#     for j in range(sprite.rect.height - 1, 0, -1):
#         strip = pg.Surface((sprite.rect.width, 1)).convert_alpha()
#         strip.fill((0, 0, 0, 0))
#         for i in range(sprite.rect.width):
#             pixel = sprite.image.get_at((i, j))
#             if pixel != transparent:
#                 alpha = min(j, 100)
#                 strip.set_at((i, 0), (10, 0, 20, alpha))
#         shadow_strips.append([strip, Vector2(sprite.rect.x + 38 * multiply,
#                                              sprite.rect.y)])
#     return shadow_strips[::-1]
#
# def draw_shadow_2(self, shadow_strips: list):
#     for i, strip in enumerate(shadow_strips):
#         pos = (strip[1].x - i * 0.6 - self.offset.x,
#                strip[1].y + i - self.offset.y)
#         self.display_surface.blit(strip[0], pos)
