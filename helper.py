import arcade

# Informal interface for all buttons
class Button:
    def __init__(self, buttonList: list):
        buttonList.append(self)  # Puts the button object in a list of buttons
    
    def in_bounds(self, x: float, y: float) -> bool:
        return False
    
    def clicked(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

# Informal interface for all pages
class Page:
    def __init__(self, app):
        self.app = app
        pass

    def setup(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

# Classic button with square background and text
class ClassicButton(Button):
    def __init__(self, buttonList: list, center_x: float, center_y: float, width: float, height: float, text: str, func, color: arcade.Color = arcade.color.BLACK, text_color: arcade.Color = arcade.color.WHITE, font_size: float = 20.0):
        super().__init__(buttonList)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = arcade.Text(text, center_x-width / 2, center_y - font_size / 2, font_size=font_size, align="center", width=width)
        self.func = func
        self.color = color
        self.text_color = text_color

    def in_bounds(self, x: float, y: float) -> bool:
        # Returns true if in bounds given by width, height, center_x, and center_y
        return (self.center_x - self.width / 2 <= x <= self.center_x + self.width / 2) and (self.center_y - self.height / 2 <= y <= self.center_y + self.height / 2)
    
    def clicked(self):
        self.func()

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
        self.text.draw()
