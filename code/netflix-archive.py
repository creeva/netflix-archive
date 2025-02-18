#!/usr/bin/python3
###############################################################################
#       _   _      _    __ _ _         ___           _     _                  #
#      | \ | |    | |  / _| (_)       / _ \         | |   (_)                 #
#      |  \| | ___| |_| |_| |___  __ / /_\ \_ __ ___| |__  ___   _____        #
#      | . ` |/ _ \ __|  _| | \ \/ / |  _  | '__/ __| '_ \| \ \ / / _ \       #
#      | |\  |  __/ |_| | | | |>  <  | | | | | | (__| | | | |\ V /  __/       #
#      \_| \_/\___|\__|_| |_|_/_/\_\ \_| |_/_|  \___|_| |_|_| \_/ \___|       #
###############################################################################
# Title           : netflix-archive.py                                        #
# Description     : Script to Parse exported Netflix viewing data             #
# Authot          : Creeva                                                    #
# Date            : 2025-02-17                                                #
# Version         : 1.0                                                       #
# Notes           : https://github.com/creeva/netflix-archive                 #
###############################################################################
# Version History                                                             #
#       Version   : 1.0 - Initial Version                                     #
###############################################################################
# Script Setup                                                                #
###############################################################################
#
import csv
import glob
import os
import re
from datetime import datetime
#
###############################################################################
# Variables                                                                   #
###############################################################################
#
input_file = 'NetflixViewingHistory.csv'
output_all = 'netflix.txt'
output_shows = 'netflix-shows.txt'
output_movies = 'netflix-movies.txt'
# Regular expression to detect TV shows: 'Season [int]:', 'Limited Series:', or 'Part [int]:'
show_pattern = re.compile(r'(Season \d+:|Limited Series:|Part \d+:)')
#
###############################################################################
# Main Script Start                                                           #
###############################################################################
#
# Directory Checking and Creation
#
if not glob.glob('data'): os.makedirs('data')
if not glob.glob('daily/shows'): os.makedirs('daily/shows')
if not glob.glob('daily/movies'): os.makedirs('daily/movies')
# opening files
with open(input_file, newline='', encoding='utf-8') as csvfile, \
    open(output_all, 'w', encoding='utf-8') as all_file, \
    open(output_shows, 'w', encoding='utf-8') as shows_file, \
    open(output_movies, 'w', encoding='utf-8') as movies_file:
    reader = csv.reader(csvfile)
# Skip header row    
    next(reader)
    for row in reader:       
        data = row[0].strip() 
        raw_date = row[1].strip() 
        date = datetime.strptime(raw_date, '%m/%d/%y')
        formatted_date = date.strftime('%Y-%m-%d')
        logline = f'{formatted_date}   --   00:00:00   --   NETFLIX   --   CONSUMED   --   {data}\n'
        all_file.write(logline)
        dailyshow = f'daily/shows/{formatted_date}-netflix-shows.txt'
        dailymovie = f'daily/movies/{formatted_date}-netflix-movies.txt'
        if show_pattern.search(data):  
            shows_file.write(logline)
            with open(dailyshow, 'w', encoding='utf-8') as daily_shows: daily_shows.write(f'{data}\n')
        else:
            movies_file.write(logline)
            with open(dailymovie, 'w', encoding='utf-8') as daily_movies: daily_movies.write(f'{data}\n') 
