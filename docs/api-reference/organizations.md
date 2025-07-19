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

=== "cURL"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "My Company",
        "user_id": "usr_123"
      }'
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

=== "Rust"
    ```rust
    use tonic::transport::Channel;
    use permio_proto::organisation::v1::{
        organisation_service_client::OrganisationServiceClient,
        CreateOrganisationRequest,
    };

    async fn create_organisation(client: &mut OrganisationServiceClient<Channel>) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(CreateOrganisationRequest {
            name: "My Company".to_string(),
            user_id: "usr_123".to_string(),
        });
        
        let response = client.create_organisation(request).await?;
        println!("Created organisation: {}", response.get_ref().organisation.as_ref().unwrap().id);
        
        Ok(())
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

=== "Java"
    ```java
    import io.grpc.ManagedChannel;
    import io.grpc.ManagedChannelBuilder;
    import permio.organisation.v1.OrganisationServiceGrpc;
    import permio.organisation.v1.Organisation.CreateOrganisationRequest;
    import permio.organisation.v1.Organisation.CreateOrganisationResponse;

    public void createOrganisation() {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        CreateOrganisationRequest request = CreateOrganisationRequest.newBuilder()
                .setName("My Company")
                .setUserId("usr_123")
                .build();
        
        CreateOrganisationResponse response = client.createOrganisation(request);
        System.out.println("Created organisation: " + response.getOrganisation().getId());
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    import * as grpc from '@grpc/grpc-js';
    import * as protoLoader from '@grpc/proto-loader';

    const packageDefinition = protoLoader.loadSync('organisation_service.proto');
    const organisationService = grpc.loadPackageDefinition(packageDefinition).organisation_service.v1 as any;

    const client = new organisationService.OrganisationService('api.perms.io:443', 
        grpc.credentials.createSsl());

    interface CreateOrganisationRequest {
        name: string;
        user_id: string;
    }

    function createOrganisation(): void {
        const request: CreateOrganisationRequest = {
            name: 'My Company',
            user_id: 'usr_123'
        };
        
        client.CreateOrganisation(request, (error: grpc.ServiceError | null, response: any) => {
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

### Update Organization

Updates an organisation's details. Requires `organisation.update` permission.

=== "cURL"
    ```bash
    curl -X PUT "https://api.perms.io/organisation-service/v1/organisation/{id}" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Updated Company Name"
      }'
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

=== "Rust"
    ```rust
    async fn update_organisation(client: &mut OrganisationServiceClient<Channel>, org_id: &str, new_name: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(UpdateOrganisationRequest {
            id: org_id.to_string(),
            name: new_name.to_string(),
        });
        
        let response = client.update_organisation(request).await?;
        println!("Updated organisation: {}", response.get_ref().organisation.as_ref().unwrap().name);
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def update_organisation(org_id: str, new_name: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.UpdateOrganisationRequest(
            id=org_id,
            name=new_name
        )
        
        response = client.UpdateOrganisation(request)
        print(f"Updated organisation: {response.organisation.name}")
    ```

=== "Java"
    ```java
    public void updateOrganisation(String orgId, String newName) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        UpdateOrganisationRequest request = UpdateOrganisationRequest.newBuilder()
                .setId(orgId)
                .setName(newName)
                .build();
        
        UpdateOrganisationResponse response = client.updateOrganisation(request);
        System.out.println("Updated organisation: " + response.getOrganisation().getName());
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface UpdateOrganisationRequest {
        id: string;
        name: string;
    }

    function updateOrganisation(orgId: string, newName: string): void {
        const request: UpdateOrganisationRequest = {
            id: orgId,
            name: newName
        };
        
        client.UpdateOrganisation(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Updated organisation: ${response.organisation.name}`);
        });
    }
    ```

## Project Management

### Create Project

Creates a new project within an organisation. Requires `project.create` permission.

=== "cURL"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/project" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "production",
        "organisation_id": "org_123"
      }'
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

=== "Rust"
    ```rust
    async fn create_project(client: &mut OrganisationServiceClient<Channel>, org_id: &str, project_name: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(CreateProjectRequest {
            organisation_id: org_id.to_string(),
            name: project_name.to_string(),
        });
        
        let response = client.create_project(request).await?;
        println!("Created project: {}", response.get_ref().project.as_ref().unwrap().name);
        
        Ok(())
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

=== "Java"
    ```java
    public void createProject(String orgId, String projectName) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        CreateProjectRequest request = CreateProjectRequest.newBuilder()
                .setOrganisationId(orgId)
                .setName(projectName)
                .build();
        
        CreateProjectResponse response = client.createProject(request);
        System.out.println("Created project: " + response.getProject().getName());
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface CreateProjectRequest {
        organisation_id: string;
        name: string;
    }

    function createProject(orgId: string, projectName: string): void {
        const request: CreateProjectRequest = {
            organisation_id: orgId,
            name: projectName
        };
        
        client.CreateProject(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Created project: ${response.project.name}`);
        });
    }
    ```

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

### Delete Project

Deletes a project from an organisation. Requires `project.delete` permission.

=== "cURL"
    ```bash
    curl -X DELETE "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/project?project_name={project_name}" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

## API Key Management

### Create API Key

Creates a new API key for programmatic access to a specific project.

=== "cURL"
    ```bash
    curl -X POST "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/api-key" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "project_name": "production",
        "name": "CI/CD Pipeline Key"
      }'
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

=== "Rust"
    ```rust
    async fn create_api_key(client: &mut OrganisationServiceClient<Channel>, org_id: &str, project_name: &str, key_name: &str) -> Result<(), Box<dyn std::error::Error>> {
        let request = tonic::Request::new(CreateApiKeyRequest {
            organisation_id: org_id.to_string(),
            project_name: project_name.to_string(),
            name: key_name.to_string(),
        });
        
        let response = client.create_api_key(request).await?;
        println!("Created API key: {}", response.get_ref().api_key.as_ref().unwrap().key);
        // Store this key securely - it won't be shown again
        
        Ok(())
    }
    ```

=== "Python"
    ```python
    def create_api_key(org_id: str, project_name: str, key_name: str):
        channel = grpc.secure_channel('api.perms.io:443', grpc.ssl_channel_credentials())
        client = organisation_service_pb2_grpc.OrganisationServiceStub(channel)
        
        request = organisation_service_pb2.CreateAPIKeyRequest(
            organisation_id=org_id,
            project_name=project_name,
            name=key_name
        )
        
        response = client.CreateAPIKey(request)
        print(f"Created API key: {response.api_key.key}")
        # Store this key securely - it won't be shown again
    ```

=== "Java"
    ```java
    public void createAPIKey(String orgId, String projectName, String keyName) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("api.perms.io", 443)
                .useTransportSecurity()
                .build();
        
        OrganisationServiceGrpc.OrganisationServiceBlockingStub client = 
                OrganisationServiceGrpc.newBlockingStub(channel);
        
        CreateAPIKeyRequest request = CreateAPIKeyRequest.newBuilder()
                .setOrganisationId(orgId)
                .setProjectName(projectName)
                .setName(keyName)
                .build();
        
        CreateAPIKeyResponse response = client.createAPIKey(request);
        System.out.println("Created API key: " + response.getApiKey().getKey());
        // Store this key securely - it won't be shown again
        
        channel.shutdown();
    }
    ```

=== "TypeScript"
    ```typescript
    interface CreateAPIKeyRequest {
        organisation_id: string;
        project_name: string;
        name: string;
    }

    function createAPIKey(orgId: string, projectName: string, keyName: string): void {
        const request: CreateAPIKeyRequest = {
            organisation_id: orgId,
            project_name: projectName,
            name: keyName
        };
        
        client.CreateAPIKey(request, (error: grpc.ServiceError | null, response: any) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`Created API key: ${response.api_key.key}`);
            // Store this key securely - it won't be shown again
        });
    }
    ```

### List API Keys

Lists all API keys for a project. Requires `apiKeys.list` permission.

=== "cURL"
    ```bash
    curl -X GET "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/api-key?project_name={project_name}" \
      -H "Authorization: Bearer YOUR_TOKEN"
    ```

### Invalidate API Key

Invalidates an API key, making it unusable for future requests.

=== "cURL"
    ```bash
    curl -X DELETE "https://api.perms.io/organisation-service/v1/organisation/{organisation_id}/api-key/{id}?project_name={project_name}" \
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