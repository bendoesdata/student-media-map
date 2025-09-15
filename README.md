
# student-media-map

This template should help get you started developing with Vue 3 in Vite.

## GitHub Actions & Deployment

This project uses GitHub Actions for automated deployment to GitHub Pages:

- **Daily Geocode Student Outlets:** once a day at midnight, data is fetched from the Google Spreadsheet which is hosting the student media outlets. Each university name is then geocoded to find the LAT and LONG points, and added as new column. The CSV file is then saved to `outlets.csv` in the Vue `public` folder. 
- **Automatic Deploy:** Every time you push to the `main` branch, a GitHub Actions workflow builds the app and publishes the contents of the `dist` dir to the `gh-pages` branch.
- **Live Site:** The site is available at `https://bendoesdata.github.io/student-media-map/` after each successful deploy.

### How it works

1. The workflow installs dependencies and builds the project using Vite.
2. The build output (`dist` folder) is deployed to the `gh-pages` branch using the [`peaceiris/actions-gh-pages`](https://github.com/peaceiris/actions-gh-pages) action.
3. No manual deployment steps are needed—just push to `main`!

You can find the workflow file at `.github/workflows/deploy.yml`.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```
