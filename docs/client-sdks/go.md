# Go Client SDK

The Permio Go Client SDK provides a simple and idiomatic way to interact with the Permio API from your Go applications.

## Installation

Install the client library using `go get`:

```bash
go get github.com/perms-io/client-go
```

## Initialization

Initialize the client with your API key:

```go
import (
    "context"
    
    permsclient "github.com/perms-io/client-go"
)

func main() {
    // Create a new client with an API key
    client, err := permsclient.NewClient("your-api-key")
    if err != nil {
        panic(err)
    }
    defer client.Close()
    
    // The client is now ready to use
    // client.Permissions - access Permissions Service
    // client.Organisation - access Organisation Service
}
```

## Client Configuration

Customize the client behavior with options:

```go
import (
    "context"
    "time"
    
    permsclient "github.com/perms-io/client-go"
    "github.com/perms-io/client-go/options"
)

func main() {
    // Create a client with custom options
    client, err := permsclient.NewClient(
        "your-api-key",
        options.WithTimeout(5 * time.Second),
        options.WithEndpoint("https://custom-api.perms.io"),
        options.WithRetries(3),
    )
    if err != nil {
        panic(err)
    }
    defer client.Close()
}
```

## Error Handling

The SDK returns standard errors that you can handle appropriately:

```go
permission, err := client.Permissions.CreatePermission(context.Background(), &pb.CreatePermissionRequest{
    ProjectName: "default",
    Name:        "document.read",
    Description: "Permission to read documents",
})

if err != nil {
    // Handle specific error types
    if permsclient.IsPermissionDeniedError(err) {
        log.Println("You don't have permission to create permissions")
    } else if permsclient.IsNotFoundError(err) {
        log.Println("Project not found")
    } else if permsclient.IsAlreadyExistsError(err) {
        log.Println("Permission with this name already exists")
    } else {
        log.Printf("Unknown error: %v", err)
    }
    return
}
```

## Common Use Cases

### Permission Management

```go
import (
    "context"
    
    permsclient "github.com/perms-io/client-go"
    pb "github.com/perms-io/client-go/proto/permissions_service/v1"
)

func main() {
    client, err := permsclient.NewClient("your-api-key")
    if err != nil {
        panic(err)
    }
    defer client.Close()
    
    // Create permissions
    viewPermission, err := client.Permissions.CreatePermission(context.Background(), &pb.CreatePermissionRequest{
        ProjectName: "default",
        Name:        "invoice.view",
        Description: "View invoice details",
    })
    if err != nil {
        panic(err)
    }
    
    editPermission, err := client.Permissions.CreatePermission(context.Background(), &pb.CreatePermissionRequest{
        ProjectName: "default",
        Name:        "invoice.edit",
        Description: "Edit invoice details",
    })
    if err != nil {
        panic(err)
    }
    
    // Create a role with these permissions
    role, err := client.Permissions.CreateRole(context.Background(), &pb.CreateRoleRequest{
        ProjectName: "default",
        Name:        "Invoice Manager",
        Description: "Can view and edit invoices",
        Permissions: []string{viewPermission.Id, editPermission.Id},
    })
    if err != nil {
        panic(err)
    }
    
    // Assign role to a user on a specific resource
    _, err = client.Permissions.GrantUserPermissionsAndRolesOnResource(context.Background(), &pb.GrantUserPermissionsAndRolesOnResourceRequest{
        ProjectName: "default",
        UserId:      "user-123",
        ResourceUri: "/invoices/5678",
        Roles:       []string{role.Id},
    })
    if err != nil {
        panic(err)
    }
    
    // Check if the user has permission to view the invoice
    checkResponse, err := client.Permissions.Check(context.Background(), &pb.CheckPermissionRequest{
        ProjectName:  "default",
        PrincipalId:  "user-123",
        ResourceUris: []string{"/invoices/5678"},
        Permissions:  []string{"invoice.view"},
    })
    if err != nil {
        panic(err)
    }
    
    if checkResponse.Passed {
        fmt.Println("User can view the invoice")
    } else {
        fmt.Println("Access denied")
    }
}
```

