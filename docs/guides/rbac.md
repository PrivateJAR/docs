# Role-Based Access Control (RBAC)

This guide explains how to implement Role-Based Access Control (RBAC) with Permio, providing practical examples and best practices.

## What is RBAC?

Role-Based Access Control (RBAC) is an approach to restricting system access to authorized users based on roles. In Permio, RBAC is implemented through:

1. **Permissions**: Individual actions that can be performed (e.g., `document.read`)
2. **Roles**: Collections of permissions (e.g., "Editor" role with read and write permissions)
3. **Resources**: Objects that are being protected (e.g., `/documents/123`)
4. **Principals**: Users or API keys that are granted roles

## Basic RBAC Implementation

### Step 1: Define Permissions

Start by defining the granular permissions for your application:

#### Go SDK
```go
import (
    "context"
    "log"
    
    permsclient "github.com/perms-io/client-go"
    pb "github.com/perms-io/client-go/proto/permissions_service/v1"
)

func definePermissions(client *permsclient.Client) (map[string]string, error) {
    ctx := context.Background()
    permissionIds := make(map[string]string)
    
    // Define document permissions
    permissions := []struct {
        name        string
        description string
    }{
        {"document.create", "Create new documents"},
        {"document.read", "View document content"},
        {"document.update", "Modify document content"},
        {"document.delete", "Delete documents"},
        {"document.share", "Share documents with others"},
    }
    
    for _, p := range permissions {
        resp, err := client.Permissions.CreatePermission(ctx, &pb.CreatePermissionRequest{
            ProjectName: "default",
            Name:        p.name,
            Description: p.description,
        })
        if err != nil {
            return nil, err
        }
        
        permissionIds[p.name] = resp.Id
        log.Printf("Created permission: %s with ID: %s", p.name, resp.Id)
    }
    
    return permissionIds, nil
}
```

#### REST API
```bash
# Create document.create permission
curl -X POST https://api.perms.io/v1/permissions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "document.create",
    "description": "Create new documents"
  }'

# Create document.read permission
curl -X POST https://api.perms.io/v1/permissions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "document.read",
    "description": "View document content"
  }'

# Continue for other permissions...
```

### Step 2: Create Roles

Define roles that bundle permissions together for common user types:

#### Go SDK
```go
func createRoles(client *permsclient.Client, permissionIds map[string]string) (map[string]string, error) {
    ctx := context.Background()
    roleIds := make(map[string]string)
    
    // Define roles with their permissions
    roles := []struct {
        name        string
        description string
        permissions []string
    }{
        {
            name:        "Viewer",
            description: "Can only view documents",
            permissions: []string{"document.read"},
        },
        {
            name:        "Editor",
            description: "Can create and modify documents",
            permissions: []string{"document.create", "document.read", "document.update"},
        },
        {
            name:        "Admin",
            description: "Full access to all documents",
            permissions: []string{"document.create", "document.read", "document.update", "document.delete", "document.share"},
        },
    }
    
    for _, r := range roles {
        // Convert permission names to IDs
        permissionIdList := make([]string, 0, len(r.permissions))
        for _, p := range r.permissions {
            permissionIdList = append(permissionIdList, permissionIds[p])
        }
        
        resp, err := client.Permissions.CreateRole(ctx, &pb.CreateRoleRequest{
            ProjectName: "default",
            Name:        r.name,
            Description: r.description,
            Permissions: permissionIdList,
        })
        if err != nil {
            return nil, err
        }
        
        roleIds[r.name] = resp.Id
        log.Printf("Created role: %s with ID: %s", r.name, resp.Id)
    }
    
    return roleIds, nil
}
```

#### REST API
```bash
# Create Viewer role
curl -X POST https://api.perms.io/v1/roles \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "Viewer",
    "description": "Can only view documents",
    "permissions": ["perm_id_from_previous_step"]
  }'
  
# Create Editor role (with multiple permissions)
curl -X POST https://api.perms.io/v1/roles \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "Editor",
    "description": "Can create and modify documents",
    "permissions": ["perm_id_1", "perm_id_2", "perm_id_3"]
  }'
```

### Step 3: Assign Roles to Users

