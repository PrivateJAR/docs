# Organizations & Projects

Learn about the organizational structure in perms.io and how to work with your existing setup.

## Overview

Your perms.io setup is built around **organizations** as the top-level container for all resources. Within an organization, you can have **projects** to logically separate different applications or environments.

### Key Concepts

- **Organization**: The primary container for all resources
- **Project**: A logical grouping within an organization (e.g., "production", "staging")
- **User**: Members of an organization with various roles and permissions
- **API Key**: Programmatic access credentials scoped to a specific project

## Authentication

All API endpoints require authentication via:
- **Bearer Token**: For user-based authentication
- **API Key**: For programmatic access (format: `Bearer pk_<key>`)

## Base URL

```
https://api.perms.io/organisation-service/v1
```

## Organization Management

Organizations are created and managed through the [dashboard](https://app.perms.io). Once created, you can work with your organization's data through the API.

### Get Organization

Retrieves details of a specific organisation.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{id}" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

=== "Go"
    ```go
    func getOrganisation(client organisationv1.OrganisationServiceClient, orgId string) {
        req := &organisationv1.GetOrganisationRequest{
            Id: orgId,
        }
        
        resp, err := client.GetOrganisation(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get organisation: %v", err)
        }
        
        log.Printf("Organisation: %s (%s)", resp.Organisation.Name, resp.Organisation.Id)
    }
    ```

=== "Rust"
    ```rust
    async fn get_organisation(client: &mut OrganisationServiceClient<Channel>, org_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GetOrganisationRequest {
            id: org_id.to_string(),
        });
        
        let response = client.get_organisation(request).await?;
        let org = response.get_ref().organisation.as_ref().unwrap();
        println!("Organisation: {} ({})", org.name, org.id);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def get_organisation(org_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.GetOrganisationRequest(id=org_id)
        response = client.GetOrganisation(request)
        
        print(f"Organisation: {response.organisation.name} ({response.organisation.id})")
    ```

=== "Java"
    ```java
    public void getOrganisation(String orgId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        GetOrganisationRequest request = GetOrganisationRequest.newBuilder()
                .setId(orgId)
                .build();
        
        GetOrganisationResponse response = client.getOrganisation(request);
        System.out.println("Organisation: " + response.getOrganisation().getName() + 
                          " (" + response.getOrganisation().getId() + ")");
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GetOrganisationRequest {
        id: string;
    }

    function getOrganisation(orgId: string): void {
        const request: GetOrganisationRequest = {
            id: orgId
        };
        
        client.GetOrganisation(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Organisation: ${response.organisation.name} (${response.organisation.id})`);
        });
    }
    ```

## Project Management

Projects are created and managed through the [dashboard](https://app.perms.io). Use the API to work with your existing projects.

### Get Project

Retrieves details of a specific project. Requires `project.get` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/project?project_name={project_name}" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

### List Projects

Lists all projects within an organisation. Requires `project.get` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/projects?limit=10&cursor=abc123" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

=== "Go"
    ```go
    func listProjects(client organisationv1.OrganisationServiceClient, orgId string) {
        req := &organisationv1.GetProjectsForOrganisationRequest{
            OrganisationId: orgId,
            Pagination: &paginationv1.PaginationRequest{
                Limit: proto.Int32(10),
            },
        }
        
        resp, err := client.GetProjectsForOrganisation(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to list projects: %v", err)
        }
        
        for _, project := range resp.Projects {
            log.Printf("Project: %s", project.Name)
        }
    }
    ```

=== "Rust"
    ```rust
    use permio_proto::pagination::PaginationRequest;

    async fn list_projects(client: &mut OrganisationServiceClient<Channel>, org_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GetProjectsForOrganisationRequest {
            organisation_id: org_id.to_string(),
            pagination: Some(PaginationRequest {
                limit: Some(10),
                cursor: None,
            }),
            search: None,
        });
        
        let response = client.get_projects_for_organisation(request).await?;
        
        for project in response.get_ref().projects.iter() {
            println!("Project: {}", project.name);
        }
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def list_projects(org_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.GetProjectsForOrganisationRequest(
            organisation_id=org_id,
            pagination=pagination_pb2.PaginationRequest(limit=10)
        )
        
        response = client.GetProjectsForOrganisation(request)
        
        for project in response.projects:
            print(f"Project: {project.name}")
    ```

=== "Java"
    ```java
    public void listProjects(String orgId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        GetProjectsForOrganisationRequest request = GetProjectsForOrganisationRequest.newBuilder()
                .setOrganisationId(orgId)
                .setPagination(PaginationRequest.newBuilder().setLimit(10).build())
                .build();
        
        GetProjectsForOrganisationResponse response = client.getProjectsForOrganisation(request);
        
        for (Project project : response.getProjectsList()) {
            System.out.println("Project: " + project.getName());
        }
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GetProjectsForOrganisationRequest {
        organisation_id: string;
        pagination?: {
            limit?: number;
            cursor?: string;
        };
        search?: string;
    }

    function listProjects(orgId: string): void {
        const request: GetProjectsForOrganisationRequest = {
            organisation_id: orgId,
            pagination: {
                limit: 10
            }
        };
        
        client.GetProjectsForOrganisation(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            response.projects.forEach((project: any) => {
                console.log(`Project: ${project.name}`);
            });
        });
    }
    ```

## API Key Management

API keys are created and managed through the [dashboard](https://app.perms.io). Use the API to list your existing keys.

### List API Keys

Lists all API keys for a project. Requires `apiKeys.list` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/api-key?project_name={project_name}" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

## User Management

### Invite User to Organisation

Invites a user to join an organisation via email.

=== "cURL"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/invite" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "email": "user@example.com"
      }'
    ```

=== "Go"
    ```go
    func inviteUser(client organisationv1.OrganisationServiceClient, orgId, email string) {
        req := &organisationv1.InviteUserToOrganisationRequest{
            OrganisationId: orgId,
            Email:         email,
        }
        
        _, err := client.InviteUserToOrganisation(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to invite user: %v", err)
        }
        
        log.Printf("Invited user: %s", email)
    }
    ```

=== "Rust"
    ```rust
    async fn invite_user(client: &mut OrganisationServiceClient<Channel>, org_id: &str, email: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(InviteUserToOrganisationRequest {
            organisation_id: org_id.to_string(),
            email: email.to_string(),
        });
        
        client.invite_user_to_organisation(request).await?;
        println!("Invited user: {}", email);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def invite_user(org_id: str, email: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.InviteUserToOrganisationRequest(
            organisation_id=org_id,
            email=email
        )
        
        client.InviteUserToOrganisation(request)
        print(f"Invited user: {email}")
    ```

=== "Java"
    ```java
    public void inviteUser(String orgId, String email) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        InviteUserToOrganisationRequest request = InviteUserToOrganisationRequest.newBuilder()
                .setOrganisationId(orgId)
                .setEmail(email)
                .build();
        
        client.inviteUserToOrganisation(request);
        System.out.println("Invited user: " + email);
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface InviteUserToOrganisationRequest {
        organisation_id: string;
        email: string;
    }

    function inviteUser(orgId: string, email: string): void {
        const request: InviteUserToOrganisationRequest = {
            organisation_id: orgId,
            email: email
        };
        
        client.InviteUserToOrganisation(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Invited user: ${email}`);
        });
    }
    ```

### Remove User from Organisation

Removes a user from an organisation. Requires `organisation.user.remove` permission.

=== "cURL"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/user/{user_id}" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{}'
    ```

