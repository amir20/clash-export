const webpack = require("webpack");
const path = require("path");
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const ManifestPlugin = require("webpack-manifest-plugin");
const CleanWebpackPlugin = require("clean-webpack-plugin");
const { BugsnagBuildReporterPlugin } = require('webpack-bugsnag-plugins');

require('dotenv').config();


module.exports = {
  context: __dirname + "/assets",
  entry: {
    "details-page": "./js/details-page.js",
    index: "./js/index.js",
    styles: "./css/styles.css"
  },
  output: {
    path: __dirname + "/clashleaders/static/",
    filename: "js/[name].js"
  },
  resolve: {
    extensions: [".js", ".vue", ".json"],
    alias: {
      vue$: "vue/dist/vue.esm.js"
    }
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ["babel-loader"]
      },
      {
        test: /\.vue$/,
        loader: "vue-loader"
      },
      {
        test: /.*flags.*\.(svg)$/,
        loader: "file-loader",
        options: {
          name: "[name]-[hash].[ext]",
          outputPath: "flags/",
          publicPath: "/static/"
        }
      },
      {
        test: /\.svg$/,
        exclude: [/flags/],
        use: {
          loader: "svg-url-loader"
        }
      },
      {
        test: /\.(sass|scss|css)$/,
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: [
            {
              loader: "css-loader",
              query: {
                importLoaders: 1
              }
            },
            {
              loader: "postcss-loader",
              options: {
                "postcss-custom-properties": { warnings: false }
              }
            },
            "sass-loader"
          ]
        })
      }
    ]
  },
  plugins: [
    new ManifestPlugin(),
    new webpack.EnvironmentPlugin(['BUGSNAG_API_KEY']),
    new webpack.optimize.CommonsChunkPlugin({
      name: "vendor",
      chunks: ["details-page", "index"]
    }),
    new ExtractTextPlugin("css/[name].[hash].css"),
    new CleanWebpackPlugin([
      __dirname + "/clashleaders/static/css",
      __dirname + "/clashleaders/static/js",
      __dirname + "/clashleaders/static/flags"
    ])
  ]
};

if (process.env.NODE_ENV === "production") {
  module.exports.devtool = "#source-map";
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    }),
    new BugsnagBuildReporterPlugin({
      apiKey: process.env.BUGSNAG_API_KEY,
    })
  ]);

  module.exports.output.filename = "js/[name].[hash].js";
}

