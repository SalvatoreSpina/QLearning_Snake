import pygame

from config import (BOARD_SIZE, BACKGROUND_COLOR, BUTTON_COLOR,
                    BUTTON_HOVER_COLOR)

pygame.init()
WINDOW_WIDTH = pygame.display.Info().current_w
WINDOW_HEIGHT = pygame.display.Info().current_h


class ConfigScreen:
    def __init__(self, ui, defaults):
        self.ui = ui
        self.font = pygame.font.Font(None, 40)
        self.options = {
            "Board Size": str(defaults.get('board_size', BOARD_SIZE)),
            "Sessions": str(defaults.get('sessions', 1)),
            "Visual": 'on' if defaults.get('visual', True) else 'off',
            "Learn": 'on' if defaults.get('learn', True) else 'off',
            "Speed": defaults.get('speed', 'Normal'),
            "Print Terminal": (
                'on' if defaults.get('print_terminal', True) else 'off'),
            "Step-by-Step": (
                'on' if defaults.get('step_by_step', False) else 'off')
        }
        self.selected_option = 0
        self.option_keys = list(self.options.keys())
        self.active_input = False
        self.input_rects = {}
        self.save_button_rect = pygame.Rect(100, 600, 400, 50)
        self.total_options = len(self.option_keys) + 1

    def display(self):
        if self.ui.visual:
            self.ui.screen.fill(BACKGROUND_COLOR)
            self._render_options()
            self._render_save_button()
            pygame.display.flip()

    def _render_options(self):
        screen_width = self.ui.WINDOW_WIDTH
        y_offset = 70
        _value = len(self.option_keys) * y_offset + self.save_button_rect.height
        y = (self.ui.WINDOW_HEIGHT - _value) // 2

        for i, key in enumerate(self.option_keys):
            color = BUTTON_COLOR
            if i == self.selected_option:
                color = BUTTON_HOVER_COLOR
            rect = pygame.Rect(0, 0, 400, 50)
            rect.centerx = screen_width // 2  # Center horizontally
            rect.y = y
            pygame.draw.rect(self.ui.screen, color, rect, border_radius=10)
            option_text = f"{key}: {self.options[key]}"
            if self.active_input and i == self.selected_option:
                option_text += "|"
            self.ui.render_text(option_text, rect.centerx, rect.centery)
            self.input_rects[key] = rect
            y += y_offset

        self.save_button_rect.y = y

    def _render_save_button(self):
        screen_width = self.ui.WINDOW_WIDTH
        button_color = BUTTON_COLOR
        if self.selected_option == self.total_options - 1:
            button_color = BUTTON_HOVER_COLOR
        self.save_button_rect.centerx = screen_width // 2
        pygame.draw.rect(self.ui.screen, button_color,
                         self.save_button_rect, border_radius=10)
        self.ui.render_text("Save and Start", self.save_button_rect.centerx,
                            self.save_button_rect.centery)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            return self._handle_keyboard_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_event(event)
        return None

    def _handle_keyboard_event(self, event):
        if self.active_input:
            self._update_option_value(event)
        else:
            modulus = self.total_options
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % modulus
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % modulus
            elif event.key == pygame.K_RETURN:
                if self.selected_option < len(self.option_keys):
                    key = self.option_keys[self.selected_option]
                    if key in ["Visual", "Learn", "Print Terminal",
                               "Step-by-Step", "Speed"]:
                        self._toggle_option(key)
                    else:
                        self.active_input = True
                else:
                    # Save and Start button selected
                    self.apply_config()
                    return "back"
        return None

    def _handle_mouse_event(self, event):
        pos = event.pos
        # Check if Save and Start button is clicked
        if self.save_button_rect.collidepoint(pos):
            self.apply_config()
            return "back"
        # Check if any option is clicked
        for i, key in enumerate(self.option_keys):
            rect = self.input_rects.get(key)
            if rect and rect.collidepoint(pos):
                self.selected_option = i
                if key in ["Visual", "Learn", "Print Terminal",
                           "Step-by-Step", "Speed"]:
                    self._toggle_option(key)
                else:
                    self.active_input = True
        return None

    def _toggle_option(self, key):
        if key in ["Visual", "Learn", "Print Terminal", "Step-by-Step"]:
            self.options[key] = "off" if self.options[key] == "on" else "on"
        elif key == "Speed":
            speeds = ["Really Slow", "Slow", "Normal", "Fast"]
            current_index = speeds.index(self.options[key])
            self.options[key] = speeds[(current_index + 1) % len(speeds)]

    def _update_option_value(self, event):
        key = self.option_keys[self.selected_option]
        if event.key == pygame.K_RETURN:
            self.active_input = False
        elif event.key == pygame.K_BACKSPACE:
            self.options[key] = self.options[key][:-1]
        else:
            if key not in ["Visual", "Learn", "Speed",
                           "Print Terminal", "Step-by-Step"]:
                self.options[key] += event.unicode

    def apply_config(self):
        self.ui.board_size = int(self.options["Board Size"])
        self.ui.sessions = int(self.options["Sessions"])
        self.ui.visual = self.options["Visual"] == "on"
        self.ui.learn = self.options["Learn"] == "on"
        self.ui.speed = self.options["Speed"]
        self.ui.print_terminal = self.options["Print Terminal"] == "on"
        self.ui.step_by_step = self.options["Step-by-Step"] == "on"
        if self.ui.visual:
            self.ui.screen = pygame.display.set_mode((WINDOW_WIDTH,
                                                      WINDOW_HEIGHT))
        else:
            self.ui.screen = None
