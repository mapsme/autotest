var path = require("path");
var webpack = require("webpack");

module.exports = function(env) {

	var pack = require("./package.json");
	var ExtractTextPlugin = require("extract-text-webpack-plugin");
	var MiniCssExtractPlugin = require("mini-css-extract-plugin");

	var production = !!(env && env.production === "true");
	var asmodule = !!(env && env.module === "true");
	var standalone = !!(env && env.standalone === "true");

	var babelSettings = {
		extends: path.join(__dirname, '/.babelrc')
	};

	var config = {
		entry: "./sources/app.js",
		output: {
			path: path.join(path.dirname(__dirname), "backend", "main", "static"),
			publicPath:"/codebase/",
			filename: "app.js"
		},
		devtool: "inline-source-map",

		performance: {
            hints: false
        },

        mode: "production",

		resolve: {
			extensions: [".js"],
			modules: ["./sources", "./node_modules"],
			alias:{
				"jet-views":path.resolve(__dirname, "sources/views"),
				"jet-locales":path.resolve(__dirname, "sources/locales")
			}
		},
		plugins: [
			new MiniCssExtractPlugin(path.join(path.dirname(__dirname), "backend", "main", "static", "app.css")),
			new webpack.DefinePlugin({
				VERSION: `"${pack.version}"`,
				APPNAME: `"${pack.name}"`,
				PRODUCTION : production,
				BUILD_AS_MODULE : (asmodule || standalone)
			})
		],
		module: {
			rules: [
				{
					test: /\.js$/,
					loader: "babel-loader?" + JSON.stringify(babelSettings)
				},
				{
					test: /\.(svg|png|jpg|gif)$/,
					loader: "url-loader?limit=25000"
				},
				{
					test: /\.(css)$/,
					use: [
                        MiniCssExtractPlugin.loader,
                        {
                            loader: 'css-loader',
                            options: {
                                importLoaders: 2,
                                sourceMap: true
                            }
                        }
                    ]
				}
			]
		},
	};

	if (asmodule){
		if (!standalone){
			config.externals = config.externals || {};
			config.externals = [ "webix-jet" ];
		}

		const out = config.output;
		const sub = standalone ? "full" : "module";

		out.library = pack.name.replace(/[^a-z0-9]/gi, "");
		out.libraryTarget= "umd";
		out.path = path.join(__dirname, "dist", sub);
		out.publicPath = "/dist/"+sub+"/";
	}

	return config;
}