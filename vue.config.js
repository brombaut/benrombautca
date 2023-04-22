const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  publicPath: "",
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "Ben Rombaut | Software Developer";
      return args;
    });
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: "@import \"@/styles/variables.scss\"; @import \"@/styles/common.scss\"; @import \"@/styles/keyframes.scss\";",
      },
    },
  },
  configureWebpack: {
    plugins: [
      new CopyPlugin({
        patterns: [
          {
            from: "./CNAME",
            to: "./",
          },
          {
            from: "./src/bookshelf/book-thumbnails",
            to: "./book-thumbails/",
          },
          {
            from: "./src/assets/resumes",
            to: "./resumes/",
          },
          {
            from: "./src/assets/publications",
            to: "./publications/",
          },
          {
            from: "./src/running/running-images",
            to: "./running-images/",
          },
        ]
      }),
    ],
  },
};