### Get User's Organisation

Retrieves the organisation associated with a user. Requires `user.organisation.get` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/user" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

## Dashboard & Analytics

### Get Dashboard

Retrieves dashboard statistics for an organisation. Requires `organisation.dashboard.view` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/dashboard" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

=== "Go"
    ```go
    func getDashboard(client organisationv1.OrganisationServiceClient, orgId string) {
        req := &organisationv1.GetOrganisationDashboardRequest{
            OrganisationId: orgId,
        }
        
        resp, err := client.GetOrganisationDashboard(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get dashboard: %v", err)
        }
        
        log.Printf("Dashboard stats - Roles: %d, Permissions: %d, Principals: %d, Users: %d",
            resp.TotalRoles, resp.TotalPermissions, resp.TotalPrincipals, resp.TotalUsers)
    }
    ```

=== "Rust"
    ```rust
    async fn get_dashboard(client: &mut OrganisationServiceClient<Channel>, org_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GetOrganisationDashboardRequest {
            organisation_id: org_id.to_string(),
        });
        
        let response = client.get_organisation_dashboard(request).await?;
        let dashboard = response.get_ref();
        
        println!("Dashboard stats - Roles: {}, Permissions: {}, Principals: {}, Users: {}",
            dashboard.total_roles, dashboard.total_permissions, dashboard.total_principals, dashboard.total_users);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def get_dashboard(org_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.GetOrganisationDashboardRequest(
            organisation_id=org_id
        )
        
        response = client.GetOrganisationDashboard(request)
        print(f"Dashboard stats - Roles: {response.total_roles}, Permissions: {response.total_permissions}, "
              f"Principals: {response.total_principals}, Users: {response.total_users}")
    ```

