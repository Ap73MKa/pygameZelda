# import game as pg
# from main_scene.player import Player
# from misc.font import *
# from misc.config import get_weapon_data
#
#
# class UI:
#     def __init__(self):
#         self.display_surface = pg.display.get_surface()
#         self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
#         self.health_bar_rect = pg.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
#         self.energy_bar_rect = pg.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
#         self.weapon_graphics: list[pg.image] = [pg.image.load(weapon['graphic']).convert_alpha()
#                                                 for weapon in get_weapon_data().values()]
#
#     def show_bar(self, current: int, max_amount: int, bg_rect: pg.Rect, color: str):
#         pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
#         current_width = bg_rect.width * (current / max_amount)
#         current_rect = bg_rect.copy()
#         current_rect.width = current_width
#         pg.draw.rect(self.display_surface, color, current_rect)
#         pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
#
#     def show_exp(self, exp):
#         text_surf = self.font.render(str(exp), False, TEXT_COLOR)
#         pos = self.display_surface.get_size()
#         text_rect = text_surf.get_rect(bottomright=(pos[0] - 20, pos[1] - 20))
#         pg.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))
#         self.display_surface.blit(text_surf, text_rect)
#         pg.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
#
#     def selection_box(self, left, top, has_switched: bool) -> pg.Rect:
#         bg_rect = pg.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
#         pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
#         border_color = UI_BORDER_COLOR_ACTIVE if has_switched else UI_BORDER_COLOR
#         pg.draw.rect(self.display_surface, border_color, bg_rect, 3)
#         return bg_rect
#
#     def weapon_overlay(self, weapon_index: int, has_switched: bool):
#         bg_rect = self.selection_box(10, 630, has_switched)
#         weapon_surf = self.weapon_graphics[weapon_index]
#         weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
#         self.display_surface.blit(weapon_surf, weapon_rect)
#
#     def display(self, player: Player):
#         self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
#         self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
#         self.show_exp(player.exp)
#         # self.selection_box(85, 635)
#         self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
#
#
