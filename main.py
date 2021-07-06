#!/usr/bin/python

#  V .01 - Figured out how to drive display, add date, temperatures


#  Want To Do
#  Better InfluxDB
#  Google Calendar integration
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

sleep_time = 900

time_list = []
host_names = []
room_temps = []
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

while running is True:
    try:
        epd = epd7in5_HD.EPD()
        display_width = 528

        print("EPD HEIGHT " + str(epd.height))
        print("EPD WIDTH " + str(epd.width))

        # Vertical draw
        Black_Layer = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        Red_Layer = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        NoImageLayer = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw_TextImage_Black = ImageDraw.Draw(Black_Layer)  # White box
        last_message, message_time, message_host = influx_rt.pull_last_message()
        draw_TextImage_Red = ImageDraw.Draw(Red_Layer)  # White box

        server_temp_host_names, room_temps, room_humidities = influx_rt.pull_last_influx()


        public_ip_host_names, public_ip_addresses = influx_rt.pull_last_public_ip()


        # Time text
        now = datetime.now()  # Load the current time to show on display
        date_text = now.strftime("%A, %B, %d")  # The date text

        # All the temperature and name stuff below
        draw_TextImage_Black.text(screen_update_text_location, "Screen updated on " + date_text + " at " + str(now.strftime("%I:%M %p")),
                                  font=really_small_font, fill=0)  #

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
                print("the hostname " + host_names[n] + " wasn't recognized")

        message_display_text = last_message

        draw_TextImage_Black.text((message_display_offset), str(message_display_text) + " from " + str(message_host) + " at ", font=Prefs.medium_font,
                fill=0)


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
                print("the hostname " + host_names[n] + " wasn't recognized")

        draw_TextImage_Black.text((epd.height * .1, public_ip_height_offset), ubuntu_main_public_ip,
                                  font=medium_font, fill=0)  #
        draw_TextImage_Black.text((epd.height * .1, public_ip_height_offset - 30), "Ubuntu Main",
                                  font=medium_font, fill=0)  #

        draw_TextImage_Black.text((epd.height * .6, public_ip_height_offset), ubuntu_private_public_ip,
                                  font=medium_font, fill=0)  #

        draw_TextImage_Black.text((epd.height * .6, public_ip_height_offset - 30), "Ubuntu Secure",
                                  font=medium_font, fill=0)  #



        for n, name in enumerate(server_temp_host_names):  # Change names into what I want to call them

            if name == 'RetroPie':
                server_temp_host_names[n] = 'Living Room'
            elif name == 'RaspiTest':
                server_temp_host_names[n] = 'Server Closet'
            elif name == 'RaspiZeroW':
                server_temp_host_names[n] = "Daniel's Room"
                # print(room_temps[n])
            elif name == "Nates Room":
                server_temp_host_names[n] = "Nate's Room"
                # print(room_temps[n])
            else:
                print("the hostname " + host_names[n] + " wasn't recognized")


        server_temp_list_length = len(server_temp_host_names)
        divider_distance = 1.0 / server_temp_list_length
        # Lines!!
        draw_TextImage_Black.line((0, 20, epd.width, 20), fill=0)  # Line below times
        draw_TextImage_Black.line((0, 600, epd.width, 600), fill=0)  # Line below times


        host_names, room_temps, time_list = influx_rt.pull_last_24h_influx()
        list_points = 0

        for n, name in enumerate(host_names):  # Change names into what I want to call them
            if name == 'RetroPie':
                host_names[n] = 'Living Room'
                list_points = list_points + 1
                # print(room_temps[n])
                living_room_temp_list.append(room_temps[n])
                living_room_time_list.append(time_list[n])
            elif name == 'RaspiTest':
                host_names[n] = 'Server Closet'
                server_closet_temp_list.append(room_temps[n])
                server_closet_time_list.append(time_list[n])
                list_points = list_points + 1
                # print(room_temps[n])
            elif name == 'RaspiZeroW':
                host_names[n] = "Daniel's Room"
                list_points = list_points + 1
                daniels_room_temp_list.append(room_temps[n])
                daniels_room_time_list.append(time_list[n])
                # print(room_temps[n])
            elif name == "Nates Room":
                host_names[n] = "Nate's Room"
                list_points = list_points + 1
                nates_room_temp_list.append(room_temps[n])
                nates_room_time_list.append(time_list[n])
                # print(room_temps[n])
            elif name == "RaspiMain":
                host_names[n] = "Server Rack"
                list_points = list_points + 1
                server_rack_temp_list.append(room_temps[n])
                server_rack_time_list.append(time_list[n])
                # print(room_temps[n])
            else:
                print("the hostname " + host_names[n] + " wasn't recognized")


        for n in range (0, server_temp_list_length):
            print(n)
            draw_TextImage_Black.text(((epd.height * (n * divider_distance)), server_temps_display_offset), server_temp_host_names[n],
                                  font=really_small_font, fill=0)  #
            draw_TextImage_Black.text(((epd.height * (n *divider_distance)), (server_temps_display_offset - 30)),
                                  str(round((room_temps[n]), 1)) + Prefs.degree_sign + " F", font=medium_font,
                                  fill=0)  # 1st server temperature
        # print(room_temps)
        # print(host_names)

        living_room_max_temp = max(living_room_temp_list)
        living_room_min_temp = min(living_room_temp_list)

        server_closet_max_temp = max(server_closet_temp_list)
        server_closet_min_temp = min(server_closet_temp_list)

        living_list_length = enumerate(living_list)
        # N = 1000 # Max events for graph (288 is number of 5 minute increments for 24h)
        #
        # server_closet_temp_list = server_closet_temp_list[-N:]
        # server_closet_time_list = server_closet_time_list[-N:]
        # living_room_temp_list = living_room_temp_list[-N:]
        # living_room_time_list = living_room_time_list[-N:]

        draw_TextImage_Black.text(((epd.height * 0.0), min_max_display_offset),
                                  str(round(server_closet_max_temp, 2)) + Prefs.degree_sign + " F", font=medium_font,
                                  fill=0)  # 1st server temperature
        draw_TextImage_Black.text(((epd.height * 0.0), min_max_display_offset + 25), "Server Closet Max",
                                  font=really_small_font, fill=0)  #
        draw_TextImage_Black.text(((epd.height * 0.25), min_max_display_offset),
                                  str(round(server_closet_min_temp, 2)) + Prefs.degree_sign + " F", font=medium_font,
                                  fill=0)  # 1st server temperature
        draw_TextImage_Black.text(((epd.height * 0.25), min_max_display_offset + 25), "Server Closet Min",
                                  font=really_small_font, fill=0)  #

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




        list_a = server_closet_temp_list
        list_b = living_room_temp_list
        list_c = server_closet_time_list
        list_d = living_room_time_list

        if len(list_a) < len(list_b):
            list_b = list_b[: len(list_a)]
        elif len(list_a) > len(list_b):
            list_a = list_a[: len(list_b)]
        if len(list_c) < len(list_d):
            list_d = list_d[: len(list_c)]
        elif len(list_c) > len(list_d):
            list_c = list_c[: len(list_d)]

        server_closet_temp_list = list_a
        living_room_temp_list = list_b
        server_closet_time_list = list_c
        living_room_time_list = list_d


        print(len(server_closet_temp_list), len(living_room_temp_list))
        print(len(server_closet_time_list), len(living_room_time_list))

        plt.plot(server_closet_time_list, server_closet_temp_list, color='black', linewidth=1, label='_nolegend_')
        plt.plot(server_closet_time_list, living_room_temp_list, color='black', linewidth=1, linestyle='dashed',
                 marker='.')

        frame1 = plt.gca()
        frame1.axes.get_xaxis().set_visible(False)
        frame1.axes.get_yaxis().set_visible(False)

        # function to show the plot
        plt.savefig('closet_temps.png')

        server_closet_graph_image = Image.open('closet_temps.png')
        newsize = (600, 200)
        im1 = server_closet_graph_image.resize(newsize)

        Black_Layer.paste(im1, Graph_offset)

        # Black layer then red layer
        # Push to display

        epd.init()
        epd.Clear()

        epd.display(epd.getbuffer(Black_Layer))  # Push to display,
        print("displayed")

        time.sleep(sleep_time)

        logging.info("Clear...")
        epd.init()
        epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5b_HD.epdconfig.module_exit()
        exit()