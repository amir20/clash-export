const Bugsnag = require("@bugsnag/js");
const BugsnagPluginVue = require("@bugsnag/plugin-vue");

let bugsnagClient = null;
export default (instance) =>
  (bugsnagClient = Bugsnag.start({
    apiKey: "cdb173414b6d879639165cedcc730d73",
    notifyReleaseStages: ["production"],
    appVersion: CLASHLEADERS_VERSION,
    plugins: [new BugsnagPluginVue(instance)],
  }));

export { bugsnagClient };
