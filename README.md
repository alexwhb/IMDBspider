IMDB Spider
===========

## Notes
This spider is written in python using the Scrapy framework. It is licensed under the MIT lisense. Do with it what you will. If you'd like to contribute please contact me at alexwhb(at)gmail(dot)com. 

## The Current State
Currently this spider starts at the imdb top 250 movie page and goes through each film coppys it's title, and the link url then goes to each film page intern and collects a good chunk of the data avalible for each film. It then goes and sends that data to the Scrapy pipeline, where there is some cleaning that is done before it's finally saved into a sqlite3 db. 

Right now there is diffinatly room for improvment. I just wrote this because I've not seen vary many open source Scrapy spider projects, and I thought I'd give it a shot. 


##License:
<pre>
The MIT License
</pre>


The MIT License (MIT)
Copyright (c) 2013 Alex Black

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
