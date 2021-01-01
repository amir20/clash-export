export const event = (action, event_category, event_label, value) =>
  gtag("event", action, {
    event_category,
    event_label,
    value,
  });

export const gaMixin = {
  methods: {
    gaEvent: event,
  },
};
