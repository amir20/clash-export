import { GraphQLClient } from "graphql-request";
import Cookies from "js-cookie";

const csrfToken = () => Cookies.get("csrf_token");

const client = new GraphQLClient("/graphql", { headers: { "X-CSRFToken": csrfToken() } });

async function request(query, variable) {
  try {
    return await client.request(query, variable);
  } catch (e) {
    if (e.status == 401) {
      client.setHeader("X-CSRFToken", csrfToken());
      return client.request(query, variable);
    } else {
      throw e;
    }
  }
}

export { request, csrfToken };
