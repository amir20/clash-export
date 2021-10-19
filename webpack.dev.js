const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = merge(common, {
  mode: "development",
  devtool: "inline-source-map",
  plugins: [
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
    }),
    new webpack.DefinePlugin({
      CLASHLEADERS_VERSION: JSON.stringify("dev"),
    }),
  ],
});
