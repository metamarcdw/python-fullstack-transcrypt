const path = require("path");
const UglifyJSPlugin = require("uglifyjs-webpack-plugin");

module.exports = {
  entry: "./src/__javascript__/index.js",

  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist")
  },

  plugins: [new UglifyJSPlugin()]
};
