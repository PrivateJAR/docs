# Organisation Service API

The Organisation Service manages organizations, projects, and API keys within Permio. Use these endpoints to handle organization-level operations and project management.

## Organization Operations

### Create an Organization

Create a new organization.

#### gRPC (Go)

```go
response, err := client.Organisation.CreateOrganisation(context.Background(), &pb.CreateOrganisationRequest{
    Name:   "Acme Inc.",
    UserId: "user_1234567890",
})
if err != nil {
    log.Fatalf("Failed to create organization: %v", err)
}
log.Printf("Created organization: %v with ID: %v", response.Organisation.Name, response.Organisation.Id)
```

#### REST API

```bash
curl -X POST https://api.perms.io/v1/organisations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Inc.",
    "user_id": "user_1234567890"
  }'
```

### Get an Organization

Retrieve an organization by its ID.

#### gRPC (Go)

```go
response, err := client.Organisation.GetOrganisation(context.Background(), &pb.GetOrganisationRequest{
    Id: "org_1234567890",
})
if err != nil {
    log.Fatalf("Failed to get organization: %v", err)
}
log.Printf("Retrieved organization: %v", response.Organisation.Name)
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/organisations/org_1234567890 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Update an Organization

Update an existing organization's name.

#### gRPC (Go)

```go
response, err := client.Organisation.UpdateOrganisation(context.Background(), &pb.UpdateOrganisationRequest{
    Id:   "org_1234567890",
    Name: "Acme Corporation",
})
if err != nil {
    log.Fatalf("Failed to update organization: %v", err)
}
log.Printf("Updated organization: %v", response.Organisation.Name)
```

#### REST API

```bash
curl -X PATCH https://api.perms.io/v1/organisations/org_1234567890 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation"
  }'
```

### Get User's Organization

Retrieve the organization a user belongs to.

#### gRPC (Go)

```go
response, err := client.Organisation.GetUsersOrganisation(context.Background(), &pb.GetUsersOrganisationRequest{
    UserId: "user_1234567890",
})
if err != nil {
    log.Fatalf("Failed to get user's organization: %v", err)
}
log.Printf("User's organization: %v", response.Organisation.Name)
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/users/user_1234567890/organisation \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Invite User to Organization

Invite a user to join an organization.

#### gRPC (Go)

```go
_, err = client.Organisation.InviteUserToOrganisation(context.Background(), &pb.InviteUserToOrganisationRequest{
    OrganisationId: "org_1234567890",
    Email:          "newuser@example.com",
})
if err != nil {
    log.Fatalf("Failed to invite user: %v", err)
}
log.Println("User invitation sent successfully")
```

#### REST API

```bash
curl -X POST https://api.perms.io/v1/organisations/org_1234567890/invitations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com"
  }'
```

## Project Operations

### Create a Project

Create a new project within an organization.

#### gRPC (Go)

```go
response, err := client.Organisation.CreateProject(context.Background(), &pb.CreateProjectRequest{
    OrganisationId: "org_1234567890",
    Name:           "mobile-app",
})
if err != nil {
    log.Fatalf("Failed to create project: %v", err)
}
log.Printf("Created project: %v for organization: %v", 
    response.Project.Name, response.Project.OrganisationId)
```

#### REST API

```bash
curl -X POST https://api.perms.io/v1/organisations/org_1234567890/projects \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "mobile-app"
  }'
```

### Get a Project

Retrieve a project by its name.

#### gRPC (Go)

```go
response, err := client.Organisation.GetProject(context.Background(), &pb.GetProjectRequest{
    OrganisationId: "org_1234567890",
    ProjectName:    "mobile-app",
})
if err != nil {
    log.Fatalf("Failed to get project: %v", err)
}
log.Printf("Retrieved project: %v", response.Project.Name)
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/organisations/org_1234567890/projects/mobile-app \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Get Projects for Organization

List all projects within an organization.

#### gRPC (Go)

```go
response, err := client.Organisation.GetProjectsForOrganisation(context.Background(), &pb.GetProjectsForOrganisationRequest{
    OrganisationId: "org_1234567890",
})
if err != nil {
    log.Fatalf("Failed to get projects: %v", err)
}

for _, project := range response.Projects {
    log.Printf("Project: %v, Created: %v", project.Name, project.CreatedAt.AsTime())
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/organisations/org_1234567890/projects \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Delete a Project

Delete a project from an organization.

#### gRPC (Go)

```go
_, err := client.Organisation.DeleteProject(context.Background(), &pb.DeleteProjectRequest{
    OrganisationId: "org_1234567890",
    ProjectName:    "mobile-app",
})
if err != nil {
    log.Fatalf("Failed to delete project: %v", err)
}
log.Println("Project deleted successfully")
```

#### REST API

```bash
curl -X DELETE https://api.perms.io/v1/organisations/org_1234567890/projects/mobile-app \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## API Key Operations

### Create an API Key

Create a new API key for accessing the Permio API programmatically.

#### gRPC (Go)

```go
response, err := client.Organisation.CreateAPIKey(context.Background(), &pb.CreateAPIKeyRequest{
    OrganisationId: "org_1234567890",
    ProjectName:    "default",
    Name:           "Production Service Key",
})
if err != nil {
    log.Fatalf("Failed to create API key: %v", err)
}
log.Printf("Created API key: %v", response.ApiKey.Key)
log.Printf("Make sure to save this key; it won't be displayed again: %v", response.ApiKey.Key)
```

#### REST API

```bash
curl -X POST https://api.perms.io/v1/organisations/org_1234567890/apikeys \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "default",
    "name": "Production Service Key"
  }'
