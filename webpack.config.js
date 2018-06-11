const ManifestPlugin = require("webpack-manifest-plugin");
const CleanWebpackPlugin = require("clean-webpack-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const { VueLoaderPlugin } = require("vue-loader");
var MiniCssExtractPlugin = require("mini-css-extract-plugin");

const PROD = process.env.NODE_ENV === "production";

module.exports = {
  devtool: false,
  context: __dirname + "/assets",
  entry: {
    "details-page": "./js/details-page.js",
    index: "./js/index.js",
    common: "./js/common.js",
    styles: "./css/styles.css"
  },
  optimization: {
    concatenateModules: true,
    // runtimeChunk: true,
    minimizer: [
      new OptimizeCssAssetsPlugin({
        cssProcessorOptions: {
          safe: true
        }
      })
    ],
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendors",
          chunks: "all"
        },
        "styles-compiled": {
          name: "styles-compiled",
          test: module =>
            module.nameForCondition &&
            /\.(s?css|vue)$/.test(module.nameForCondition()) &&
            !/^javascript/.test(module.type),
          chunks: "initial",
          minChunks: 1,
          enforce: true
        }
      }
    }
  },
  output: {
    path: __dirname + "/clashleaders/static/",
    filename: PROD ? "js/[name].[chunkhash].js" : "js/[name].js"
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
          publicPath: "/static/flags/"
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
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            query: {
              importLoaders: 1
            }
          },
          {
            loader: "postcss-loader",
            options: {
              ident: "postcss",
              plugins: loader => [
                require("postcss-import")(),
                require("postcss-cssnext")({
                  features: {
                    customProperties: { warnings: false }
                  }
                }),
                require("postcss-font-magician")()
              ]
            }
          },
          "sass-loader"
        ]
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new ManifestPlugin(),
    new MiniCssExtractPlugin({
      filename: "css/[name].[contenthash].css"
    }),
    new CleanWebpackPlugin([
      __dirname + "/clashleaders/static/css",
      __dirname + "/clashleaders/static/js",
      __dirname + "/clashleaders/static/flags"
    ])
  ]
};
