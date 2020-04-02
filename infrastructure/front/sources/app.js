import "./styles/app.css";
import {JetApp, EmptyRouter, HashRouter } from "webix-jet";

export default class MyApp extends JetApp{
	constructor(config){
		const defaults = {
			id 		: APPNAME,
			version : VERSION,
			router 	: BUILD_AS_MODULE ? EmptyRouter : HashRouter,
			debug 	: !PRODUCTION,
			start 	: "/top/devices.list",
			views   : (name) => {
                if (name.includes("uuid_")) {
                    var view = require("jet-views/compare/result");
                    return view
                }
                else {
                    var name_1 = name.replace(/\./g, "/");
                    var view = require("jet-views/"+name_1);
                    return view
                }
            }
		};

		super({ ...defaults, ...config });
	}
}

if (!BUILD_AS_MODULE){
	webix.ready(() => new MyApp().render() );
}