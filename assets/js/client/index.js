import { ApolloClient, InMemoryCache, createHttpLink, from } from "@apollo/client/core";
import { onError } from "@apollo/client/link/error";
import { setContext } from "@apollo/client/link/context";
import Cookies from "js-cookie";

export const csrfToken = () => Cookies.get("csrf_token");

const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
  if (networkError.statusCode == 400) {
    const oldHeaders = operation.getContext().headers;
    operation.setContext({
      headers: {
        ...oldHeaders,
        "X-CSRFToken": csrfToken(),
      },
    });
    return forward(operation);
  }
});

const authLink = setContext((_, { headers }) => {
  return {
    headers: {
      ...headers,
      "X-CSRFToken": csrfToken(),
    },
  };
});
const httpLink = createHttpLink({ uri: "/graphql" });

export const apolloClient = new ApolloClient({
  link: from([authLink, errorLink, httpLink]),
  cache: new InMemoryCache(),
});
