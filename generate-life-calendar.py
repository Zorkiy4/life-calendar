from PIL import Image, ImageDraw, ImageFont
import datetime

def get_life_weeks(years=80):
    birthdate = datetime.datetime(1983, 9, 29)  # Replace with your birthdate
    current_date = datetime.datetime.now()
    weeks_in_year = 52

    this_year_birthday = datetime.datetime(datetime.datetime.now().year, birthdate.month, birthdate.day)

    if this_year_birthday > current_date:
        last_birthday = datetime.datetime(datetime.datetime.now().year - 1, birthdate.month, birthdate.day)
    else:
        last_birthday = datetime.datetime(datetime.datetime.now().year, birthdate.month, birthdate.day)

    total_weeks = years * weeks_in_year
    passed_days = (current_date - birthdate).days
    passed_years = last_birthday.year - birthdate.year
    passed_years_in_weeks = passed_years * weeks_in_year
    weeks_since_last_birthday = int((current_date - last_birthday).days / 7)
    passed_weeks = passed_years_in_weeks + weeks_since_last_birthday

    return total_weeks, passed_weeks

def generate_life_calendar(years=80, cell_size=10, index_size=10):
    total_weeks, passed_weeks = get_life_weeks(years)
    weeks_in_year = 52
    
    grid_width = weeks_in_year * cell_size
    grid_height = (years + 1) * cell_size 
    
    index_offset = index_size + 5
    
    image = Image.new("RGB", (grid_width + index_offset, grid_height + index_offset), "white")
    draw = ImageDraw.Draw(image)
    
    for week in range(total_weeks):
        row = week // weeks_in_year
        col = week % weeks_in_year
        x0 = col * cell_size + index_offset
        y0 = row * cell_size + index_offset
        x1 = x0 + cell_size
        y1 = y0 + cell_size

        color = "green" if week < passed_weeks else "white"
        draw.rectangle([x0, y0, x1, y1], fill=color, outline="black")

    # Load a font with the specified size
    font = ImageFont.truetype("arial.ttf", index_size)

    # Add index labels along the top every 5 years
    for col in range(0, weeks_in_year * years, weeks_in_year * 5):
        draw.text((col * cell_size / weeks_in_year + index_offset, 5), str(col // weeks_in_year), fill="black", font=font)

    # Add index labels along the left every 5 weeks
    for row in range(0, total_weeks, 5):
        draw.text((5, row * cell_size / weeks_in_year + index_offset), str(row // weeks_in_year), fill="black", font=font)
    
    return image

if __name__ == "__main__":
    life_calendar = generate_life_calendar()
    life_calendar.save("life_calendar.png")
    print("Life calendar saved as 'life_calendar.png'")
