# Pagination

The perms.io API uses cursor-based pagination for efficient traversal of large result sets. This approach provides consistent performance regardless of the dataset size and handles real-time data changes gracefully.

## Overview

Cursor-based pagination uses opaque tokens to mark positions in result sets, making it ideal for:
- Large datasets with frequent updates
- Real-time applications requiring consistent performance
- APIs that need to handle concurrent modifications

## Pagination Request

All list endpoints support optional pagination parameters:

```protobuf
message PaginationRequest {
  // The number of items to return. Must be between 1 and 100. Default is 10.
  optional int32 limit = 1;
  // The cursor to start from. If not provided, starts from the beginning.
  optional string cursor = 2;
}
```

### Parameters

- **limit**: Number of items per page (1-100, default: 10)
- **cursor**: Token indicating where to start the next page

## Pagination Response

List endpoints return pagination metadata in their responses:

```protobuf
message PaginationResponse {
  // The next cursor to use for the next page of results. If there are no more pages, this will be empty.
  string next_cursor = 1;
}
```

### Response Fields

- **next_cursor**: Token for the next page (empty if no more pages)

## Usage Examples

### Basic Pagination

=== "HTTP"
    ```http
    GET /permissions-service/v1/permissions?project_name=production&limit=10
    ```

    ```json
    {
      "permissions": [...],
      "pagination": {
        "next_cursor": "eyJpZCI6IjEyMyIsInRzIjoiMjAyNC0wMS0xNVQxMDowMDowMFoifQ=="
      }
    }
    ```

=== "Go"
    ```go
    func listAllPermissions(client permissionsv1.PermissionsServiceClient, projectName string) {
        var allPermissions []*permissionsv1.Permission
        var cursor *string
        
        for {
            req := &permissionsv1.ListPermissionsRequest{
                ProjectName: projectName,
                Pagination: &paginationv1.PaginationRequest{
                    Limit: proto.Int32(50),
                },
            }
            
            if cursor != nil {
                req.Pagination.Cursor = cursor
            }
            
            resp, err := client.ListPermissions(context.Background(), req)
            if err != nil {
                log.Fatalf("Failed to list permissions: %v", err)
            }
            
            allPermissions = append(allPermissions, resp.Permissions...)
            
            // Check if there are more pages
            if resp.Pagination.NextCursor == "" {
                break
            }
            cursor = &resp.Pagination.NextCursor
        }
        
        log.Printf("Retrieved %d total permissions", len(allPermissions))
    }
    ```

=== "Rust"
    ```rust
    use permio_proto::permissions::v1::{
        permissions_service_client::PermissionsServiceClient,
        ListPermissionsRequest,
    };
    use permio_proto::pagination::PaginationRequest;
    use tonic::transport::Channel;

    async fn list_all_permissions(client: &mut PermissionsServiceClient<Channel>, project_name: &str) -> Result<Vec<Permission>, Box<dyn std::error::Error>> {
        let mut all_permissions = Vec::new();
        let mut cursor: Option<String> = None;
        
        loop {
            let mut pagination = PaginationRequest {
                limit: Some(50),
                cursor: cursor.clone(),
            };
            
            let request = tonic::Request::new(ListPermissionsRequest {
                project_name: project_name.to_string(),
                pagination: Some(pagination),
                search: None,
            });
            
            let response = client.list_permissions(request).await?;
            let list_response = response.get_ref();
            
            all_permissions.extend(list_response.permissions.clone());
            
            // Check if there are more pages
            if let Some(pagination_response) = &list_response.pagination {
                if pagination_response.next_cursor.is_empty() {
                    break;
                }
                cursor = Some(pagination_response.next_cursor.clone());
            } else {
                break;
            }
        }
        
        println!("Retrieved {} total permissions", all_permissions.len());
        Ok(all_permissions)
    }
    ```

=== "Python"
    ```python
    def list_all_permissions(client, project_name: str):
        all_permissions = []
        cursor = None
        
        while True:
            request = permissions_service_pb2.ListPermissionsRequest(
                project_name=project_name,
                pagination=pagination_pb2.PaginationRequest(limit=50)
            )
            
            if cursor:
                request.pagination.cursor = cursor
            
            response = client.ListPermissions(request)
            all_permissions.extend(response.permissions)
            
            # Check if there are more pages
            if not response.pagination.next_cursor:
                break
            cursor = response.pagination.next_cursor
        
        print(f"Retrieved {len(all_permissions)} total permissions")
        return all_permissions
    ```

