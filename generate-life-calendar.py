from PIL import Image, ImageDraw
import datetime

def get_life_weeks(years=80):
    birthdate = datetime.datetime(1983, 9, 29)  # Replace with your birthdate
    current_date = datetime.datetime.now()
    weeks_in_year = 52

    total_weeks = years * weeks_in_year
    passed_weeks = int((current_date - birthdate).days / 7)

    return total_weeks, passed_weeks

def generate_life_calendar(years=80, cell_size=10):
    total_weeks, passed_weeks = get_life_weeks(years)
    grid_size = (years * cell_size, total_weeks // years * cell_size)
    
    image = Image.new("RGB", grid_size, "white")
    draw = ImageDraw.Draw(image)
    
    for week in range(total_weeks):
        row = week // years
        col = week % years
        x0 = col * cell_size
        y0 = row * cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size

        color = "green" if week < passed_weeks else "white"
        draw.rectangle([x0, y0, x1, y1], fill=color, outline="black")
    
    return image

if __name__ == "__main__":
    life_calendar = generate_life_calendar()
    life_calendar.save("life_calendar.png")
    print("Life calendar saved as 'life_calendar.png'")
