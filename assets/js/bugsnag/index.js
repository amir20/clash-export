const bugsnag = require("bugsnag-js");
const bugsnagVue = require("bugsnag-vue");

export const bugsnagClient = bugsnag({
  apiKey: process.env.BUGSNAG_API_KEY,
  notifyReleaseStages: ["production"]
});

export default instance => bugsnagClient.use(bugsnagVue(instance));
