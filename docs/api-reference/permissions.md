# Permissions & Roles

Manage permissions, roles, and access control through perms.io's **Resource-Specific Role-Based Access Control (RBAC)** system. Control who can access what resources in your application with fine-grained precision.

## Overview

The permissions system implements a hierarchical RBAC model with the following key components:

- **Permissions**: Individual actions that can be performed (e.g., `read`, `write`, `delete`)
- **Roles**: Collections of permissions that can be assigned as a group
- **Principals**: Users or entities that can be granted permissions
- **Resources**: Specific objects or paths that permissions apply to (e.g., `/project/123`, `/user/456/documents`)

### Key Features

- **Resource-Specific Access**: Permissions apply to specific resource URIs
- **Hierarchical Inheritance**: Permissions on parent resources cascade to child resources
- **Flexible Principal Model**: Support for users, service accounts, and other principal types
- **High-Performance Checks**: Optimized permission checking for real-time applications

## Base URL

```
https://api.perms.io/permissions-service/v1
```

## Permission Management

### Create Permission

Creates a new permission within a project. Permissions are idempotent - creating an existing permission will update it.

**Required Permission**: `permission.create` on `/organisation/{organisation_id}`

=== "cURL"
    ```bash
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "document.read",
        "description": "Allows reading documents"
      }'
    ```

=== "Go"
    ```go
    package main

    import (
        "context"
        "log"
        
        permissionsv1 "github.com/PrivateJAR/permio-go/proto/permissions/v1"
    )

    func createPermission(client permissionsv1.PermissionsServiceClient) {
        req := &permissionsv1.CreatePermissionRequest{
            ProjectName: "production",
            Name:        "document.read",
            Description: "Allows reading documents",
        }
        
        resp, err := client.CreatePermission(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to create permission: %v", err)
        }
        
        log.Printf("Created permission: %s (ID: %s)", resp.Name, resp.Id)
    }
    ```

=== "Rust"
    ```rust
    use tonic::transport::Channel;
    use permio_proto::permissions::v1::{
        permissions_service_client::PermissionsServiceClient,
        CreatePermissionRequest,
    };

    async fn create_permission(client: &mut PermissionsServiceClient<Channel>) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(CreatePermissionRequest {
            project_name: "production".to_string(),
            name: "document.read".to_string(),
            description: "Allows reading documents".to_string(),
        });
        
        let response = client.create_permission(request).await?;
        println!("Created permission: {} (ID: {})", response.get_ref().name, response.get_ref().id);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    import grpc
    from proto.permissions.v1 import permissions_service_pb2
    from proto.permissions.v1 import permissions_service_pb2_grpc

    def create_permission():
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.CreatePermissionRequest(
            project_name="production",
            name="document.read",
            description="Allows reading documents"
        )
        
        response = client.CreatePermission(request)
        print(f"Created permission: {response.name} (ID: {response.id})")
    ```