=== "Java"
    ```java
    import java.util.ArrayList;
    import java.util.List;
    import permio.permissions.v1.PermissionsServiceGrpc;
    import permio.permissions.v1.Permissions.ListPermissionsRequest;
    import permio.permissions.v1.Permissions.ListPermissionsResponse;
    import permio.permissions.v1.Permissions.Permission;
    import permio.pagination.PaginationOuterClass.PaginationRequest;

    public List<Permission> listAllPermissions(PermissionsServiceGrpc.PermissionsServiceBlockingStub client, String projectName) {
        List<Permission> allPermissions = new ArrayList<>();
        String cursor = null;
        
        while (true) {
            PaginationRequest.Builder paginationBuilder = PaginationRequest.newBuilder()
                    .setLimit(50);
            
            if (cursor != null) {
                paginationBuilder.setCursor(cursor);
            }
            
            ListPermissionsRequest request = ListPermissionsRequest.newBuilder()
                    .setProjectName(projectName)
                    .setPagination(paginationBuilder.build())
                    .build();
            
            ListPermissionsResponse response = client.listPermissions(request);
            allPermissions.addAll(response.getPermissionsList());
            
            // Check if there are more pages
            if (response.getPagination().getNextCursor().isEmpty()) {
                break;
            }
            cursor = response.getPagination().getNextCursor();
        }
        
        System.out.println("Retrieved " + allPermissions.size() + " total permissions");
        return allPermissions;
    }
    ```

=== "TypeScript"
    ```typescript
    interface ListPermissionsRequest {
        project_name: string;
        pagination?: {
            limit?: number;
            cursor?: string;
        };
        search?: string;
    }

    interface Permission {
        id: string;
        name: string;
        description: string;
    }

    async function listAllPermissions(client: any, projectName: string): Promise<Permission[]> {
        const allPermissions: Permission[] = [];
        let cursor: string | null = null;
        
        while (true) {
            const request: ListPermissionsRequest = {
                project_name: projectName,
                pagination: { limit: 50 }
            };
            
            if (cursor) {
                request.pagination!.cursor = cursor;
            }
            
            const response = await new Promise<any>((resolve, reject) => {
                client.ListPermissions(request, (error: Error | null, response: any) => {
                    if (error) reject(error);
                    else resolve(response);
                });
            });
            
            allPermissions.push(...response.permissions);
            
            // Check if there are more pages
            if (!response.pagination.next_cursor) {
                break;
            }
            cursor = response.pagination.next_cursor;
        }
        
        console.log(`Retrieved ${allPermissions.length} total permissions`);
        return allPermissions;
    }
    ```

### Next Page Request

=== "HTTP"
    ```http
    GET /permissions-service/v1/permissions?project_name=production&limit=10&cursor=eyJpZCI6IjEyMyIsInRzIjoiMjAyNC0wMS0xNVQxMDowMDowMFoifQ==
    ```

### Handling Search with Pagination

When using search parameters, pagination works the same way:

=== "HTTP"
    ```http
    GET /permissions-service/v1/permissions?project_name=production&search=document&limit=10
    ```

=== "Go"
    ```go
    func searchPermissions(client permissionsv1.PermissionsServiceClient, projectName, searchTerm string) {
        req := &permissionsv1.ListPermissionsRequest{
            ProjectName: projectName,
            Search:      proto.String(searchTerm),
            Pagination: &paginationv1.PaginationRequest{
                Limit: proto.Int32(20),
            },
        }
        
        resp, err := client.ListPermissions(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to search permissions: %v", err)
        }
        
        log.Printf("Found %d permissions matching '%s'", len(resp.Permissions), searchTerm)
        
        // Process next page if available
        if resp.Pagination.NextCursor != "" {
            log.Printf("Next page available with cursor: %s", resp.Pagination.NextCursor)
        }
    }
    ```

