# Organizations & Projects

Manage your organizations, projects, users, and API keys through perms.io's comprehensive management APIs.

## Overview

Your perms.io setup is built around **organizations** as the top-level container for all resources. Within an organization, you can create **projects** to logically separate different applications or environments, manage **users** and their access, and create **API keys** for programmatic access.

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

### Create Organization

Creates a new organization with the specified user as the initial admin.

=== "HTTP"
    ```http
    POST /organisation
    Content-Type: application/json

    {
      "name": "My Company",
      "user_id": "usr_123"
    }
    ```

=== "Go"
    ```go
    package main

    import (
        "context"
        "log"
        
        "google.golang.org/grpc"
        organisationv1 "github.com/PrivateJAR/permio-go/proto/organisation/v1"
    )

    func createOrganisation(client organisationv1.OrganisationServiceClient) {
        req := &organisationv1.CreateOrganisationRequest{
            Name:   "My Company",
            UserId: "usr_123",
        }
        
        resp, err := client.CreateOrganisation(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to create organisation: %v", err)
        }
        
        log.Printf("Created organisation: %s", resp.Organisation.Id)
    }
    ```

=== "Python"
    ```python
    import grpc
    from proto.organisation.v1 import organisation_service_pb2
    from proto.organisation.v1 import organisation_service_pb2_grpc

    def create_organisation():
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.CreateOrganisationRequest(
            name="My Company",
            user_id="usr_123"
        )
        
        response = client.CreateOrganisation(request)
        print(f"Created organisation: {response.organisation.id}")
    ```

=== "Node.js"
    ```javascript
    const grpc = require('@grpc/grpc-js');
    const protoLoader = require('@grpc/proto-loader');

    const packageDefinition = protoLoader.loadSync('organisation_service.proto');
    const organisationService = grpc.loadPackageDefinition(packageDefinition).organisation_service.v1;

    const client = new organisationService.OrganisationService('api.perms.io:443', 
        grpc.credentials.createSsl());

    function createOrganisation() {
        const request = {
            name: 'My Company',
            user_id: 'usr_123'
        };
        
        client.CreateOrganisation(request, (error, response) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log('Created organisation:', response.organisation.id);
        });
    }
    ```

### Get Organization

Retrieves details of a specific organisation.

=== "HTTP"
    ```http
    GET /organisation/{id}
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

=== "Python"
    ```python
    def get_organisation(org_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.GetOrganisationRequest(id=org_id)
        response = client.GetOrganisation(request)
        
        print(f"Organisation: {response.organisation.name} ({response.organisation.id})")
    ```

### Update Organization

Updates an organisation's details. Requires `organisation.update` permission.

=== "HTTP"
    ```http
    PUT /organisation/{id}
    Content-Type: application/json

    {
      "name": "Updated Company Name"
    }
    ```

=== "Go"
    ```go
    func updateOrganisation(client organisationv1.OrganisationServiceClient, orgId, newName string) {
        req := &organisationv1.UpdateOrganisationRequest{
            Id:   orgId,
            Name: newName,
        }
        
        resp, err := client.UpdateOrganisation(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to update organisation: %v", err)
        }
        
        log.Printf("Updated organisation: %s", resp.Organisation.Name)
    }
    ```

## Project Management

### Create Project

Creates a new project within an organisation. Requires `project.create` permission.

=== "HTTP"
    ```http
    POST /organisation/{organisation_id}/project
    Content-Type: application/json

    {
      "name": "production",
      "organisation_id": "org_123"
    }
    ```

=== "Go"
    ```go
    func createProject(client organisationv1.OrganisationServiceClient, orgId, projectName string) {
        req := &organisationv1.CreateProjectRequest{
            OrganisationId: orgId,
            Name:          projectName,
        }
        
        resp, err := client.CreateProject(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to create project: %v", err)
        }
        
        log.Printf("Created project: %s", resp.Project.Name)
    }
    ```

=== "Python"
    ```python
    def create_project(org_id: str, project_name: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.CreateProjectRequest(
            organisation_id=org_id,
            name=project_name
        )
        
        response = client.CreateProject(request)
        print(f"Created project: {response.project.name}")
    ```

### Get Project

Retrieves details of a specific project. Requires `project.get` permission.

=== "HTTP"
    ```http
    GET /organisation/{organisation_id}/project?project_name={project_name}
    ```

### List Projects

Lists all projects within an organisation. Requires `project.get` permission.

=== "HTTP"
    ```http
    GET /organisation/{organisation_id}/projects?limit=10&cursor=abc123
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

### Delete Project

Deletes a project from an organisation. Requires `project.delete` permission.

=== "HTTP"
    ```http
    DELETE /organisation/{organisation_id}/project?project_name={project_name}
    ```

## API Key Management

### Create API Key

Creates a new API key for programmatic access to a specific project.

=== "HTTP"
    ```http
    POST /organisation/{organisation_id}/api-key
    Content-Type: application/json

    {
      "project_name": "production",
      "name": "CI/CD Pipeline Key"
    }
    ```

=== "Go"
    ```go
    func createAPIKey(client organisationv1.OrganisationServiceClient, orgId, projectName, keyName string) {
        req := &organisationv1.CreateAPIKeyRequest{
            OrganisationId: orgId,
            ProjectName:    projectName,
            Name:          keyName,
        }
        
        resp, err := client.CreateAPIKey(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to create API key: %v", err)
        }
        
        log.Printf("Created API key: %s", resp.ApiKey.Key)
        // Store this key securely - it won't be shown again
    }
    ```

### List API Keys

Lists all API keys for a project. Requires `apiKeys.list` permission.

=== "HTTP"
    ```http
    GET /organisation/{organisation_id}/api-key?project_name={project_name}
    ```

### Invalidate API Key

Invalidates an API key, making it unusable for future requests.

=== "HTTP"
    ```http
    DELETE /organisation/{organisation_id}/api-key/{id}?project_name={project_name}
    ```

## User Management

### Invite User to Organisation

Invites a user to join an organisation via email.

=== "HTTP"
    ```http
    POST /organisation/{organisation_id}/invite
    Content-Type: application/json

    {
      "email": "user@example.com"
    }
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

### Remove User from Organisation

Removes a user from an organisation. Requires `organisation.user.remove` permission.

=== "HTTP"
    ```http
    POST /organisation/{organisation_id}/user/{user_id}
    Content-Type: application/json

    {}
    ```

### Get User's Organisation

Retrieves the organisation associated with a user. Requires `user.organisation.get` permission.

=== "HTTP"
    ```http
    GET /organisation/user
    ```

## Dashboard & Analytics

### Get Dashboard

Retrieves dashboard statistics for an organisation. Requires `organisation.dashboard.view` permission.

=== "HTTP"
    ```http
    GET /organisation/{organisation_id}/dashboard
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

### Get Principal Usage Stats

Retrieves usage statistics for billing purposes. Requires `billing.view` permission.

=== "HTTP"
    ```http
    GET /organisation/{organisation_id}/principal-usage
    ```

### Get Usage History

Retrieves historical usage data for charting. Requires `billing.view` permission.

=== "HTTP"
    ```http
    GET /organisation/{organisation_id}/usage-history?days=30
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

## Best Practices

1. **Project Organization**: Use projects to separate environments (production, staging, development)
2. **API Key Management**: 
   - Create separate API keys for different applications
   - Rotate keys regularly
   - Use descriptive names for easy identification
3. **User Management**: 
   - Invite users via email rather than adding them directly
   - Regularly audit user access
4. **Error Handling**: Always check for permission errors and handle them gracefully