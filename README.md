# student-media-map

This template should help get you started developing with Vue 3 in Vite.

## GitHub Actions & Deployment

This project uses GitHub Actions for automated deployment to Netlify:

- **Automatic Deploy:** Every time you push to the `main` branch, a Netlify build process is triggered.

### How it works

1. The workflow installs dependencies and builds the project using Vite.
2. The build output (`dist` folder) is automatically deployed by Netlify.
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
