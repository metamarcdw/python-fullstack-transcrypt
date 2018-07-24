const webpack = require("webpack");
const path = require("path");
const UglifyJSPlugin = require("uglifyjs-webpack-plugin");

module.exports = {
  mode: "development",
  stats: { performance: false },

  entry: "./src/__javascript__/index.js",

  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist")
  },

  module: {
    rules: []
  },

  devServer: {
    contentBase: path.join(__dirname, "dist"),
    compress: true,
    host: "localhost",
    port: 3000
  },

  plugins: [new UglifyJSPlugin()]
};
