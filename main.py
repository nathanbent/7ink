#!/usr/bin/python

#  V .01 - Figured out how to drive display, add date, temperatures
#  V .1 - Lots of updates

#  Want To Do
#  Better InfluxDB
#  Day of week stuff to do
# Graphing

# -*- coding:utf-8 -*-
from __future__ import print_function
import sys
from waveshare_epd import epd7in5_HD
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime, timedelta
import influx_rt
import os.path
import logging

from prefs import Prefs
import matplotlib.pyplot as plt

sleep_time = 60

host_names_24h = []
room_temps_24h = []
time_list_24h = []
last_time_list = []
last_host_names = []
last_room_temps = []
living_room_temp_list = []
server_closet_temp_list = []
living_room_time_list = []
server_closet_time_list = []
server_rack_temp_list = []
server_rack_time_list = []
daniels_room_temp_list = []
daniels_room_time_list = []
nates_room_temp_list = []
nates_room_time_list = []

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

sys_font_path = "/usr/share/fonts/truetype/"
really_small_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Regular.ttf", 14)
small_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Regular.ttf", 18)
small_font_bold = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Bold.ttf", 18)
medium_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Medium.ttf", 24)
large_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Bold.ttf", 40)
really_large_font = ImageFont.truetype(sys_font_path + "Montserrat/Montserrat-Bold.ttf", 50)
running = True
credentials = ['host_name', '10.0.0.12', 8086, 'bme280monitor', 'Subaru15', 'bme280']

Display_total_width = 528  # In portrait mode
Display_total_height = 880  # In portrait mode

# Spacing stuff
date_display_offset = 0
current_weather_offset = 85
forecast_display_offset = 135
server_temps_display_offset = 580
min_max_display_offset = 630
google_calendar_display_offset = 600
Graph_offset = (-35, 680)
public_ip_height_offset = 425
internet_speed_offset = 450
screen_update_text_location = (0, 0)
message_display_offset = (15, 100)

living_room_24h = []
server_closet_temps = []

def convert_last_names():
    global last_host_names
    global last_room_temps
    global last_time_list
    for n, name in enumerate(last_host_names):  # Change names into what I want to call them
        if name == 'RetroPie' or 'Living Room':
            last_host_names[n] = 'Living Room'
        elif name == 'RaspiTest' or 'Server Closet':
            last_host_names[n] = 'Server Closet'
        elif name == 'RaspiZeroW' or "Daniel's Room":
            last_host_names[n] = "Daniel's Room"
        elif name == "Nates Room" or "Nate's Room":
            last_host_names[n] = "Nate's Room"
        elif name == "RaspiMain" or 'Server Rack':
            last_host_names[n] = "Server Rack"
        else:
            print("the hostname " + last_ost_names[n] + " wasn't recognized")

def influx_import():  # Import and break down the information from our influxDB
    # Lots of global variables to import, there should be a better way to do this
    global living_room_temp_list
    global server_closet_temp_list
    global living_room_time_list
    global server_closet_time_list
    global server_rack_temp_list
    global server_rack_time_list
    global daniels_room_temp_list
    global daniels_room_time_list
    global nates_room_temp_list
    global nates_room_time_list
    global host_names_24h
    global room_temps_24h
    global time_list_24h

    host_names_24h, room_temps_24h, time_list_24h = influx_rt.pull_last_24h_influx()  # Pull data from the influx db

    for n, name in enumerate(host_names_24h):  # Change names into what I want to call them
        if name == 'RetroPie' or 'Living Room':
            host_names_24h[n] = 'Living Room'
            # print(room_temps[n])
            if time_list_24h[n] not in living_room_time_list:  # Only add to the list if not already there
                living_room_temp_list.append(room_temps_24h[n])
                living_room_time_list.append(time_list_24h[n])
        elif name == 'RaspiTest' or 'Server Closet':
            host_names_24h[n] = 'Server Closet'
            if time_list_24h[n] not in server_closet_time_list:  # Only add to the list if not already there
                server_closet_temp_list.append(room_temps_24h[n])
                server_closet_time_list.append(time_list_24h[n])
            # print(room_temps[n])
        elif name == 'RaspiZeroW' or "Daniel's Room":
            host_names_24h[n] = "Daniel's Room"
            if time_list_24h[n] not in daniels_room_time_list:  # Only add to the list if not already there
                daniels_room_temp_list.append(room_temps_24h[n])
                daniels_room_time_list.append(time_list_24h[n])
            # print(room_temps[n])
        elif name == "Nates Room" or "Nate's Room":
            host_names_24h[n] = "Nate's Room"
            if time_list_24h[n] not in nates_room_time_list:  # Only add to the list if not already there
                nates_room_temp_list.append(room_temps_24h[n])
                nates_room_time_list.append(time_list_24h[n])
            # print(room_temps[n])
        elif name == "RaspiMain" or 'Server Rack':
            host_names_24h[n] = "Server Rack"
            if time_list_24h[n] not in server_rack_time_list:  # Only add to the list if not already there
                server_rack_temp_list.append(room_temps_24h[n])
                server_rack_time_list.append(time_list_24h[n])
            # print(room_temps[n])
        else:
            print("the hostname " + host_names_24h[n] + " wasn't recognized")