```

### List API Keys

List all API keys for an organization and project.

#### gRPC (Go)

```go
response, err := client.Organisation.ListAPIKeys(context.Background(), &pb.ListAPIKeysRequest{
    OrganisationId: "org_1234567890",
    ProjectName:    "default",
})
if err != nil {
    log.Fatalf("Failed to list API keys: %v", err)
}

for _, apiKey := range response.ApiKeys {
    log.Printf("API Key: %v, Created: %v", apiKey.Name, apiKey.CreatedAt.AsTime())
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/organisations/org_1234567890/apikeys?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Invalidate an API Key

Invalidate (revoke) an existing API key.

#### gRPC (Go)

```go
_, err := client.Organisation.InvalidateAPIKey(context.Background(), &pb.InvalidateAPIKeyRequest{
    OrganisationId: "org_1234567890",
    ProjectName:    "default",
    Id:             "apikey_1234567890",
})
if err != nil {
    log.Fatalf("Failed to invalidate API key: %v", err)
}
log.Println("API key invalidated successfully")
```

#### REST API

```bash
curl -X DELETE https://api.perms.io/v1/organisations/org_1234567890/apikeys/apikey_1234567890?project_name=default \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Billing Operations

### Get Customer Billing Session

Get a session for managing billing settings.

#### gRPC (Go)

```go
response, err := client.Organisation.GetCustomerBillingSession(context.Background(), &pb.GetCustomerBillingSessionRequest{
    OrganisationId: "org_1234567890",
})
if err != nil {
    log.Fatalf("Failed to get billing session: %v", err)
}
log.Printf("Billing session secret: %v", response.SessionSecret)
```

#### REST API

```bash
curl -X POST https://api.perms.io/v1/organisations/org_1234567890/billing/sessions \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Get Customer Active Subscription

Get information about the current active subscription.

#### gRPC (Go)

```go
response, err := client.Organisation.GetCustomerActiveSubscription(context.Background(), &pb.GetCustomerActiveSubscriptionRequest{
    OrganisationId: "org_1234567890",
})
if err != nil {
    log.Fatalf("Failed to get active subscription: %v", err)
}

if response.ActiveSubscriptionId != "" {
    log.Printf("Active subscription: %v with price: %v", 
        response.ActiveSubscriptionId, response.ActivePriceId)
} else {
    log.Println("No active subscription found")
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/organisations/org_1234567890/billing/subscription \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Activate Billing Subscription

Activate a billing subscription with a specific price.

#### gRPC (Go)

```go
_, err := client.Organisation.ActivateBillingSubscription(context.Background(), &pb.ActivateBillingSubscriptionRequest{
    OrganisationId: "org_1234567890",
    PriceId:        "price_1234567890",
})
if err != nil {
    log.Fatalf("Failed to activate subscription: %v", err)
}
log.Println("Subscription activated successfully")
```

#### REST API

```bash
curl -X POST https://api.perms.io/v1/organisations/org_1234567890/billing/subscriptions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "price_id": "price_1234567890"
  }'
```

### Check Organization Grant Permission

Check if an organization is permitted to grant permissions (based on plan limits).

#### gRPC (Go)

```go
response, err := client.Organisation.IsOrganisationPermittedToGrant(context.Background(), &pb.IsOrganisationPermittedToGrantRequest{
    OrganisationId: "org_1234567890",
})
if err != nil {
    log.Fatalf("Failed to check grant permission: %v", err)
}

if response.Permitted {
    log.Println("Organization is permitted to grant permissions")
} else {
    log.Println("Organization has reached its permission grant limit")
}
```

#### REST API

```bash
curl -X GET https://api.perms.io/v1/organisations/org_1234567890/grant-permission-check \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Join Mailing List

Add an email address to the product mailing list.

#### gRPC (Go)

```go
_, err := client.Organisation.AddEmailToMailingList(context.Background(), &pb.AddEmailToMailingListRequest{
    Email: "user@example.com",
})
if err != nil {
    log.Fatalf("Failed to add email to mailing list: %v", err)
}
log.Println("Email added to mailing list successfully")
```

#### REST API

```bash
curl -X POST https://api.perms.io/v1/mailing-list \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com"
  }'
```