=== "Java"
    ```java
    public void getDashboard(String orgId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        GetOrganisationDashboardRequest request = GetOrganisationDashboardRequest.newBuilder()
                .setOrganisationId(orgId)
                .build();
        
        GetOrganisationDashboardResponse response = client.getOrganisationDashboard(request);
        System.out.println(String.format("Dashboard stats - Roles: %d, Permissions: %d, Principals: %d, Users: %d",
                response.getTotalRoles(), response.getTotalPermissions(), 
                response.getTotalPrincipals(), response.getTotalUsers()));
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GetOrganisationDashboardRequest {
        organisation_id: string;
    }

    function getDashboard(orgId: string): void {
        const request: GetOrganisationDashboardRequest = {
            organisation_id: orgId
        };
        
        client.GetOrganisationDashboard(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Dashboard stats - Roles: ${response.total_roles}, Permissions: ${response.total_permissions}, ` +
                       `Principals: ${response.total_principals}, Users: ${response.total_users}`);
        });
    }
    ```

### Get Principal Usage Stats

Retrieves usage statistics for billing purposes. Requires `billing.view` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/principal-usage" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

### Get Usage History

Retrieves historical usage data for charting. Requires `billing.view` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/usage-history?days=30" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

## Error Handling

The service returns standard gRPC status codes:

- `OK` (0): Success
- `INVALID_ARGUMENT` (3): Invalid request parameters
- `NOT_FOUND` (5): Resource not found
- `PERMISSION_DENIED` (7): Insufficient permissions
- `ALREADY_EXISTS` (6): Resource already exists
- `RESOURCE_EXHAUSTED` (8): Rate limit exceeded

### Example Error Response

```json
{
  "error": {
    "code": 7,
    "message": "Permission denied: missing required permission 'project.create' on resource '/organisation/org_123'"
  }
}
```

## Rate Limits

API requests are subject to rate limiting:
- **Authenticated users**: 1000 requests per hour
- **API keys**: 10000 requests per hour
- **Burst limit**: 100 requests per minute

## Setup Instructions

To set up your organization structure:

1. **Create Organization**: Use the [dashboard](https://app.perms.io) to create your organization
2. **Add Projects**: Create projects for different environments or applications
3. **Generate API Keys**: Create API keys for programmatic access to specific projects
4. **Invite Users**: Add team members to your organization
5. **Configure Permissions**: Use the permissions API to set up your access control

For detailed setup instructions, see the [Quick Start Guide](../quickstart.md).