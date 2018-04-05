const path = require('path');
module.exports = {
  entry: {
    findwine: './assets/js/findwine.js',
    search: './assets/js/search.js',
  },
  output: {
    path: path.resolve('static', 'js'),
    filename: '[name]-bundle.js'
  },
  module: {
    loaders: [
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.css$/, loaders: ['style-loader', 'css-loader', 'sass-loader']},
      { test: /\.scss$/, loaders: ['style-loader', 'css-loader', 'sass-loader'], exclude: /node_modules/},
    ]
  }
}