=== "Java"
    ```java
    import io.grpc.ManagedChannel;
    import io.grpc.ManagedChannelBuilder;
    import permio.permissions.v1.PermissionsServiceGrpc;
    import permio.permissions.v1.Permissions.CreatePermissionRequest;
    import permio.permissions.v1.Permissions.CreatePermissionResponse;

    public void createPermission() {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        CreatePermissionRequest request = CreatePermissionRequest.newBuilder()
                .setProjectName("production")
                .setName("document.read")
                .setDescription("Allows reading documents")
                .build();
        
        CreatePermissionResponse response = client.createPermission(request);
        System.out.println("Created permission: " + response.getName() + " (ID: " + response.getId() + ")");
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    import * as grpc from '@grpc/grpc-js';
    import * as protoLoader from '@grpc/proto-loader';

    const packageDefinition = protoLoader.loadSync('permissions_service.proto');
    const permissionsService = grpc.loadPackageDefinition(packageDefinition).permissions.v1 as any;

    const client = new permissionsService.PermissionsService('api.perms.io:443', 
        grpc.credentials.createSsl());

    interface CreatePermissionRequest {
        project_name: string;
        name: string;
        description: string;
    }

    function createPermission(): void {
        const request: CreatePermissionRequest = {
            project_name: 'production',
            name: 'document.read',
            description: 'Allows reading documents'
        };
        
        client.CreatePermission(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Created permission: ${response.name} (ID: ${response.id})`);
        });
    }
    ```

### Get Permission

Retrieves details of a specific permission.

**Required Permission**: `permission.get` on `/organisation/{organisation_id}/permission/{id}`

=== "HTTP"
    ```bash
    curl -X GET "https://api.perms.io/permissions-service/v1/permissions/{id}?project_name=production" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func getPermission(client permissionsv1.PermissionsServiceClient, projectName, permissionId string) {
        req := &permissionsv1.GetPermissionRequest{
            ProjectName: projectName,
            Id:          permissionId,
        }
        
        resp, err := client.GetPermission(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get permission: %v", err)
        }
        
        log.Printf("Permission: %s - %s", resp.Name, resp.Description)
    }
    ```

=== "Rust"
    ```rust
    async fn get_permission(client: &mut PermissionsServiceClient<Channel>, project_name: &str, permission_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GetPermissionRequest {
            project_name: project_name.to_string(),
            id: permission_id.to_string(),
        });
        
        let response = client.get_permission(request).await?;
        let permission = response.get_ref();
        println!("Permission: {} - {}", permission.name, permission.description);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def get_permission(project_name: str, permission_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.GetPermissionRequest(
            project_name=project_name,
            id=permission_id
        )
        
        response = client.GetPermission(request)
        print(f"Permission: {response.name} - {response.description}")
    ```

=== "Java"
    ```java
    public void getPermission(String projectName, String permissionId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        GetPermissionRequest request = GetPermissionRequest.newBuilder()
                .setProjectName(projectName)
                .setId(permissionId)
                .build();
        
        GetPermissionResponse response = client.getPermission(request);
        System.out.println("Permission: " + response.getName() + " - " + response.getDescription());
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GetPermissionRequest {
        project_name: string;
        id: string;
    }

    function getPermission(projectName: string, permissionId: string): void {
        const request: GetPermissionRequest = {
            project_name: projectName,
            id: permissionId
        };
        
        client.GetPermission(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Permission: ${response.name} - ${response.description}`);
        });
    }
    ```

### Update Permission

Updates an existing permission.

**Required Permission**: `permission.update` on `/organisation/{organisation_id}/permission/{id}`

=== "HTTP"
    ```bash
    curl -X PUT "https://api.perms.io/permissions-service/v1/permissions/{id}" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "document.read",
        "description": "Updated description for reading documents"
      }'
    ```

=== "Go"
    ```go
    func updatePermission(client permissionsv1.PermissionsServiceClient, projectName, permissionId string) {
        req := &permissionsv1.UpdatePermissionRequest{
            ProjectName: projectName,
            Id:          permissionId,
            Name:        "document.read",
            Description: "Updated description for reading documents",
        }
        
        resp, err := client.UpdatePermission(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to update permission: %v", err)
        }
        
        log.Printf("Updated permission: %s", resp.Name)
    }
    ```

=== "Rust"
    ```rust
    async fn update_permission(client: &mut PermissionsServiceClient<Channel>, project_name: &str, permission_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(UpdatePermissionRequest {
            project_name: project_name.to_string(),
            id: permission_id.to_string(),
            name: "document.read".to_string(),
            description: "Updated description for reading documents".to_string(),
        });
        
        let response = client.update_permission(request).await?;
        println!("Updated permission: {}", response.get_ref().name);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def update_permission(project_name: str, permission_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.UpdatePermissionRequest(
            project_name=project_name,
            id=permission_id,
            name="document.read",
            description="Updated description for reading documents"
        )
        
        response = client.UpdatePermission(request)
        print(f"Updated permission: {response.name}")
    ```

=== "Java"
    ```java
    public void updatePermission(String projectName, String permissionId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        UpdatePermissionRequest request = UpdatePermissionRequest.newBuilder()
                .setProjectName(projectName)
                .setId(permissionId)
                .setName("document.read")
                .setDescription("Updated description for reading documents")
                .build();
        
        UpdatePermissionResponse response = client.updatePermission(request);
        System.out.println("Updated permission: " + response.getName());
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface UpdatePermissionRequest {
        project_name: string;
        id: string;
        name: string;
        description: string;
    }

    function updatePermission(projectName: string, permissionId: string): void {
        const request: UpdatePermissionRequest = {
            project_name: projectName,
            id: permissionId,
            name: 'document.read',
            description: 'Updated description for reading documents'
        };
        
        client.UpdatePermission(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Updated permission: ${response.name}`);
        });
    }
    ```

### Delete Permission

Deletes a permission. This operation is idempotent.

**Required Permission**: `permission.delete` on `/organisation/{organisation_id}/permission/{id}`

=== "HTTP"
    ```bash
    curl -X DELETE "https://api.perms.io/permissions-service/v1/permissions/{id}?project_name=production" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func deletePermission(client permissionsv1.PermissionsServiceClient, projectName, permissionId string) {
        req := &permissionsv1.DeletePermissionRequest{
            ProjectName: projectName,
            Id:          permissionId,
        }
        
        _, err := client.DeletePermission(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to delete permission: %v", err)
        }
        
        log.Printf("Deleted permission: %s", permissionId)
    }
    ```

=== "Rust"
    ```rust
    async fn delete_permission(client: &mut PermissionsServiceClient<Channel>, project_name: &str, permission_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(DeletePermissionRequest {
            project_name: project_name.to_string(),
            id: permission_id.to_string(),
        });
        
        client.delete_permission(request).await?;
        println!("Deleted permission: {}", permission_id);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def delete_permission(project_name: str, permission_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.DeletePermissionRequest(
            project_name=project_name,
            id=permission_id
        )
        
        client.DeletePermission(request)
        print(f"Deleted permission: {permission_id}")
    ```

=== "Java"
    ```java
    public void deletePermission(String projectName, String permissionId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        DeletePermissionRequest request = DeletePermissionRequest.newBuilder()
                .setProjectName(projectName)
                .setId(permissionId)
                .build();
        
        client.deletePermission(request);
        System.out.println("Deleted permission: " + permissionId);
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface DeletePermissionRequest {
        project_name: string;
        id: string;
    }

    function deletePermission(projectName: string, permissionId: string): void {
        const request: DeletePermissionRequest = {
            project_name: projectName,
            id: permissionId
        };
        
        client.DeletePermission(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Deleted permission: ${permissionId}`);
        });
    }
    ```

### List Permissions

Lists all permissions within a project with optional search and pagination.

**Required Permission**: `permission.list` on `/organisation/{organisation_id}`

=== "HTTP"
    ```bash
    curl -X GET "https://api.perms.io/permissions-service/v1/permissions?project_name=production&limit=10&cursor=abc123&search=document" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func listPermissions(client permissionsv1.PermissionsServiceClient, projectName string) {
        req := &permissionsv1.ListPermissionsRequest{
            ProjectName: projectName,
            Pagination: &paginationv1.PaginationRequest{
                Limit: proto.Int32(10),
            },
            Search: proto.String("document"),
        }
        
        resp, err := client.ListPermissions(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to list permissions: %v", err)
        }
        
        for _, permission := range resp.Permissions {
            log.Printf("Permission: %s - %s", permission.Name, permission.Description)
        }
    }
    ```

=== "Rust"
    ```rust
    async fn list_permissions(client: &mut PermissionsServiceClient<Channel>, project_name: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(ListPermissionsRequest {
            project_name: project_name.to_string(),
            pagination: Some(PaginationRequest {
                limit: Some(10),
                cursor: None,
            }),
            search: Some("document".to_string()),
        });
        
        let response = client.list_permissions(request).await?;
        
        for permission in response.get_ref().permissions.iter() {
            println!("Permission: {} - {}", permission.name, permission.description);
        }
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def list_permissions(project_name: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.ListPermissionsRequest(
            project_name=project_name,
            pagination=pagination_pb2.PaginationRequest(limit=10),
            search="document"
        )
        
        response = client.ListPermissions(request)
        
        for permission in response.permissions:
            print(f"Permission: {permission.name} - {permission.description}")
    ```

=== "Java"
    ```java
    public void listPermissions(String projectName) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        ListPermissionsRequest request = ListPermissionsRequest.newBuilder()
                .setProjectName(projectName)
                .setPagination(PaginationRequest.newBuilder().setLimit(10).build())
                .setSearch("document")
                .build();
        
        ListPermissionsResponse response = client.listPermissions(request);
        
        for (Permission permission : response.getPermissionsList()) {
            System.out.println("Permission: " + permission.getName() + " - " + permission.getDescription());
        }
        
        channel.shutdown();
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

    function listPermissions(projectName: string): void {
        const request: ListPermissionsRequest = {
            project_name: projectName,
            pagination: {
                limit: 10
            },
            search: "document"
        };
        
        client.ListPermissions(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            response.permissions.forEach((permission: any) => {
                console.log(`Permission: ${permission.name} - ${permission.description}`);
            });
        });
    }
    ```

## Role Management

### Create Role

Creates a new role with a collection of permissions.

**Required Permissions**: 
- `role.create` on `/organisation/{organisation_id}`
- `permission.get` on `/organisation/{organisation_id}/permission/{permission_id}` for each permission

=== "HTTP"
    ```bash
    curl -X POST "https://api.perms.io/permissions-service/v1/roles" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "document_editor",
        "description": "Can read and write documents",
        "permissions": ["perm_123", "perm_456"]
      }'
    ```

=== "Go"
    ```go
    func createRole(client permissionsv1.PermissionsServiceClient, projectName string, permissionIds []string) {
        req := &permissionsv1.CreateRoleRequest{
            ProjectName: projectName,
            Name:        "document_editor",
            Description: "Can read and write documents",
            Permissions: permissionIds,
        }
        
        resp, err := client.CreateRole(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to create role: %v", err)
        }
        
        log.Printf("Created role: %s (ID: %s)", resp.Name, resp.Id)
    }
    ```

=== "Rust"
    ```rust
    async fn create_role(client: &mut PermissionsServiceClient<Channel>, permission_ids: Vec<String>) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(CreateRoleRequest {
            project_name: "production".to_string(),
            name: "document_editor".to_string(),
            description: "Can read and write documents".to_string(),
            permissions: permission_ids,
        });
        
        let response = client.create_role(request).await?;
        println!("Created role: {} (ID: {})", response.get_ref().name, response.get_ref().id);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def create_role(permission_ids: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.CreateRoleRequest(
            project_name="production",
            name="document_editor",
            description="Can read and write documents",
            permissions=permission_ids
        )
        
        response = client.CreateRole(request)
        print(f"Created role: {response.name} (ID: {response.id})")
    ```

=== "Java"
    ```java
    public void createRole(List<String> permissionIds) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        CreateRoleRequest request = CreateRoleRequest.newBuilder()
                .setProjectName("production")
                .setName("document_editor")
                .setDescription("Can read and write documents")
                .addAllPermissions(permissionIds)
                .build();
        
        CreateRoleResponse response = client.createRole(request);
        System.out.println("Created role: " + response.getName() + " (ID: " + response.getId() + ")");
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface CreateRoleRequest {
        project_name: string;
        name: string;
        description: string;
        permissions: string[];
    }

    function createRole(permissionIds: string[]): void {
        const request: CreateRoleRequest = {
            project_name: 'production',
            name: 'document_editor',
            description: 'Can read and write documents',
            permissions: permissionIds
        };
        
        client.CreateRole(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Created role: ${response.name} (ID: ${response.id})`);
        });
    }
    ```

### Get Role

Retrieves details of a specific role, including all associated permissions.

**Required Permission**: `role.get` on `/organisation/{organisation_id}/role/{id}`

=== "HTTP"
    ```bash
    curl -X GET "https://api.perms.io/permissions-service/v1/roles/{id}?project_name=production" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func getRole(client permissionsv1.PermissionsServiceClient, projectName, roleId string) {
        req := &permissionsv1.GetRoleRequest{
            ProjectName: projectName,
            Id:          roleId,
        }
        
        resp, err := client.GetRole(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get role: %v", err)
        }
        
        log.Printf("Role: %s - %s (Permissions: %d)", resp.Name, resp.Description, len(resp.Permissions))
    }
    ```

=== "Rust"
    ```rust
    async fn get_role(client: &mut PermissionsServiceClient<Channel>, project_name: &str, role_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GetRoleRequest {
            project_name: project_name.to_string(),
            id: role_id.to_string(),
        });
        
        let response = client.get_role(request).await?;
        let role = response.get_ref();
        println!("Role: {} - {} (Permissions: {})", role.name, role.description, role.permissions.len());
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def get_role(project_name: str, role_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.GetRoleRequest(
            project_name=project_name,
            id=role_id
        )
        
        response = client.GetRole(request)
        print(f"Role: {response.name} - {response.description} (Permissions: {len(response.permissions)})")
    ```

=== "Java"
    ```java
    public void getRole(String projectName, String roleId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        GetRoleRequest request = GetRoleRequest.newBuilder()
                .setProjectName(projectName)
                .setId(roleId)
                .build();
        
        GetRoleResponse response = client.getRole(request);
        System.out.println("Role: " + response.getName() + " - " + response.getDescription() + 
                " (Permissions: " + response.getPermissionsList().size() + ")");
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GetRoleRequest {
        project_name: string;
        id: string;
    }

    function getRole(projectName: string, roleId: string): void {
        const request: GetRoleRequest = {
            project_name: projectName,
            id: roleId
        };
        
        client.GetRole(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Role: ${response.name} - ${response.description} (Permissions: ${response.permissions.length})`);
        });
    }
    ```

### Update Role

Updates an existing role's permissions and metadata.

**Required Permission**: `role.update` on `/organisation/{organisation_id}/role/{id}`

=== "HTTP"
    ```bash
    curl -X PUT "https://api.perms.io/permissions-service/v1/roles/{id}" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "document_editor",
        "description": "Updated description",
        "permissions": ["perm_123", "perm_456", "perm_789"]
      }'
    ```

=== "Go"
    ```go
    func updateRole(client permissionsv1.PermissionsServiceClient, projectName, roleId string, permissionIds []string) {
        req := &permissionsv1.UpdateRoleRequest{
            ProjectName: projectName,
            Id:          roleId,
            Name:        "document_editor",
            Description: "Updated description",
            Permissions: permissionIds,
        }
        
        resp, err := client.UpdateRole(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to update role: %v", err)
        }
        
        log.Printf("Updated role: %s", resp.Name)
    }
    ```

=== "Rust"
    ```rust
    async fn update_role(client: &mut PermissionsServiceClient<Channel>, project_name: &str, role_id: &str, permission_ids: Vec<String>) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(UpdateRoleRequest {
            project_name: project_name.to_string(),
            id: role_id.to_string(),
            name: "document_editor".to_string(),
            description: "Updated description".to_string(),
            permissions: permission_ids,
        });
        
        let response = client.update_role(request).await?;
        println!("Updated role: {}", response.get_ref().name);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def update_role(project_name: str, role_id: str, permission_ids: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.UpdateRoleRequest(
            project_name=project_name,
            id=role_id,
            name="document_editor",
            description="Updated description",
            permissions=permission_ids
        )
        
        response = client.UpdateRole(request)
        print(f"Updated role: {response.name}")
    ```

=== "Java"
    ```java
    public void updateRole(String projectName, String roleId, List<String> permissionIds) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        UpdateRoleRequest request = UpdateRoleRequest.newBuilder()
                .setProjectName(projectName)
                .setId(roleId)
                .setName("document_editor")
                .setDescription("Updated description")
                .addAllPermissions(permissionIds)
                .build();
        
        UpdateRoleResponse response = client.updateRole(request);
        System.out.println("Updated role: " + response.getName());
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface UpdateRoleRequest {
        project_name: string;
        id: string;
        name: string;
        description: string;
        permissions: string[];
    }

    function updateRole(projectName: string, roleId: string, permissionIds: string[]): void {
        const request: UpdateRoleRequest = {
            project_name: projectName,
            id: roleId,
            name: 'document_editor',
            description: 'Updated description',
            permissions: permissionIds
        };
        
        client.UpdateRole(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Updated role: ${response.name}`);
        });
    }
    ```

### Delete Role

Deletes a role. This operation is idempotent.

**Required Permission**: `role.delete` on `/organisation/{organisation_id}/role/{id}`

=== "HTTP"
    ```bash
    curl -X DELETE "https://api.perms.io/permissions-service/v1/roles/{id}?project_name=production" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func deleteRole(client permissionsv1.PermissionsServiceClient, projectName, roleId string) {
        req := &permissionsv1.DeleteRoleRequest{
            ProjectName: projectName,
            Id:          roleId,
        }
        
        _, err := client.DeleteRole(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to delete role: %v", err)
        }
        
        log.Printf("Deleted role: %s", roleId)
    }
    ```

=== "Rust"
    ```rust
    async fn delete_role(client: &mut PermissionsServiceClient<Channel>, project_name: &str, role_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(DeleteRoleRequest {
            project_name: project_name.to_string(),
            id: role_id.to_string(),
        });
        
        client.delete_role(request).await?;
        println!("Deleted role: {}", role_id);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def delete_role(project_name: str, role_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.DeleteRoleRequest(
            project_name=project_name,
            id=role_id
        )
        
        client.DeleteRole(request)
        print(f"Deleted role: {role_id}")
    ```

=== "Java"
    ```java
    public void deleteRole(String projectName, String roleId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        DeleteRoleRequest request = DeleteRoleRequest.newBuilder()
                .setProjectName(projectName)
                .setId(roleId)
                .build();
        
        client.deleteRole(request);
        System.out.println("Deleted role: " + roleId);
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface DeleteRoleRequest {
        project_name: string;
        id: string;
    }

    function deleteRole(projectName: string, roleId: string): void {
        const request: DeleteRoleRequest = {
            project_name: projectName,
            id: roleId
        };
        
        client.DeleteRole(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Deleted role: ${roleId}`);
        });
    }
    ```

### List Roles

Lists all roles within a project with optional search and pagination.

**Required Permission**: `role.list` on `/organisation/{organisation_id}`

=== "HTTP"
    ```bash
    curl -X GET "https://api.perms.io/permissions-service/v1/roles?project_name=production&limit=10&search=editor" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func listRoles(client permissionsv1.PermissionsServiceClient, projectName string) {
        req := &permissionsv1.ListRolesRequest{
            ProjectName: projectName,
            Pagination: &paginationv1.PaginationRequest{
                Limit: proto.Int32(10),
            },
            Search: proto.String("editor"),
        }
        
        resp, err := client.ListRoles(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to list roles: %v", err)
        }
        
        for _, role := range resp.Roles {
            log.Printf("Role: %s - %s (Permissions: %d)", role.Name, role.Description, len(role.Permissions))
        }
    }
    ```

=== "Rust"
    ```rust
    async fn list_roles(client: &mut PermissionsServiceClient<Channel>, project_name: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(ListRolesRequest {
            project_name: project_name.to_string(),
            pagination: Some(PaginationRequest {
                limit: Some(10),
                cursor: None,
            }),
            search: Some("editor".to_string()),
        });
        
        let response = client.list_roles(request).await?;
        
        for role in response.get_ref().roles.iter() {
            println!("Role: {} - {} (Permissions: {})", role.name, role.description, role.permissions.len());
        }
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def list_roles(project_name: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.ListRolesRequest(
            project_name=project_name,
            pagination=pagination_pb2.PaginationRequest(limit=10),
            search="editor"
        )
        
        response = client.ListRoles(request)
        
        for role in response.roles:
            print(f"Role: {role.name} - {role.description} (Permissions: {len(role.permissions)})")
    ```

=== "Java"
    ```java
    public void listRoles(String projectName) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        ListRolesRequest request = ListRolesRequest.newBuilder()
                .setProjectName(projectName)
                .setPagination(PaginationRequest.newBuilder().setLimit(10).build())
                .setSearch("editor")
                .build();
        
        ListRolesResponse response = client.listRoles(request);
        
        for (Role role : response.getRolesList()) {
            System.out.println("Role: " + role.getName() + " - " + role.getDescription() + 
                    " (Permissions: " + role.getPermissionsList().size() + ")");
        }
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface ListRolesRequest {
        project_name: string;
        pagination?: {
            limit?: number;
            cursor?: string;
        };
        search?: string;
    }

    function listRoles(projectName: string): void {
        const request: ListRolesRequest = {
            project_name: projectName,
            pagination: {
                limit: 10
            },
            search: "editor"
        };
        
        client.ListRoles(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            response.roles.forEach((role: any) => {
                console.log(`Role: ${role.name} - ${role.description} (Permissions: ${role.permissions.length})`);
            });
        });
    }
    ```

## Access Control

### Grant Permissions and Roles

Grants permissions and roles to a principal on a specific resource. This operation is additive - it won't remove existing permissions.

**Required Permissions**:
- `permission.get` on `/organisation/{organisation_id}/permission/{permission_id}` for each permission
- `role.get` on `/organisation/{organisation_id}/role/{role_id}` for each role  
- `principal.assignment.create` on `/organisation/{organisation_id}/principal/{user_id}`

=== "HTTP"
    ```bash
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/assign" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "user_id": "usr_123",
        "resource_uri": "/project/456/documents/789",
        "permissions": ["perm_123"],
        "roles": ["role_456"]
      }'
    ```

=== "Go"
    ```go
    func grantPermissions(client permissionsv1.PermissionsServiceClient, userId, resourceUri string, permissions, roles []string) {
        req := &permissionsv1.GrantUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      userId,
            ResourceUri: resourceUri,
            Permissions: permissions,
            Roles:       roles,
        }
        
        _, err := client.GrantUserPermissionsAndRolesOnResource(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to grant permissions: %v", err)
        }
        
        log.Printf("Granted permissions to user %s on resource %s", userId, resourceUri)
    }
    ```

=== "Rust"
    ```rust
    async fn grant_permissions(client: &mut PermissionsServiceClient<Channel>, user_id: &str, resource_uri: &str, permissions: Vec<String>, roles: Vec<String>) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GrantUserPermissionsAndRolesOnResourceRequest {
            project_name: "production".to_string(),
            user_id: user_id.to_string(),
            resource_uri: resource_uri.to_string(),
            permissions,
            roles,
        });
        
        client.grant_user_permissions_and_roles_on_resource(request).await?;
        println!("Granted permissions to user {} on resource {}", user_id, resource_uri);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def grant_permissions(user_id: str, resource_uri: str, permissions: list[str], roles: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.GrantUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id=user_id,
            resource_uri=resource_uri,
            permissions=permissions,
            roles=roles
        )
        
        client.GrantUserPermissionsAndRolesOnResource(request)
        print(f"Granted permissions to user {user_id} on resource {resource_uri}")
    ```

=== "Java"
    ```java
    public void grantPermissions(String userId, String resourceUri, List<String> permissions, List<String> roles) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        GrantUserPermissionsAndRolesOnResourceRequest request = 
                GrantUserPermissionsAndRolesOnResourceRequest.newBuilder()
                        .setProjectName("production")
                        .setUserId(userId)
                        .setResourceUri(resourceUri)
                        .addAllPermissions(permissions)
                        .addAllRoles(roles)
                        .build();
        
        client.grantUserPermissionsAndRolesOnResource(request);
        System.out.println("Granted permissions to user " + userId + " on resource " + resourceUri);
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GrantUserPermissionsAndRolesOnResourceRequest {
        project_name: string;
        user_id: string;
        resource_uri: string;
        permissions: string[];
        roles: string[];
    }

    function grantPermissions(userId: string, resourceUri: string, permissions: string[], roles: string[]): void {
        const request: GrantUserPermissionsAndRolesOnResourceRequest = {
            project_name: 'production',
            user_id: userId,
            resource_uri: resourceUri,
            permissions,
            roles
        };
        
        client.GrantUserPermissionsAndRolesOnResource(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Granted permissions to user ${userId} on resource ${resourceUri}`);
        });
    }
    ```

### Revoke Permissions and Roles

Revokes specific permissions and roles from a principal on a resource.

**Required Permission**: `principal.assignment.delete` on the resource URI

=== "HTTP"
    ```bash
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/revoke" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "user_id": "usr_123",
        "resource_uri": "/project/456/documents/789",
        "permissions": ["perm_123"],
        "roles": ["role_456"]
      }'
    ```

=== "Go"
    ```go
    func revokePermissions(client permissionsv1.PermissionsServiceClient, userId, resourceUri string, permissions, roles []string) {
        req := &permissionsv1.RevokeUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      userId,
            ResourceUri: resourceUri,
            Permissions: permissions,
            Roles:       roles,
        }
        
        _, err := client.RevokeUserPermissionsAndRolesOnResource(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to revoke permissions: %v", err)
        }
        
        log.Printf("Revoked permissions from user %s on resource %s", userId, resourceUri)
    }
    ```

=== "Rust"
    ```rust
    async fn revoke_permissions(client: &mut PermissionsServiceClient<Channel>, user_id: &str, resource_uri: &str, permissions: Vec<String>, roles: Vec<String>) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(RevokeUserPermissionsAndRolesOnResourceRequest {
            project_name: "production".to_string(),
            user_id: user_id.to_string(),
            resource_uri: resource_uri.to_string(),
            permissions,
            roles,
        });
        
        client.revoke_user_permissions_and_roles_on_resource(request).await?;
        println!("Revoked permissions from user {} on resource {}", user_id, resource_uri);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def revoke_permissions(user_id: str, resource_uri: str, permissions: list[str], roles: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.RevokeUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id=user_id,
            resource_uri=resource_uri,
            permissions=permissions,
            roles=roles
        )
        
        client.RevokeUserPermissionsAndRolesOnResource(request)
        print(f"Revoked permissions from user {user_id} on resource {resource_uri}")
    ```

=== "Java"
    ```java
    public void revokePermissions(String userId, String resourceUri, List<String> permissions, List<String> roles) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        RevokeUserPermissionsAndRolesOnResourceRequest request = 
                RevokeUserPermissionsAndRolesOnResourceRequest.newBuilder()
                        .setProjectName("production")
                        .setUserId(userId)
                        .setResourceUri(resourceUri)
                        .addAllPermissions(permissions)
                        .addAllRoles(roles)
                        .build();
        
        client.revokeUserPermissionsAndRolesOnResource(request);
        System.out.println("Revoked permissions from user " + userId + " on resource " + resourceUri);
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface RevokeUserPermissionsAndRolesOnResourceRequest {
        project_name: string;
        user_id: string;
        resource_uri: string;
        permissions: string[];
        roles: string[];
    }

    function revokePermissions(userId: string, resourceUri: string, permissions: string[], roles: string[]): void {
        const request: RevokeUserPermissionsAndRolesOnResourceRequest = {
            project_name: 'production',
            user_id: userId,
            resource_uri: resourceUri,
            permissions,
            roles
        };
        
        client.RevokeUserPermissionsAndRolesOnResource(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Revoked permissions from user ${userId} on resource ${resourceUri}`);
        });
    }
    ```

### Get Principal's Permissions

Retrieves all permissions and roles assigned to a principal on a specific resource.

**Required Permission**: `principal.assignment.get` on the resource URI

=== "HTTP"
    ```bash
    curl -X GET "https://api.perms.io/permissions-service/v1/permissions/user/{user_id}/resource/{resource_uri}?project_name=production" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func getUserPermissions(client permissionsv1.PermissionsServiceClient, userId, resourceUri string) {
        req := &permissionsv1.GetUserPermissionsAndRolesOnResourceRequest{
            ProjectName: "production",
            UserId:      userId,
            ResourceUri: resourceUri,
        }
        
        resp, err := client.GetUserPermissionsAndRolesOnResource(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get user permissions: %v", err)
        }
        
        log.Printf("User has %d permissions and %d roles on resource %s", 
            len(resp.Permissions), len(resp.Roles), resourceUri)
    }
    ```

=== "Rust"
    ```rust
    async fn get_user_permissions(client: &mut PermissionsServiceClient<Channel>, user_id: &str, resource_uri: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GetUserPermissionsAndRolesOnResourceRequest {
            project_name: "production".to_string(),
            user_id: user_id.to_string(),
            resource_uri: resource_uri.to_string(),
        });
        
        let response = client.get_user_permissions_and_roles_on_resource(request).await?;
        let result = response.get_ref();
        println!("User has {} permissions and {} roles on resource {}", 
            result.permissions.len(), result.roles.len(), resource_uri);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def get_user_permissions(user_id: str, resource_uri: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.GetUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id=user_id,
            resource_uri=resource_uri
        )
        
        response = client.GetUserPermissionsAndRolesOnResource(request)
        print(f"User has {len(response.permissions)} permissions and {len(response.roles)} roles on resource {resource_uri}")
    ```

=== "Java"
    ```java
    public void getUserPermissions(String userId, String resourceUri) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        GetUserPermissionsAndRolesOnResourceRequest request = 
                GetUserPermissionsAndRolesOnResourceRequest.newBuilder()
                        .setProjectName("production")
                        .setUserId(userId)
                        .setResourceUri(resourceUri)
                        .build();
        
        GetUserPermissionsAndRolesOnResourceResponse response = 
                client.getUserPermissionsAndRolesOnResource(request);
        System.out.println("User has " + response.getPermissionsList().size() + 
                " permissions and " + response.getRolesList().size() + 
                " roles on resource " + resourceUri);
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GetUserPermissionsAndRolesOnResourceRequest {
        project_name: string;
        user_id: string;
        resource_uri: string;
    }

    function getUserPermissions(userId: string, resourceUri: string): void {
        const request: GetUserPermissionsAndRolesOnResourceRequest = {
            project_name: 'production',
            user_id: userId,
            resource_uri: resourceUri
        };
        
        client.GetUserPermissionsAndRolesOnResource(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`User has ${response.permissions.length} permissions and ${response.roles.length} roles on resource ${resourceUri}`);
        });
    }
    ```

## User Management

### List Users

Lists all users within a project.

**Required Permission**: `principal.list` on `/organisation/{organisation_id}`

=== "HTTP"
    ```bash
    curl -X GET "https://api.perms.io/permissions-service/v1/permissions/principals?project_name=production&limit=10&search=user" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func listPrincipals(client permissionsv1.PermissionsServiceClient, projectName string) {
        req := &permissionsv1.ListPrincipalsRequest{
            ProjectName: projectName,
            Pagination: &paginationv1.PaginationRequest{
                Limit: proto.Int32(10),
            },
        }
        
        resp, err := client.ListPrincipals(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to list principals: %v", err)
        }
        
        for _, principal := range resp.Principals {
            log.Printf("Principal: %s", principal)
        }
    }
    ```

=== "Rust"
    ```rust
    async fn list_principals(client: &mut PermissionsServiceClient<Channel>, project_name: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(ListPrincipalsRequest {
            project_name: project_name.to_string(),
            pagination: Some(PaginationRequest {
                limit: Some(10),
                cursor: None,
            }),
        });
        
        let response = client.list_principals(request).await?;
        
        for principal in response.get_ref().principals.iter() {
            println!("Principal: {}", principal);
        }
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def list_principals(project_name: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.ListPrincipalsRequest(
            project_name=project_name,
            pagination=pagination_pb2.PaginationRequest(limit=10)
        )
        
        response = client.ListPrincipals(request)
        
        for principal in response.principals:
            print(f"Principal: {principal}")
    ```

=== "Java"
    ```java
    public void listPrincipals(String projectName) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        ListPrincipalsRequest request = ListPrincipalsRequest.newBuilder()
                .setProjectName(projectName)
                .setPagination(PaginationRequest.newBuilder().setLimit(10).build())
                .build();
        
        ListPrincipalsResponse response = client.listPrincipals(request);
        
        for (String principal : response.getPrincipalsList()) {
            System.out.println("Principal: " + principal);
        }
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface ListPrincipalsRequest {
        project_name: string;
        pagination?: {
            limit?: number;
            cursor?: string;
        };
    }

    function listPrincipals(projectName: string): void {
        const request: ListPrincipalsRequest = {
            project_name: projectName,
            pagination: {
                limit: 10
            }
        };
        
        client.ListPrincipals(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            response.principals.forEach((principal: string) => {
                console.log(`Principal: ${principal}`);
            });
        });
    }
    ```

### Get User Permissions

Retrieves all permission assignments for a specific user within an organization.

**Required Permission**: `principal.assignment.list` on `/organisation/{organisation_id}/principal/{principal_id}`

=== "HTTP"
    ```bash
    curl -X GET "https://api.perms.io/permissions-service/v1/permissions/assignments/principal/{principal_id}?project_name=production" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```

=== "Go"
    ```go
    func getAllAssignments(client permissionsv1.PermissionsServiceClient, projectName, principalId string) {
        req := &permissionsv1.GetAllAssignmentsForPrincipalRequest{
            ProjectName: projectName,
            PrincipalId: principalId,
        }
        
        resp, err := client.GetAllAssignmentsForPrincipal(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to get assignments: %v", err)
        }
        
        for _, assignment := range resp.Assignments {
            log.Printf("Resource: %s, Permissions: %d, Roles: %d", 
                assignment.ResourceUri, len(assignment.Permissions), len(assignment.Roles))
        }
    }
    ```

=== "Rust"
    ```rust
    async fn get_all_assignments(client: &mut PermissionsServiceClient<Channel>, project_name: &str, principal_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(GetAllAssignmentsForPrincipalRequest {
            project_name: project_name.to_string(),
            principal_id: principal_id.to_string(),
        });
        
        let response = client.get_all_assignments_for_principal(request).await?;
        
        for assignment in response.get_ref().assignments.iter() {
            println!("Resource: {}, Permissions: {}, Roles: {}", 
                assignment.resource_uri, assignment.permissions.len(), assignment.roles.len());
        }
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def get_all_assignments(project_name: str, principal_id: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.GetAllAssignmentsForPrincipalRequest(
            project_name=project_name,
            principal_id=principal_id
        )
        
        response = client.GetAllAssignmentsForPrincipal(request)
        
        for assignment in response.assignments:
            print(f"Resource: {assignment.resource_uri}, Permissions: {len(assignment.permissions)}, Roles: {len(assignment.roles)}")
    ```

=== "Java"
    ```java
    public void getAllAssignments(String projectName, String principalId) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        GetAllAssignmentsForPrincipalRequest request = 
                GetAllAssignmentsForPrincipalRequest.newBuilder()
                        .setProjectName(projectName)
                        .setPrincipalId(principalId)
                        .build();
        
        GetAllAssignmentsForPrincipalResponse response = 
                client.getAllAssignmentsForPrincipal(request);
        
        for (Assignment assignment : response.getAssignmentsList()) {
            System.out.println("Resource: " + assignment.getResourceUri() + 
                    ", Permissions: " + assignment.getPermissionsList().size() + 
                    ", Roles: " + assignment.getRolesList().size());
        }
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface GetAllAssignmentsForPrincipalRequest {
        project_name: string;
        principal_id: string;
    }

    function getAllAssignments(projectName: string, principalId: string): void {
        const request: GetAllAssignmentsForPrincipalRequest = {
            project_name: projectName,
            principal_id: principalId
        };
        
        client.GetAllAssignmentsForPrincipal(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            response.assignments.forEach((assignment: any) => {
                console.log(`Resource: ${assignment.resource_uri}, Permissions: ${assignment.permissions.length}, Roles: ${assignment.roles.length}`);
            });
        });
    }
    ```

## Permission Checking

### Check Permissions

The core permission checking endpoint that determines if a principal has specific permissions on resources.

=== "HTTP"
    ```bash
    curl -X POST "https://api.perms.io/permissions-service/v1/permissions/check" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "principal_id": "usr_123",
        "resource_uris": ["/project/456/documents/789", "/project/456/documents/101"],
        "permissions": ["read", "write"]
      }'
    ```

=== "Go"
    ```go
    func checkPermissions(client permissionsv1.PermissionsServiceClient, principalId string, resourceUris, permissions []string) {
        req := &permissionsv1.CheckPermissionRequest{
            ProjectName:  "production",
            PrincipalId:  principalId,
            ResourceUris: resourceUris,
            Permissions:  permissions,
        }
        
        resp, err := client.Check(context.Background(), req)
        if err != nil {
            log.Fatalf("Failed to check permissions: %v", err)
        }
        
        if resp.Passed {
            log.Printf("Permission check passed for principal %s", principalId)
        } else {
            log.Printf("Permission check failed:")
            for _, missing := range resp.MissingPermissions {
                log.Printf("  Resource %s missing: %v", missing.ResourceUri, missing.MissingPermissions)
            }
        }
    }
    ```

=== "Rust"
    ```rust
    async fn check_permissions(client: &mut PermissionsServiceClient<Channel>, principal_id: &str, resource_uris: Vec<String>, permissions: Vec<String>) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(CheckPermissionRequest {
            project_name: "production".to_string(),
            principal_id: principal_id.to_string(),
            resource_uris,
            permissions,
        });
        
        let response = client.check(request).await?;
        let result = response.get_ref();
        
        if result.passed {
            println!("Permission check passed for principal {}", principal_id);
        } else {
            println!("Permission check failed:");
            for missing in result.missing_permissions.iter() {
                println!("  Resource {} missing: {:?}", missing.resource_uri, missing.missing_permissions);
            }
        }
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def check_permissions(principal_id: str, resource_uris: list[str], permissions: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        request = permissions_service_pb2.CheckPermissionRequest(
            project_name="production",
            principal_id=principal_id,
            resource_uris=resource_uris,
            permissions=permissions
        )
        
        response = client.Check(request)
        
        if response.passed:
            print(f"Permission check passed for principal {principal_id}")
        else:
            print("Permission check failed:")
            for missing in response.missing_permissions:
                print(f"  Resource {missing.resource_uri} missing: {missing.missing_permissions}")
    ```

=== "Java"
    ```java
    public void checkPermissions(String principalId, List<String> resourceUris, List<String> permissions) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        PermissionsServiceGrpc.PermissionsServiceBlockingStub client = 
                PermissionsServiceGrpc.newBlockingStub(channel);
        
        CheckPermissionRequest request = CheckPermissionRequest.newBuilder()
                .setProjectName("production")
                .setPrincipalId(principalId)
                .addAllResourceUris(resourceUris)
                .addAllPermissions(permissions)
                .build();
        
        CheckPermissionResponse response = client.check(request);
        
        if (response.getPassed()) {
            System.out.println("Permission check passed for principal " + principalId);
        } else {
            System.out.println("Permission check failed:");
            for (MissingPermission missing : response.getMissingPermissionsList()) {
                System.out.println("  Resource " + missing.getResourceUri() + 
                        " missing: " + missing.getMissingPermissionsList());
            }
        }
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface CheckPermissionRequest {
        project_name: string;
        principal_id: string;
        resource_uris: string[];
        permissions: string[];
    }

    function checkPermissions(principalId: string, resourceUris: string[], permissions: string[]): void {
        const request: CheckPermissionRequest = {
            project_name: 'production',
            principal_id: principalId,
            resource_uris: resourceUris,
            permissions: permissions
        };
        
        client.Check(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            
            if (response.passed) {
                console.log(`Permission check passed for principal ${principalId}`);
            } else {
                console.log('Permission check failed:');
                response.missing_permissions.forEach((missing: any) => {
                    console.log(`  Resource ${missing.resource_uri} missing: ${missing.missing_permissions}`);
                });
            }
        });
    }
    ```

## Resource URI Patterns

Resource URIs follow a hierarchical pattern that enables inheritance:

### URI Structure

```
/organisation/{org_id}/project/{project_name}/resource/{resource_id}
```

### Examples

- `/project/456` - Top-level project resource
- `/project/456/documents` - All documents in project 456
- `/project/456/documents/789` - Specific document 789
- `/user/123` - User resource
- `/user/123/profile` - User's profile

### Inheritance Rules

Permissions granted on parent resources automatically apply to child resources:

- Permission on `/project/456` applies to `/project/456/documents/789`
- Permission on `/user/123` applies to `/user/123/profile`

## Common RBAC Patterns

### Document Management System

```go
// Create permissions
permissions := []string{"document.read", "document.write", "document.delete"}

// Create roles
editorRole := createRole("document_editor", []string{"document.read", "document.write"})
viewerRole := createRole("document_viewer", []string{"document.read"})
adminRole := createRole("document_admin", []string{"document.read", "document.write", "document.delete"})

// Grant permissions
grantPermissions("user_123", "/project/456/documents", []string{}, []string{editorRole.Id})
grantPermissions("user_456", "/project/456/documents/789", []string{}, []string{viewerRole.Id})
```

### Multi-tenant Application

```go
// Organization-level permissions
grantPermissions("user_123", "/organization/789", []string{}, []string{"org_admin"})

// Project-level permissions  
grantPermissions("user_456", "/organization/789/project/456", []string{}, []string{"project_manager"})

// Resource-specific permissions
grantPermissions("user_789", "/organization/789/project/456/resource/123", []string{"read"}, []string{})
```

## Best Practices

### 1. Permission Naming

Use descriptive, hierarchical names:
- `document.read` instead of `read`
- `user.profile.update` instead of `update`
- `billing.invoice.create` instead of `create`

### 2. Resource URI Design

Design URIs to reflect your application's hierarchy:
- Use consistent patterns across resources
- Consider future scalability
- Group related resources under common parents

### 3. Role Management

- Create roles for common permission sets
- Use descriptive role names
- Regularly audit role permissions
- Consider role inheritance patterns

### 4. Performance Optimization

- Batch permission checks when possible
- Cache permission results where appropriate
- Use specific resource URIs rather than wildcards
- Consider permission inheritance in your URI design

### 5. Security Considerations

- Always validate resource URIs
- Use least privilege principle
- Regularly audit permission assignments
- Monitor for permission escalation

## Error Handling

### Common Error Codes

- `INVALID_ARGUMENT` (3): Invalid request parameters
- `NOT_FOUND` (5): Resource not found
- `PERMISSION_DENIED` (7): Insufficient permissions
- `ALREADY_EXISTS` (6): Resource already exists

### Example Error Response

```json
{
  "error": {
    "code": 7,
    "message": "Permission denied: missing required permission 'permission.create' on resource '/organisation/org_123'"
  }
}
```

## Rate Limits

- **Permission Checks**: 10,000 requests per minute
- **Management Operations**: 1,000 requests per minute
- **Bulk Operations**: 100 requests per minute

## Monitoring and Metrics

The service provides metrics for:
- Permission check latency
- Grant/revoke operation counts
- Principal assignment statistics
- Resource access patterns

These metrics are available through the organisation dashboard and usage APIs.