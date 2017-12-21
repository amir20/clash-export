const webpack = require("webpack");
const path = require("path");
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const ManifestPlugin = require("webpack-manifest-plugin");

module.exports = {
  context: __dirname + "/app",
  entry: {
    "details-page": "./assets/js/details-page.js",
    index: "./assets/js/index.js"
  },
  output: {
    path: __dirname + "/app/static/",
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
        loader: "vue-loader",
        options: {
          extractCSS: true
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
            "postcss-loader",
            "sass-loader"
          ]
        })
      }
    ]
  },
  plugins: [
    new ManifestPlugin({
      map: function(file) { 
        console.log(file)
        return file; 
    },
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: "vendor"
    }),
    new ExtractTextPlugin("css/styles.[hash].css", {
      allChunks: true
    })
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
    })
  ]);

  module.exports.output.filename = "js/[name].[hash].js";
}
