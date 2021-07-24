# 🔵 Berowra CMS & CDN

With Berowra you can get a CMS & CDN up in a minute, not a day. Through Deta Space, Berowra gives you the control of self hosting without any need for infrastructure maintenance. It's easy to use, flexible and completely free.

Berowra has the following features:

- Build collections of content pieces
- Use multiple field types in your content pieces
  - Short Strings
  - Numbers
  - Longer Strings with Markdown
  - Dates
  - String Arrays
  - Files
  - Colours
- Upload files and host them on Deta Base
- Fetch your content with a great API

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