def plot_graph():
    global living_room_temp_list
    global server_closet_temp_list
    global living_room_time_list
    global server_closet_time_list
    global server_rack_temp_list
    global server_rack_time_list
    global daniels_room_temp_list
    global daniels_room_time_list
    global nates_room_temp_list
    global nates_room_time_list

    list_a = server_closet_temp_list  # Make the lists the same length
    list_b = living_room_temp_list  # Make the lists the same length
    list_c = server_closet_time_list  # Make the lists the same length
    list_d = living_room_time_list  # Make the lists the same length

    if len(list_a) < len(list_b):  # Compare length of lists
        list_b = list_b[: len(list_a)]  # Compare length of lists
    elif len(list_a) > len(list_b):  # Compare length of lists
        list_a = list_a[: len(list_b)]  # Compare length of lists
    if len(list_c) < len(list_d):  # Compare length of lists
        list_d = list_d[: len(list_c)]  # Compare length of lists
    elif len(list_c) > len(list_d):  # Compare length of lists
        list_c = list_c[: len(list_d)]  # Compare length of lists

    server_closet_temp_list = list_a  # Make the lists the same length
    living_room_temp_list = list_b  # Make the lists the same length
    server_closet_time_list = list_c  # Make the lists the same length
    living_room_time_list = list_d  # Make the lists the same length

    print(len(server_closet_temp_list), len(living_room_temp_list))  # Show us the list lengths
    print(len(server_closet_time_list), len(living_room_time_list))  # Show us the list lengths

    plt.plot(server_closet_time_list, server_closet_temp_list, color='black', linewidth=1, label='_nolegend_')
    plt.plot(server_closet_time_list, living_room_temp_list, color='black', linewidth=1, linestyle='dashed',
             marker='.')

    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    plt.show()
    # function to show the plot
    plt.savefig('closet_temps.png')


