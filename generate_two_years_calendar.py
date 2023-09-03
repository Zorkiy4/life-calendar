import datetime
from PIL import Image

from generate_life_calendar import generate_life_calendar
from generate_year_calendar import generate_year_calendar

def merge_images(image1, image2, offset_x = 0, offset_y = 0):
    image1_size = image1.size
    new_image = Image.new('RGB',(image1_size[0] + image2.size[0] + offset_x, image1_size[1]), (250,250,250))
    new_image.paste(image1,(0,0))
    new_image.paste(image2,(image1_size[0] + offset_x, offset_y))
    return new_image

cell_size=25

current_year = datetime.datetime.now().year
current_year_calendar_image = generate_year_calendar(current_year, cell_size)

next_year = current_year + 1
next_year_calendar_image = generate_year_calendar(next_year, cell_size)

two_years_image = merge_images(current_year_calendar_image, next_year_calendar_image)

life_calendar = generate_life_calendar()

all_calendars_image = merge_images(two_years_image, life_calendar, offset_y = 40)

all_calendars_image.save("my_life_calendar.png")
all_calendars_image.show()