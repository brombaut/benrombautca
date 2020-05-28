const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  publicPath: "",
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "Ben Rombaut";
      return args;
    });
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: "@import \"@/styles/variables.scss\"; @import \"@/styles/common.scss\"; @import \"@/styles/keyframes.scss\";"
      }
    }
  },
  configureWebpack: {
    plugins: [
      new CopyPlugin([
        {
          from: "./CNAME",
          to: "./"
        },
        {
          from: "./src/bookshelf/goodreads-response.xml",
          to: "./"
        }
      ])
    ]
  }
};
