from PIL import Image, ImageDraw
import datetime
import calendar

def generate_year_calendar(year, cell_size=40):
    now = datetime.datetime.now()
    current_year = now.year
    
    # Create a blank image
    cal_width = 7 * cell_size
    cal_height = 6 * cell_size * 4  # Four rows of months
    image = Image.new("RGB", (cal_width * 3, cal_height), "white")
    draw = ImageDraw.Draw(image)
    
    for month_num in range(1, 13):
        row = (month_num - 1) // 3
        col = (month_num - 1) % 3
        month_calendar = calendar.monthcalendar(year, month_num)
        
        for week_num, week in enumerate(month_calendar):
            for day_num, day in enumerate(week):
                x0 = col * cal_width + day_num * cell_size
                y0 = row * cal_height // 4 + week_num * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                
                if day == 0:
                    continue  # Empty day cell (not part of the current month)
                
                if year < current_year or (year == current_year and month_num < now.month) or (year == current_year and month_num == now.month and day <= now.day):
                    # Cross out past dates
                    draw.line([(x0, y0), (x1, y1)], fill="red", width=2)
                    draw.line([(x0, y1), (x1, y0)], fill="red", width=2)
                
                draw.rectangle([x0, y0, x1, y1], outline="black")
                draw.text((x0 + cell_size // 2, y0 + cell_size // 2), str(day), fill="black", anchor="mm")
        
    return image

if __name__ == "__main__":
    current_year = datetime.datetime.now().year

    calendar_image = generate_year_calendar(current_year)
    calendar_image.save("current_year_calendar.png")
    print("Calendar saved as 'current_year_calendar.png'")
