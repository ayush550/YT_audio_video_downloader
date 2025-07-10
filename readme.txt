This is the beginning of my Youtube video/audio downloader.

Version 1.0 - setup the environment and ran code successfully for both mp3 and mp4 files {tested url - https://www.youtube.com/watch?v=2Vv-BfVoq4g}

About yt-dlp or YoutubeDL mainly consists of 4 parts:
a) YoutubeDL, 
b) extractors, 
c) downloaders and 
d) postprocessors

a) YoutubeDL - is the core program. This is the part that interprets the options you give, decide how to name the files, etc. 
This is also the part selects the correct extractor/downloader/postprocessor and tells them what to do. 
(There is actually a youtube_dl module as well which does some of this work, but I'm considering these two to be the same for sake of simplicity)

b) extractors - are the part that finds the video information (including the formats available and their URLs) from the website. 
When you see a new website has been added, it means someone wrote a new extractor for that website. How does the extractor find this information? 
There are generally 2 ways. (1) From the webpage - youtube-dl downloads the webpage (like what browser does) and then take the necessary info from the html. 
(2) Using API - many websites have APIs that can be used to obtain the same info, but in a more programmer friendly way (in JSON format). 
If an API is available, this is generally the prefered method. Many extractors like youtube make use of both these techniques to get different parts of the data.

c) downloaders - downloads the actual video. Once the extractor has obtained all the necessary information, YoutubeDL looks at this and decides how the file 
can be downloaded (HTTP, DASH, m3u8 etc has to be downloaded using different methods) and hands the data over to the correct downloader. 
It then downloads the video file (and stiches them together if needed) and informs YoutubeDL when it is done.

d) postprocessors - does the additional tasks like extracting audio, merging video+audio, embedding thumbnail etc. 
Once the downloader is done downloading the file, YoutubeDL prepares a list of postprocessors to run based on the options 
the user has given and then runs them one by one.


read more from - https://github.com/pH-7/Download-Simply-Videos-From-YouTube/blob/main/download.py
