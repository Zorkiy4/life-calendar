import datetime
from PIL import Image

from generate_life_calendar import generate_life_calendar
from generate_year_calendar import generate_year_calendar

def merge_images(image1, image2, offset_x = 0, offset_y = 0):
    image1_size = image1.size
    new_image = Image.new('RGB',(image1_size[0] + image2.size[0] + offset_x, image1_size[1]), (255,255,255))
    new_image.paste(image1,(0,0))
    new_image.paste(image2,(image1_size[0] + offset_x, offset_y))
    return new_image

year_calendar_cell_size=25
life_calendar_cell_size=10

current_year = datetime.datetime.now().year
current_year_calendar_image = generate_year_calendar(current_year, year_calendar_cell_size)

next_year = current_year + 1
next_year_calendar_image = generate_year_calendar(next_year, year_calendar_cell_size)

two_years_image = merge_images(current_year_calendar_image, next_year_calendar_image)

life_calendar = generate_life_calendar(cell_size = life_calendar_cell_size, index_size = life_calendar_cell_size)

all_calendars_image = merge_images(two_years_image, life_calendar, offset_y = year_calendar_cell_size * 2)

all_calendars_image.save("my_life_calendar.png")
all_calendars_image.show()