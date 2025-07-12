
const webpack = require('webpack');

module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      const fallback = webpackConfig.resolve.fallback || {};
      Object.assign(fallback, {
        "http": require.resolve("stream-http"),
        "https": require.resolve("https-browserify"),
        "util": require.resolve("util/"),
        "zlib": require.resolve("browserify-zlib"),
        "stream": require.resolve("stream-browserify"),
        "buffer": require.resolve("buffer"),
        "process": require.resolve("process/browser"),
        "url": require.resolve("url/")
      });
      webpackConfig.resolve.fallback = fallback;
      webpackConfig.plugins = (
        webpackConfig.plugins || []
      ).concat([
        new webpack.ProvidePlugin({
          process: 'process/browser',
          Buffer: ['buffer', 'Buffer']
        })
      ]);
      return webpackConfig;
    }
  }
};
