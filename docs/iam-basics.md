# IAM Basics

Identity and Access Management (IAM) is a fundamental security framework that controls **who** can access **what** resources in your application and **what actions** they can perform. Understanding IAM concepts is crucial for implementing secure, scalable access control systems.

## What is IAM?

IAM encompasses two core security functions:

### Authentication
**"Who are you?"** - Verifying the identity of users, services, or systems
- Login credentials (username/password)
- Multi-factor authentication (MFA)
- OAuth providers (Google, GitHub, etc.)
- API keys and tokens
- Biometric verification

### Authorization
**"What can you do?"** - Determining what authenticated entities are allowed to access
- Permission checking
- Access control policies
- Resource-level restrictions
- Role-based access control (RBAC)

## Core IAM Components

### 1. Identity (Principal)

An **identity** (also called a **principal**) represents an entity that can be authenticated and granted permissions. Identities include:

#### Users
Real people with accounts in your system:
```json
{
  "id": "user_12345",
  "email": "alice@company.com",
  "name": "Alice Johnson",
  "type": "user"
}
```

#### Service Accounts
Applications or automated systems:
```json
{
  "id": "service_backup_system",
  "name": "Backup Service",
  "type": "service_account"
}
```

#### API Keys
Programmatic access tokens:
```json
{
  "id": "api_key_67890",
  "name": "Mobile App API Key",
  "type": "api_key"
}
```

#### Groups/Teams
Collections of users:
```json
{
  "id": "group_engineering",
  "name": "Engineering Team",
  "members": ["user_12345", "user_67890"],
  "type": "group"
}
```

### 2. Resources

**Resources** are the objects, data, or services you want to protect. Everything that requires access control is a resource.

#### Physical Resources
- Servers and infrastructure
- Database instances
- Storage systems
- Network devices

#### Digital Resources
- Files and documents
- Database records
- API endpoints
- Applications and services

#### Logical Resources
- Projects and workspaces
- Organizations and teams
- Workflows and processes
- Configurations and settings

#### Resource Identification

Resources are identified using **Resource URIs** - hierarchical identifiers that uniquely specify each resource:

```
/organization/acme
├── /organization/acme/project/web-app
│   ├── /organization/acme/project/web-app/environment/production
│   ├── /organization/acme/project/web-app/environment/staging
│   └── /organization/acme/project/web-app/database/users
├── /organization/acme/project/mobile-app
│   ├── /organization/acme/project/mobile-app/api/v1
│   └── /organization/acme/project/mobile-app/api/v2
└── /organization/acme/billing
    ├── /organization/acme/billing/invoices
    └── /organization/acme/billing/payments
```

### 3. Permissions

**Permissions** define specific actions that can be performed on resources. They represent the most granular level of access control.

#### Action-Based Permissions
```
document.read      - View document content
document.write     - Create or modify documents
document.delete    - Remove documents
document.share     - Share documents with others
```

#### CRUD Operations
```
create    - Add new resources
read      - View existing resources
update    - Modify existing resources
delete    - Remove resources
```

#### Administrative Permissions
```
admin.users.create    - Create new user accounts
admin.users.suspend   - Suspend user accounts
admin.billing.view    - View billing information
admin.logs.access     - Access system logs
```

#### Domain-Specific Permissions
```
deploy.staging      - Deploy to staging environment
deploy.production   - Deploy to production environment
database.backup     - Create database backups
support.tickets     - Access support tickets
```

### 4. Roles

**Roles** are collections of permissions that can be assigned as a group. They simplify access management by grouping related permissions together.

#### Predefined Roles

**Viewer Role**
```json
{
  "name": "viewer",
  "description": "Read-only access to resources",
  "permissions": [
    "read",
    "list",
    "view"
  ]
}
```

**Editor Role**
```json
{
  "name": "editor", 
  "description": "Can view and modify resources",
  "permissions": [
    "read",
    "write", 
    "update",
    "create"
  ]
}
```

**Admin Role**
```json
{
  "name": "admin",
  "description": "Full control over resources",
  "permissions": [
    "read",
    "write",
    "update", 
    "create",
    "delete",
    "manage",
    "configure"
  ]
}
```

#### Custom Roles

Create roles specific to your application's needs:

**Content Manager**
```json
{
  "name": "content_manager",
  "description": "Manages content creation and publication",
  "permissions": [
    "content.create",
    "content.edit",
    "content.publish",
    "content.review",
    "media.upload"
  ]
}
```

**DevOps Engineer**
```json
{
  "name": "devops_engineer",
  "description": "Manages infrastructure and deployments",
  "permissions": [
    "deploy.staging",
    "deploy.production",
    "infrastructure.configure",
    "monitoring.access",
    "logs.view"
  ]
}
```

### 5. Policies

**Policies** define the rules that govern access control. They specify which principals can perform which actions on which resources under what conditions.

#### Basic Policy Structure
```json
{
  "principal": "user_alice",
  "resource": "/project/web-app/database/users",
  "permissions": ["read", "write"],
  "effect": "allow"
}
```

