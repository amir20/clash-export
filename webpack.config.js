const webpack = require("webpack");
const path = require("path");
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');

module.exports = {
    context: __dirname + "/app",
    entry: {
        app: "./javascript/index.js"
    },
    output: {
        path: __dirname + "/app/static/",
        filename: "js/[name].[hash].js",
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            use: ['babel-loader']
        }, {
            test: /\.css$/,
            loader: ExtractTextPlugin.extract({
                fallback: 'style-loader',
                use: [{
                        loader: 'css-loader',
                        query: {
                            importLoaders: 1
                        },
                    },
                    {
                        loader: 'postcss-loader',
                    }
                ]
            })
        }, {
            test: /\.(png|woff|woff2|eot|ttf|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
            use: 'file-loader?name=./fonts/[hash].[ext]&publicPath=../'
        }]
    },
    plugins: [
        new ExtractTextPlugin("css/[name].bundle.css"),
        new ManifestPlugin()
    ]
};