### Organization and Project Management

```go
import (
    "context"
    
    permsclient "github.com/perms-io/client-go"
    org_pb "github.com/perms-io/client-go/proto/organisation_service/v1"
)

func main() {
    client, err := permsclient.NewClient("your-api-key")
    if err != nil {
        panic(err)
    }
    defer client.Close()
    
    // Create a new organization
    orgResponse, err := client.Organisation.CreateOrganisation(context.Background(), &org_pb.CreateOrganisationRequest{
        Name:   "My Company",
        UserId: "user-123",
    })
    if err != nil {
        panic(err)
    }
    
    orgId := orgResponse.Organisation.Id
    
    // Create a new project
    projectResponse, err := client.Organisation.CreateProject(context.Background(), &org_pb.CreateProjectRequest{
        OrganisationId: orgId,
        Name:           "mobile-backend",
    })
    if err != nil {
        panic(err)
    }
    
    // Create an API key for this project
    apiKeyResponse, err := client.Organisation.CreateAPIKey(context.Background(), &org_pb.CreateAPIKeyRequest{
        OrganisationId: orgId,
        ProjectName:    projectResponse.Project.Name,
        Name:           "Mobile API Key",
    })
    if err != nil {
        panic(err)
    }
    
    // Save this API key, it won't be retrievable again
    fmt.Printf("New API Key: %s\n", apiKeyResponse.ApiKey.Key)
}
```

## Integration with Middleware

Integrate Permio authorization into your HTTP handlers:

```go
import (
    "net/http"
    
    permsclient "github.com/perms-io/client-go"
    pb "github.com/perms-io/client-go/proto/permissions_service/v1"
)

func PermioAuthMiddleware(client *permsclient.Client, projectName string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // Get user ID from your authentication system
            userId := r.Header.Get("X-User-ID")
            if userId == "" {
                http.Error(w, "Unauthorized", http.StatusUnauthorized)
                return
            }
            
            // Extract resource ID from URL parameters
            resourceId := r.URL.Path // e.g., "/invoices/123"
            
            // Check if user has required permission
            checkResponse, err := client.Permissions.Check(r.Context(), &pb.CheckPermissionRequest{
                ProjectName:  projectName,
                PrincipalId:  userId,
                ResourceUris: []string{resourceId},
                Permissions:  []string{"invoice.view"}, // Permission needed for this endpoint
            })
            
            if err != nil {
                http.Error(w, "Authorization service error", http.StatusInternalServerError)
                return
            }
            
            if !checkResponse.Passed {
                http.Error(w, "Permission denied", http.StatusForbidden)
                return
            }
            
            // User has permission, continue to the handler
            next.ServeHTTP(w, r)
        })
    }
}

// Usage in main application
func main() {
    client, _ := permsclient.NewClient("your-api-key")
    defer client.Close()
    
    // Create a router (using standard library for simplicity)
    mux := http.NewServeMux()
    
    // Register routes with authorization middleware
    mux.Handle("/invoices/", PermioAuthMiddleware(client, "default")(
        http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // Handler code for invoices endpoint
            w.Write([]byte("Invoice details"))
        }),
    ))
    
    http.ListenAndServe(":8080", mux)
}
```

## Batch Operations

Efficiently check multiple permissions at once:

```go
checkResponse, err := client.Permissions.Check(context.Background(), &pb.CheckPermissionRequest{
    ProjectName: "default",
    PrincipalId: "user-123",
    ResourceUris: []string{
        "/documents/123",
        "/documents/456",
        "/documents/789",
    },
    Permissions: []string{"document.read", "document.edit"},
})

if err != nil {
    panic(err)
}

if checkResponse.Passed {
    // User has all permissions on all resources
    fmt.Println("Full access granted")
} else {
    // Check which specific permissions are missing
    for _, missing := range checkResponse.MissingPermissions {
        fmt.Printf("Resource %s is missing: %v\n", missing.ResourceUri, missing.MissingPermissions)
    }
}
```