#### Conditional Policies
```json
{
  "principal": "group_developers",
  "resource": "/project/*/environment/staging",
  "permissions": ["deploy"],
  "effect": "allow",
  "conditions": {
    "time_of_day": "09:00-17:00",
    "source_ip": "10.0.0.0/8"
  }
}
```

#### Deny Policies
```json
{
  "principal": "*",
  "resource": "/organization/acme/billing/*",
  "permissions": ["*"],
  "effect": "deny",
  "conditions": {
    "user_role": "contractor"
  }
}
```

## IAM Models

### 1. Discretionary Access Control (DAC)

Resource owners control access to their resources:

- **User-controlled**: Individual users set permissions
- **Flexible**: Easy to share and delegate access
- **Scalability issues**: Difficult to manage at scale
- **Security risks**: Users may grant excessive permissions

**Example**: File system permissions where file owners can set read/write permissions for other users.

### 2. Mandatory Access Control (MAC)

System-wide policies control access:

- **Centrally controlled**: Administrators set all permissions
- **Security focused**: Strong security guarantees
- **Inflexible**: Difficult to adapt to changing needs
- **Complex**: Requires detailed security classifications

**Example**: Military security systems with Top Secret, Secret, and Confidential classifications.

### 3. Role-Based Access Control (RBAC)

Access based on user roles within the organization:

- **Role-centric**: Permissions assigned to roles, not individuals
- **Scalable**: Easy to manage large numbers of users
- **Organizational alignment**: Reflects real-world job functions
- **Standard approach**: Widely adopted in business applications

#### RBAC Components
```
Users ──→ Roles ──→ Permissions ──→ Objects/Resources
  │                                          
  └─────→ Sessions ──→ Roles
```

**Users** → assigned to → **Roles** → granted → **Permissions** → on → **Resources**

#### RBAC Example
```
Alice (User) → Editor Role → [read, write, publish] → /blog/posts/*
Bob (User) → Viewer Role → [read] → /blog/posts/*
Carol (User) → Admin Role → [read, write, delete, manage] → /blog/*
```

### 4. Attribute-Based Access Control (ABAC)

Dynamic access based on attributes:

- **Context-aware**: Considers user, resource, and environmental attributes
- **Fine-grained**: Very precise access control
- **Complex**: Requires sophisticated policy engines
- **Flexible**: Adapts to complex business rules

#### ABAC Example
```json
{
  "policy": "Allow access if user is manager AND resource is in their department AND current time is business hours",
  "user_attributes": {
    "role": "manager",
    "department": "engineering",
    "clearance_level": "3"
  },
  "resource_attributes": {
    "department": "engineering", 
    "classification": "internal",
    "data_type": "source_code"
  },
  "environment_attributes": {
    "time": "14:30",
    "day_of_week": "Tuesday",
    "location": "office_network"
  }
}
```

## Permission Inheritance and Hierarchies

### Hierarchical Resources

Resources often exist in hierarchical relationships where permissions granted at higher levels automatically apply to lower levels:

```
/organization/acme                 ← Admin permissions here
├── /organization/acme/project/web ← apply to all projects
│   ├── /environment/staging       ← and all environments
│   └── /environment/production    ← within those projects
└── /organization/acme/project/api
    ├── /environment/staging
    └── /environment/production
```

### Inheritance Rules

1. **Explicit permissions** override inherited permissions
2. **Deny permissions** override allow permissions
3. **More specific** permissions override general permissions
4. **Closest parent** permissions take precedence

### Inheritance Example

Given these permission assignments:
```json
[
  {
    "principal": "alice",
    "resource": "/organization/acme",
    "permissions": ["read"]
  },
  {
    "principal": "alice", 
    "resource": "/organization/acme/project/web",
    "permissions": ["write"]
  },
  {
    "principal": "alice",
    "resource": "/organization/acme/project/web/environment/production", 
    "permissions": ["deny:write"]
  }
]
```

Alice's effective permissions:
- `/organization/acme/*`: **read** (inherited)
- `/organization/acme/project/web/*`: **read + write** (inherited + explicit)
- `/organization/acme/project/web/environment/production`: **read only** (deny overrides write)

## Best Practices

### 1. Principle of Least Privilege

Grant the minimum permissions necessary for users to perform their job functions:

```json
// Good: Specific permissions
{
  "role": "content_editor",
  "permissions": [
    "articles.create",
    "articles.edit", 
    "articles.publish",
    "media.upload"
  ]
}

// Avoid: Overly broad permissions
{
  "role": "content_editor", 
  "permissions": [
    "admin.*",
    "system.*"
  ]
}
```

### 2. Role-Based Organization

Design roles that mirror your organization structure:

```json
{
  "engineering_roles": [
    "software_engineer",
    "senior_engineer", 
    "engineering_manager",
    "principal_engineer"
  ],
  "product_roles": [
    "product_manager",
    "product_owner",
    "product_analyst"
  ],
  "operations_roles": [
    "devops_engineer",
    "site_reliability_engineer",
    "system_administrator"
  ]
}
```

### 3. Resource Hierarchy Design

Create logical resource hierarchies that support inheritance:

```bash
# Good: Logical hierarchy
/company/departments/engineering/teams/platform/projects/auth-service

# Avoid: Flat structure
/auth-service-engineering-platform-team
```

