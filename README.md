# 🔵 Berowra CMS & CDN

With Berowra you can get a CMS & CDN up in a minute, not a day. Through Deta Space, Berowra gives you the control of self hosting without any need for infrastructure maintenance. It's easy to use, flexible and completely free.

Berowra has the following features:

- Build collections of content pieces
- Use multiple field types in your content pieces
- Upload files and host them on Deta Base
- Fetch your content with a great API

## The Publishing Process 


|![](https://cloud-cusao41w8-hack-club-bot.vercel.app/2screenshot_2021-07-24_at_12.48.29_pm.png) Create A New Collection  | ![](https://cloud-cusao41w8-hack-club-bot.vercel.app/1screenshot_2021-07-24_at_12.49.06_pm.png) Add The Template |
|--|--|

| ![](https://cloud-cusao41w8-hack-club-bot.vercel.app/3screenshot_2021-07-24_at_1.04.53_pm.png) <strong>Create A New Item</strong> | ![](https://cloud-cusao41w8-hack-club-bot.vercel.app/0screenshot_2021-07-24_at_12.53.23_pm.png)<strong>Fill In The Template</strong>  |
|--|--|


## Contributing

This project is built with Python & Flask with Tailwind CSS for styling. 

To run it, first create a project and find your project ID from the `Settings` page. Then set that value as your `DETA_PROJECT_KEY` in your `.env`. You can now run the web app with `python3 main.py`. 

If you plan to make changes to the styles, first run:

```sh
npx tailwindcss -o static/tailwind-dev.css
```

This will make a version of Tailwind with all the styles. Then when you plan to push run:

```sh
NODE_ENV=production npx tailwindcss -o static/tailwind.css --minify  
```

Now, you're all set to get coding!

If you require support or locate a bug please open a GitHub Issue [here](https://github.com/sampoder/berowra/issues/new/choose).
