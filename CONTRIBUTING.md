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
