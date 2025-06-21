# Getting Started

Welcome to Permio, an API-First Identity and Access Management (IAM) platform designed for modern applications.

This guide assumes some base level knowledge of IAM, if you are new to IAM, please read the documentation on IAM basics [here](https://docs.perms.io/iam-basics).

# Creating an Account

## 1. Sign In
Go to [app.perms.io](https://app.perms.io) and log in.

## 2. Create Your Organization
When you first login to your account you will be prompted to create an organisation. The only requirement for an organisation at this stage is a name.

When an organisation is created it will also create a default *project*, but you can create a new one or switch to an alternative in the dashboard in the top left of the screen.

## 3. Define Permissions & Roles
=== "GO"

    ```go
    package main

    func main() {
        apiKeyTokenSource := authentication.NewAPIKeyTokenSource(<YOUR_API_KEY>)
        grpcConn, err := grpc.NewClient('api.perms.io',
            grpc.WithTransportCredentials(credentials.NewTLS(nil)),
            grpc.WithPerRPCCredentials(apiKeyTokenSource),
        )
        if err != nil {
            // TODO: Handle Error
        }
        permissionsServiceClient := permissionsPB.NewPermissionsServiceClient(grpcConn)
    }
    ```
=== "UI"
    Navigate to the Permissions page from the burger menu. Click the `Create New Permission` button. New permissions require a name and a description, we recommend using dot notation for the name as it doubles as the id of the permission, for example `customer.info.view`.

    Once created the permission should be visible in the table.

## 4. Assign Roles
Attach users or API keys to roles on specific resources.

## 5. Perform Permission Checks
Use the /check endpoint to authorize requests in your backend.