### 4. Regular Access Reviews

Implement periodic reviews of permissions:

- **Quarterly access reviews**: Review all role assignments
- **Project completion**: Remove project-specific access
- **Role changes**: Update permissions when people change roles
- **Offboarding**: Immediately revoke all access when people leave

### 5. Audit and Logging

Track all access control decisions:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "principal": "alice@company.com",
  "resource": "/project/web-app/database/users",
  "action": "read",
  "result": "allowed",
  "reason": "role:database_reader"
}
```

### 6. Separation of Duties

Prevent conflicts of interest by separating incompatible functions:

```json
// Finance roles - separate creation from approval
{
  "expense_creator": ["expense.create", "expense.submit"],
  "expense_approver": ["expense.approve", "expense.reject"],
  "expense_payer": ["payment.create", "payment.execute"]
}

// Development roles - separate development from production  
{
  "developer": ["code.write", "deploy.staging"],
  "release_manager": ["deploy.production", "rollback.production"]
}
```

## Common IAM Challenges

### 1. Permission Sprawl

**Problem**: Too many fine-grained permissions become unmanageable

**Solution**: 
- Group related permissions into logical roles
- Use permission hierarchies (e.g., `document.*` includes `document.read`, `document.write`)
- Regular permission audits and cleanup

### 2. Role Explosion

**Problem**: Creating too many specific roles

**Solution**:
- Use composable permissions instead of many roles
- Implement role hierarchies (e.g., Senior Engineer inherits Engineer permissions)
- Focus on job functions, not individuals

### 3. Orphaned Permissions

**Problem**: Permissions granted to users who no longer need them

**Solution**:
- Automated access reviews
- Time-limited permissions for temporary access
- Integration with HR systems for role changes

### 4. Privilege Escalation

**Problem**: Users gaining more permissions than intended

**Solution**:
- Explicit deny policies for sensitive resources
- Regular audit of permission inheritance
- Principle of least privilege enforcement

### 5. Cross-System Consistency

**Problem**: Inconsistent permissions across multiple systems

**Solution**:
- Centralized IAM system
- Single source of truth for user roles
- Automated permission synchronization

## Implementation Patterns

### 1. Multi-Tenant Applications

Isolate tenants using hierarchical resource URIs:

```bash
/tenant/company-a/projects/web-app
/tenant/company-a/users/alice
/tenant/company-b/projects/mobile-app  
/tenant/company-b/users/bob
```

### 2. Microservices Architecture

Each service validates permissions independently:

```go
// In each microservice
func authMiddleware(requiredPermission string) gin.HandlerFunc {
    return func(c *gin.Context) {
        userID := getUserFromToken(c.GetHeader("Authorization"))
        resourceURI := getResourceURI(c.Request.URL.Path)
        
        if !checkPermission(userID, resourceURI, requiredPermission) {
            c.JSON(403, gin.H{"error": "Access denied"})
            c.Abort()
            return
        }
        
        c.Next()
    }
}
```

### 3. API Gateway Integration

Centralize permission checking at the gateway level:

```yaml
# API Gateway configuration
routes:
  - path: /api/documents/*
    backend: document-service
    auth:
      required_permission: document.read
      resource_template: "/documents/{id}"
      
  - path: /api/admin/*
    backend: admin-service  
    auth:
      required_role: admin
      resource_template: "/admin/*"
```

## Getting Started with IAM

### 1. Assessment Phase

- **Identify resources**: List all systems, data, and services requiring protection
- **Map user roles**: Document existing job functions and responsibilities  
- **Define permissions**: Catalog all actions users perform on resources
- **Assess current state**: Evaluate existing access controls and gaps

### 2. Design Phase

- **Design resource hierarchy**: Create logical URI structure
- **Define permission model**: Choose between RBAC, ABAC, or hybrid approach
- **Create role taxonomy**: Design roles that match your organization
- **Plan inheritance strategy**: Determine how permissions will cascade

### 3. Implementation Phase

- **Choose IAM platform**: Select tool that meets your requirements (like Permio)
- **Configure resources**: Set up resource hierarchy and permissions
- **Create roles and policies**: Implement your permission model
- **Integrate applications**: Add permission checks to your systems

### 4. Operation Phase

- **Monitor access patterns**: Track permission usage and violations
- **Regular reviews**: Periodically audit roles and permissions
- **Update as needed**: Adapt permissions as your organization evolves
- **Train users**: Educate teams on IAM best practices

## Conclusion

Effective IAM is critical for application security and requires careful planning and implementation. Key takeaways:

- **Start simple**: Begin with basic RBAC and expand as needed
- **Think hierarchically**: Design resource structures that support inheritance
- **Follow best practices**: Implement least privilege, separation of duties, and regular reviews
- **Monitor continuously**: Track access patterns and audit permissions regularly
- **Choose the right tools**: Select IAM solutions that fit your architecture and scale

Ready to implement robust access control? Permio provides a modern, scalable IAM platform that simplifies permission management while providing enterprise-grade security. Check out our [Quick Start Guide](./quickstart.md) to begin implementing fine-grained access control in your applications.