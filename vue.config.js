const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
    publicPath: '/',
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
