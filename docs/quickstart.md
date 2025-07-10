# Quick Start Guide

Get up and running with perms.io's Resource-Specific RBAC system in minutes. This guide will walk you through creating your first organisation, setting up permissions, and performing access checks.

## Overview

perms.io provides a complete RBAC system with:
- **Organisations** - Top-level containers for your resources
- **Projects** - Logical groupings within organisations 
- **Permissions** - Individual actions (read, write, delete)
- **Roles** - Collections of permissions
- **Principals** - Users or entities that can be granted access

## Prerequisites

- Account at [app.perms.io](https://app.perms.io)
- API access (Bearer token or API key)
- Basic understanding of REST APIs or gRPC

## Step 1: Create Your Organisation

First, create an organisation to house all your resources.

=== "HTTP"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "My Company",
        "user_id": "your-user-id"
      }'
    ```

=== "Go"
    ```go
    package main

    import (
        "context"
        "fmt"
        "log"
        
        "google.golang.org/grpc"
        "google.golang.org/grpc/credentials"
        "google.golang.org/grpc/metadata"
        
        organisationv1 "github.com/PrivateJAR/permio-go/proto/organisation/v1"
    )

    func main() {
        // Create connection
        conn, err := grpc.Dial("api.perms.io:443", grpc.WithTransportCredentials(credentials.NewTLS(nil)))
        if err != nil {
            log.Fatalf("Failed to connect: %v", err)
        }
        defer conn.Close()

        client := organisationv1.NewOrganisationServiceClient(conn)
        
        // Add authentication
        ctx := metadata.AppendToOutgoingContext(context.Background(), "authorization", "Bearer YOUR_TOKEN")
        
        // Create organisation
        req := &organisationv1.CreateOrganisationRequest{
            Name:   "My Company",
            UserId: "your-user-id",
        }
        
        resp, err := client.CreateOrganisation(ctx, req)
        if err != nil {
            log.Fatalf("Failed to create organisation: %v", err)
        }
        
        fmt.Printf("Created organisation: %s (ID: %s)\n", resp.Organisation.Name, resp.Organisation.Id)
    }
    ```

=== "Python"
    ```python
    import grpc
    from grpc import ssl_channel_credentials
    
    from proto.organisation.v1 import organisation_service_pb2
    from proto.organisation.v1 import organisation_service_pb2_grpc

    def create_organisation():
        # Create secure channel
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        # Create metadata for authentication
        metadata = [('authorization', 'Bearer YOUR_TOKEN')]
        
        # Create organisation
        request = organisation_service_pb2.CreateOrganisationRequest(
            name="My Company",
            user_id="your-user-id"
        )
        
        response = client.CreateOrganisation(request, metadata=metadata)
        print(f"Created organisation: {response.organisation.name} (ID: {response.organisation.id})")
        return response.organisation.id

    if __name__ == "__main__":
        org_id = create_organisation()
    ```

=== "Node.js"
    ```javascript
    const grpc = require('@grpc/grpc-js');
    const protoLoader = require('@grpc/proto-loader');

    // Load the proto file
    const packageDefinition = protoLoader.loadSync('./proto/organisation/v1/organisation_service.proto');
    const organisationService = grpc.loadPackageDefinition(packageDefinition).organisation_service.v1;

    // Create client with SSL credentials
    const client = new organisationService.OrganisationService('api.perms.io:443', 
        grpc.credentials.createSsl());

    function createOrganisation() {
        return new Promise((resolve, reject) => {
            const request = {
                name: 'My Company',
                user_id: 'your-user-id'
            };
            
            const metadata = new grpc.Metadata();
            metadata.add('authorization', 'Bearer YOUR_TOKEN');
            
            client.CreateOrganisation(request, metadata, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                console.log(`Created organisation: ${response.organisation.name} (ID: ${response.organisation.id})`);
                resolve(response.organisation.id);
            });
        });
    }

    // Usage
    createOrganisation().then(orgId => {
        console.log('Organisation created successfully');
    }).catch(err => {
        console.error('Error:', err);
    });
    ```

## Step 2: Create a Project

Projects help organize permissions within your organisation.

=== "HTTP"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation/ORG_ID/project" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "production",
        "organisation_id": "ORG_ID"
      }'
    ```

