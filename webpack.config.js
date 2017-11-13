const path = require('path');
module.exports = {
  entry: './assets/js/findwine.js',
  output: {
    path: path.resolve('static', 'js'),
    filename: 'findwine-bundle.js'
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
