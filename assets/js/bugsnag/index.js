const bugsnag = require("bugsnag-js");
const bugsnagVue = require("bugsnag-vue");

export const bugsnagClient = bugsnag({
  apiKey: "cdb173414b6d879639165cedcc730d73",
  notifyReleaseStages: ["production"],
});

export default (instance) => bugsnagClient.use(bugsnagVue(instance));
