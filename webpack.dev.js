const path = require("path");
const merge = require('webpack-merge');
const common = require('./webpack.common');

module.exports = merge(common, {
  mode: "development",
  stats: { performance: false },

  devServer: {
    contentBase: path.join(__dirname, "dist"),
    compress: true,
    host: "localhost",
    port: 3000
  }
});
