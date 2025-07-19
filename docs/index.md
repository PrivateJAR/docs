<div style="text-align: center;">
    <img src="./assets/transparentLogoSquare.png" alt="My Image" width="400" height="400">
</div>

Permio is a **Resource-Specific Role-Based Access Control (RBAC)** system designed for modern applications that require **fine-grained and scalable permission management**. With an **API-First approach**, **authentication-agnostic design**, and a built-in **UI Dashboard**, Permio empowers developers and admins to define and enforce permissions at the most granular level.

Manage your organization visually via the dashboard at [app.perms.io](https://app.perms.io) or programmatically via the API.

---

## 🔧 Key Features

### ✅ Resource-Level RBAC
Permio enables access control at the *individual object level*. You can define access rules for *specific instances* of data (e.g., /project/42, /user/1234), enabling secure and flexible permissioning for complex apps.

### 🏗️ Hierarchical Inheritance
Define roles and permissions at higher levels (e.g., /user) and let them *automatically propagate* to nested resources (e.g., /user/1234, /user/1234/documents/5678).

### 🔌 API-First Design
- **REST API** for web applications
- **gRPC API** for backend services
- **Authentication-agnostic** - works with any auth provider
- **gRPC clients** for Go, Rust, Python, Java, TypeScript

---

## 🚀 Quick Start

Ready to get started? Follow our comprehensive guide:

**[📖 Quick Start Guide →](./quickstart.md)**

Learn the fundamentals of access control:

**[🔐 IAM Basics →](./iam-basics.md)**

Understand how Permio works:

**[⚙️ How It Works →](./how-it-works.md)**

---

## 📚 Documentation

### Core Concepts
- **[How It Works](./how-it-works.md)** - Understanding resource-specific RBAC
- **[IAM Basics](./iam-basics.md)** - Identity and access management fundamentals

### API Reference
- **[Organizations & Projects](./api-reference/organizations.md)** - Manage your organization structure
- **[Permissions](./api-reference/permissions.md)** - Create and manage permissions
- **[Pagination](./api-reference/pagination.md)** - Handle large result sets efficiently

### Integration Examples
- **Multi-tenant Applications** - Isolate tenant data securely
- **Document Management Systems** - File-level access control
- **Project-based Access** - Team and environment permissions

---

## 💬 Support

Need help getting started or have questions?

- **📧 Email**: [support@perms.io](mailto:support@perms.io)
- **💬 Discord**: [Join our community](https://discord.gg/permio)
- **📖 Documentation**: Browse these docs for detailed guides
- **🐛 Issues**: [Report bugs or request features](https://github.com/permio/permio/issues)