Assign roles to users on specific resources:

#### Go SDK
```go
func assignRoles(client *permsclient.Client, roleIds map[string]string) error {
    ctx := context.Background()
    
    // Team structure
    assignments := []struct {
        userId      string
        resourceUri string
        role        string
    }{
        {"user123", "/workspace/docs", "Viewer"},
        {"user456", "/workspace/docs", "Editor"},
        {"user789", "/workspace/docs", "Admin"},
        {"user123", "/workspace/shared", "Editor"}, // Same user, different resource
    }
    
    for _, a := range assignments {
        _, err := client.Permissions.GrantUserPermissionsAndRolesOnResource(ctx, &pb.GrantUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "default",
            UserId:      a.userId,
            ResourceUri: a.resourceUri,
            Roles:       []string{roleIds[a.role]},
        })
        if err != nil {
            return err
        }
        
        log.Printf("Assigned role %s to user %s on resource %s", a.role, a.userId, a.resourceUri)
    }
    
    return nil
}
```

#### REST API
```bash
# Assign Admin role to user789 on the docs workspace
curl -X POST https://api.perms.io/v1/grants \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "user_id": "user789",
    "resource_uri": "/workspace/docs",
    "roles": ["role_id_for_admin"]
  }'
```

### Step 4: Check Permissions

Check if a user has the required permissions for an action:

#### Go SDK
```go
func checkAccess(client *permsclient.Client, userId string, resourceUri string, permission string) (bool, error) {
    ctx := context.Background()
    
    resp, err := client.Permissions.Check(ctx, &pb.CheckPermissionRequest{
        ProjectName:  "default",
        PrincipalId:  userId,
        ResourceUris: []string{resourceUri},
        Permissions:  []string{permission},
    })
    if err != nil {
        return false, err
    }
    
    if resp.Passed {
        log.Printf("Access GRANTED for user %s on resource %s for permission %s", userId, resourceUri, permission)
        return true, nil
    } else {
        log.Printf("Access DENIED for user %s on resource %s for permission %s", userId, resourceUri, permission)
        return false, nil
    }
}

// Usage example
func handleDocumentAccess(client *permsclient.Client) {
    // Check if user123 can read a document
    hasAccess, _ := checkAccess(client, "user123", "/workspace/docs/report.pdf", "document.read")
    if hasAccess {
        // Serve the document
    } else {
        // Show access denied message
    }
    
    // Check if user456 can edit a document
    hasAccess, _ = checkAccess(client, "user456", "/workspace/docs/report.pdf", "document.update")
    if hasAccess {
        // Allow document editing
    } else {
        // Show read-only view
    }
}
```

#### REST API
```bash
# Check if user123 has document.read permission
curl -X POST https://api.perms.io/v1/check \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "principal_id": "user123",
    "resource_uris": ["/workspace/docs/report.pdf"],
    "permissions": ["document.read"]
  }'
```

## Advanced RBAC Patterns

### Dynamic Resource-Based Authorization

Permio's resource URI system allows for dynamic authorization patterns where access control adapts to your data structure.

#### Example: Team-Based Access Control

```go
// Grant access at the team level
_, err = client.Permissions.GrantUserPermissionsAndRolesOnResource(ctx, &pb.GrantUserPermissionsAndRolesOnResourceRequest{
    ProjectName: "default",
    UserId:      "team_lead_user",
    ResourceUri: "/teams/engineering",  // Team-level resource
    Roles:       []string{teamLeadRoleId},
})

// Later, check access to a project within that team
resp, err := client.Permissions.Check(ctx, &pb.CheckPermissionRequest{
    ProjectName:  "default",
    PrincipalId:  "team_lead_user",
    ResourceUris: []string{"/teams/engineering/projects/new-service"},
    Permissions:  []string{"project.edit"},
})

// The user will have access due to hierarchical inheritance
```

### Role Composition

Create more complex access control by composing roles:

```go
// Create base roles
viewerRoleId := createRoleWithPermissions("Viewer", []string{"resource.view"})
commenterRoleId := createRoleWithPermissions("Commenter", []string{"resource.comment"})

// Create a composed role
composedRole, err := client.Permissions.CreateRole(ctx, &pb.CreateRoleRequest{
    ProjectName: "default",
    Name:        "Reviewer",
    Description: "Can view content and add comments",
    Permissions: []string{"resource.view", "resource.comment"},
})
```