## Advanced Patterns

### Hierarchical Resource Authorization

Take advantage of Permio's hierarchical inheritance model:

```go
// Grant admin role at department level
_, err = client.Permissions.GrantUserPermissionsAndRolesOnResource(context.Background(), &pb.GrantUserPermissionsAndRolesOnResourceRequest{
    ProjectName: "default",
    UserId:      "manager-456",
    ResourceUri: "/departments/engineering",  // Parent resource
    Roles:       []string{"departmentAdmin"},
})

// Check permission on a child resource
checkResponse, err := client.Permissions.Check(context.Background(), &pb.CheckPermissionRequest{
    ProjectName:  "default",
    PrincipalId:  "manager-456",
    ResourceUris: []string{"/departments/engineering/teams/frontend/projects/redesign"},  // Child resource
    Permissions:  []string{"project.view"},
})

// The manager will have this permission due to hierarchical inheritance
```

### Caching Authorization Results

Implement caching for performance optimization:

```go
import (
    "context"
    "time"
    
    "github.com/patrickmn/go-cache"
    permsclient "github.com/perms-io/client-go"
    pb "github.com/perms-io/client-go/proto/permissions_service/v1"
)

type CachedPermioClient struct {
    client *permsclient.Client
    cache  *cache.Cache
}

func NewCachedPermioClient(apiKey string) (*CachedPermioClient, error) {
    client, err := permsclient.NewClient(apiKey)
    if err != nil {
        return nil, err
    }
    
    return &CachedPermioClient{
        client: client,
        cache:  cache.New(5*time.Minute, 10*time.Minute),
    }, nil
}

func (c *CachedPermioClient) Close() {
    c.client.Close()
}

func (c *CachedPermioClient) CheckPermission(ctx context.Context, principalId string, resourceUri string, permission string) (bool, error) {
    // Create a cache key
    cacheKey := principalId + ":" + resourceUri + ":" + permission
    
    // Check if we have a cached result
    if result, found := c.cache.Get(cacheKey); found {
        return result.(bool), nil
    }
    
    // Otherwise, make the API call
    resp, err := c.client.Permissions.Check(ctx, &pb.CheckPermissionRequest{
        ProjectName:  "default",
        PrincipalId:  principalId,
        ResourceUris: []string{resourceUri},
        Permissions:  []string{permission},
    })
    
    if err != nil {
        return false, err
    }
    
    // Cache the result for future checks
    c.cache.Set(cacheKey, resp.Passed, cache.DefaultExpiration)
    
    return resp.Passed, nil
}
```

## Troubleshooting

Common issues and their solutions:

### Connection Issues

If you're having trouble connecting to the Permio API:

```go
client, err := permsclient.NewClient(
    "your-api-key",
    options.WithDebug(true),  // Enable debug logging
    options.WithTimeout(10 * time.Second),  // Increase timeout
)
```

### Rate Limiting

If you're encountering rate limits:

```go
client, err := permsclient.NewClient(
    "your-api-key",
    options.WithRetries(5),  // Increase retry count
    options.WithBackoffFactor(1.5),  // Use exponential backoff
)
```

### Large Request Sets

For checking permissions on many resources at once:

```go
// Split into smaller batches
const batchSize = 50
resourceUris := []string{...} // Large set of resources

for i := 0; i < len(resourceUris); i += batchSize {
    end := i + batchSize
    if end > len(resourceUris) {
        end = len(resourceUris)
    }
    
    batch := resourceUris[i:end]
    resp, err := client.Permissions.Check(ctx, &pb.CheckPermissionRequest{
        ProjectName:  "default",
        PrincipalId:  "user-123",
        ResourceUris: batch,
        Permissions:  []string{"resource.view"},
    })
    
    // Process batch result
}
```