=== "Go"
    ```go
    func createProject(client organisationv1.OrganisationServiceClient, ctx context.Context, orgId string) string {
        req := &organisationv1.CreateProjectRequest{
            OrganisationId: orgId,
            Name:          "production",
        }
        
        resp, err := client.CreateProject(ctx, req)
        if err != nil {
            log.Fatalf("Failed to create project: %v", err)
        }
        
        fmt.Printf("Created project: %s\n", resp.Project.Name)
        return resp.Project.Name
    }
    ```

=== "Python"
    ```python
    def create_project(org_id: str):
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        metadata = [('authorization', 'Bearer YOUR_TOKEN')]
        
        request = organisation_service_pb2.CreateProjectRequest(
            organisation_id=org_id,
            name="production"
        )
        
        response = client.CreateProject(request, metadata=metadata)
        print(f"Created project: {response.project.name}")
        return response.project.name
    ```

## Step 3: Create an API Key

API keys allow your applications to access the perms.io API programmatically.

=== "HTTP"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation/ORG_ID/api-key" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "My Application API Key"
      }'
    ```

=== "Go"
    ```go
    func createAPIKey(client organisationv1.OrganisationServiceClient, ctx context.Context, orgId string) string {
        req := &organisationv1.CreateAPIKeyRequest{
            OrganisationId: orgId,
            ProjectName:    "production",
            Name:          "My Application API Key",
        }
        
        resp, err := client.CreateAPIKey(ctx, req)
        if err != nil {
            log.Fatalf("Failed to create API key: %v", err)
        }
        
        fmt.Printf("Created API key: %s\n", resp.ApiKey.Name)
        fmt.Printf("API Key (store securely): %s\n", resp.ApiKey.Key)
        return resp.ApiKey.Key
    }
    ```

!!! warning "Store API Keys Securely"
    API keys are only shown once during creation. Store them securely and never expose them in client-side code.

## Step 4: Create Permissions

Define the actions that can be performed in your application.

=== "HTTP"
    ```bash
    # Create read permission
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "document.read",
        "description": "Allows reading documents"
      }'

    # Create write permission
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "document.write",
        "description": "Allows writing documents"
      }'
    ```

=== "Go"
    ```go
    func createPermissions(client permissionsv1.PermissionsServiceClient, ctx context.Context) ([]string, error) {
        permissions := []struct {
            name        string
            description string
        }{
            {"document.read", "Allows reading documents"},
            {"document.write", "Allows writing documents"},
            {"document.delete", "Allows deleting documents"},
        }
        
        var permissionIds []string
        
        for _, perm := range permissions {
            req := &permissionsv1.CreatePermissionRequest{
                ProjectName: "production",
                Name:        perm.name,
                Description: perm.description,
            }
            
            resp, err := client.CreatePermission(ctx, req)
            if err != nil {
                return nil, fmt.Errorf("failed to create permission %s: %v", perm.name, err)
            }
            
            permissionIds = append(permissionIds, resp.Id)
            fmt.Printf("Created permission: %s (ID: %s)\n", resp.Name, resp.Id)
        }
        
        return permissionIds, nil
    }
    ```

=== "Python"
    ```python
    def create_permissions():
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        metadata = [('authorization', 'Bearer YOUR_API_KEY')]
        
        permissions = [
            ("document.read", "Allows reading documents"),
            ("document.write", "Allows writing documents"),
            ("document.delete", "Allows deleting documents")
        ]
        
        permission_ids = []
        
        for name, description in permissions:
            request = permissions_service_pb2.CreatePermissionRequest(
                project_name="production",
                name=name,
                description=description
            )
            
            response = client.CreatePermission(request, metadata=metadata)
            permission_ids.append(response.id)
            print(f"Created permission: {response.name} (ID: {response.id})")
        
        return permission_ids
    ```

## Step 5: Create Roles

Group permissions into roles for easier management.

=== "HTTP"
    ```bash
    # Create editor role
    curl -X POST "https://api.perms.io/permissions-service/v1/roles" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "document_editor",
        "description": "Can read and write documents",
        "permissions": ["PERMISSION_ID_1", "PERMISSION_ID_2"]
      }'
    ```

=== "Go"
    ```go
    func createRoles(client permissionsv1.PermissionsServiceClient, ctx context.Context, permissionIds []string) ([]string, error) {
        roles := []struct {
            name        string
            description string
            permissions []string
        }{
            {
                name:        "document_viewer",
                description: "Can read documents",
                permissions: []string{permissionIds[0]}, // read only
            },
            {
                name:        "document_editor",
                description: "Can read and write documents",
                permissions: []string{permissionIds[0], permissionIds[1]}, // read + write
            },
            {
                name:        "document_admin",
                description: "Full access to documents",
                permissions: permissionIds, // all permissions
            },
        }
        
        var roleIds []string
        
        for _, role := range roles {
            req := &permissionsv1.CreateRoleRequest{
                ProjectName: "production",
                Name:        role.name,
                Description: role.description,
                Permissions: role.permissions,
            }
            
            resp, err := client.CreateRole(ctx, req)
            if err != nil {
                return nil, fmt.Errorf("failed to create role %s: %v", role.name, err)
            }
            
            roleIds = append(roleIds, resp.Id)
            fmt.Printf("Created role: %s (ID: %s)\n", resp.Name, resp.Id)
        }
        
        return roleIds, nil
    }
    ```

## Step 6: Grant Permissions to Users

Assign permissions and roles to users on specific resources.

=== "HTTP"
    ```bash
    # Grant editor role to user on specific document
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/assign" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "user_id": "user_123",
        "resource_uri": "/documents/doc_456",
        "permissions": [],
        "roles": ["ROLE_ID"]
      }'
    ```

=== "Go"
    ```go
    func grantPermissions(client permissionsv1.PermissionsServiceClient, ctx context.Context, roleIds []string) error {
        // Grant viewer role to user on all documents
        req := &permissionsv1.GrantUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      "user_123",
            ResourceUri: "/documents",
            Permissions: []string{},
            Roles:       []string{roleIds[0]}, // viewer role
        }
        
        _, err := client.GrantUserPermissionsAndRolesOnResource(ctx, req)
        if err != nil {
            return fmt.Errorf("failed to grant permissions: %v", err)
        }
        
        fmt.Printf("Granted viewer permissions to user_123 on /documents\n")
        
        // Grant editor role to user on specific document
        req = &permissionsv1.GrantUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      "user_456",
            ResourceUri: "/documents/doc_789",
            Permissions: []string{},
            Roles:       []string{roleIds[1]}, // editor role
        }
        
        _, err = client.GrantUserPermissionsAndRolesOnResource(ctx, req)
        if err != nil {
            return fmt.Errorf("failed to grant permissions: %v", err)
        }
        
        fmt.Printf("Granted editor permissions to user_456 on /documents/doc_789\n")
        return nil
    }
    ```

## Step 7: Check Permissions

Verify that users have the required permissions for specific actions.

=== "HTTP"
    ```bash
    # Check if user can read document
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "principal_id": "user_123",
        "resource_uris": ["/documents/doc_456"],
        "permissions": ["document.read"]
      }'
    ```

=== "Go"
    ```go
    func checkPermissions(client permissionsv1.PermissionsServiceClient, ctx context.Context) error {
        req := &permissionsv1.CheckPermissionRequest{
            ProjectName:  "production",
            PrincipalId:  "user_123",
            ResourceUris: []string{"/documents/doc_456"},
            Permissions:  []string{"document.read", "document.write"},
        }
        
        resp, err := client.Check(ctx, req)
        if err != nil {
            return fmt.Errorf("failed to check permissions: %v", err)
        }
        
        if resp.Passed {
            fmt.Printf("✅ User user_123 has required permissions\n")
        } else {
            fmt.Printf("❌ User user_123 missing permissions:\n")
            for _, missing := range resp.MissingPermissions {
                fmt.Printf("  Resource: %s, Missing: %v\n", missing.ResourceUri, missing.MissingPermissions)
            }
        }
        
        return nil
    }
    ```

=== "Python"
    ```python
    def check_permissions():
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        metadata = [('authorization', 'Bearer YOUR_API_KEY')]
        
        request = permissions_service_pb2.CheckPermissionRequest(
            project_name="production",
            principal_id="user_123",
            resource_uris=["/documents/doc_456"],
            permissions=["document.read", "document.write"]
        )
        
        response = client.Check(request, metadata=metadata)
        
        if response.passed:
            print("✅ User user_123 has required permissions")
        else:
            print("❌ User user_123 missing permissions:")
            for missing in response.missing_permissions:
                print(f"  Resource: {missing.resource_uri}, Missing: {missing.missing_permissions}")
    ```

## Complete Example

Here's a complete example that sets up a basic document management system:

=== "Go"
    ```go
    package main

    import (
        "context"
        "fmt"
        "log"
        
        "google.golang.org/grpc"
        "google.golang.org/grpc/credentials"
        "google.golang.org/grpc/metadata"
        
        organisationv1 "github.com/PrivateJAR/permio-go/proto/organisation/v1"
        permissionsv1 "github.com/PrivateJAR/permio-go/proto/permissions/v1"
    )

    func main() {
        // Connect to the API
        conn, err := grpc.Dial("api.perms.io:443", grpc.WithTransportCredentials(credentials.NewTLS(nil)))
        if err != nil {
            log.Fatalf("Failed to connect: %v", err)
        }
        defer conn.Close()

        // Create clients
        orgClient := organisationv1.NewOrganisationServiceClient(conn)
        permClient := permissionsv1.NewPermissionsServiceClient(conn)
        
        // Setup authentication context
        ctx := metadata.AppendToOutgoingContext(context.Background(), "authorization", "Bearer YOUR_TOKEN")
        
        // 1. Create organisation
        orgResp, err := orgClient.CreateOrganisation(ctx, &organisationv1.CreateOrganisationRequest{
            Name:   "Document Management Co",
            UserId: "admin_user",
        })
        if err != nil {
            log.Fatalf("Failed to create organisation: %v", err)
        }
        fmt.Printf("Created organisation: %s\n", orgResp.Organisation.Id)
        
        // 2. Create project
        projectResp, err := orgClient.CreateProject(ctx, &organisationv1.CreateProjectRequest{
            OrganisationId: orgResp.Organisation.Id,
            Name:          "production",
        })
        if err != nil {
            log.Fatalf("Failed to create project: %v", err)
        }
        fmt.Printf("Created project: %s\n", projectResp.Project.Name)
        
        // 3. Create API key
        apiKeyResp, err := orgClient.CreateAPIKey(ctx, &organisationv1.CreateAPIKeyRequest{
            OrganisationId: orgResp.Organisation.Id,
            ProjectName:    "production",
            Name:          "Application API Key",
        })
        if err != nil {
            log.Fatalf("Failed to create API key: %v", err)
        }
        fmt.Printf("Created API key: %s\n", apiKeyResp.ApiKey.Name)
        
        // Switch to API key authentication
        ctx = metadata.AppendToOutgoingContext(context.Background(), "authorization", "Bearer " + apiKeyResp.ApiKey.Key)
        
        // 4. Create permissions
        permissions := []struct{ name, desc string }{
            {"document.read", "Read documents"},
            {"document.write", "Write documents"},
            {"document.delete", "Delete documents"},
        }
        
        var permIds []string
        for _, perm := range permissions {
            permResp, err := permClient.CreatePermission(ctx, &permissionsv1.CreatePermissionRequest{
                ProjectName: "production",
                Name:        perm.name,
                Description: perm.desc,
            })
            if err != nil {
                log.Fatalf("Failed to create permission: %v", err)
            }
            permIds = append(permIds, permResp.Id)
            fmt.Printf("Created permission: %s\n", permResp.Name)
        }
        
        // 5. Create roles
        roleResp, err := permClient.CreateRole(ctx, &permissionsv1.CreateRoleRequest{
            ProjectName: "production",
            Name:        "document_editor",
            Description: "Can read and write documents",
            Permissions: permIds[:2], // read + write
        })
        if err != nil {
            log.Fatalf("Failed to create role: %v", err)
        }
        fmt.Printf("Created role: %s\n", roleResp.Name)
        
        // 6. Grant permissions
        _, err = permClient.GrantUserPermissionsAndRolesOnResource(ctx, &permissionsv1.GrantUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      "user_123",
            ResourceUri: "/documents",
            Roles:       []string{roleResp.Id},
        })
        if err != nil {
            log.Fatalf("Failed to grant permissions: %v", err)
        }
        fmt.Printf("Granted permissions to user_123\n")
        
        // 7. Check permissions
        checkResp, err := permClient.Check(ctx, &permissionsv1.CheckPermissionRequest{
            ProjectName:  "production",
            PrincipalId:  "user_123",
            ResourceUris: []string{"/documents/doc_456"},
            Permissions:  []string{"document.read"},
        })
        if err != nil {
            log.Fatalf("Failed to check permissions: %v", err)
        }
        
        if checkResp.Passed {
            fmt.Printf("✅ Permission check passed!\n")
        } else {
            fmt.Printf("❌ Permission check failed\n")
        }
        
        fmt.Printf("Setup complete! Your RBAC system is ready to use.\n")
    }
    ```

## Next Steps

Now that you have a working RBAC system, you can:

1. **Integrate with your application** - Add permission checks to your application endpoints
2. **Create more complex hierarchies** - Use nested resource URIs for fine-grained control
3. **Add more users** - Invite team members to your organisation
4. **Monitor usage** - Check the dashboard for usage statistics
5. **Implement caching** - Cache permission results for better performance

## Common Patterns

### Multi-tenant Applications

```go
// Tenant-specific resources
resourceUri := fmt.Sprintf("/tenant/%s/projects/%s", tenantId, projectId)

