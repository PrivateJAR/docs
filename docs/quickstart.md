# Quick Start Guide

Get up and running with perms.io's Resource-Specific RBAC system in minutes. This guide will walk you through setting up permissions and performing access checks.

## Overview

perms.io provides a complete RBAC system with:
- **Organisations** - Top-level containers for your resources
- **Projects** - Logical groupings within organisations 
- **Permissions** - Individual actions (read, write, delete)
- **Roles** - Collections of permissions
- **Principals** - Users or entities that can be granted access

## Prerequisites

- Account at [app.perms.io](https://app.perms.io)
- Organization, project, and API key created via the dashboard
- Basic understanding of REST APIs or gRPC

## Step 1: Setup via Dashboard

Before using the API, complete the initial setup through the web dashboard:

1. **Create Your Organisation**: Go to [app.perms.io](https://app.perms.io) and create your organization
2. **Create a Project**: Create a project within your organization (e.g., "production")
3. **Generate API Key**: Create an API key for your project to use in the examples below

## Step 2: Create Permissions

Define the actions that can be performed in your application.

=== "cURL"
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
            ("document.write", "Allows writing documents")
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

## Step 3: Create Roles

Group permissions into roles for easier management.

=== "cURL"
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

=== "Python"
    ```python
    def create_roles(permission_ids: list[str]) -> list[str]:
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        metadata = [('authorization', 'Bearer YOUR_API_KEY')]
        
        roles = [
            ("document_viewer", "Can read documents", [permission_ids[0]]),
            ("document_editor", "Can read and write documents", [permission_ids[0], permission_ids[1]]),
        ]
        
        role_ids = []
        
        for name, description, permissions in roles:
            request = permissions_service_pb2.CreateRoleRequest(
                project_name="production",
                name=name,
                description=description,
                permissions=permissions
            )
            
            response = client.CreateRole(request, metadata=metadata)
            role_ids.append(response.id)
            print(f"Created role: {response.name} (ID: {response.id})")
        
        return role_ids
    ```

## Step 4: Grant Permissions to Users

Assign permissions and roles to users on specific resources.

=== "cURL"
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
        
        fmt.Printf("Granted permissions to user_123 on /documents\n")
        return nil
    }
    ```

=== "Python"
    ```python
    def grant_permissions(role_ids: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        metadata = [('authorization', 'Bearer YOUR_API_KEY')]
        
        request = permissions_service_pb2.GrantUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id="user_123",
            resource_uri="/documents",
            permissions=[],
            roles=[role_ids[0]]  # viewer role
        )
        
        client.GrantUserPermissionsAndRolesOnResource(request, metadata=metadata)
        print("Granted permissions to user_123 on /documents")
    ```

## Step 5: Check Permissions

Verify that users have the required permissions for specific actions.

=== "cURL"
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
            Permissions:  []string{"document.read"},
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
            permissions=["document.read"]
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

=== "cURL"
    ```bash
    # 1. Create permissions
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "production", "name": "document.read", "description": "Read documents"}'
    
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "production", "name": "document.write", "description": "Write documents"}'
    
    # 2. Create role
    curl -X POST "https://api.perms.io/permissions-service/v1/roles" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "production", "name": "document_editor", "description": "Can read and write", "permissions": ["PERM_ID_1", "PERM_ID_2"]}'
    
    # 3. Grant permissions
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/assign" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "production", "user_id": "user_123", "resource_uri": "/documents", "roles": ["ROLE_ID"]}'
    
    # 4. Check permissions
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "production", "principal_id": "user_123", "resource_uris": ["/documents/doc_456"], "permissions": ["document.read"]}'
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
        
        permissionsv1 "github.com/PrivateJAR/permio-go/proto/permissions/v1"
    )

    func main() {
        // Connect to the API
        conn, err := grpc.Dial("api.perms.io:443", grpc.WithTransportCredentials(credentials.NewTLS(nil)))
        if err != nil {
            log.Fatalf("Failed to connect: %v", err)
        }
        defer conn.Close()

        client := permissionsv1.NewPermissionsServiceClient(conn)
        
        // Setup authentication context
        ctx := metadata.AppendToOutgoingContext(context.Background(), "authorization", "Bearer YOUR_API_KEY")
        
        // 1. Create permissions
        permissionIds, err := createPermissions(client, ctx)
        if err != nil {
            log.Fatalf("Failed to create permissions: %v", err)
        }
        
        // 2. Create roles
        roleIds, err := createRoles(client, ctx, permissionIds)
        if err != nil {
            log.Fatalf("Failed to create roles: %v", err)
        }
        
        // 3. Grant permissions
        err = grantPermissions(client, ctx, roleIds)
        if err != nil {
            log.Fatalf("Failed to grant permissions: %v", err)
        }
        
        // 4. Check permissions
        err = checkPermissions(client, ctx)
        if err != nil {
            log.Fatalf("Failed to check permissions: %v", err)
        }
        
        fmt.Printf("Setup complete! Your RBAC system is ready to use.\n")
    }
    ```

=== "Python"
    ```python
    import grpc
    from grpc import ssl_channel_credentials
    
    from proto.permissions.v1 import permissions_service_pb2
    from proto.permissions.v1 import permissions_service_pb2_grpc

    def main():
        # 1. Create permissions
        permission_ids = create_permissions()
        
        # 2. Create roles
        role_ids = create_roles(permission_ids)
        
        # 3. Grant permissions
        grant_permissions(role_ids)
        
        # 4. Check permissions
        check_permissions()
        
        print("Setup complete! Your RBAC system is ready to use.")

    if __name__ == "__main__":
        main()
    ```

## Next Steps

Now that you have a working RBAC system, you can:

1. **Integrate with your application** - Add permission checks to your application endpoints
2. **Create more complex hierarchies** - Use nested resource URIs for fine-grained control
3. **Add more users** - Invite team members to your organisation via the dashboard
4. **Monitor usage** - Check the dashboard for usage statistics
5. **Implement caching** - Cache permission results for better performance

## Common Patterns

### Multi-tenant Applications

=== "cURL"
    ```bash
    # Tenant-specific resources
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "principal_id": "user_123",
        "resource_uris": ["/tenant/456/projects/789"],
        "permissions": ["project.read"]
      }'
    ```

=== "Go"
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

=== "cURL"
    ```bash
    # Grant permissions at different levels
    # Organisation level
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/assign" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "production", "user_id": "user_123", "resource_uri": "/organisation/123", "permissions": ["org.admin"]}'
    
    # Project level
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/assign" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"project_name": "production", "user_id": "user_123", "resource_uri": "/organisation/123/project/456", "permissions": ["project.manage"]}'
    ```

=== "Go"
    ```go
    // Grant permissions at different levels
    // Organisation level
    grantPermissions(userId, "/organisation/123", []string{"org.admin"}, []string{})

    // Project level
    grantPermissions(userId, "/organisation/123/project/456", []string{"project.manage"}, []string{})

    // Resource level
    grantPermissions(userId, "/organisation/123/project/456/document/789", []string{"document.edit"}, []string{})
    ```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Check that you have the required permissions for the operation
2. **Resource Not Found**: Verify the resource URIs are correct
3. **Authentication Failed**: Ensure your API key is valid
4. **Rate Limiting**: Implement exponential backoff for API calls

### Getting Help

- Check the [API Reference](./api-reference/organizations.md) for detailed endpoint documentation
- Visit [app.perms.io](https://app.perms.io) for the web dashboard
- Review the [IAM Fundamentals](./iam-basics.md) guide for RBAC concepts

You're now ready to implement fine-grained access control in your applications with perms.io!