=== "Rust"
    ```rust
    async fn search_permissions(client: &mut PermissionsServiceClient<Channel>, project_name: &str, search_term: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(ListPermissionsRequest {
            project_name: project_name.to_string(),
            search: Some(search_term.to_string()),
            pagination: Some(PaginationRequest {
                limit: Some(20),
                cursor: None,
            }),
        });
        
        let response = client.list_permissions(request).await?;
        let list_response = response.get_ref();
        
        println!("Found {} permissions matching '{}'", list_response.permissions.len(), search_term);
        
        // Process next page if available
        if let Some(pagination) = &list_response.pagination {
            if !pagination.next_cursor.is_empty() {
                println!("Next page available with cursor: {}", pagination.next_cursor);
            }
        }
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def search_permissions(client, project_name: str, search_term: str):
        request = permissions_service_pb2.ListPermissionsRequest(
            project_name=project_name,
            search=search_term,
            pagination=pagination_pb2.PaginationRequest(limit=20)
        )
        
        response = client.ListPermissions(request)
        
        print(f"Found {len(response.permissions)} permissions matching '{search_term}'")
        
        # Process next page if available
        if response.pagination.next_cursor:
            print(f"Next page available with cursor: {response.pagination.next_cursor}")
    ```

=== "Java"
    ```java
    public void searchPermissions(PermissionsServiceGrpc.PermissionsServiceBlockingStub client, String projectName, String searchTerm) {
        ListPermissionsRequest request = ListPermissionsRequest.newBuilder()
                .setProjectName(projectName)
                .setSearch(searchTerm)
                .setPagination(PaginationRequest.newBuilder().setLimit(20).build())
                .build();
        
        ListPermissionsResponse response = client.listPermissions(request);
        
        System.out.println("Found " + response.getPermissionsCount() + " permissions matching '" + searchTerm + "'");
        
        // Process next page if available
        if (!response.getPagination().getNextCursor().isEmpty()) {
            System.out.println("Next page available with cursor: " + response.getPagination().getNextCursor());
        }
    }
    ```

=== "TypeScript"
    ```typescript
    function searchPermissions(client: any, projectName: string, searchTerm: string): void {
        const request: ListPermissionsRequest = {
            project_name: projectName,
            search: searchTerm,
            pagination: {
                limit: 20
            }
        };
        
        client.ListPermissions(request, (error: Error | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            console.log(`Found ${response.permissions.length} permissions matching '${searchTerm}'`);
            
            // Process next page if available
            if (response.pagination.next_cursor) {
                console.log(`Next page available with cursor: ${response.pagination.next_cursor}`);
            }
        });
    }
    ```

## Best Practices

### 1. Choose Appropriate Page Sizes

- **Small pages (10-25)**: Better for user interfaces, real-time updates
- **Medium pages (50-100)**: Good balance for most use cases
- **Large pages (100)**: Better for bulk operations, data processing

### 2. Handle Empty Results

Always check for empty result sets:

```go
if len(resp.Permissions) == 0 {
    log.Printf("No permissions found")
    return
}
```

### 3. Store Cursors Appropriately

- **Short-term**: Store in memory or session storage
- **Long-term**: Store in database for resumable operations
- **Never**: Attempt to decode or manipulate cursor values

### 4. Implement Retry Logic

```go
func listPermissionsWithRetry(client permissionsv1.PermissionsServiceClient, req *permissionsv1.ListPermissionsRequest) (*permissionsv1.ListPermissionsResponse, error) {
    maxRetries := 3
    for i := 0; i < maxRetries; i++ {
        resp, err := client.ListPermissions(context.Background(), req)
        if err == nil {
            return resp, nil
        }
        
        if i == maxRetries-1 {
            return nil, err
        }
        
        // Exponential backoff
        time.Sleep(time.Duration(1<<i) * time.Second)
    }
    return nil, nil
}
```

### 5. Monitor Performance

Track pagination performance metrics:
- Average response times by page size
- Memory usage for large result sets
- Error rates for different cursor ages

## Pagination Patterns

### Simple Iteration

For processing all items in a collection:

```go
func processAllRoles(client permissionsv1.PermissionsServiceClient, projectName string) {
    var cursor *string
    
    for {
        roles, nextCursor, err := getRolesPage(client, projectName, cursor, 50)
        if err != nil {
            log.Printf("Error fetching roles: %v", err)
            break
        }
        
        // Process each role
        for _, role := range roles {
            processRole(role)
        }
        
        if nextCursor == "" {
            break
        }
        cursor = &nextCursor
    }
}
```

### Concurrent Processing

For parallel processing of paginated results:

