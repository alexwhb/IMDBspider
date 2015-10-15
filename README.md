IMDB Spider
===========

## Notes
This spider is written in python using the Scrapy framework. It is licensed under the MIT lisense. Do with it what you will. If you'd like to contribute please contact me at alexwhb(at)gmail(dot)com. 

One thing to note if you do use this project, be aware that I'm not sure of the legality of this in a proffessinal setting, so use it at your own risk. Also be aware that you can get your ip address banned from websites if you scrap. There are ways of mitagating this risk such as adding delay between requests, which I've built into this by default, but nonetheless there is still risk. 

To run this code you need to have [Python 2.7](https://www.python.org/downloads/) installed on your computer and you need to have [Scrapy 0.24 installed](http://scrapy.org/)

## The Current State
Currently this spider starts at the imdb top 250 movie page. It then goes through each film copies its title, and the link url, then goes to each film page intern and collects a good chunk of the data avalible. It then goes and sends that data to the Scrapy pipeline, where there is some cleaning that is done before it's finally saved into a sqlite3 db. The code is pretty crued at this point. It took me about 3 hours to write, and I deffinatly will be doing some major overhauling when I get more time. 

Right now there is diffinatly room for improvment. I just wrote this because I've not seen vary many open source Scrapy spider projects, and I thought I'd give it a shot. 


## Ideas for the Future:
I just found this page: http://www.imdb.com/year/ 
You can find all moves by year, which could ultimatly allow this system to pull all data off IMDB if you where so inclined... That's one idea I had.

I'd also like to clean up the code considerably, and get the system to be a bit more robust and tollerant of data not being in the exact right form. 



##License:
<pre>
The MIT License
</pre>


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
