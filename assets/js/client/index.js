import { ApolloClient, ApolloLink, InMemoryCache, HttpLink } from "apollo-boost";

const httpLink = new HttpLink({ uri: "/graphql" });

const authLink = new ApolloLink((operation, forward) => {
  operation.setContext({
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN,
    },
  });

  return forward(operation);
});

export const apolloClient = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