```go
func processPrincipalsAsync(client permissionsv1.PermissionsServiceClient, projectName string) {
    type pageResult struct {
        principals []*string
        cursor     string
        err        error
    }
    
    resultChan := make(chan pageResult, 10)
    var wg sync.WaitGroup
    
    // Start first page
    wg.Add(1)
    go func() {
        defer wg.Done()
        principals, cursor, err := getPrincipalsPage(client, projectName, nil, 100)
        resultChan <- pageResult{principals, cursor, err}
    }()
    
    // Process results and spawn next page requests
    go func() {
        for result := range resultChan {
            if result.err != nil {
                log.Printf("Error: %v", result.err)
                continue
            }
            
            // Process principals
            for _, principal := range result.principals {
                log.Printf("Processing principal: %s", *principal)
            }
            
            // Spawn next page if available
            if result.cursor != "" {
                wg.Add(1)
                go func(cursor string) {
                    defer wg.Done()
                    principals, nextCursor, err := getPrincipalsPage(client, projectName, &cursor, 100)
                    resultChan <- pageResult{principals, nextCursor, err}
                }(result.cursor)
            }
        }
    }()
    
    wg.Wait()
    close(resultChan)
}
```

## Error Handling

### Cursor Expiration

Cursors may expire after a certain period. Handle this gracefully:

```go
func handleCursorExpiration(client permissionsv1.PermissionsServiceClient, req *permissionsv1.ListPermissionsRequest) {
    resp, err := client.ListPermissions(context.Background(), req)
    if err != nil {
        if isCursorExpiredError(err) {
            log.Printf("Cursor expired, restarting from beginning")
            req.Pagination.Cursor = nil
            resp, err = client.ListPermissions(context.Background(), req)
        }
        
        if err != nil {
            log.Fatalf("Failed to list permissions: %v", err)
        }
    }
    
    // Process response...
}
```

### Rate Limiting

Implement rate limiting between requests:

```go
func listWithRateLimit(client permissionsv1.PermissionsServiceClient, projectName string) {
    rateLimiter := time.NewTicker(100 * time.Millisecond)
    defer rateLimiter.Stop()
    
    var cursor *string
    
    for {
        <-rateLimiter.C // Wait for rate limit
        
        roles, nextCursor, err := getRolesPage(client, projectName, cursor, 50)
        if err != nil {
            log.Printf("Error: %v", err)
            break
        }
        
        processRoles(roles)
        
        if nextCursor == "" {
            break
        }
        cursor = &nextCursor
    }
}
```

## Limitations

- **Maximum limit**: 100 items per page
- **Cursor lifetime**: Cursors expire after 24 hours
- **Sort stability**: Results are sorted by creation time and ID
- **Concurrent modifications**: Results may include items created during iteration

## Endpoints Supporting Pagination

All list endpoints support pagination:

- `ListPermissions`
- `ListRoles`  
- `ListPrincipals`
- `GetAllAssignmentsForPrincipal`
- `ListAPIKeys`
- `GetProjectsForOrganisation`

## Migration from Offset-Based Pagination

If migrating from offset-based pagination:

```go
// Old offset-based approach
func listPermissionsOffset(offset, limit int) {
    // This approach doesn't work with cursor-based pagination
}

// New cursor-based approach
func listPermissionsCursor(cursor *string, limit int) {
    req := &permissionsv1.ListPermissionsRequest{
        ProjectName: "production",
        Pagination: &paginationv1.PaginationRequest{
            Limit: proto.Int32(int32(limit)),
        },
    }
    
    if cursor != nil {
        req.Pagination.Cursor = cursor
    }
    
    // Make request...
}
```

## Testing Pagination

### Unit Tests

```go
func TestPaginationFlow(t *testing.T) {
    // Mock client setup
    client := &mockPermissionsClient{}
    
    // Test first page
    resp1, err := client.ListPermissions(context.Background(), &permissionsv1.ListPermissionsRequest{
        ProjectName: "test",
        Pagination: &paginationv1.PaginationRequest{
            Limit: proto.Int32(2),
        },
    })
    assert.NoError(t, err)
    assert.Len(t, resp1.Permissions, 2)
    assert.NotEmpty(t, resp1.Pagination.NextCursor)
    
    // Test second page
    resp2, err := client.ListPermissions(context.Background(), &permissionsv1.ListPermissionsRequest{
        ProjectName: "test",
        Pagination: &paginationv1.PaginationRequest{
            Limit:  proto.Int32(2),
            Cursor: &resp1.Pagination.NextCursor,
        },
    })
    assert.NoError(t, err)
    assert.Len(t, resp2.Permissions, 2)
    
    // Verify different results
    assert.NotEqual(t, resp1.Permissions[0].Id, resp2.Permissions[0].Id)
}
```