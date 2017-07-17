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
        filename: "js/[name].js",
    },
    resolve: {
        extensions: ['.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
        }
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
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
        ]
    },
    plugins: [
        new ExtractTextPlugin("css/[name].bundle.css"),
        new ManifestPlugin()
    ]
};

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map'
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
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
    ])
}