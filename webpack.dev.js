const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const SWPrecacheWebpackPlugin = require("sw-precache-webpack-plugin");
const path = require("path");

const assetsPath = path.resolve(__dirname, "./clashleaders");

module.exports = merge(common, {
  mode: "development",
  devtool: "inline-source-map",
  plugins: [
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
    }),
    new SWPrecacheWebpackPlugin({
      staticFileGlobsIgnorePatterns: [/\.map$/, /\.svg$/],
      stripPrefix: assetsPath,
    }),
  ],
});
