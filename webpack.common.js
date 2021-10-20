const webpack = require("webpack");
const { WebpackManifestPlugin } = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const { VueLoaderPlugin } = require("vue-loader");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");
const SpritesmithPlugin = require("webpack-spritesmith");

module.exports = {
  context: path.resolve(process.cwd(), "assets"),
  entry: {
    "clan-page": "./js/clan-page.js",
    "player-page": "./js/player-page.js",
    // "troop-page": "./js/troop-page.js",
    index: "./js/index.js",
    common: "./js/common.js",
    styles: "./css/styles.scss",
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test(mod /* , chunk */) {
            if (!mod.context.includes("node_modules") || ["node_modules/core-js-pure", "node_modules/whatwg-fetch"].some((str) => mod.context.includes(str))) {
              return false;
            }

            return true;
          },
          chunks: "initial",
          name: "vendors",
        },
        shims: {
          test(mod /* , chunk */) {
            return ["node_modules/core-js-pure", "node_modules/whatwg-fetch"].some((str) => mod.context.includes(str));
          },
          chunks: "all",
          name: "shims",
        },
        "styles-compiled": {
          name: "styles-compiled",
          test: (module) => module.nameForCondition && /\.(s?css|vue)$/.test(module.nameForCondition()) && !/^javascript/.test(module.type),
          chunks: "all",
          enforce: true,
        },
      },
    },
  },
  resolve: {
    extensions: [".js", ".vue", ".json"],
    alias: {
      vue$: "vue/dist/vue.runtime.esm.js",
    },
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ["babel-loader"],
      },
      {
        test: /\.vue$/,
        loader: "vue-loader",
      },
      {
        test: /.*flags.*\.(svg)$/,
        loader: "file-loader",
        options: {
          name: "[name]-[hash].[ext]",
          outputPath: "flags/",
          publicPath: "/static/flags/",
        },
      },
      {
        test: /\.png$/,
        loader: "file-loader",
        options: {
          name: "[name]-[hash].[ext]",
          outputPath: "images/compiled/",
          publicPath: "/static/images/compiled/",
        },
      },
      {
        test: /\.svg$/,
        exclude: [/flags/],
        use: {
          loader: "svg-url-loader",
        },
      },
      {
        test: /\.(sass|scss|css)$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              importLoaders: 2,
            },
          },
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [
                  require("autoprefixer"),
                  require("postcss-font-magician")({
                    display: "swap",
                  }),
                ],
              },
            },
          },
          "sass-loader",
        ],
      },
    ],
  },
  plugins: [
    new webpack.ProgressPlugin(),
    new VueLoaderPlugin(),
    new WebpackManifestPlugin(),
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: ["**/*", "!web-manifest*", "!**images", "!**images/*"],
    }),
    new SpritesmithPlugin({
      src: {
        cwd: path.resolve(__dirname, "assets/sprites"),
        glob: "*.png",
      },
      retina: "@2x",
      target: {
        image: path.resolve(__dirname, "assets/images/sprite.png"),
        css: path.resolve(__dirname, "assets/css/sprite.scss"),
      },
      apiOptions: {
        cssImageRef: "../images/sprite.png",
      },
    }),
  ],
  output: {
    path: __dirname + "/clashleaders/static/",
    filename: "js/[name].js",
    publicPath: "/static/",
  },
  experiments: {
    topLevelAwait: true,
  },
};
