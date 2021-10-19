const webpack = require("webpack");
const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");
const TerserPlugin = require("terser-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;

module.exports = merge(common, {
  mode: "production",
  devtool: "source-map",
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin(), new CssMinimizerPlugin()],
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("production"),
      CLASHLEADERS_VERSION: JSON.stringify(process.env.VERSION_TAG),
    }),
    new MiniCssExtractPlugin({ filename: "css/[name].[chunkhash].css" }),
  ],
  output: {
    filename: "js/[name].[chunkhash].js",
  },
});

if (process.env.SHOW_ANALYZER == "true") {
  module.exports = merge(module.exports, {
    plugins: [new BundleAnalyzerPlugin()],
  });
}
