from PIL import Image, ImageDraw, ImageFont
import datetime
import calendar
import os

from ruamel import yaml

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text_string)
    return width, baseline

def load_events(events_file_name = 'events.yaml'):
    if os.path.exists(events_file_name):
        with open(events_file_name, 'r') as file:
            return yaml.load(file, Loader=yaml.RoundTripLoader)
    return

def cross_out_date(draw, x0, y0, x1, y1, cross_color = 'red'):
    draw.line([(x0, y0), (x1, y1)], fill=cross_color, width=2)
    draw.line([(x0, y1), (x1, y0)], fill=cross_color, width=2)

def generate_year_calendar(year, cell_size=40):
    now = datetime.datetime.now()

    # Create a blank image
    # Dark Theme
    # bkg_color = "black"
    # text_color = "white"
    # cross_color = "red"
    # Light Theme
    bkg_color = "white"
    text_color = "black"
    cross_color = "red"
    page_padding = cell_size
    cal_width = 8 * cell_size
    cal_height = 9 * cell_size * 4 # Four rows of months
    image = Image.new("RGB", (cal_width * 3 + page_padding, cal_height + page_padding), bkg_color)
    draw = ImageDraw.Draw(image)
    base_font_size = int(cell_size * 0.5)
    font = ImageFont.truetype('arial.ttf', base_font_size)
    titles_font = ImageFont.truetype('arial.ttf', int(base_font_size * 1.3))

    # Load evemts from file
    events = load_events()

    year_width, year_height = get_text_dimensions(str(year), font)
    year_padding = (cal_width * 3 - year_width) // 2
    draw.text((year_padding, page_padding // 4), str(year), fill=text_color, font=titles_font)
    
    for month_num in range(1, 13):
        row = (month_num - 1) // 3
        col = (month_num - 1) % 3
        month_calendar = calendar.monthcalendar(year, month_num)
        
        month_name = calendar.month_name[month_num]
        text_width, text_height = get_text_dimensions(month_name, font)
        month_name_padding = (cal_width - text_width) // 2
        
        draw.text((col * cal_width + month_name_padding, row * cal_height // 4 + page_padding), month_name, fill=text_color, font=titles_font)
        
        weekdays = calendar.weekheader(2).split()
        for weekday_num, weekday in enumerate(weekdays):
            x0 = page_padding + col * cal_width + weekday_num * cell_size
            y0 = page_padding + row * cal_height // 4 + cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            
            draw.rectangle([x0, y0, x1, y1], outline="black")
            draw.text((x0 + cell_size // 2, y0 + cell_size // 2), weekday, fill=text_color, anchor="mm", font=font)
        
        for week_num, week in enumerate(month_calendar):
            for day_num, day in enumerate(week):
                x0 = page_padding + col * cal_width + day_num * cell_size
                y0 = page_padding + row * cal_height // 4 + (week_num + 2) * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                if day == 0:
                    continue  # Empty day cell (not part of the current month)

                current_date = datetime.date(year, month_num, day)

                if events:
                    for event in events:
                        if event['date'] == current_date:
                            draw.rectangle([x0, y0, x1, y1], outline="black", fill = event['color'] if 'color' in event else 'lightskyblue')
                            break

                if current_date < datetime.date.today():
                    cross_out_date(draw, x0, y0, x1, y1, cross_color)

                draw.rectangle([x0, y0, x1, y1], outline="black")
                draw.text((x0 + cell_size // 2, y0 + cell_size // 2), str(day), fill=text_color, anchor="mm", font=font)
        
    return image

if __name__ == "__main__":
    current_year = datetime.datetime.now().year

    calendar_image = generate_year_calendar(current_year)
    calendar_image.save("current_year_calendar.png")
    print("Calendar saved as 'current_year_calendar.png'")
