import { GraphQLClient } from "graphql-request";
import Cookies from "js-cookie";

const csrfToken = () => Cookies.get("csrf_token");

const client = new GraphQLClient("/graphql", { headers: { "X-CSRFToken": csrfToken() } });

const request = (query, variable) => client.request(query, variable);

export { request, csrfToken };
