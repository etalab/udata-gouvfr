var path = require('path');
var webpack = require('webpack');

var ExtractTextPlugin = require('extract-text-webpack-plugin');
var node_path = path.join(__dirname, 'node_modules');
var static_path = path.join(__dirname, 'udata_gouvfr', 'theme', 'static');
var source_path = path.join(__dirname, 'theme');

var css_loader = ExtractTextPlugin.extract('style', 'css?root='+source_path+'&sourceMap'),
    less_loader = ExtractTextPlugin.extract('style', 'css?root='+source_path+'&sourceMap!less?sourceMap=source-map-less-inline');

module.exports = {
    context: source_path,
    entry: {
        theme: "theme",
        admin: "admin",
        oembed: 'oembed',
    },
    output: {
        path: static_path,
        publicPath: "/_themes/gouvfr/",
        filename: "[name].js"
    },
    resolve: {
        root: source_path
    },
    devtools: 'eval-source-map',
    module: {
        loaders: [
            {test: /img\/.*\.(jpg|jpeg|png|gif|svg)$/, loader: 'file?name=[path][name].[ext]'},
            {test: /\.css$/, loader: css_loader},
            {test: /\.less$/, loader: less_loader},
            {test: /\.json$/, loader: "json"},
            {test: /\.html$/, loader: "html"},
            {test: /\.(woff|svg|ttf|eot|otf)([\?]?.*)$/, exclude: /img/, loader: "file?name=[name].[ext]"},
            {test: /\.js$/, loader: 'babel-loader', include: [
                    path.resolve(source_path, 'js'),
                ]
            }
        ]
    },
    babel: {
        presets: ['es2015'],
        comments: false,
        plugins: ['transform-runtime']
    },
    plugins: [
        new ExtractTextPlugin('[name].css'),
        require('webpack-fail-plugin'),
    ]
};
