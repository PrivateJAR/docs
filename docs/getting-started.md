# Getting Started

Welcome to Permio, an API-First Identity and Access Management (IAM) platform designed for modern applications.

This guide assumes some base level knowledge of IAM, if you are new to IAM, please read the documentation on [IAM basics](iam-basics.md).

## 1. Sign In

Go to [app.perms.io](https://app.perms.io) and log in.

## 2. Create Your Organization

When you first login to your account you will be prompted to create an organisation. The only requirement for an organisation at this stage is a name.

When an organisation is created it will also create a default *project*, but you can create a new one or switch to an alternative in the dashboard in the top left of the screen.

## 3. Define Permissions & Roles

You can define permissions and roles through either the UI or API:

### UI

Navigate to the Permissions page from the burger menu. Click the `Create New Permission` button. New permissions require a name and a description, we recommend using dot notation for the name as it doubles as the id of the permission, for example `customer.info.view`. 

Once created the permission should be visible in the table.

### API

#### Using gRPC (Go)

```go
import (
    "context"
    "log"
    
    permsclient "github.com/perms-io/client-go"
    pb "github.com/perms-io/client-go/proto/permissions_service/v1"
)

func main() {
    // Initialize the client with your API key
    client, err := permsclient.NewClient("your-api-key")
    if err != nil {
        log.Fatalf("Failed to create client: %v", err)
    }
    defer client.Close()
    
    // Create a permission
    permission, err := client.Permissions.CreatePermission(context.Background(), &pb.CreatePermissionRequest{
        ProjectName: "default",
        Name:        "customer.info.view",
        Description: "Permission to view customer information",
    })
    if err != nil {
        log.Fatalf("Failed to create permission: %v", err)
    }
    
    log.Printf("Created permission: %v", permission.Id)
    
    // Create a role with the permission
    role, err := client.Permissions.CreateRole(context.Background(), &pb.CreateRoleRequest{
        ProjectName: "default",
        Name:        "Customer Support",
        Description: "Role for customer support staff",
        Permissions: []string{permission.Id},
    })
    if err != nil {
        log.Fatalf("Failed to create role: %v", err)
    }
    
    log.Printf("Created role: %v", role.Id)
}
```

#### Using REST API

Creating a permission:

```bash
curl -X POST https://api.perms.io/v1/permissions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "customer.info.view",
    "description": "Permission to view customer information"
  }'
```

Creating a role:

```bash
curl -X POST https://api.perms.io/v1/roles \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "Customer Support",
    "description": "Role for customer support staff",
    "permissions": ["permission-id-from-previous-response"]
  }'
```

## 4. Assign Roles to Principals

Attach users or API keys to roles on specific resources.

### Using gRPC (Go)

```go
// Grant permissions and roles to a user on a specific resource
_, err = client.Permissions.GrantUserPermissionsAndRolesOnResource(context.Background(), &pb.GrantUserPermissionsAndRolesOnResourceRequest{
    ProjectName: "default",
    UserId:      "user-123",
    ResourceUri: "/customer/1234",
    Permissions: []string{},  // Optionally assign direct permissions
    Roles:       []string{"role-id-from-previous-step"},
})
if err != nil {
    log.Fatalf("Failed to grant role: %v", err)
}
```

### Using REST API

```bash
curl -X POST https://api.perms.io/v1/grants \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "user_id": "user-123",
    "resource_uri": "/customer/1234",
    "roles": ["role-id-from-previous-step"]
  }'
```

## 5. Perform Permission Checks

Use the check endpoint to authorize requests in your backend.

### Using gRPC (Go)

```go
// Check if a user has the specified permissions
response, err := client.Permissions.Check(context.Background(), &pb.CheckPermissionRequest{
    ProjectName: "default",
    PrincipalId: "user-123",
    ResourceUris: []string{"/customer/1234"},
    Permissions: []string{"customer.info.view"},
})
if err != nil {
    log.Fatalf("Failed to check permission: %v", err)
}

if response.Passed {
    log.Println("User has permission to view customer info")
} else {
    log.Println("Permission denied")
    for _, missingPerm := range response.MissingPermissions {
        log.Printf("Missing permission %v on resource %v", 
            missingPerm.MissingPermissions, missingPerm.ResourceUri)
    }
}
```

### Using REST API

```bash
curl -X POST https://api.perms.io/v1/check \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "principal_id": "user-123",
    "resource_uris": ["/customer/1234"],
    "permissions": ["customer.info.view"]
  }'
```

## Next Steps

Now that you've set up basic permissions and roles:

1. Learn more about [How It Works](how-it-works.md)
2. Explore our [API Reference](api-reference/overview.md)
3. See common implementation patterns in our [Guides](guides/rbac.md)
`
