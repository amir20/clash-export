const webpack = require("webpack");
const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");
const TerserPlugin = require("terser-webpack-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const SWPrecacheWebpackPlugin = require("sw-precache-webpack-plugin");
const path = require("path");

const assetsPath = path.resolve(__dirname, "./clashleaders");

module.exports = merge(common, {
  mode: "production",
  devtool: "source-map",
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin(),
      new OptimizeCssAssetsPlugin({
        cssProcessorOptions: {
          parser: require("postcss-safe-parser"),
        },
      }),
    ],
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("production"),
    }),
    new MiniCssExtractPlugin({ filename: "css/[name].[chunkhash].css" }),
    new SWPrecacheWebpackPlugin({
      staticFileGlobsIgnorePatterns: [/\.map$/, /\.svg$/, /\.br$/, /\.gz$/, , /\.LICENSE\.txt$/],
      stripPrefix: assetsPath,
    }),
  ],
  output: {
    filename: "js/[name].[chunkhash].js",
  },
});
