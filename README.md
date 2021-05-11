IMDB Spider
===========

## Notes
This spider is written in python using the Scrapy framework. It is licensed under the MIT lisense. Do with it what you will. If you'd like to contribute please send me a PR. 

One thing to note if you do use this project, be aware that I'm not sure of the legality of this in a professional setting, so use it at your own risk. Also be aware that you can get your ip address banned from websites if you scrap. There are ways of mitigating this risk such as adding delay between requests, which I've built into this by default, but nonetheless there is still risk. 

To run this code you need to have [Python 3.7](https://www.python.org/downloads/) installed on your computer and you need to have [Scrapy 1.7 installed](http://scrapy.org/). Also, included is a pipfile so you can use pip env with this project. install by running pipenv install inside the project directory. 

## The Current State
This spider was last updated in 2019 to search for a list of movies using the IMDB search engine and pull data into a pipeline. 
This data can then be exported as a CSV or as JSON using Scrapy's built in export system using `scrapy crawl <spider name> -o file.csv -t csv`


## License:

The MIT License

The MIT License (MIT)
Copyright (c) 2014 Alex Black

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE. 
