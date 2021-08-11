Hi friends! I've always found CMSs a challenge in the past, whether hosting them was painful or they cost a ton. No fun :( I wanted to make a CMS that was a little more fun and that you could use for a couple of minutes and then have the job done :D So I built Berowra: https://berowra.xyz (named after my grandparent's home town).

First up, I built Berowra on Deta Space. The CMS will run in your own sandboxed 'personal cloud' in Deta Space, without the need for maintenance by yourself, for free (the best part IMO). You can directly view & access the data Berowra stores through Space, which gives you a nice look into how it all works. I think that hosting Berowra on Deta Space strikes a nice balance between the benefits of a self hosted CMS and a hosted CMS, which I'm reallly happy with. I used Flask & Python to build the backend and then plain old HTML with some Tailwind tossed in for the frontend :D

Here are the key parts of Berowra:

- Content is stored in collections to keep things nice and organised
- Seven different data formats available: string, date, number, markdown, colour, string array and files!
- File hosting for images, videos and more
- A well documented API that is organised and supports filtering 

I've open sourced Berowra at https://github.com/sampoder/berowra and would love to hear what you think about Berowra! This is probably this biggest programming project of mine, it's been a journey for sure!

Thank you :)