### Temporary Access Grants

For systems requiring temporary access:

```go
// In your application logic, implement expiring access
func grantTemporaryAccess(client *permsclient.Client, userId string, resourceUri string, role string, durationMinutes int) {
    // Grant the role
    _, err := client.Permissions.GrantUserPermissionsAndRolesOnResource(ctx, &pb.GrantUserPermissionsAndRolesOnResourceRequest{
        ProjectName: "default",
        UserId:      userId,
        ResourceUri: resourceUri,
        Roles:       []string{role},
    })
    
    // Set up a background task to revoke after duration
    time.AfterFunc(time.Duration(durationMinutes)*time.Minute, func() {
        _, err := client.Permissions.RevokeUserPermissionsAndRolesOnResource(ctx, &pb.RevokeUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "default",
            UserId:      userId,
            ResourceUri: resourceUri,
            Roles:       []string{role},
        })
        if err != nil {
            log.Printf("Failed to revoke temporary access: %v", err)
        }
    })
}
```

## Best Practices

### Permission Naming Conventions

Use a consistent naming pattern for permissions:

- Use lowercase with dot notation: `object.action`
- Examples: `document.read`, `user.update`, `payment.process`

### Role Design Principles

1. **Least Privilege**: Assign only the permissions needed for the job
2. **Role Granularity**: Create focused roles rather than catch-all roles
3. **Consistency**: Use consistent naming across roles

### Resource URI Structure

Design your resource URI hierarchy to take advantage of Permio's inheritance:

```
/organizations/{org_id}
/organizations/{org_id}/teams/{team_id}
/organizations/{org_id}/teams/{team_id}/projects/{project_id}
/organizations/{org_id}/teams/{team_id}/projects/{project_id}/resources/{resource_id}
```

With this structure, permissions granted at higher levels automatically propagate down.

### Implementing Multi-Tenancy

For multi-tenant applications, incorporate the tenant ID in your resource URIs:

```
/tenants/{tenant_id}/resources/{resource_id}
```

This approach allows for clean separation of authorization between tenants.

### Debugging Access Issues

When troubleshooting access problems:

1. Check the specific permissions the user is missing with the check endpoint
2. Verify the resource URI is correct and matches your hierarchy
3. Consider parent resources that might have inherited permissions

```go
// Detailed permission check for debugging
resp, err := client.Permissions.Check(ctx, &pb.CheckPermissionRequest{
    ProjectName:  "default",
    PrincipalId:  userId,
    ResourceUris: []string{resourceUri},
    Permissions:  []string{"document.read", "document.update", "document.delete"},
})

if !resp.Passed {
    for _, missing := range resp.MissingPermissions {
        log.Printf("Resource %s missing permissions: %v", 
            missing.ResourceUri, missing.MissingPermissions)
    }
}
```

## RBAC Audit and Compliance

For organizations requiring compliance and auditing:

1. Regularly review role assignments
2. Generate reports of who has access to what
3. Monitor permission checks for suspicious patterns

```go
// List all principals with access to sensitive data
assignmentsResp, err := client.Permissions.GetAllAssignmentsForResource(ctx, &pb.GetAllAssignmentsForResourceRequest{
    ProjectName: "default",
    ResourceUri: "/sensitive-data",
})

// Review all roles and permissions assigned to a user
userAssignmentsResp, err := client.Permissions.GetAllAssignmentsForPrincipal(ctx, &pb.GetAllAssignmentsForPrincipalRequest{
    ProjectName: "default",
    PrincipalId: "user123",
})
```

## Conclusion

Implementing RBAC with Permio gives you a flexible, scalable authorization system that can adapt to your application's needs. By leveraging the hierarchical resource model, you can build sophisticated access control systems with minimal code.

For more advanced use cases, see our guides on:
- [Resource Inheritance](resource-inheritance.md)
- [Principal Management](principal-management.md)
- [API Keys](api-keys.md)
