import { GraphQLClient } from "graphql-request";
import Cookies from "js-cookie";

const csrfToken = () => Cookies.get("csrf_token");

const client = new GraphQLClient("/graphql", { headers: { "X-CSRFToken": csrfToken() } });

async function request(query, variable) {
  try {
    return await client.request(query, variable);
  } catch (e) {
    if (e.status == 400) {
      client.setHeader("X-CSRFToken", csrfToken());
      return client.request(query, variable);
    }
  }
}

export { request, csrfToken };
