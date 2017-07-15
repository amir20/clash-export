module.exports = {
    plugins: [
        require('lost'),
        require("postcss-cssnext")(),
        require('postcss-font-magician')()
    ]
}
