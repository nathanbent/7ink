from PIL import ImageFont
credentials = ['host_name', 'influxdb_host', 'influxdb_port', 'influxdb_user', 'influxdb_pass', 'influxdb_db']
built_in_credentials = False
credentials_file = "credentials.txt"

def credentials_setup():
    global credentials
    global credentials_file
    try:
        with open(credentials_file) as f:
            credentials = f.read().splitlines()
    except OSError:
        credentials_file_open = open(credentials_file, 'w')
        spot = 0
        for value in credentials:
            input_value = input("What is the " + value + "for this program? ")
            credentials[spot] = input_value
            credentials_file_open.write(input_value + '\n')
            spot += 1
    return credentials

class Prefs:
    # mode = 0  # This controls how the slideshow plays, 0 = Random, 1 = Latest, 2 = Earliest, 3 = Favorites
    clean_cycles = 0  # How many times the screen has been cleaned currently
    saturation = 1  # Controls saturation for the display
    weather_spot = 25  # How many loops in-between weather checks
    bme280_spot = 15  #
    clean_spot = 10  # How many loops in-between cleaning
    clear_spot = 50  # How many loops in-between clearing
    inky_clean_cycles_2_clean = 3  # How many times the inky clean will cycle before its done, 3 is OEM
    running = True  # Main running loop
    display_time = 445  # How long to display images
    weather_works = 0

    current_program_status = 0  # Sets program to not running
    really_big_zoom_pixels = '1200x1200'
    big_zoom_pixels = '900x900'
    square_zoom_pixels = '1200x1200'
    portrait_zoom_pixels = '1200x600'
    current_is_favorite = 0  # Is the current photo a favorite
    current_display_time = 445

    file_path = '/home/pi/imageloop/'  # Path to main program
    image_loop_path = '/home/pi/imageloop/images/'  # Path to image folder
    loop_path = '/home/pi/imageloop/'  # Path to main program?
    ext_path = '/home/pi/ExtHD/Photos/eInk/'  # Path to external source
    ext_image_path = '/home/pi/ExtHD/Photos/eInk/'  # Path to external source
    log_file = "log.txt"  # Log file
    favorites_file = "favorites.txt"  # Favorites file
    min_between_reads = 0

    sys_font_path = "/usr/share/fonts/truetype/"
    small_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Regular.ttf", 20)
    medium_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Medium.ttf", 24)
    large_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Bold.ttf", 30)
    degree_sign = u"\N{DEGREE SIGN}"
    heart_icon_file = "heart.png"
    inky_open_background = "welcome_screen.png"


