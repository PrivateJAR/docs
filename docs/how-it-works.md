# How It Works

## Hierarchical Design
Permio is based on the principle of resources, individual items in your application that principals can be granted permissions on. These resources are identified by resource URIs, hierarchical strings that identify the path of a resource. For example, a valid resource URI could be `/customer/1234`. Any permission or role granted at a parent path is inherited by child resources unless overridden.

For example, if an admin is assigned the following permission:
```
{
    "resourceURI": "/customer",
    "principal": "some-user-id",
    "permissions": ["customer.info.view"],
}
```
Then they would by default have permission to view any customers info, as the resourceURI the permission is assigned to is higher up in the structure of the URI.


### Authentication-Agnostic
Permio works seamlessly with *any authentication mechanism*, including:

- API Key headers
- JWT tokens
- OAuth2 identity providers
- Custom auth systems

You bring the identity, Permio handles the authorization.

### API-First Design
Permio is designed with an *API-first* approach. No SDKs to install. Access everything via REST or gRPC.

API authentication is performed via API keys generated in the dashboard.

### Blazing-Fast Performance
Optimized for *real-time permission checks at scale*, Permio ensures that access control doesn't become a bottleneck. Smart caching and efficient data structures support high-throughput applications.