while running is True:

    try:
        epd = epd7in5_HD.EPD()
        display_width = 528  # This eInk is 528 pixels wide in Portrait mode
        display_height = 880  # This eInk is 880 pixels tall in Portrait mode

        # Vertical draw
        Black_Layer = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        Red_Layer = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        NoImageLayer = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw_TextImage_Black = ImageDraw.Draw(Black_Layer)  # White box
        draw_TextImage_Red = ImageDraw.Draw(Red_Layer)  # White box
        # Lines!!
        draw_TextImage_Black.line((0, 20, epd.width, 20), fill=0)  # Line below times
        draw_TextImage_Black.line((0, 600, epd.width, 600), fill=0)  # Line below times
        # Time text
        now = datetime.now()  # Load the current time to show on display
        date_text = now.strftime("%A, %B, %d")  # The date text
        # All the temperature and name stuff below
        draw_TextImage_Black.text(screen_update_text_location,
                                  "Screen updated on " + date_text + " at " + str(now.strftime("%I:%M %p")),
                                  font=really_small_font, fill=0)  # Screen updated section
        # Influx internet info import
        last_host_names, last_room_temps, last_room_humidities = influx_rt.pull_last_influx()  # Pulls the most recent
        public_ip_host_names, public_ip_addresses = influx_rt.pull_last_public_ip()  # Pulls the IP info
        internet_speed_hostnames, download_speeds, upload_speeds, pings, internet_speed_update_time = influx_rt.pull_last_internet_speeds()
        for n, name in enumerate(internet_speed_hostnames):  # Change names into what I want to call them
            if name == 'UbuntuMain':
                ubuntu_main_download_speed = download_speeds[n]
                ubuntu_main_upload_speed = upload_speeds[n]
                ubuntu_main_ping = pings[n]
            elif name == 'UbuntuSecure':
                ubuntu_private_download_speed = download_speeds[n]
                ubuntu_private_upload_speed = upload_speeds[n]
                ubuntu_private_ping = pings[n]
            else:
                print("the hostname " + internet_speed_hostnames[n] + " wasn't recognized")
        # MESSAGE SECTION
        last_message, message_time, message_host = influx_rt.pull_last_message()  # Import the last message and info
        message_display_text = last_message

        draw_TextImage_Black.text((message_display_offset),
                                  str(message_display_text), font=Prefs.small_font, fill=0)
        draw_TextImage_Black.text((message_display_offset + (0, 100)),
                                  str(" from " + message_host + " at " + message_time), font=Prefs.small_font, fill=0)

        draw_TextImage_Black.text((epd.height * .1, internet_speed_offset), str(ubuntu_main_download_speed),
                                  font=small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .1, internet_speed_offset + 15), "Download",
                                  font=really_small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .25, internet_speed_offset), str(ubuntu_main_upload_speed),
                                  font=small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .25, internet_speed_offset + 15), "Upload",
                                  font=really_small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .40, internet_speed_offset), str(ubuntu_main_ping),
                                  font=small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .40, internet_speed_offset + 15), "ping",
                                  font=really_small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .60, internet_speed_offset), str(ubuntu_private_download_speed),
                                  font=small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .60, internet_speed_offset + 15), "Download",
                                  font=really_small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .75, internet_speed_offset), str(ubuntu_private_upload_speed),
                                  font=small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .75, internet_speed_offset + 15), "Upload",
                                  font=really_small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .90, internet_speed_offset), str(ubuntu_private_ping),
                                  font=small_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .90, internet_speed_offset + 15), "ping",
                                  font=really_small_font, fill=0)  #

        for n, name in enumerate(public_ip_host_names):  # Change names into what I want to call them
            if name == 'UbuntuMain':
                ubuntu_main_public_ip = public_ip_addresses[n]
            elif name == 'UbuntuSecure':
                ubuntu_private_public_ip = public_ip_addresses[n]
            else:
                print("the hostname " + public_ip_host_names[n] + " wasn't recognized")

        draw_TextImage_Black.text((epd.height * .1, public_ip_height_offset), ubuntu_main_public_ip,
                                  font=medium_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .1, public_ip_height_offset - 30), "Ubuntu Main",
                                  font=medium_font, fill=0)  #

        draw_TextImage_Black.text((epd.height * .6, public_ip_height_offset), ubuntu_private_public_ip,
                                  font=medium_font, fill=0)  #

        draw_TextImage_Black.text((epd.height * .6, public_ip_height_offset - 30), "Ubuntu Secure",
                                  font=medium_font, fill=0)  #

        influx_import()
        plot_graph()

        # Most recent influx Temperatures
        last_list_length = len(last_host_names)
        divider_distance = 1.0 / lastlist_length
        list_points = 0
        convert_last_names()
        for n in range(0, last_list_length):
            print(n)
            draw_TextImage_Black.text(((epd.height * (n * divider_distance)), last_display_offset),
                                      server_temp_host_names[n],
                                      font=really_small_font, fill=0)  #
            draw_TextImage_Black.text(((epd.height * (n * divider_distance)), (server_temps_display_offset - 30)),
                                      str(round((last_room_temps[n]), 1)) + Prefs.degree_sign + " F", font=medium_font,
                                      fill=0)  # 1st server temperature
        # print(room_temps)
        # print(host_names)

        living_room_max_temp = max(living_room_temp_list)
        living_room_min_temp = min(living_room_temp_list)

        server_closet_max_temp = max(server_closet_temp_list)
        server_closet_min_temp = min(server_closet_temp_list)

        draw_TextImage_Black.text(((epd.height * 0.0), min_max_display_offset),
                                  str(round(server_closet_max_temp, 2)) + Prefs.degree_sign + " F", font=medium_font,
                                  fill=0)  # Server closet max temp
        draw_TextImage_Black.text(((epd.height * 0.0), min_max_display_offset + 25), "Server Closet Max",
                                  font=really_small_font, fill=0)  # Server closet max temp
        draw_TextImage_Black.text(((epd.height * 0.25), min_max_display_offset),
                                  str(round(server_closet_min_temp, 2)) + Prefs.degree_sign + " F", font=medium_font,
                                  fill=0)  # Server closet min temp
        draw_TextImage_Black.text(((epd.height * 0.25), min_max_display_offset + 25), "Server Closet Min",
                                  font=really_small_font, fill=0)  # Server closet min temp

        draw_TextImage_Black.text(((epd.height * 0.50), min_max_display_offset),
                                  str(round(living_room_max_temp, 2)) + Prefs.degree_sign + " F", font=medium_font,
                                  fill=0)  # 1st server temperature
        draw_TextImage_Black.text(((epd.height * 0.50), min_max_display_offset + 25), "Living Room Max",
                                  font=really_small_font, fill=0)  #
        draw_TextImage_Black.text(((epd.height * 0.75), min_max_display_offset),
                                  str(round(living_room_min_temp, 2)) + Prefs.degree_sign + " F", font=medium_font,
                                  fill=0)  # 1st server temperature
        draw_TextImage_Black.text(((epd.height * 0.75), min_max_display_offset + 25), "Living Room Min",
                                  font=really_small_font, fill=0)  #

        draw_TextImage_Black.text(((epd.height * .33), (min_max_display_offset - 25)), "24 Hour Temps",
                                  font=medium_font,
                                  fill=0)  # 1st server temperature

        server_closet_graph_image = Image.open('closet_temps.png')  # Load the graph for display
        newsize = (600, 200)  # Resize the graph to better fit the screen
        im1 = server_closet_graph_image.resize(newsize)  # Resize to better fit

        Black_Layer.paste(im1, Graph_offset)  # Paste the graph on the screen at the graph offset

        # Black layer then red layer
        # Push to display

        epd.init()  # Get screen ready
        epd.Clear()  # Clear the screen

        epd.display(epd.getbuffer(Black_Layer))  # Push to display,
        print("displayed")  # Let us know it's displayed

        time.sleep(sleep_time)  # Sleep for desired time

        logging.info("Clear...")  # Log
        epd.init()  # Get screen ready
        epd.Clear()  # Clear screen

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5b_HD.epdconfig.module_exit()
        exit()
