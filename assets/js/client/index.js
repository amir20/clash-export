import { ApolloClient, ApolloLink, InMemoryCache, HttpLink } from "apollo-boost";
import Cookies from "js-cookie";

const httpLink = new HttpLink({ uri: "/graphql" });
export const csrfToken = Cookies.get("csrf_token");

const authLink = new ApolloLink((operation, forward) => {
  operation.setContext({
    headers: {
      "X-CSRFToken": csrfToken,
    },
  });
  return forward(operation);
});

export const apolloClient = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
