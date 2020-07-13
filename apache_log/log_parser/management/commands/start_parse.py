import re
import sqlite3
from datetime import datetime

import wget
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Parse Apache access log file'

    regexp = re.compile(r'(?P<ip>\d+.\d+.\d+.\d+).+ .+ \[(?P<date>\S+) .+\] "(?P<http_method>\w{3,8}) (?P<url>\S+) +\S+ (?P<respone_code>\S+) (?P<bytes>\S+)')



    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Enter files url for download')

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        dir = settings.FILES_DIR
        # download log file to base files dir
        wget.download(url, out=dir)
        # get log file name (work only for test case file. irl line http://excample.com/somedir/anotherdir/access.log)
        filename = url.split('/')[-1]

        result = []

        with open(f'{dir}/{filename}') as file:
            for line in file:
                try:
                    output = self.regexp.search(line).groupdict()
                    # if no bytes were transmitted, set to 0
                    if output['bytes'] == '-':
                        output['bytes'] = 0
                    date = output['date']
                    # format date from str to datetime format
                    output['date'] = datetime.strptime(date,'%d/%b/%Y:%H:%M:%S')
                    # all http methods to uppercase
                    output['http_method'] = output['http_method'].upper()
                    result.append(tuple(output.values()))
                # if line is incorrect write it to errors file
                except AttributeError:
                    with open(f'{dir}/errors', 'a') as error_lines:
                        error_lines.write(line)


        #write data to DB

        query = 'INSERT into log_parser_logdata(ip,date,http_method,url,response_code,response_size)' \
                ' values (?, ?, ?, ?, ?, ?)'
        connection = sqlite3.connect(settings.DATABASES['default']['NAME'])
        connection.executemany(query, result)
        connection.commit()










