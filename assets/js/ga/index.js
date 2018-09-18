export const event = (eventName, event_category, event_label, value) =>
  gtag("event", eventName, {
    event_category,
    event_label,
    value
  });

export const gaMixin = {
  methods: {
    gaEvent: event
  }
};