// Check tenant access
checkResp, err := permClient.Check(ctx, &permissionsv1.CheckPermissionRequest{
    ProjectName:  "production",
    PrincipalId:  userId,
    ResourceUris: []string{resourceUri},
    Permissions:  []string{"project.read"},
})
```

### Hierarchical Permissions

```go
// Grant permissions at different levels
// Organisation level
grantPermissions(userId, "/organisation/123", []string{"org.admin"})

// Project level
grantPermissions(userId, "/organisation/123/project/456", []string{"project.manage"})

// Resource level
grantPermissions(userId, "/organisation/123/project/456/document/789", []string{"document.edit"})
```

### Role-based Teams

```go
// Create team roles
teamRoles := []string{"team_lead", "developer", "viewer"}

// Assign team members
for _, member := range teamMembers {
    grantPermissions(member.UserId, "/team/123", []string{}, []string{member.Role})
}
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Check that you have the required permissions for the operation
2. **Resource Not Found**: Verify the resource URIs are correct
3. **Authentication Failed**: Ensure your API key or token is valid
4. **Rate Limiting**: Implement exponential backoff for API calls

### Getting Help

- Check the [API Reference](./api-reference/organizations.md) for detailed endpoint documentation
- Visit [app.perms.io](https://app.perms.io) for the web dashboard
- Review the [IAM Basics](./iam-basics.md) guide for RBAC concepts

You're now ready to implement fine-grained access control in your applications with perms.io!