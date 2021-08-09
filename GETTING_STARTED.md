# Getting Started

👋 Howdy friend! I heard you were looking to get started with Berowra! Well you've came to the right place... in this little piece, we'll be exploring building a pizza review website.

1. First up you're going to want to install Berowra, head to https://deta.space/discovery/berowra and click the big blue `Install` button!
2. Select Berowra in the App Library and let it launch!
3. Next up, select `New Collection`: <br />
<img src="https://cloud-cusao41w8-hack-club-bot.vercel.app/2screenshot_2021-07-24_at_12.48.29_pm.png" width="400" />
4. We're now going to want to create a template for each piece of content, in this case we'll want to create a numbers field to give each pizza joint a rating out of five and a files field to upload photos of the pizza at each shop.
5. We'll be redirected home, here we want to select our `Pizza Reviews!` collection
6. And then we'll choose `Create New` to create a new pizza review
7. Now, we're going to need to fill out the template. I'm going to review Joe's Pizza and give it a 4 star rating. Make sure to select Published, only published content will be returned by the API.
8. Speaking of an API, we can now fetch all of our Pizza reviews at the end point shown on the API page. Let's head there now.
9. As I alluded to earlier, we can then open the endpoint displayed. We can append `?content` for even more details.
10. Before I leave you to let your explore, I'd also like to point out the filtering feature! I can append `?content.6348025765512.value!gt=3` to get all which have a rating higher then three. It's important to note your field ID fill be different so check the API response for that.

And that's a wrap! All the best on your adventures with Berowra :D

\- Sam
