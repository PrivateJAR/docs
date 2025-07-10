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

=== "Rust"
    ```rust
    use tonic::{transport::Channel, metadata::MetadataValue, Request};
    use tonic::transport::ClientTlsConfig;
    
    pub mod organisation {
        tonic::include_proto!("organisation_service.v1");
    }
    
    use organisation::{organisation_service_client::OrganisationServiceClient, CreateOrganisationRequest};
    
    #[tokio::main]
    async fn main() -> Result<(), Box<dyn std::error::Error>> {
        // Create TLS connection
        let channel = Channel::from_static("https://api.perms.io:443")
            .tls_config(ClientTlsConfig::new())?
            .connect()
            .await?;
    
        let mut client = OrganisationServiceClient::new(channel);
        
        // Create organisation request
        let mut request = Request::new(CreateOrganisationRequest {
            name: "My Company".to_string(),
            user_id: "your-user-id".to_string(),
        });
        
        // Add authentication header
        let token: MetadataValue<_> = "Bearer YOUR_TOKEN".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        // Make the request
        let response = client.create_organisation(request).await?;
        let org = response.into_inner().organisation.unwrap();
        
        println!("Created organisation: {} (ID: {})", org.name, org.id);
        Ok(())
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

=== "Java"
    ```java
    import io.grpc.Channel;
    import io.grpc.ManagedChannelBuilder;
    import io.grpc.Metadata;
    import io.grpc.stub.MetadataUtils;
    
    import organisation.v1.OrganisationServiceGrpc;
    import organisation.v1.OrganisationServiceOuterClass.*;
    
    public class CreateOrganisation {
        public static void main(String[] args) {
            // Create channel
            Channel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
            
            // Create client
            OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
            
            // Add authentication metadata
            Metadata metadata = new Metadata();
            Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
            metadata.put(authKey, "Bearer YOUR_TOKEN");
            
            client = MetadataUtils.attachHeaders(client, metadata);
            
            // Create organisation request
            CreateOrganisationRequest request = CreateOrganisationRequest.newBuilder()
                .setName("My Company")
                .setUserId("your-user-id")
                .build();
            
            // Make the request
            CreateOrganisationResponse response = client.createOrganisation(request);
            Organisation org = response.getOrganisation();
            
            System.out.printf("Created organisation: %s (ID: %s)%n", org.getName(), org.getId());
        }
    }
    ```

=== "TypeScript"
    ```typescript
    import * as grpc from '@grpc/grpc-js';
    import * as protoLoader from '@grpc/proto-loader';

    interface CreateOrganisationRequest {
        name: string;
        user_id: string;
    }

    interface Organisation {
        id: string;
        name: string;
        user_id: string;
    }

    interface CreateOrganisationResponse {
        organisation: Organisation;
    }

    interface OrganisationServiceClient {
        CreateOrganisation(
            request: CreateOrganisationRequest,
            metadata: grpc.Metadata,
            callback: (error: grpc.ServiceError | null, response: CreateOrganisationResponse | null) => void
        ): void;
    }

    // Load the proto file
    const packageDefinition = protoLoader.loadSync('./proto/organisation/v1/organisation_service.proto');
    const organisationService = grpc.loadPackageDefinition(packageDefinition).organisation_service.v1 as any;

    // Create client with SSL credentials
    const client: OrganisationServiceClient = new organisationService.OrganisationService(
        'api.perms.io:443', 
        grpc.credentials.createSsl()
    );

    function createOrganisation(): Promise<string> {
        return new Promise((resolve, reject) => {
            const request: CreateOrganisationRequest = {
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
                if (!response) {
                    reject(new Error('No response received'));
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

=== "Rust"
    ```rust
    async fn create_project(
        client: &mut OrganisationServiceClient<Channel>, 
        org_id: String
    ) -> Result<String, Box<dyn std::error::Error>> {
        let mut request = Request::new(CreateProjectRequest {
            organisation_id: org_id,
            name: "production".to_string(),
        });
        
        // Add authentication header
        let token: MetadataValue<_> = "Bearer YOUR_TOKEN".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let response = client.create_project(request).await?;
        let project = response.into_inner().project.unwrap();
        
        println!("Created project: {}", project.name);
        Ok(project.name)
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

=== "Java"
    ```java
    public static String createProject(OrganisationServiceGrpc.OrganisationServiceBlockingStub client, String orgId) {
        // Add authentication metadata
        Metadata metadata = new Metadata();
        Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
        metadata.put(authKey, "Bearer YOUR_TOKEN");
        
        client = MetadataUtils.attachHeaders(client, metadata);
        
        CreateProjectRequest request = CreateProjectRequest.newBuilder()
            .setOrganisationId(orgId)
            .setName("production")
            .build();
        
        CreateProjectResponse response = client.createProject(request);
        Project project = response.getProject();
        
        System.out.printf("Created project: %s%n", project.getName());
        return project.getName();
    }
    ```

=== "TypeScript"
    ```typescript
    interface CreateProjectRequest {
        organisation_id: string;
        name: string;
    }

    interface Project {
        name: string;
        organisation_id: string;
    }

    interface CreateProjectResponse {
        project: Project;
    }

    function createProject(client: OrganisationServiceClient, orgId: string): Promise<string> {
        return new Promise((resolve, reject) => {
            const request: CreateProjectRequest = {
                organisation_id: orgId,
                name: 'production'
            };
            
            const metadata = new grpc.Metadata();
            metadata.add('authorization', 'Bearer YOUR_TOKEN');
            
            client.CreateProject(request, metadata, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                if (!response) {
                    reject(new Error('No response received'));
                    return;
                }
                console.log(`Created project: ${response.project.name}`);
                resolve(response.project.name);
            });
        });
    }
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

=== "Rust"
    ```rust
    async fn create_api_key(
        client: &mut OrganisationServiceClient<Channel>, 
        org_id: String
    ) -> Result<String, Box<dyn std::error::Error>> {
        let mut request = Request::new(CreateApiKeyRequest {
            organisation_id: org_id,
            project_name: "production".to_string(),
            name: "My Application API Key".to_string(),
        });
        
        // Add authentication header
        let token: MetadataValue<_> = "Bearer YOUR_TOKEN".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let response = client.create_api_key(request).await?;
        let api_key = response.into_inner().api_key.unwrap();
        
        println!("Created API key: {}", api_key.name);
        println!("API Key (store securely): {}", api_key.key);
        Ok(api_key.key)
    }
    ```

=== "Python"
    ```python
    def create_api_key(org_id: str) -> str:
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        metadata = [('authorization', 'Bearer YOUR_TOKEN')]
        
        request = organisation_service_pb2.CreateAPIKeyRequest(
            organisation_id=org_id,
            project_name="production",
            name="My Application API Key"
        )
        
        response = client.CreateAPIKey(request, metadata=metadata)
        print(f"Created API key: {response.api_key.name}")
        print(f"API Key (store securely): {response.api_key.key}")
        return response.api_key.key
    ```

=== "Java"
    ```java
    public static String createAPIKey(OrganisationServiceGrpc.OrganisationServiceBlockingStub client, String orgId) {
        // Add authentication metadata
        Metadata metadata = new Metadata();
        Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
        metadata.put(authKey, "Bearer YOUR_TOKEN");
        
        client = MetadataUtils.attachHeaders(client, metadata);
        
        CreateAPIKeyRequest request = CreateAPIKeyRequest.newBuilder()
            .setOrganisationId(orgId)
            .setProjectName("production")
            .setName("My Application API Key")
            .build();
        
        CreateAPIKeyResponse response = client.createAPIKey(request);
        APIKey apiKey = response.getApiKey();
        
        System.out.printf("Created API key: %s%n", apiKey.getName());
        System.out.printf("API Key (store securely): %s%n", apiKey.getKey());
        return apiKey.getKey();
    }
    ```

=== "TypeScript"
    ```typescript
    interface CreateAPIKeyRequest {
        organisation_id: string;
        project_name: string;
        name: string;
    }

    interface APIKey {
        name: string;
        key: string;
        organisation_id: string;
        project_name: string;
    }

    interface CreateAPIKeyResponse {
        api_key: APIKey;
    }

    function createAPIKey(client: OrganisationServiceClient, orgId: string): Promise<string> {
        return new Promise((resolve, reject) => {
            const request: CreateAPIKeyRequest = {
                organisation_id: orgId,
                project_name: 'production',
                name: 'My Application API Key'
            };
            
            const metadata = new grpc.Metadata();
            metadata.add('authorization', 'Bearer YOUR_TOKEN');
            
            client.CreateAPIKey(request, metadata, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                if (!response) {
                    reject(new Error('No response received'));
                    return;
                }
                console.log(`Created API key: ${response.api_key.name}`);
                console.log(`API Key (store securely): ${response.api_key.key}`);
                resolve(response.api_key.key);
            });
        });
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

=== "Rust"
    ```rust
    use permissions::permissions_service_client::PermissionsServiceClient;
    use permissions::{CreatePermissionRequest};
    
    async fn create_permissions(
        client: &mut PermissionsServiceClient<Channel>
    ) -> Result<Vec<String>, Box<dyn std::error::Error>> {
        let permissions = vec![
            ("document.read", "Allows reading documents"),
            ("document.write", "Allows writing documents"),
            ("document.delete", "Allows deleting documents"),
        ];
        
        let mut permission_ids = Vec::new();
        
        for (name, description) in permissions {
            let mut request = Request::new(CreatePermissionRequest {
                project_name: "production".to_string(),
                name: name.to_string(),
                description: description.to_string(),
            });
            
            // Add authentication header
            let token: MetadataValue<_> = "Bearer YOUR_API_KEY".parse()?;
            request.metadata_mut().insert("authorization", token);
            
            let response = client.create_permission(request).await?;
            let permission = response.into_inner();
            
            permission_ids.push(permission.id.clone());
            println!("Created permission: {} (ID: {})", permission.name, permission.id);
        }
        
        Ok(permission_ids)
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

=== "Java"
    ```java
    import permissions.v1.PermissionsServiceGrpc;
    import permissions.v1.PermissionsServiceOuterClass.*;
    
    public static List<String> createPermissions(PermissionsServiceGrpc.PermissionsServiceBlockingStub client) {
        // Add authentication metadata
        Metadata metadata = new Metadata();
        Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
        metadata.put(authKey, "Bearer YOUR_API_KEY");
        
        client = MetadataUtils.attachHeaders(client, metadata);
        
        String[][] permissions = {
            {"document.read", "Allows reading documents"},
            {"document.write", "Allows writing documents"},
            {"document.delete", "Allows deleting documents"}
        };
        
        List<String> permissionIds = new ArrayList<>();
        
        for (String[] perm : permissions) {
            CreatePermissionRequest request = CreatePermissionRequest.newBuilder()
                .setProjectName("production")
                .setName(perm[0])
                .setDescription(perm[1])
                .build();
            
            CreatePermissionResponse response = client.createPermission(request);
            
            permissionIds.add(response.getId());
            System.out.printf("Created permission: %s (ID: %s)%n", response.getName(), response.getId());
        }
        
        return permissionIds;
    }
    ```

=== "TypeScript"
    ```typescript
    interface CreatePermissionRequest {
        project_name: string;
        name: string;
        description: string;
    }

    interface CreatePermissionResponse {
        id: string;
        name: string;
        description: string;
        project_name: string;
    }

    interface PermissionsServiceClient {
        CreatePermission(
            request: CreatePermissionRequest,
            metadata: grpc.Metadata,
            callback: (error: grpc.ServiceError | null, response: CreatePermissionResponse | null) => void
        ): void;
    }

    async function createPermissions(client: PermissionsServiceClient): Promise<string[]> {
        const permissions = [
            { name: "document.read", description: "Allows reading documents" },
            { name: "document.write", description: "Allows writing documents" },
            { name: "document.delete", description: "Allows deleting documents" }
        ];
        
        const permissionIds: string[] = [];
        
        for (const perm of permissions) {
            const permissionId = await new Promise<string>((resolve, reject) => {
                const request: CreatePermissionRequest = {
                    project_name: "production",
                    name: perm.name,
                    description: perm.description
                };
                
                const metadata = new grpc.Metadata();
                metadata.add('authorization', 'Bearer YOUR_API_KEY');
                
                client.CreatePermission(request, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    if (!response) {
                        reject(new Error('No response received'));
                        return;
                    }
                    console.log(`Created permission: ${response.name} (ID: ${response.id})`);
                    resolve(response.id);
                });
            });
            
            permissionIds.push(permissionId);
        }
        
        return permissionIds;
    }
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

=== "Rust"
    ```rust
    async fn create_roles(
        client: &mut PermissionsServiceClient<Channel>,
        permission_ids: Vec<String>
    ) -> Result<Vec<String>, Box<dyn std::error::Error>> {
        let roles = vec![
            ("document_viewer", "Can read documents", vec![permission_ids[0].clone()]),
            ("document_editor", "Can read and write documents", vec![permission_ids[0].clone(), permission_ids[1].clone()]),
            ("document_admin", "Full access to documents", permission_ids.clone()),
        ];
        
        let mut role_ids = Vec::new();
        
        for (name, description, permissions) in roles {
            let mut request = Request::new(CreateRoleRequest {
                project_name: "production".to_string(),
                name: name.to_string(),
                description: description.to_string(),
                permissions,
            });
            
            // Add authentication header
            let token: MetadataValue<_> = "Bearer YOUR_API_KEY".parse()?;
            request.metadata_mut().insert("authorization", token);
            
            let response = client.create_role(request).await?;
            let role = response.into_inner();
            
            role_ids.push(role.id.clone());
            println!("Created role: {} (ID: {})", role.name, role.id);
        }
        
        Ok(role_ids)
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
            ("document_admin", "Full access to documents", permission_ids),
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

=== "Java"
    ```java
    public static List<String> createRoles(PermissionsServiceGrpc.PermissionsServiceBlockingStub client, List<String> permissionIds) {
        // Add authentication metadata
        Metadata metadata = new Metadata();
        Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
        metadata.put(authKey, "Bearer YOUR_API_KEY");
        
        client = MetadataUtils.attachHeaders(client, metadata);
        
        Object[][] roles = {
            {"document_viewer", "Can read documents", Arrays.asList(permissionIds.get(0))},
            {"document_editor", "Can read and write documents", Arrays.asList(permissionIds.get(0), permissionIds.get(1))},
            {"document_admin", "Full access to documents", permissionIds}
        };
        
        List<String> roleIds = new ArrayList<>();
        
        for (Object[] role : roles) {
            CreateRoleRequest request = CreateRoleRequest.newBuilder()
                .setProjectName("production")
                .setName((String) role[0])
                .setDescription((String) role[1])
                .addAllPermissions((List<String>) role[2])
                .build();
            
            CreateRoleResponse response = client.createRole(request);
            
            roleIds.add(response.getId());
            System.out.printf("Created role: %s (ID: %s)%n", response.getName(), response.getId());
        }
        
        return roleIds;
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

    interface CreateRoleResponse {
        id: string;
        name: string;
        description: string;
        permissions: string[];
    }

    async function createRoles(client: PermissionsServiceClient, permissionIds: string[]): Promise<string[]> {
        const roles = [
            { name: "document_viewer", description: "Can read documents", permissions: [permissionIds[0]] },
            { name: "document_editor", description: "Can read and write documents", permissions: [permissionIds[0], permissionIds[1]] },
            { name: "document_admin", description: "Full access to documents", permissions: permissionIds },
        ];
        
        const roleIds: string[] = [];
        
        for (const role of roles) {
            const roleId = await new Promise<string>((resolve, reject) => {
                const request: CreateRoleRequest = {
                    project_name: "production",
                    name: role.name,
                    description: role.description,
                    permissions: role.permissions
                };
                
                const metadata = new grpc.Metadata();
                metadata.add('authorization', 'Bearer YOUR_API_KEY');
                
                client.CreateRole(request, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    if (!response) {
                        reject(new Error('No response received'));
                        return;
                    }
                    console.log(`Created role: ${response.name} (ID: ${response.id})`);
                    resolve(response.id);
                });
            });
            
            roleIds.push(roleId);
        }
        
        return roleIds;
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

=== "Rust"
    ```rust
    async fn grant_permissions(
        client: &mut PermissionsServiceClient<Channel>,
        role_ids: Vec<String>
    ) -> Result<(), Box<dyn std::error::Error>> {
        // Grant viewer role to user on all documents
        let mut request = Request::new(GrantUserPermissionsAndRolesOnResourceRequest {
            project_name: "production".to_string(),
            user_id: "user_123".to_string(),
            resource_uri: "/documents".to_string(),
            permissions: vec![],
            roles: vec![role_ids[0].clone()], // viewer role
        });
        
        // Add authentication header
        let token: MetadataValue<_> = "Bearer YOUR_API_KEY".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        client.grant_user_permissions_and_roles_on_resource(request).await?;
        println!("Granted viewer permissions to user_123 on /documents");
        
        // Grant editor role to user on specific document
        let mut request = Request::new(GrantUserPermissionsAndRolesOnResourceRequest {
            project_name: "production".to_string(),
            user_id: "user_456".to_string(),
            resource_uri: "/documents/doc_789".to_string(),
            permissions: vec![],
            roles: vec![role_ids[1].clone()], // editor role
        });
        
        let token: MetadataValue<_> = "Bearer YOUR_API_KEY".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        client.grant_user_permissions_and_roles_on_resource(request).await?;
        println!("Granted editor permissions to user_456 on /documents/doc_789");
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def grant_permissions(role_ids: list[str]):
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        metadata = [('authorization', 'Bearer YOUR_API_KEY')]
        
        # Grant viewer role to user on all documents
        request = permissions_service_pb2.GrantUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id="user_123",
            resource_uri="/documents",
            permissions=[],
            roles=[role_ids[0]]  # viewer role
        )
        
        client.GrantUserPermissionsAndRolesOnResource(request, metadata=metadata)
        print("Granted viewer permissions to user_123 on /documents")
        
        # Grant editor role to user on specific document
        request = permissions_service_pb2.GrantUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id="user_456",
            resource_uri="/documents/doc_789",
            permissions=[],
            roles=[role_ids[1]]  # editor role
        )
        
        client.GrantUserPermissionsAndRolesOnResource(request, metadata=metadata)
        print("Granted editor permissions to user_456 on /documents/doc_789")
    ```

=== "Java"
    ```java
    public static void grantPermissions(PermissionsServiceGrpc.PermissionsServiceBlockingStub client, List<String> roleIds) {
        // Add authentication metadata
        Metadata metadata = new Metadata();
        Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
        metadata.put(authKey, "Bearer YOUR_API_KEY");
        
        client = MetadataUtils.attachHeaders(client, metadata);
        
        // Grant viewer role to user on all documents
        GrantUserPermissionsAndRolesOnResourceRequest request = GrantUserPermissionsAndRolesOnResourceRequest.newBuilder()
            .setProjectName("production")
            .setUserId("user_123")
            .setResourceUri("/documents")
            .addRoles(roleIds.get(0)) // viewer role
            .build();
        
        client.grantUserPermissionsAndRolesOnResource(request);
        System.out.println("Granted viewer permissions to user_123 on /documents");
        
        // Grant editor role to user on specific document
        request = GrantUserPermissionsAndRolesOnResourceRequest.newBuilder()
            .setProjectName("production")
            .setUserId("user_456")
            .setResourceUri("/documents/doc_789")
            .addRoles(roleIds.get(1)) // editor role
            .build();
        
        client.grantUserPermissionsAndRolesOnResource(request);
        System.out.println("Granted editor permissions to user_456 on /documents/doc_789");
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

    async function grantPermissions(client: PermissionsServiceClient, roleIds: string[]): Promise<void> {
        // Grant viewer role to user on all documents
        await new Promise<void>((resolve, reject) => {
            const request: GrantUserPermissionsAndRolesOnResourceRequest = {
                project_name: "production",
                user_id: "user_123",
                resource_uri: "/documents",
                permissions: [],
                roles: [roleIds[0]] // viewer role
            };
            
            const metadata = new grpc.Metadata();
            metadata.add('authorization', 'Bearer YOUR_API_KEY');
            
            client.GrantUserPermissionsAndRolesOnResource(request, metadata, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                console.log("Granted viewer permissions to user_123 on /documents");
                resolve();
            });
        });
        
        // Grant editor role to user on specific document
        await new Promise<void>((resolve, reject) => {
            const request: GrantUserPermissionsAndRolesOnResourceRequest = {
                project_name: "production",
                user_id: "user_456",
                resource_uri: "/documents/doc_789",
                permissions: [],
                roles: [roleIds[1]] // editor role
            };
            
            const metadata = new grpc.Metadata();
            metadata.add('authorization', 'Bearer YOUR_API_KEY');
            
            client.GrantUserPermissionsAndRolesOnResource(request, metadata, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                console.log("Granted editor permissions to user_456 on /documents/doc_789");
                resolve();
            });
        });
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

=== "Rust"
    ```rust
    async fn check_permissions(
        client: &mut PermissionsServiceClient<Channel>
    ) -> Result<(), Box<dyn std::error::Error>> {
        let mut request = Request::new(CheckPermissionRequest {
            project_name: "production".to_string(),
            principal_id: "user_123".to_string(),
            resource_uris: vec!["/documents/doc_456".to_string()],
            permissions: vec!["document.read".to_string(), "document.write".to_string()],
        });
        
        // Add authentication header
        let token: MetadataValue<_> = "Bearer YOUR_API_KEY".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let response = client.check(request).await?;
        let check_result = response.into_inner();
        
        if check_result.passed {
            println!("✅ User user_123 has required permissions");
        } else {
            println!("❌ User user_123 missing permissions:");
            for missing in check_result.missing_permissions {
                println!("  Resource: {}, Missing: {:?}", missing.resource_uri, missing.missing_permissions);
            }
        }
        
        Ok(())
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

=== "Java"
    ```java
    public static void checkPermissions(PermissionsServiceGrpc.PermissionsServiceBlockingStub client) {
        // Add authentication metadata
        Metadata metadata = new Metadata();
        Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
        metadata.put(authKey, "Bearer YOUR_API_KEY");
        
        client = MetadataUtils.attachHeaders(client, metadata);
        
        CheckPermissionRequest request = CheckPermissionRequest.newBuilder()
            .setProjectName("production")
            .setPrincipalId("user_123")
            .addResourceUris("/documents/doc_456")
            .addPermissions("document.read")
            .addPermissions("document.write")
            .build();
        
        CheckPermissionResponse response = client.check(request);
        
        if (response.getPassed()) {
            System.out.println("✅ User user_123 has required permissions");
        } else {
            System.out.println("❌ User user_123 missing permissions:");
            for (MissingPermission missing : response.getMissingPermissionsList()) {
                System.out.printf("  Resource: %s, Missing: %s%n", 
                    missing.getResourceUri(), missing.getMissingPermissionsList());
            }
        }
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

    interface MissingPermission {
        resource_uri: string;
        missing_permissions: string[];
    }

    interface CheckPermissionResponse {
        passed: boolean;
        missing_permissions: MissingPermission[];
    }

    async function checkPermissions(client: PermissionsServiceClient): Promise<void> {
        return new Promise((resolve, reject) => {
            const request: CheckPermissionRequest = {
                project_name: "production",
                principal_id: "user_123",
                resource_uris: ["/documents/doc_456"],
                permissions: ["document.read", "document.write"]
            };
            
            const metadata = new grpc.Metadata();
            metadata.add('authorization', 'Bearer YOUR_API_KEY');
            
            client.Check(request, metadata, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                if (!response) {
                    reject(new Error('No response received'));
                    return;
                }
                
                if (response.passed) {
                    console.log("✅ User user_123 has required permissions");
                } else {
                    console.log("❌ User user_123 missing permissions:");
                    for (const missing of response.missing_permissions) {
                        console.log(`  Resource: ${missing.resource_uri}, Missing: ${missing.missing_permissions}`);
                    }
                }
                
                resolve();
            });
        });
    }
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

=== "Rust"
    ```rust
    use tonic::{transport::Channel, metadata::MetadataValue, Request};
    use tonic::transport::ClientTlsConfig;
    
    pub mod organisation {
        tonic::include_proto!("organisation_service.v1");
    }
    
    pub mod permissions {
        tonic::include_proto!("permissions_service.v1");
    }
    
    use organisation::{organisation_service_client::OrganisationServiceClient, CreateOrganisationRequest, CreateProjectRequest, CreateApiKeyRequest};
    use permissions::{permissions_service_client::PermissionsServiceClient, CreatePermissionRequest, CreateRoleRequest, GrantUserPermissionsAndRolesOnResourceRequest, CheckPermissionRequest};
    
    #[tokio::main]
    async fn main() -> Result<(), Box<dyn std::error::Error>> {
        // Create TLS connection
        let channel = Channel::from_static("https://api.perms.io:443")
            .tls_config(ClientTlsConfig::new())?
            .connect()
            .await?;
    
        let mut org_client = OrganisationServiceClient::new(channel.clone());
        let mut perm_client = PermissionsServiceClient::new(channel);
        
        // 1. Create organisation
        let mut request = Request::new(CreateOrganisationRequest {
            name: "Document Management Co".to_string(),
            user_id: "admin_user".to_string(),
        });
        
        let token: MetadataValue<_> = "Bearer YOUR_TOKEN".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let org_response = org_client.create_organisation(request).await?;
        let org = org_response.into_inner().organisation.unwrap();
        println!("Created organisation: {}", org.id);
        
        // 2. Create project
        let mut request = Request::new(CreateProjectRequest {
            organisation_id: org.id.clone(),
            name: "production".to_string(),
        });
        
        let token: MetadataValue<_> = "Bearer YOUR_TOKEN".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let project_response = org_client.create_project(request).await?;
        let project = project_response.into_inner().project.unwrap();
        println!("Created project: {}", project.name);
        
        // 3. Create API key
        let mut request = Request::new(CreateApiKeyRequest {
            organisation_id: org.id.clone(),
            project_name: "production".to_string(),
            name: "Application API Key".to_string(),
        });
        
        let token: MetadataValue<_> = "Bearer YOUR_TOKEN".parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let api_key_response = org_client.create_api_key(request).await?;
        let api_key = api_key_response.into_inner().api_key.unwrap();
        println!("Created API key: {}", api_key.name);
        
        // Switch to API key authentication
        let api_token = format!("Bearer {}", api_key.key);
        
        // 4. Create permissions
        let permissions = vec![
            ("document.read", "Read documents"),
            ("document.write", "Write documents"),
            ("document.delete", "Delete documents"),
        ];
        
        let mut perm_ids = Vec::new();
        
        for (name, desc) in permissions {
            let mut request = Request::new(CreatePermissionRequest {
                project_name: "production".to_string(),
                name: name.to_string(),
                description: desc.to_string(),
            });
            
            let token: MetadataValue<_> = api_token.parse()?;
            request.metadata_mut().insert("authorization", token);
            
            let perm_response = perm_client.create_permission(request).await?;
            let permission = perm_response.into_inner();
            perm_ids.push(permission.id.clone());
            println!("Created permission: {}", permission.name);
        }
        
        // 5. Create role
        let mut request = Request::new(CreateRoleRequest {
            project_name: "production".to_string(),
            name: "document_editor".to_string(),
            description: "Can read and write documents".to_string(),
            permissions: perm_ids[..2].to_vec(), // read + write
        });
        
        let token: MetadataValue<_> = api_token.parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let role_response = perm_client.create_role(request).await?;
        let role = role_response.into_inner();
        println!("Created role: {}", role.name);
        
        // 6. Grant permissions
        let mut request = Request::new(GrantUserPermissionsAndRolesOnResourceRequest {
            project_name: "production".to_string(),
            user_id: "user_123".to_string(),
            resource_uri: "/documents".to_string(),
            permissions: vec![],
            roles: vec![role.id.clone()],
        });
        
        let token: MetadataValue<_> = api_token.parse()?;
        request.metadata_mut().insert("authorization", token);
        
        perm_client.grant_user_permissions_and_roles_on_resource(request).await?;
        println!("Granted permissions to user_123");
        
        // 7. Check permissions
        let mut request = Request::new(CheckPermissionRequest {
            project_name: "production".to_string(),
            principal_id: "user_123".to_string(),
            resource_uris: vec!["/documents/doc_456".to_string()],
            permissions: vec!["document.read".to_string()],
        });
        
        let token: MetadataValue<_> = api_token.parse()?;
        request.metadata_mut().insert("authorization", token);
        
        let check_response = perm_client.check(request).await?;
        let check_result = check_response.into_inner();
        
        if check_result.passed {
            println!("✅ Permission check passed!");
        } else {
            println!("❌ Permission check failed");
        }
        
        println!("Setup complete! Your RBAC system is ready to use.");
        Ok(())
    }
    ```

=== "Python"
    ```python
    import grpc
    from grpc import ssl_channel_credentials
    
    from proto.organisation.v1 import organisation_service_pb2
    from proto.organisation.v1 import organisation_service_pb2_grpc
    from proto.permissions.v1 import permissions_service_pb2
    from proto.permissions.v1 import permissions_service_pb2_grpc

    def main():
        # Create secure channel
        channel = grpc.secure_channel('api.perms.io:443', ssl_channel_credentials())
        org_client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        perm_client = permissions_service_pb2_grpc.PermissionsServiceStub(channel)
        
        # Initial authentication with bearer token
        token_metadata = [('authorization', 'Bearer YOUR_TOKEN')]
        
        # 1. Create organisation
        org_request = organisation_service_pb2.CreateOrganisationRequest(
            name="Document Management Co",
            user_id="admin_user"
        )
        org_response = org_client.CreateOrganisation(org_request, metadata=token_metadata)
        org = org_response.organisation
        print(f"Created organisation: {org.id}")
        
        # 2. Create project
        project_request = organisation_service_pb2.CreateProjectRequest(
            organisation_id=org.id,
            name="production"
        )
        project_response = org_client.CreateProject(project_request, metadata=token_metadata)
        project = project_response.project
        print(f"Created project: {project.name}")
        
        # 3. Create API key
        api_key_request = organisation_service_pb2.CreateAPIKeyRequest(
            organisation_id=org.id,
            project_name="production",
            name="Application API Key"
        )
        api_key_response = org_client.CreateAPIKey(api_key_request, metadata=token_metadata)
        api_key = api_key_response.api_key
        print(f"Created API key: {api_key.name}")
        
        # Switch to API key authentication
        api_metadata = [('authorization', f'Bearer {api_key.key}')]
        
        # 4. Create permissions
        permissions = [
            ("document.read", "Read documents"),
            ("document.write", "Write documents"),
            ("document.delete", "Delete documents")
        ]
        
        perm_ids = []
        
        for name, description in permissions:
            perm_request = permissions_service_pb2.CreatePermissionRequest(
                project_name="production",
                name=name,
                description=description
            )
            perm_response = perm_client.CreatePermission(perm_request, metadata=api_metadata)
            perm_ids.append(perm_response.id)
            print(f"Created permission: {perm_response.name}")
        
        # 5. Create role
        role_request = permissions_service_pb2.CreateRoleRequest(
            project_name="production",
            name="document_editor",
            description="Can read and write documents",
            permissions=perm_ids[:2]  # read + write
        )
        role_response = perm_client.CreateRole(role_request, metadata=api_metadata)
        role = role_response
        print(f"Created role: {role.name}")
        
        # 6. Grant permissions
        grant_request = permissions_service_pb2.GrantUserPermissionsAndRolesOnResourceRequest(
            project_name="production",
            user_id="user_123",
            resource_uri="/documents",
            permissions=[],
            roles=[role.id]
        )
        perm_client.GrantUserPermissionsAndRolesOnResource(grant_request, metadata=api_metadata)
        print("Granted permissions to user_123")
        
        # 7. Check permissions
        check_request = permissions_service_pb2.CheckPermissionRequest(
            project_name="production",
            principal_id="user_123",
            resource_uris=["/documents/doc_456"],
            permissions=["document.read"]
        )
        check_response = perm_client.Check(check_request, metadata=api_metadata)
        
        if check_response.passed:
            print("✅ Permission check passed!")
        else:
            print("❌ Permission check failed")
        
        print("Setup complete! Your RBAC system is ready to use.")

    if __name__ == "__main__":
        main()
    ```

=== "Java"
    ```java
    import io.grpc.Channel;
    import io.grpc.ManagedChannelBuilder;
    import io.grpc.Metadata;
    import io.grpc.stub.MetadataUtils;
    
    import organisation.v1.OrganisationServiceGrpc;
    import organisation.v1.OrganisationServiceOuterClass.*;
    import permissions.v1.PermissionsServiceGrpc;
    import permissions.v1.PermissionsServiceOuterClass.*;
    
    import java.util.Arrays;
    import java.util.List;
    
    public class PermsIoQuickStart {
        public static void main(String[] args) {
            // Create channel
            Channel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
            
            // Create clients
            OrganisationServiceGrpc.OrganisationServiceBlockingStub orgClient = 
                OrganisationServiceGrpc.newBlockingStub(channel);
            PermissionsServiceGrpc.PermissionsServiceBlockingStub permClient = 
                PermissionsServiceGrpc.newBlockingStub(channel);
            
            // Initial authentication metadata
            Metadata tokenMetadata = new Metadata();
            Metadata.Key<String> authKey = Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER);
            tokenMetadata.put(authKey, "Bearer YOUR_TOKEN");
            
            orgClient = MetadataUtils.attachHeaders(orgClient, tokenMetadata);
            
            // 1. Create organisation
            CreateOrganisationRequest orgRequest = CreateOrganisationRequest.newBuilder()
                .setName("Document Management Co")
                .setUserId("admin_user")
                .build();
            
            CreateOrganisationResponse orgResponse = orgClient.createOrganisation(orgRequest);
            Organisation org = orgResponse.getOrganisation();
            System.out.printf("Created organisation: %s%n", org.getId());
            
            // 2. Create project
            CreateProjectRequest projectRequest = CreateProjectRequest.newBuilder()
                .setOrganisationId(org.getId())
                .setName("production")
                .build();
            
            CreateProjectResponse projectResponse = orgClient.createProject(projectRequest);
            Project project = projectResponse.getProject();
            System.out.printf("Created project: %s%n", project.getName());
            
            // 3. Create API key
            CreateAPIKeyRequest apiKeyRequest = CreateAPIKeyRequest.newBuilder()
                .setOrganisationId(org.getId())
                .setProjectName("production")
                .setName("Application API Key")
                .build();
            
            CreateAPIKeyResponse apiKeyResponse = orgClient.createAPIKey(apiKeyRequest);
            APIKey apiKey = apiKeyResponse.getApiKey();
            System.out.printf("Created API key: %s%n", apiKey.getName());
            
            // Switch to API key authentication
            Metadata apiMetadata = new Metadata();
            apiMetadata.put(authKey, "Bearer " + apiKey.getKey());
            permClient = MetadataUtils.attachHeaders(permClient, apiMetadata);
            
            // 4. Create permissions
            String[][] permissions = {
                {"document.read", "Read documents"},
                {"document.write", "Write documents"},
                {"document.delete", "Delete documents"}
            };
            
            String[] permIds = new String[permissions.length];
            
            for (int i = 0; i < permissions.length; i++) {
                CreatePermissionRequest permRequest = CreatePermissionRequest.newBuilder()
                    .setProjectName("production")
                    .setName(permissions[i][0])
                    .setDescription(permissions[i][1])
                    .build();
                
                CreatePermissionResponse permResponse = permClient.createPermission(permRequest);
                permIds[i] = permResponse.getId();
                System.out.printf("Created permission: %s%n", permResponse.getName());
            }
            
            // 5. Create role
            CreateRoleRequest roleRequest = CreateRoleRequest.newBuilder()
                .setProjectName("production")
                .setName("document_editor")
                .setDescription("Can read and write documents")
                .addAllPermissions(Arrays.asList(permIds[0], permIds[1])) // read + write
                .build();
            
            CreateRoleResponse roleResponse = permClient.createRole(roleRequest);
            System.out.printf("Created role: %s%n", roleResponse.getName());
            
            // 6. Grant permissions
            GrantUserPermissionsAndRolesOnResourceRequest grantRequest = 
                GrantUserPermissionsAndRolesOnResourceRequest.newBuilder()
                    .setProjectName("production")
                    .setUserId("user_123")
                    .setResourceUri("/documents")
                    .addRoles(roleResponse.getId())
                    .build();
            
            permClient.grantUserPermissionsAndRolesOnResource(grantRequest);
            System.out.println("Granted permissions to user_123");
            
            // 7. Check permissions
            CheckPermissionRequest checkRequest = CheckPermissionRequest.newBuilder()
                .setProjectName("production")
                .setPrincipalId("user_123")
                .addResourceUris("/documents/doc_456")
                .addPermissions("document.read")
                .build();
            
            CheckPermissionResponse checkResponse = permClient.check(checkRequest);
            
            if (checkResponse.getPassed()) {
                System.out.println("✅ Permission check passed!");
            } else {
                System.out.println("❌ Permission check failed");
            }
            
            System.out.println("Setup complete! Your RBAC system is ready to use.");
        }
    }
    ```

=== "TypeScript"
    ```typescript
    import * as grpc from '@grpc/grpc-js';
    import * as protoLoader from '@grpc/proto-loader';

    // Type definitions
    interface CreateOrganisationRequest {
        name: string;
        user_id: string;
    }

    interface Organisation {
        id: string;
        name: string;
        user_id: string;
    }

    interface CreateOrganisationResponse {
        organisation: Organisation;
    }

    interface CreateProjectRequest {
        organisation_id: string;
        name: string;
    }

    interface Project {
        name: string;
        organisation_id: string;
    }

    interface CreateProjectResponse {
        project: Project;
    }

    interface CreateAPIKeyRequest {
        organisation_id: string;
        project_name: string;
        name: string;
    }

    interface APIKey {
        name: string;
        key: string;
        organisation_id: string;
        project_name: string;
    }

    interface CreateAPIKeyResponse {
        api_key: APIKey;
    }

    interface CreatePermissionRequest {
        project_name: string;
        name: string;
        description: string;
    }

    interface CreatePermissionResponse {
        id: string;
        name: string;
        description: string;
        project_name: string;
    }

    interface CreateRoleRequest {
        project_name: string;
        name: string;
        description: string;
        permissions: string[];
    }

    interface CreateRoleResponse {
        id: string;
        name: string;
        description: string;
        permissions: string[];
    }

    interface GrantUserPermissionsAndRolesOnResourceRequest {
        project_name: string;
        user_id: string;
        resource_uri: string;
        permissions: string[];
        roles: string[];
    }

    interface CheckPermissionRequest {
        project_name: string;
        principal_id: string;
        resource_uris: string[];
        permissions: string[];
    }

    interface CheckPermissionResponse {
        passed: boolean;
        missing_permissions: any[];
    }

    // Service client interfaces
    interface OrganisationServiceClient {
        CreateOrganisation(request: CreateOrganisationRequest, metadata: grpc.Metadata, callback: grpc.requestCallback<CreateOrganisationResponse>): void;
        CreateProject(request: CreateProjectRequest, metadata: grpc.Metadata, callback: grpc.requestCallback<CreateProjectResponse>): void;
        CreateAPIKey(request: CreateAPIKeyRequest, metadata: grpc.Metadata, callback: grpc.requestCallback<CreateAPIKeyResponse>): void;
    }

    interface PermissionsServiceClient {
        CreatePermission(request: CreatePermissionRequest, metadata: grpc.Metadata, callback: grpc.requestCallback<CreatePermissionResponse>): void;
        CreateRole(request: CreateRoleRequest, metadata: grpc.Metadata, callback: grpc.requestCallback<CreateRoleResponse>): void;
        GrantUserPermissionsAndRolesOnResource(request: GrantUserPermissionsAndRolesOnResourceRequest, metadata: grpc.Metadata, callback: grpc.requestCallback<any>): void;
        Check(request: CheckPermissionRequest, metadata: grpc.Metadata, callback: grpc.requestCallback<CheckPermissionResponse>): void;
    }

    async function main(): Promise<void> {
        // Load proto files
        const orgPackageDefinition = protoLoader.loadSync('./proto/organisation/v1/organisation_service.proto');
        const permPackageDefinition = protoLoader.loadSync('./proto/permissions/v1/permissions_service.proto');
        
        const orgService = grpc.loadPackageDefinition(orgPackageDefinition).organisation_service.v1 as any;
        const permService = grpc.loadPackageDefinition(permPackageDefinition).permissions_service.v1 as any;

        // Create clients
        const orgClient: OrganisationServiceClient = new orgService.OrganisationService(
            'api.perms.io:443', 
            grpc.credentials.createSsl()
        );
        
        const permClient: PermissionsServiceClient = new permService.PermissionsService(
            'api.perms.io:443', 
            grpc.credentials.createSsl()
        );

        try {
            // 1. Create organisation
            const org = await new Promise<Organisation>((resolve, reject) => {
                const metadata = new grpc.Metadata();
                metadata.add('authorization', 'Bearer YOUR_TOKEN');
                
                orgClient.CreateOrganisation({
                    name: 'Document Management Co',
                    user_id: 'admin_user'
                }, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    if (!response) {
                        reject(new Error('No response received'));
                        return;
                    }
                    console.log(`Created organisation: ${response.organisation.id}`);
                    resolve(response.organisation);
                });
            });

            // 2. Create project
            const project = await new Promise<Project>((resolve, reject) => {
                const metadata = new grpc.Metadata();
                metadata.add('authorization', 'Bearer YOUR_TOKEN');
                
                orgClient.CreateProject({
                    organisation_id: org.id,
                    name: 'production'
                }, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    if (!response) {
                        reject(new Error('No response received'));
                        return;
                    }
                    console.log(`Created project: ${response.project.name}`);
                    resolve(response.project);
                });
            });

            // 3. Create API key
            const apiKey = await new Promise<APIKey>((resolve, reject) => {
                const metadata = new grpc.Metadata();
                metadata.add('authorization', 'Bearer YOUR_TOKEN');
                
                orgClient.CreateAPIKey({
                    organisation_id: org.id,
                    project_name: 'production',
                    name: 'Application API Key'
                }, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    if (!response) {
                        reject(new Error('No response received'));
                        return;
                    }
                    console.log(`Created API key: ${response.api_key.name}`);
                    resolve(response.api_key);
                });
            });

            // 4. Create permissions
            const permissions = [
                { name: "document.read", description: "Read documents" },
                { name: "document.write", description: "Write documents" },
                { name: "document.delete", description: "Delete documents" }
            ];

            const permIds: string[] = [];

            for (const perm of permissions) {
                const permId = await new Promise<string>((resolve, reject) => {
                    const metadata = new grpc.Metadata();
                    metadata.add('authorization', `Bearer ${apiKey.key}`);
                    
                    permClient.CreatePermission({
                        project_name: 'production',
                        name: perm.name,
                        description: perm.description
                    }, metadata, (error, response) => {
                        if (error) {
                            reject(error);
                            return;
                        }
                        if (!response) {
                            reject(new Error('No response received'));
                            return;
                        }
                        console.log(`Created permission: ${response.name}`);
                        resolve(response.id);
                    });
                });
                permIds.push(permId);
            }

            // 5. Create role
            const role = await new Promise<CreateRoleResponse>((resolve, reject) => {
                const metadata = new grpc.Metadata();
                metadata.add('authorization', `Bearer ${apiKey.key}`);
                
                permClient.CreateRole({
                    project_name: 'production',
                    name: 'document_editor',
                    description: 'Can read and write documents',
                    permissions: permIds.slice(0, 2) // read + write
                }, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    if (!response) {
                        reject(new Error('No response received'));
                        return;
                    }
                    console.log(`Created role: ${response.name}`);
                    resolve(response);
                });
            });

            // 6. Grant permissions
            await new Promise<void>((resolve, reject) => {
                const metadata = new grpc.Metadata();
                metadata.add('authorization', `Bearer ${apiKey.key}`);
                
                permClient.GrantUserPermissionsAndRolesOnResource({
                    project_name: 'production',
                    user_id: 'user_123',
                    resource_uri: '/documents',
                    permissions: [],
                    roles: [role.id]
                }, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    console.log('Granted permissions to user_123');
                    resolve();
                });
            });

            // 7. Check permissions
            const checkResult = await new Promise<CheckPermissionResponse>((resolve, reject) => {
                const metadata = new grpc.Metadata();
                metadata.add('authorization', `Bearer ${apiKey.key}`);
                
                permClient.Check({
                    project_name: 'production',
                    principal_id: 'user_123',
                    resource_uris: ['/documents/doc_456'],
                    permissions: ['document.read']
                }, metadata, (error, response) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    if (!response) {
                        reject(new Error('No response received'));
                        return;
                    }
                    resolve(response);
                });
            });

            if (checkResult.passed) {
                console.log('✅ Permission check passed!');
            } else {
                console.log('❌ Permission check failed');
            }

            console.log('Setup complete! Your RBAC system is ready to use.');

        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Run the example
    main().catch(console.error);
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

=== "Rust"
    ```rust
    // Tenant-specific resources
    let resource_uri = format!("/tenant/{}/projects/{}", tenant_id, project_id);

    // Check tenant access
    let mut request = Request::new(CheckPermissionRequest {
        project_name: "production".to_string(),
        principal_id: user_id,
        resource_uris: vec![resource_uri],
        permissions: vec!["project.read".to_string()],
    });

    let token: MetadataValue<_> = "Bearer YOUR_API_KEY".parse()?;
    request.metadata_mut().insert("authorization", token);

    let check_response = perm_client.check(request).await?;
    ```

=== "Python"
    ```python
    # Tenant-specific resources
    resource_uri = f"/tenant/{tenant_id}/projects/{project_id}"

    # Check tenant access
    request = permissions_service_pb2.CheckPermissionRequest(
        project_name="production",
        principal_id=user_id,
        resource_uris=[resource_uri],
        permissions=["project.read"]
    )

    response = client.Check(request, metadata=metadata)
    ```

=== "Java"
    ```java
    // Tenant-specific resources
    String resourceUri = String.format("/tenant/%s/projects/%s", tenantId, projectId);

    // Check tenant access
    CheckPermissionRequest request = CheckPermissionRequest.newBuilder()
        .setProjectName("production")
        .setPrincipalId(userId)
        .addResourceUris(resourceUri)
        .addPermissions("project.read")
        .build();

    CheckPermissionResponse response = client.check(request);
    ```

=== "TypeScript"
    ```typescript
    // Tenant-specific resources
    const resourceUri = `/tenant/${tenantId}/projects/${projectId}`;

    // Check tenant access
    const request: CheckPermissionRequest = {
        project_name: "production",
        principal_id: userId,
        resource_uris: [resourceUri],
        permissions: ["project.read"]
    };

    const response = await checkPermissions(client, request);
    ```

### Hierarchical Permissions

=== "Go"
    ```go
    // Grant permissions at different levels
    // Organisation level
    grantPermissions(userId, "/organisation/123", []string{"org.admin"})

    // Project level
    grantPermissions(userId, "/organisation/123/project/456", []string{"project.manage"})

    // Resource level
    grantPermissions(userId, "/organisation/123/project/456/document/789", []string{"document.edit"})
    ```

=== "Rust"
    ```rust
    // Grant permissions at different levels
    // Organisation level
    grant_permissions(user_id.clone(), "/organisation/123".to_string(), vec!["org.admin".to_string()]).await?;

    // Project level
    grant_permissions(user_id.clone(), "/organisation/123/project/456".to_string(), vec!["project.manage".to_string()]).await?;

    // Resource level
    grant_permissions(user_id, "/organisation/123/project/456/document/789".to_string(), vec!["document.edit".to_string()]).await?;
    ```

=== "Python"
    ```python
    # Grant permissions at different levels
    # Organisation level
    grant_permissions(user_id, "/organisation/123", ["org.admin"])

    # Project level
    grant_permissions(user_id, "/organisation/123/project/456", ["project.manage"])

    # Resource level
    grant_permissions(user_id, "/organisation/123/project/456/document/789", ["document.edit"])
    ```

=== "Java"
    ```java
    // Grant permissions at different levels
    // Organisation level
    grantPermissions(userId, "/organisation/123", Arrays.asList("org.admin"));

    // Project level
    grantPermissions(userId, "/organisation/123/project/456", Arrays.asList("project.manage"));

    // Resource level
    grantPermissions(userId, "/organisation/123/project/456/document/789", Arrays.asList("document.edit"));
    ```

=== "TypeScript"
    ```typescript
    // Grant permissions at different levels
    // Organisation level
    await grantPermissions(userId, "/organisation/123", ["org.admin"]);

    // Project level
    await grantPermissions(userId, "/organisation/123/project/456", ["project.manage"]);

    // Resource level
    await grantPermissions(userId, "/organisation/123/project/456/document/789", ["document.edit"]);
    ```

### Role-based Teams

=== "Go"
    ```go
    // Create team roles
    teamRoles := []string{"team_lead", "developer", "viewer"}

    // Assign team members
    for _, member := range teamMembers {
        grantPermissions(member.UserId, "/team/123", []string{}, []string{member.Role})
    }
    ```

=== "Rust"
    ```rust
    // Create team roles
    let team_roles = vec!["team_lead", "developer", "viewer"];

    // Assign team members
    for member in team_members {
        grant_permissions_and_roles(
            member.user_id,
            "/team/123".to_string(),
            vec![], // no specific permissions
            vec![member.role]
        ).await?;
    }
    ```

=== "Python"
    ```python
    # Create team roles
    team_roles = ["team_lead", "developer", "viewer"]

    # Assign team members
    for member in team_members:
        grant_permissions_and_roles(
            member.user_id,
            "/team/123",
            [],  # no specific permissions
            [member.role]
        )
    ```

=== "Java"
    ```java
    // Create team roles
    List<String> teamRoles = Arrays.asList("team_lead", "developer", "viewer");

    // Assign team members
    for (TeamMember member : teamMembers) {
        grantPermissionsAndRoles(
            member.getUserId(),
            "/team/123",
            Collections.emptyList(), // no specific permissions
            Arrays.asList(member.getRole())
        );
    }
    ```

=== "TypeScript"
    ```typescript
    // Create team roles
    const teamRoles = ["team_lead", "developer", "viewer"];

    // Assign team members
    for (const member of teamMembers) {
        await grantPermissionsAndRoles(
            member.userId,
            "/team/123",
            [], // no specific permissions
            [member.role]
        );
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