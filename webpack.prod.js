const webpack = require("webpack");
const merge = require("webpack-merge");
const common = require("./webpack.common.js");
const UglifyJSPlugin = require("uglifyjs-webpack-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CompressionPlugin = require("compression-webpack-plugin");
const BrotliPlugin = require("brotli-webpack-plugin");
const SWPrecacheWebpackPlugin = require("sw-precache-webpack-plugin");
const path = require("path");

const assetsPath = path.resolve(__dirname, "./clashleaders");

module.exports = merge(common, {
  mode: "production",
  devtool: "source-map",
  optimization: {
    minimizer: [
      new UglifyJSPlugin({
        cache: true,
        parallel: true,
        sourceMap: true
      }),
      new OptimizeCssAssetsPlugin({
        cssProcessorOptions: {
          parser: require("postcss-safe-parser")
        }
      })
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("production")
    }),
    new MiniCssExtractPlugin({ filename: "css/[name].[chunkhash].css" }),
    new CompressionPlugin({ test: /\.(js|css|map|svg)$/ }),
    new BrotliPlugin({ test: /\.(js|css|map|svg)$/ }),
    new SWPrecacheWebpackPlugin({
      staticFileGlobsIgnorePatterns: [/\.map$/, /\.svg$/, /\.svg.gz$/, /\.map.gz$/],
      stripPrefix: assetsPath
    })
  ],
  output: {
    filename: "js/[name].[chunkhash].js"
  }
});
