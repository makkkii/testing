const express = require('express');
const path = require('path');

const app = express();

if (process.env.NODE_ENV === 'development'){
  const webpack = require('webpack');
  const config = require('./webpack.config.js');
  const compiler = webpack(config);
  var history = require('connect-history-api-fallback');
  
  app.use('/static', express.static(path.resolve(__dirname, 'etesting', 'default')));
  /**
   * Use webpack-dev-middleware, which facilitates creating a bundle.js in memory and updating it automatically
   * based on changed files
   */
  app.use(history());
  app.use(require('webpack-dev-middleware')(compiler,{
      /**
       * @noInfo Only display warnings and errors to the concsole
       */
      noInfo: true,
      publicPath: config.output.publicPath,
      stats: {
          assets: false,
          colors: true,
          version: false,
          hash: false,
          timings: false,
          chunks: false,
          chunkModules: false
      }
  }));

  /**
   * Hot middleware allows the page to reload automatically while we are working on it
   * Can be used instead of react-hot-middleware if Redux is being used to manage app state
   */
  // app.use(require('webpack-hot-middleware')(compiler));
} else {
  const path = require('path');
  const fs = require('fs');
  app.use((req, res, next) => {
    res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
    res.set('Cache-Control', 'public, max-age=31536000');
    next();
});
  const expressStaticGzip = require('express-static-gzip');
  
  app.use('/static', expressStaticGzip(path.resolve(__dirname, 'etesting', 'default', 'js', 'bundles'), {
    enableBrotli: true,
    orderPreference: ['br', 'gz']
 }));
}

const PORT = process.env.PORT || 3000;

app.listen(3000, () => {
  console.log(`Server bound to ${PORT}`);
})
