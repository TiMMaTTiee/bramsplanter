// const IS_PRODUCTION = process.env.NODE_ENV === 'production'

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  // baseUrl: IS_PRODUCTION
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to flask dev server
        target: 'http://localhost:5000/'
      }
    }
  },
  configureWebpack: {
    devServer: {
      port: 8080,
      // https://github.com/vuejs-templates/webpack/issues/378
      watchOptions: {
        poll: true
      }
    }
  }
}
