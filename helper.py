import arcade

# Class that manages mouse attributes
class Mouse:
    def __init__(self):
        self.up = True
        self.x = 0.0
        self.y = 0.0
    
    def setLocation(self, x, y):
        self.x = x
        self.y = y

# Informal interface for all buttons
class Button:
    def __init__(self, buttonList: list):
        buttonList.append(self)  # Puts the button object in a list of buttons
    
    def in_bounds(self, x: float, y: float) -> bool:
        return False
    
    def clicked(self):
        pass

    def released(self):
        pass

    def update(self, mouse: Mouse):
        pass

    def draw(self):
        pass

# Informal interface for all pages
class Page:
    def __init__(self, app):
        self.app = app
        pass

    def update(self, mouse: Mouse, dt):
        pass

    def draw(self):
        pass

# Classic button with square background and text
class ClassicButton(Button):
    def __init__(self, buttonList: list, center_x: float, center_y: float, width: float, height: float, text: str, func, color: arcade.Color = arcade.color.BLACK, text_color: arcade.Color = arcade.color.WHITE, font_size: float = 20.0, hidden: bool = False):
        super().__init__(buttonList)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = arcade.Text(text, center_x-width / 2, center_y - font_size / 2, font_size=font_size, align="center", width=width)
        self.func = func
        self.color = color
        self.text_color = text_color
        self.hidden = hidden

    def in_bounds(self, x: float, y: float) -> bool:
        # Returns true if in bounds given by width, height, center_x, and center_y
        return not self.hidden and ((self.center_x - self.width / 2 <= x <= self.center_x + self.width / 2) and (self.center_y - self.height / 2 <= y <= self.center_y + self.height / 2))
    
    def clicked(self):
        self.func()

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
        self.text.draw()

# Sprite that will move its position from start to end in a given duration (seconds)
class TimeBasedSprite(arcade.Sprite):
    def __init__(self, filename: str = None, scale: float = 1, start_center_x: float = 0, start_center_y: float = 0, end_center_x: float = 0, end_center_y: float = 0, image_width: float = 0, image_height: float = 0, duration: float = 5):
        super().__init__(filename=filename, scale=scale, image_width=image_width, image_height=image_height, center_x=start_center_x, center_y=start_center_y)
        self.dx = (end_center_x - start_center_x)
        self.dy = (end_center_y - start_center_y)
        self.end_center_x = end_center_x
        self.end_center_y = end_center_y
        self.start_center_x = start_center_x
        self.start_center_y = start_center_y
        self.duration = duration
        self.elapsed_time = 0.0

    def move(self, dt):
        if self.elapsed_time > self.duration:
            return
        
        temp = self.elapsed_time + dt
        if temp > self.duration:
            self.set_position(self.end_center_x, self.end_center_y)
        else:
            self.set_position(self.start_center_x + (self.elapsed_time / self.duration) * self.dx, self.start_center_y + (self.elapsed_time / self.duration) * self.dy)
        self.elapsed_time += dt

    def move_to(self, end_x, end_y, duration):
        self.start_center_x = self.center_x
        self.start_center_y = self.center_y
        self.end_center_x = end_x
        self.end_center_y = end_y
        self.duration = duration
        self.elapsed_time = 0.0
        self.dx = (self.end_center_x - self.start_center_x)
        self.dy = (self.end_center_y - self.start_center_y)

class ProgressBar:
    def __init__(self, x, y, width, height, color, color2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.color2 = color2
        self.progress = 0.0
        self.progress2 = 0.0
        # Progress and color 2 correspond to the partially filled area of the bar

    def on_draw(self):
        # Draws the progress bar frame, then the partially filled area, then the fully filled area
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.WHITE, border_width=2)
        arcade.draw_rectangle_filled(self.x - self.width / 2 * (1-self.progress2), self.y, self.width * self.progress2, self.height, self.color2)
        arcade.draw_rectangle_filled(self.x - self.width / 2 * (1-self.progress), self.y, self.width * self.progress, self.height, self.color)

    def set_progress(self, x):
        if x < 0.0:
            x = 0.0
        elif x > 1.0:
            x = 1.0
        self.progress = x

    def set_progress2(self, x):
        if x < 0.0:
            x = 0.0
        elif x > 1.0:
            x = 1.0
        self.progress2 = x

