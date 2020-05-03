const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
    publicPath: "",
    chainWebpack: config => {
        config.plugin("html").tap(args => {
            args[0].title = "Ben Rombaut";
            return args;
        });
    },
    css: {
        loaderOptions: {
            sass: {
                prependData: "@import \"@/styles/variables.scss\";",
            },
        },
    },
    configureWebpack: {
        plugins: [
            new CopyPlugin([
                {
                    from: "./CNAME",
                    to: "./",
                },
            ]),
        ],
    },
};
