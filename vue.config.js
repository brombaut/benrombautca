const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
    publicPath: '',
    css: {
        loaderOptions: {
            sass: {
                prependData: '@import "@/styles/variables.scss";',
            },
        },
    },
    configureWebpack: {
        plugins: [
            new CopyPlugin([
                {
                    from: './CNAME',
                    to: './',
                },
            ]),
        ],
    },
};
