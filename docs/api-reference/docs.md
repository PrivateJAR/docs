# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [google/api/http.proto](#google_api_http-proto)
    - [CustomHttpPattern](#google-api-CustomHttpPattern)
    - [Http](#google-api-Http)
    - [HttpRule](#google-api-HttpRule)
  
- [google/api/annotations.proto](#google_api_annotations-proto)
    - [File-level Extensions](#google_api_annotations-proto-extensions)
  
- [validate/validate.proto](#validate_validate-proto)
    - [AnyRules](#validate-AnyRules)
    - [BoolRules](#validate-BoolRules)
    - [BytesRules](#validate-BytesRules)
    - [DoubleRules](#validate-DoubleRules)
    - [DurationRules](#validate-DurationRules)
    - [EnumRules](#validate-EnumRules)
    - [FieldRules](#validate-FieldRules)
    - [Fixed32Rules](#validate-Fixed32Rules)
    - [Fixed64Rules](#validate-Fixed64Rules)
    - [FloatRules](#validate-FloatRules)
    - [Int32Rules](#validate-Int32Rules)
    - [Int64Rules](#validate-Int64Rules)
    - [MapRules](#validate-MapRules)
    - [MessageRules](#validate-MessageRules)
    - [RepeatedRules](#validate-RepeatedRules)
    - [SFixed32Rules](#validate-SFixed32Rules)
    - [SFixed64Rules](#validate-SFixed64Rules)
    - [SInt32Rules](#validate-SInt32Rules)
    - [SInt64Rules](#validate-SInt64Rules)
    - [StringRules](#validate-StringRules)
    - [TimestampRules](#validate-TimestampRules)
    - [UInt32Rules](#validate-UInt32Rules)
    - [UInt64Rules](#validate-UInt64Rules)
  
    - [KnownRegex](#validate-KnownRegex)
  
    - [File-level Extensions](#validate_validate-proto-extensions)
    - [File-level Extensions](#validate_validate-proto-extensions)
    - [File-level Extensions](#validate_validate-proto-extensions)
    - [File-level Extensions](#validate_validate-proto-extensions)
  
- [v1/organisation_service.proto](#v1_organisation_service-proto)
    - [APIKey](#organisation_service-v1-APIKey)
    - [ActivateBillingSubscriptionRequest](#organisation_service-v1-ActivateBillingSubscriptionRequest)
    - [AddEmailToMailingListRequest](#organisation_service-v1-AddEmailToMailingListRequest)
    - [BillingCustomer](#organisation_service-v1-BillingCustomer)
    - [CreateAPIKeyRequest](#organisation_service-v1-CreateAPIKeyRequest)
    - [CreateAPIKeyResponse](#organisation_service-v1-CreateAPIKeyResponse)
    - [CreateOrganisationRequest](#organisation_service-v1-CreateOrganisationRequest)
    - [CreateOrganisationResponse](#organisation_service-v1-CreateOrganisationResponse)
    - [CreateProjectRequest](#organisation_service-v1-CreateProjectRequest)
    - [CreateProjectResponse](#organisation_service-v1-CreateProjectResponse)
    - [DeleteProjectRequest](#organisation_service-v1-DeleteProjectRequest)
    - [GetCustomerActiveSubscriptionRequest](#organisation_service-v1-GetCustomerActiveSubscriptionRequest)
    - [GetCustomerActiveSubscriptionResponse](#organisation_service-v1-GetCustomerActiveSubscriptionResponse)
    - [GetCustomerBillingSessionRequest](#organisation_service-v1-GetCustomerBillingSessionRequest)
    - [GetCustomerBillingSessionResponse](#organisation_service-v1-GetCustomerBillingSessionResponse)
    - [GetCustomerDefaultPaymentMethodAndIntentRequest](#organisation_service-v1-GetCustomerDefaultPaymentMethodAndIntentRequest)
    - [GetCustomerDefaultPaymentMethodAndIntentResponse](#organisation_service-v1-GetCustomerDefaultPaymentMethodAndIntentResponse)
    - [GetOrganisationRequest](#organisation_service-v1-GetOrganisationRequest)
    - [GetOrganisationResponse](#organisation_service-v1-GetOrganisationResponse)
    - [GetProjectRequest](#organisation_service-v1-GetProjectRequest)
    - [GetProjectResponse](#organisation_service-v1-GetProjectResponse)
    - [GetProjectsForOrganisationRequest](#organisation_service-v1-GetProjectsForOrganisationRequest)
    - [GetProjectsForOrganisationResponse](#organisation_service-v1-GetProjectsForOrganisationResponse)
    - [GetUsersOrganisationRequest](#organisation_service-v1-GetUsersOrganisationRequest)
    - [InvalidateAPIKeyRequest](#organisation_service-v1-InvalidateAPIKeyRequest)
    - [InviteUserToOrganisationRequest](#organisation_service-v1-InviteUserToOrganisationRequest)
    - [IsOrganisationPermittedToGrantRequest](#organisation_service-v1-IsOrganisationPermittedToGrantRequest)
    - [IsOrganisationPermittedToGrantResponse](#organisation_service-v1-IsOrganisationPermittedToGrantResponse)
    - [ListAPIKeysRequest](#organisation_service-v1-ListAPIKeysRequest)
    - [ListAPIKeysResponse](#organisation_service-v1-ListAPIKeysResponse)
    - [Organisation](#organisation_service-v1-Organisation)
    - [Project](#organisation_service-v1-Project)
    - [SetUsersOrganisationRequest](#organisation_service-v1-SetUsersOrganisationRequest)
    - [UpdateOrganisationRequest](#organisation_service-v1-UpdateOrganisationRequest)
    - [UpdateOrganisationResponse](#organisation_service-v1-UpdateOrganisationResponse)
    - [User](#organisation_service-v1-User)
  
    - [OrganisationService](#organisation_service-v1-OrganisationService)
  
- [v1/permissions_service.proto](#v1_permissions_service-proto)
    - [Assignment](#permissions_service-v1-Assignment)
    - [CheckPermissionRequest](#permissions_service-v1-CheckPermissionRequest)
    - [CheckPermissionResponse](#permissions_service-v1-CheckPermissionResponse)
    - [CreatePermissionRequest](#permissions_service-v1-CreatePermissionRequest)
    - [CreateRoleRequest](#permissions_service-v1-CreateRoleRequest)
    - [DeletePermissionRequest](#permissions_service-v1-DeletePermissionRequest)
    - [DeleteRoleRequest](#permissions_service-v1-DeleteRoleRequest)
    - [GetAllAssignmentsForPrincipalRequest](#permissions_service-v1-GetAllAssignmentsForPrincipalRequest)
    - [GetAllAssignmentsForPrincipalResponse](#permissions_service-v1-GetAllAssignmentsForPrincipalResponse)
    - [GetPermissionRequest](#permissions_service-v1-GetPermissionRequest)
    - [GetRoleRequest](#permissions_service-v1-GetRoleRequest)
    - [GetUserPermissionsAndRolesOnResourceRequest](#permissions_service-v1-GetUserPermissionsAndRolesOnResourceRequest)
    - [GetUserPermissionsAndRolesOnResourceResponse](#permissions_service-v1-GetUserPermissionsAndRolesOnResourceResponse)
    - [GrantUserPermissionsAndRolesOnResourceRequest](#permissions_service-v1-GrantUserPermissionsAndRolesOnResourceRequest)
    - [InheritedPermission](#permissions_service-v1-InheritedPermission)
    - [InheritedRole](#permissions_service-v1-InheritedRole)
    - [ListPermissionsRequest](#permissions_service-v1-ListPermissionsRequest)
    - [ListPermissionsResponse](#permissions_service-v1-ListPermissionsResponse)
    - [ListPrincipalsRequest](#permissions_service-v1-ListPrincipalsRequest)
    - [ListPrincipalsResponse](#permissions_service-v1-ListPrincipalsResponse)
    - [ListRolesRequest](#permissions_service-v1-ListRolesRequest)
    - [ListRolesResponse](#permissions_service-v1-ListRolesResponse)
    - [MissingPermissions](#permissions_service-v1-MissingPermissions)
    - [Permission](#permissions_service-v1-Permission)
    - [PrincipalCountUpdatedEvent](#permissions_service-v1-PrincipalCountUpdatedEvent)
    - [RevokeUserPermissionsAndRolesOnResourceRequest](#permissions_service-v1-RevokeUserPermissionsAndRolesOnResourceRequest)
    - [Role](#permissions_service-v1-Role)
    - [UpdatePermissionRequest](#permissions_service-v1-UpdatePermissionRequest)
    - [UpdateRoleRequest](#permissions_service-v1-UpdateRoleRequest)
  
    - [PermissionsService](#permissions_service-v1-PermissionsService)
  
- [Scalar Value Types](#scalar-value-types)



<a name="google_api_http-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## google/api/http.proto



<a name="google-api-CustomHttpPattern"></a>

### CustomHttpPattern
A custom pattern is used for defining custom HTTP verb.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| kind | [string](#string) |  | The name of this custom HTTP verb. |
| path | [string](#string) |  | The path matched by this custom verb. |






<a name="google-api-Http"></a>

### Http
Defines the HTTP configuration for an API service. It contains a list of
[HttpRule][google.api.HttpRule], each specifying the mapping of an RPC method
to one or more HTTP REST API methods.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| rules | [HttpRule](#google-api-HttpRule) | repeated | A list of HTTP configuration rules that apply to individual API methods.

**NOTE:** All service configuration rules follow &#34;last one wins&#34; order. |
| fully_decode_reserved_expansion | [bool](#bool) |  | When set to true, URL path parameters will be fully URI-decoded except in cases of single segment matches in reserved expansion, where &#34;%2F&#34; will be left encoded.

The default behavior is to not decode RFC 6570 reserved characters in multi segment matches. |






<a name="google-api-HttpRule"></a>

### HttpRule
gRPC Transcoding

gRPC Transcoding is a feature for mapping between a gRPC method and one or
more HTTP REST endpoints. It allows developers to build a single API service
that supports both gRPC APIs and REST APIs. Many systems, including [Google
APIs](https://github.com/googleapis/googleapis),
[Cloud Endpoints](https://cloud.google.com/endpoints), [gRPC
Gateway](https://github.com/grpc-ecosystem/grpc-gateway),
and [Envoy](https://github.com/envoyproxy/envoy) proxy support this feature
and use it for large scale production services.

`HttpRule` defines the schema of the gRPC/REST mapping. The mapping specifies
how different portions of the gRPC request message are mapped to the URL
path, URL query parameters, and HTTP request body. It also controls how the
gRPC response message is mapped to the HTTP response body. `HttpRule` is
typically specified as an `google.api.http` annotation on the gRPC method.

Each mapping specifies a URL path template and an HTTP method. The path
template may refer to one or more fields in the gRPC request message, as long
as each field is a non-repeated field with a primitive (non-message) type.
The path template controls how fields of the request message are mapped to
the URL path.

Example:

    service Messaging {
      rpc GetMessage(GetMessageRequest) returns (Message) {
        option (google.api.http) = {
            get: &#34;/v1/{name=messages/*}&#34;
        };
      }
    }
    message GetMessageRequest {
      string name = 1; // Mapped to URL path.
    }
    message Message {
      string text = 1; // The resource content.
    }

This enables an HTTP REST to gRPC mapping as below:

- HTTP: `GET /v1/messages/123456`
- gRPC: `GetMessage(name: &#34;messages/123456&#34;)`

Any fields in the request message which are not bound by the path template
automatically become HTTP query parameters if there is no HTTP request body.
For example:

    service Messaging {
      rpc GetMessage(GetMessageRequest) returns (Message) {
        option (google.api.http) = {
            get:&#34;/v1/messages/{message_id}&#34;
        };
      }
    }
    message GetMessageRequest {
      message SubMessage {
        string subfield = 1;
      }
      string message_id = 1; // Mapped to URL path.
      int64 revision = 2;    // Mapped to URL query parameter `revision`.
      SubMessage sub = 3;    // Mapped to URL query parameter `sub.subfield`.
    }

This enables a HTTP JSON to RPC mapping as below:

- HTTP: `GET /v1/messages/123456?revision=2&amp;sub.subfield=foo`
- gRPC: `GetMessage(message_id: &#34;123456&#34; revision: 2 sub:
SubMessage(subfield: &#34;foo&#34;))`

Note that fields which are mapped to URL query parameters must have a
primitive type or a repeated primitive type or a non-repeated message type.
In the case of a repeated type, the parameter can be repeated in the URL
as `...?param=A&amp;param=B`. In the case of a message type, each field of the
message is mapped to a separate parameter, such as
`...?foo.a=A&amp;foo.b=B&amp;foo.c=C`.

For HTTP methods that allow a request body, the `body` field
specifies the mapping. Consider a REST update method on the
message resource collection:

    service Messaging {
      rpc UpdateMessage(UpdateMessageRequest) returns (Message) {
        option (google.api.http) = {
          patch: &#34;/v1/messages/{message_id}&#34;
          body: &#34;message&#34;
        };
      }
    }
    message UpdateMessageRequest {
      string message_id = 1; // mapped to the URL
      Message message = 2;   // mapped to the body
    }

The following HTTP JSON to RPC mapping is enabled, where the
representation of the JSON in the request body is determined by
protos JSON encoding:

- HTTP: `PATCH /v1/messages/123456 { &#34;text&#34;: &#34;Hi!&#34; }`
- gRPC: `UpdateMessage(message_id: &#34;123456&#34; message { text: &#34;Hi!&#34; })`

The special name `*` can be used in the body mapping to define that
every field not bound by the path template should be mapped to the
request body.  This enables the following alternative definition of
the update method:

    service Messaging {
      rpc UpdateMessage(Message) returns (Message) {
        option (google.api.http) = {
          patch: &#34;/v1/messages/{message_id}&#34;
          body: &#34;*&#34;
        };
      }
    }
    message Message {
      string message_id = 1;
      string text = 2;
    }


The following HTTP JSON to RPC mapping is enabled:

- HTTP: `PATCH /v1/messages/123456 { &#34;text&#34;: &#34;Hi!&#34; }`
- gRPC: `UpdateMessage(message_id: &#34;123456&#34; text: &#34;Hi!&#34;)`

Note that when using `*` in the body mapping, it is not possible to
have HTTP parameters, as all fields not bound by the path end in
the body. This makes this option more rarely used in practice when
defining REST APIs. The common usage of `*` is in custom methods
which don&#39;t use the URL at all for transferring data.

It is possible to define multiple HTTP methods for one RPC by using
the `additional_bindings` option. Example:

    service Messaging {
      rpc GetMessage(GetMessageRequest) returns (Message) {
        option (google.api.http) = {
          get: &#34;/v1/messages/{message_id}&#34;
          additional_bindings {
            get: &#34;/v1/users/{user_id}/messages/{message_id}&#34;
          }
        };
      }
    }
    message GetMessageRequest {
      string message_id = 1;
      string user_id = 2;
    }

This enables the following two alternative HTTP JSON to RPC mappings:

- HTTP: `GET /v1/messages/123456`
- gRPC: `GetMessage(message_id: &#34;123456&#34;)`

- HTTP: `GET /v1/users/me/messages/123456`
- gRPC: `GetMessage(user_id: &#34;me&#34; message_id: &#34;123456&#34;)`

Rules for HTTP mapping

1. Leaf request fields (recursive expansion nested messages in the request
   message) are classified into three categories:
   - Fields referred by the path template. They are passed via the URL path.
   - Fields referred by the [HttpRule.body][google.api.HttpRule.body]. They
   are passed via the HTTP
     request body.
   - All other fields are passed via the URL query parameters, and the
     parameter name is the field path in the request message. A repeated
     field can be represented as multiple query parameters under the same
     name.
 2. If [HttpRule.body][google.api.HttpRule.body] is &#34;*&#34;, there is no URL
 query parameter, all fields
    are passed via URL path and HTTP request body.
 3. If [HttpRule.body][google.api.HttpRule.body] is omitted, there is no HTTP
 request body, all
    fields are passed via URL path and URL query parameters.

Path template syntax

    Template = &#34;/&#34; Segments [ Verb ] ;
    Segments = Segment { &#34;/&#34; Segment } ;
    Segment  = &#34;*&#34; | &#34;**&#34; | LITERAL | Variable ;
    Variable = &#34;{&#34; FieldPath [ &#34;=&#34; Segments ] &#34;}&#34; ;
    FieldPath = IDENT { &#34;.&#34; IDENT } ;
    Verb     = &#34;:&#34; LITERAL ;

The syntax `*` matches a single URL path segment. The syntax `**` matches
zero or more URL path segments, which must be the last part of the URL path
except the `Verb`.

The syntax `Variable` matches part of the URL path as specified by its
template. A variable template must not contain other variables. If a variable
matches a single path segment, its template may be omitted, e.g. `{var}`
is equivalent to `{var=*}`.

The syntax `LITERAL` matches literal text in the URL path. If the `LITERAL`
contains any reserved character, such characters should be percent-encoded
before the matching.

If a variable contains exactly one path segment, such as `&#34;{var}&#34;` or
`&#34;{var=*}&#34;`, when such a variable is expanded into a URL path on the client
side, all characters except `[-_.~0-9a-zA-Z]` are percent-encoded. The
server side does the reverse decoding. Such variables show up in the
[Discovery
Document](https://developers.google.com/discovery/v1/reference/apis) as
`{var}`.

If a variable contains multiple path segments, such as `&#34;{var=foo/*}&#34;`
or `&#34;{var=**}&#34;`, when such a variable is expanded into a URL path on the
client side, all characters except `[-_.~/0-9a-zA-Z]` are percent-encoded.
The server side does the reverse decoding, except &#34;%2F&#34; and &#34;%2f&#34; are left
unchanged. Such variables show up in the
[Discovery
Document](https://developers.google.com/discovery/v1/reference/apis) as
`{&#43;var}`.

Using gRPC API Service Configuration

gRPC API Service Configuration (service config) is a configuration language
for configuring a gRPC service to become a user-facing product. The
service config is simply the YAML representation of the `google.api.Service`
proto message.

As an alternative to annotating your proto file, you can configure gRPC
transcoding in your service config YAML files. You do this by specifying a
`HttpRule` that maps the gRPC method to a REST endpoint, achieving the same
effect as the proto annotation. This can be particularly useful if you
have a proto that is reused in multiple services. Note that any transcoding
specified in the service config will override any matching transcoding
configuration in the proto.

The following example selects a gRPC method and applies an `HttpRule` to it:

    http:
      rules:
        - selector: example.v1.Messaging.GetMessage
          get: /v1/messages/{message_id}/{sub.subfield}

Special notes

When gRPC Transcoding is used to map a gRPC to JSON REST endpoints, the
proto to JSON conversion must follow the [proto3
specification](https://developers.google.com/protocol-buffers/docs/proto3#json).

While the single segment variable follows the semantics of
[RFC 6570](https://tools.ietf.org/html/rfc6570) Section 3.2.2 Simple String
Expansion, the multi segment variable **does not** follow RFC 6570 Section
3.2.3 Reserved Expansion. The reason is that the Reserved Expansion
does not expand special characters like `?` and `#`, which would lead
to invalid URLs. As the result, gRPC Transcoding uses a custom encoding
for multi segment variables.

The path variables **must not** refer to any repeated or mapped field,
because client libraries are not capable of handling such variable expansion.

The path variables **must not** capture the leading &#34;/&#34; character. The reason
is that the most common use case &#34;{var}&#34; does not capture the leading &#34;/&#34;
character. For consistency, all path variables must share the same behavior.

Repeated message fields must not be mapped to URL query parameters, because
no client library can support such complicated mapping.

If an API needs to use a JSON array for request or response body, it can map
the request or response body to a repeated field. However, some gRPC
Transcoding implementations may not support this feature.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| selector | [string](#string) |  | Selects a method to which this rule applies.

Refer to [selector][google.api.DocumentationRule.selector] for syntax details. |
| get | [string](#string) |  | Maps to HTTP GET. Used for listing and getting information about resources. |
| put | [string](#string) |  | Maps to HTTP PUT. Used for replacing a resource. |
| post | [string](#string) |  | Maps to HTTP POST. Used for creating a resource or performing an action. |
| delete | [string](#string) |  | Maps to HTTP DELETE. Used for deleting a resource. |
| patch | [string](#string) |  | Maps to HTTP PATCH. Used for updating a resource. |
| custom | [CustomHttpPattern](#google-api-CustomHttpPattern) |  | The custom pattern is used for specifying an HTTP method that is not included in the `pattern` field, such as HEAD, or &#34;*&#34; to leave the HTTP method unspecified for this rule. The wild-card rule is useful for services that provide content to Web (HTML) clients. |
| body | [string](#string) |  | The name of the request field whose value is mapped to the HTTP request body, or `*` for mapping all request fields not captured by the path pattern to the HTTP body, or omitted for not having any HTTP request body.

NOTE: the referred field must be present at the top-level of the request message type. |
| response_body | [string](#string) |  | Optional. The name of the response field whose value is mapped to the HTTP response body. When omitted, the entire response message will be used as the HTTP response body.

NOTE: The referred field must be present at the top-level of the response message type. |
| additional_bindings | [HttpRule](#google-api-HttpRule) | repeated | Additional HTTP bindings for the selector. Nested bindings must not contain an `additional_bindings` field themselves (that is, the nesting may only be one level deep). |





 

 

 

 



<a name="google_api_annotations-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## google/api/annotations.proto


 

 


<a name="google_api_annotations-proto-extensions"></a>

### File-level Extensions
| Extension | Type | Base | Number | Description |
| --------- | ---- | ---- | ------ | ----------- |
| http | HttpRule | .google.protobuf.MethodOptions | 72295728 | See `HttpRule`. |

 

 



<a name="validate_validate-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## validate/validate.proto



<a name="validate-AnyRules"></a>

### AnyRules
AnyRules describe constraints applied exclusively to the
`google.protobuf.Any` well-known type


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| required | [bool](#bool) | optional | Required specifies that this field must be set |
| in | [string](#string) | repeated | In specifies that this field&#39;s `type_url` must be equal to one of the specified values. |
| not_in | [string](#string) | repeated | NotIn specifies that this field&#39;s `type_url` must not be equal to any of the specified values. |






<a name="validate-BoolRules"></a>

### BoolRules
BoolRules describes the constraints applied to `bool` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [bool](#bool) | optional | Const specifies that this field must be exactly the specified value |






<a name="validate-BytesRules"></a>

### BytesRules
BytesRules describe the constraints applied to `bytes` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [bytes](#bytes) | optional | Const specifies that this field must be exactly the specified value |
| len | [uint64](#uint64) | optional | Len specifies that this field must be the specified number of bytes |
| min_len | [uint64](#uint64) | optional | MinLen specifies that this field must be the specified number of bytes at a minimum |
| max_len | [uint64](#uint64) | optional | MaxLen specifies that this field must be the specified number of bytes at a maximum |
| pattern | [string](#string) | optional | Pattern specifies that this field must match against the specified regular expression (RE2 syntax). The included expression should elide any delimiters. |
| prefix | [bytes](#bytes) | optional | Prefix specifies that this field must have the specified bytes at the beginning of the string. |
| suffix | [bytes](#bytes) | optional | Suffix specifies that this field must have the specified bytes at the end of the string. |
| contains | [bytes](#bytes) | optional | Contains specifies that this field must have the specified bytes anywhere in the string. |
| in | [bytes](#bytes) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [bytes](#bytes) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ip | [bool](#bool) | optional | Ip specifies that the field must be a valid IP (v4 or v6) address in byte format |
| ipv4 | [bool](#bool) | optional | Ipv4 specifies that the field must be a valid IPv4 address in byte format |
| ipv6 | [bool](#bool) | optional | Ipv6 specifies that the field must be a valid IPv6 address in byte format |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-DoubleRules"></a>

### DoubleRules
DoubleRules describes the constraints applied to `double` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [double](#double) | optional | Const specifies that this field must be exactly the specified value |
| lt | [double](#double) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [double](#double) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [double](#double) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [double](#double) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [double](#double) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [double](#double) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-DurationRules"></a>

### DurationRules
DurationRules describe the constraints applied exclusively to the
`google.protobuf.Duration` well-known type


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| required | [bool](#bool) | optional | Required specifies that this field must be set |
| const | [google.protobuf.Duration](#google-protobuf-Duration) | optional | Const specifies that this field must be exactly the specified value |
| lt | [google.protobuf.Duration](#google-protobuf-Duration) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [google.protobuf.Duration](#google-protobuf-Duration) | optional | Lt specifies that this field must be less than the specified value, inclusive |
| gt | [google.protobuf.Duration](#google-protobuf-Duration) | optional | Gt specifies that this field must be greater than the specified value, exclusive |
| gte | [google.protobuf.Duration](#google-protobuf-Duration) | optional | Gte specifies that this field must be greater than the specified value, inclusive |
| in | [google.protobuf.Duration](#google-protobuf-Duration) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [google.protobuf.Duration](#google-protobuf-Duration) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |






<a name="validate-EnumRules"></a>

### EnumRules
EnumRules describe the constraints applied to enum values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [int32](#int32) | optional | Const specifies that this field must be exactly the specified value |
| defined_only | [bool](#bool) | optional | DefinedOnly specifies that this field must be only one of the defined values for this enum, failing on any undefined value. |
| in | [int32](#int32) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [int32](#int32) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |






<a name="validate-FieldRules"></a>

### FieldRules
FieldRules encapsulates the rules for each type of field. Depending on the
field, the correct set should be used to ensure proper validations.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| message | [MessageRules](#validate-MessageRules) | optional |  |
| float | [FloatRules](#validate-FloatRules) | optional | Scalar Field Types |
| double | [DoubleRules](#validate-DoubleRules) | optional |  |
| int32 | [Int32Rules](#validate-Int32Rules) | optional |  |
| int64 | [Int64Rules](#validate-Int64Rules) | optional |  |
| uint32 | [UInt32Rules](#validate-UInt32Rules) | optional |  |
| uint64 | [UInt64Rules](#validate-UInt64Rules) | optional |  |
| sint32 | [SInt32Rules](#validate-SInt32Rules) | optional |  |
| sint64 | [SInt64Rules](#validate-SInt64Rules) | optional |  |
| fixed32 | [Fixed32Rules](#validate-Fixed32Rules) | optional |  |
| fixed64 | [Fixed64Rules](#validate-Fixed64Rules) | optional |  |
| sfixed32 | [SFixed32Rules](#validate-SFixed32Rules) | optional |  |
| sfixed64 | [SFixed64Rules](#validate-SFixed64Rules) | optional |  |
| bool | [BoolRules](#validate-BoolRules) | optional |  |
| string | [StringRules](#validate-StringRules) | optional |  |
| bytes | [BytesRules](#validate-BytesRules) | optional |  |
| enum | [EnumRules](#validate-EnumRules) | optional | Complex Field Types |
| repeated | [RepeatedRules](#validate-RepeatedRules) | optional |  |
| map | [MapRules](#validate-MapRules) | optional |  |
| any | [AnyRules](#validate-AnyRules) | optional | Well-Known Field Types |
| duration | [DurationRules](#validate-DurationRules) | optional |  |
| timestamp | [TimestampRules](#validate-TimestampRules) | optional |  |






<a name="validate-Fixed32Rules"></a>

### Fixed32Rules
Fixed32Rules describes the constraints applied to `fixed32` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [fixed32](#fixed32) | optional | Const specifies that this field must be exactly the specified value |
| lt | [fixed32](#fixed32) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [fixed32](#fixed32) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [fixed32](#fixed32) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [fixed32](#fixed32) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [fixed32](#fixed32) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [fixed32](#fixed32) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-Fixed64Rules"></a>

### Fixed64Rules
Fixed64Rules describes the constraints applied to `fixed64` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [fixed64](#fixed64) | optional | Const specifies that this field must be exactly the specified value |
| lt | [fixed64](#fixed64) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [fixed64](#fixed64) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [fixed64](#fixed64) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [fixed64](#fixed64) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [fixed64](#fixed64) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [fixed64](#fixed64) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-FloatRules"></a>

### FloatRules
FloatRules describes the constraints applied to `float` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [float](#float) | optional | Const specifies that this field must be exactly the specified value |
| lt | [float](#float) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [float](#float) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [float](#float) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [float](#float) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [float](#float) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [float](#float) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-Int32Rules"></a>

### Int32Rules
Int32Rules describes the constraints applied to `int32` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [int32](#int32) | optional | Const specifies that this field must be exactly the specified value |
| lt | [int32](#int32) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [int32](#int32) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [int32](#int32) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [int32](#int32) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [int32](#int32) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [int32](#int32) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-Int64Rules"></a>

### Int64Rules
Int64Rules describes the constraints applied to `int64` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [int64](#int64) | optional | Const specifies that this field must be exactly the specified value |
| lt | [int64](#int64) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [int64](#int64) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [int64](#int64) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [int64](#int64) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [int64](#int64) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [int64](#int64) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-MapRules"></a>

### MapRules
MapRules describe the constraints applied to `map` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| min_pairs | [uint64](#uint64) | optional | MinPairs specifies that this field must have the specified number of KVs at a minimum |
| max_pairs | [uint64](#uint64) | optional | MaxPairs specifies that this field must have the specified number of KVs at a maximum |
| no_sparse | [bool](#bool) | optional | NoSparse specifies values in this field cannot be unset. This only applies to map&#39;s with message value types. |
| keys | [FieldRules](#validate-FieldRules) | optional | Keys specifies the constraints to be applied to each key in the field. |
| values | [FieldRules](#validate-FieldRules) | optional | Values specifies the constraints to be applied to the value of each key in the field. Message values will still have their validations evaluated unless skip is specified here. |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-MessageRules"></a>

### MessageRules
MessageRules describe the constraints applied to embedded message values.
For message-type fields, validation is performed recursively.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| skip | [bool](#bool) | optional | Skip specifies that the validation rules of this field should not be evaluated |
| required | [bool](#bool) | optional | Required specifies that this field must be set |






<a name="validate-RepeatedRules"></a>

### RepeatedRules
RepeatedRules describe the constraints applied to `repeated` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| min_items | [uint64](#uint64) | optional | MinItems specifies that this field must have the specified number of items at a minimum |
| max_items | [uint64](#uint64) | optional | MaxItems specifies that this field must have the specified number of items at a maximum |
| unique | [bool](#bool) | optional | Unique specifies that all elements in this field must be unique. This constraint is only applicable to scalar and enum types (messages are not supported). |
| items | [FieldRules](#validate-FieldRules) | optional | Items specifies the constraints to be applied to each item in the field. Repeated message fields will still execute validation against each item unless skip is specified here. |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-SFixed32Rules"></a>

### SFixed32Rules
SFixed32Rules describes the constraints applied to `sfixed32` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [sfixed32](#sfixed32) | optional | Const specifies that this field must be exactly the specified value |
| lt | [sfixed32](#sfixed32) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [sfixed32](#sfixed32) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [sfixed32](#sfixed32) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [sfixed32](#sfixed32) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [sfixed32](#sfixed32) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [sfixed32](#sfixed32) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-SFixed64Rules"></a>

### SFixed64Rules
SFixed64Rules describes the constraints applied to `sfixed64` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [sfixed64](#sfixed64) | optional | Const specifies that this field must be exactly the specified value |
| lt | [sfixed64](#sfixed64) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [sfixed64](#sfixed64) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [sfixed64](#sfixed64) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [sfixed64](#sfixed64) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [sfixed64](#sfixed64) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [sfixed64](#sfixed64) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-SInt32Rules"></a>

### SInt32Rules
SInt32Rules describes the constraints applied to `sint32` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [sint32](#sint32) | optional | Const specifies that this field must be exactly the specified value |
| lt | [sint32](#sint32) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [sint32](#sint32) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [sint32](#sint32) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [sint32](#sint32) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [sint32](#sint32) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [sint32](#sint32) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-SInt64Rules"></a>

### SInt64Rules
SInt64Rules describes the constraints applied to `sint64` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [sint64](#sint64) | optional | Const specifies that this field must be exactly the specified value |
| lt | [sint64](#sint64) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [sint64](#sint64) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [sint64](#sint64) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [sint64](#sint64) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [sint64](#sint64) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [sint64](#sint64) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-StringRules"></a>

### StringRules
StringRules describe the constraints applied to `string` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [string](#string) | optional | Const specifies that this field must be exactly the specified value |
| len | [uint64](#uint64) | optional | Len specifies that this field must be the specified number of characters (Unicode code points). Note that the number of characters may differ from the number of bytes in the string. |
| min_len | [uint64](#uint64) | optional | MinLen specifies that this field must be the specified number of characters (Unicode code points) at a minimum. Note that the number of characters may differ from the number of bytes in the string. |
| max_len | [uint64](#uint64) | optional | MaxLen specifies that this field must be the specified number of characters (Unicode code points) at a maximum. Note that the number of characters may differ from the number of bytes in the string. |
| len_bytes | [uint64](#uint64) | optional | LenBytes specifies that this field must be the specified number of bytes |
| min_bytes | [uint64](#uint64) | optional | MinBytes specifies that this field must be the specified number of bytes at a minimum |
| max_bytes | [uint64](#uint64) | optional | MaxBytes specifies that this field must be the specified number of bytes at a maximum |
| pattern | [string](#string) | optional | Pattern specifies that this field must match against the specified regular expression (RE2 syntax). The included expression should elide any delimiters. |
| prefix | [string](#string) | optional | Prefix specifies that this field must have the specified substring at the beginning of the string. |
| suffix | [string](#string) | optional | Suffix specifies that this field must have the specified substring at the end of the string. |
| contains | [string](#string) | optional | Contains specifies that this field must have the specified substring anywhere in the string. |
| not_contains | [string](#string) | optional | NotContains specifies that this field cannot have the specified substring anywhere in the string. |
| in | [string](#string) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [string](#string) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| email | [bool](#bool) | optional | Email specifies that the field must be a valid email address as defined by RFC 5322 |
| hostname | [bool](#bool) | optional | Hostname specifies that the field must be a valid hostname as defined by RFC 1034. This constraint does not support internationalized domain names (IDNs). |
| ip | [bool](#bool) | optional | Ip specifies that the field must be a valid IP (v4 or v6) address. Valid IPv6 addresses should not include surrounding square brackets. |
| ipv4 | [bool](#bool) | optional | Ipv4 specifies that the field must be a valid IPv4 address. |
| ipv6 | [bool](#bool) | optional | Ipv6 specifies that the field must be a valid IPv6 address. Valid IPv6 addresses should not include surrounding square brackets. |
| uri | [bool](#bool) | optional | Uri specifies that the field must be a valid, absolute URI as defined by RFC 3986 |
| uri_ref | [bool](#bool) | optional | UriRef specifies that the field must be a valid URI as defined by RFC 3986 and may be relative or absolute. |
| address | [bool](#bool) | optional | Address specifies that the field must be either a valid hostname as defined by RFC 1034 (which does not support internationalized domain names or IDNs), or it can be a valid IP (v4 or v6). |
| uuid | [bool](#bool) | optional | Uuid specifies that the field must be a valid UUID as defined by RFC 4122 |
| well_known_regex | [KnownRegex](#validate-KnownRegex) | optional | WellKnownRegex specifies a common well known pattern defined as a regex. |
| strict | [bool](#bool) | optional | This applies to regexes HTTP_HEADER_NAME and HTTP_HEADER_VALUE to enable strict header validation. By default, this is true, and HTTP header validations are RFC-compliant. Setting to false will enable a looser validations that only disallows \r\n\0 characters, which can be used to bypass header matching rules. Default: true |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-TimestampRules"></a>

### TimestampRules
TimestampRules describe the constraints applied exclusively to the
`google.protobuf.Timestamp` well-known type


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| required | [bool](#bool) | optional | Required specifies that this field must be set |
| const | [google.protobuf.Timestamp](#google-protobuf-Timestamp) | optional | Const specifies that this field must be exactly the specified value |
| lt | [google.protobuf.Timestamp](#google-protobuf-Timestamp) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [google.protobuf.Timestamp](#google-protobuf-Timestamp) | optional | Lte specifies that this field must be less than the specified value, inclusive |
| gt | [google.protobuf.Timestamp](#google-protobuf-Timestamp) | optional | Gt specifies that this field must be greater than the specified value, exclusive |
| gte | [google.protobuf.Timestamp](#google-protobuf-Timestamp) | optional | Gte specifies that this field must be greater than the specified value, inclusive |
| lt_now | [bool](#bool) | optional | LtNow specifies that this must be less than the current time. LtNow can only be used with the Within rule. |
| gt_now | [bool](#bool) | optional | GtNow specifies that this must be greater than the current time. GtNow can only be used with the Within rule. |
| within | [google.protobuf.Duration](#google-protobuf-Duration) | optional | Within specifies that this field must be within this duration of the current time. This constraint can be used alone or with the LtNow and GtNow rules. |






<a name="validate-UInt32Rules"></a>

### UInt32Rules
UInt32Rules describes the constraints applied to `uint32` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [uint32](#uint32) | optional | Const specifies that this field must be exactly the specified value |
| lt | [uint32](#uint32) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [uint32](#uint32) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [uint32](#uint32) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [uint32](#uint32) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [uint32](#uint32) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [uint32](#uint32) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |






<a name="validate-UInt64Rules"></a>

### UInt64Rules
UInt64Rules describes the constraints applied to `uint64` values


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| const | [uint64](#uint64) | optional | Const specifies that this field must be exactly the specified value |
| lt | [uint64](#uint64) | optional | Lt specifies that this field must be less than the specified value, exclusive |
| lte | [uint64](#uint64) | optional | Lte specifies that this field must be less than or equal to the specified value, inclusive |
| gt | [uint64](#uint64) | optional | Gt specifies that this field must be greater than the specified value, exclusive. If the value of Gt is larger than a specified Lt or Lte, the range is reversed. |
| gte | [uint64](#uint64) | optional | Gte specifies that this field must be greater than or equal to the specified value, inclusive. If the value of Gte is larger than a specified Lt or Lte, the range is reversed. |
| in | [uint64](#uint64) | repeated | In specifies that this field must be equal to one of the specified values |
| not_in | [uint64](#uint64) | repeated | NotIn specifies that this field cannot be equal to one of the specified values |
| ignore_empty | [bool](#bool) | optional | IgnoreEmpty specifies that the validation rules of this field should be evaluated only if the field is not empty |





 


<a name="validate-KnownRegex"></a>

### KnownRegex
WellKnownRegex contain some well-known patterns.

| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| HTTP_HEADER_NAME | 1 | HTTP header name as defined by RFC 7230. |
| HTTP_HEADER_VALUE | 2 | HTTP header value as defined by RFC 7230. |


 


<a name="validate_validate-proto-extensions"></a>

### File-level Extensions
| Extension | Type | Base | Number | Description |
| --------- | ---- | ---- | ------ | ----------- |
| rules | FieldRules | .google.protobuf.FieldOptions | 1071 | Rules specify the validations to be performed on this field. By default, no validation is performed against a field. |
| disabled | bool | .google.protobuf.MessageOptions | 1071 | Disabled nullifies any validation rules for this message, including any message fields associated with it that do support validation. |
| ignored | bool | .google.protobuf.MessageOptions | 1072 | Ignore skips generation of validation methods for this message. |
| required | bool | .google.protobuf.OneofOptions | 1071 | Required ensures that exactly one the field options in a oneof is set; validation fails if no fields in the oneof are set. |

 

 



<a name="v1_organisation_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## v1/organisation_service.proto



<a name="organisation_service-v1-APIKey"></a>

### APIKey



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| name | [string](#string) |  |  |
| key | [string](#string) |  |  |
| created_at | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |  |  |
| invalidated | [bool](#bool) |  |  |






<a name="organisation_service-v1-ActivateBillingSubscriptionRequest"></a>

### ActivateBillingSubscriptionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| price_id | [string](#string) |  |  |






<a name="organisation_service-v1-AddEmailToMailingListRequest"></a>

### AddEmailToMailingListRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| email | [string](#string) |  |  |






<a name="organisation_service-v1-BillingCustomer"></a>

### BillingCustomer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| organisation_id | [string](#string) |  |  |
| name | [string](#string) |  |  |
| email | [string](#string) |  |  |






<a name="organisation_service-v1-CreateAPIKeyRequest"></a>

### CreateAPIKeyRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| project_name | [string](#string) |  | project_name is the name of the project that the api key should be created in |
| name | [string](#string) |  |  |






<a name="organisation_service-v1-CreateAPIKeyResponse"></a>

### CreateAPIKeyResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| api_key | [APIKey](#organisation_service-v1-APIKey) |  |  |






<a name="organisation_service-v1-CreateOrganisationRequest"></a>

### CreateOrganisationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  |  |
| user_id | [string](#string) |  | user_id is the user that created the organisation and will be added as an admin |






<a name="organisation_service-v1-CreateOrganisationResponse"></a>

### CreateOrganisationResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation | [Organisation](#organisation_service-v1-Organisation) |  |  |






<a name="organisation_service-v1-CreateProjectRequest"></a>

### CreateProjectRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  | organisation_id is the id of the organisation |
| name | [string](#string) |  | name is the name of the new project |






<a name="organisation_service-v1-CreateProjectResponse"></a>

### CreateProjectResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project | [Project](#organisation_service-v1-Project) |  |  |






<a name="organisation_service-v1-DeleteProjectRequest"></a>

### DeleteProjectRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| project_name | [string](#string) |  |  |






<a name="organisation_service-v1-GetCustomerActiveSubscriptionRequest"></a>

### GetCustomerActiveSubscriptionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |






<a name="organisation_service-v1-GetCustomerActiveSubscriptionResponse"></a>

### GetCustomerActiveSubscriptionResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| active_subscription_id | [string](#string) | optional | active_subscription_id is the id of the active subscription for the customer. It is optional as the customer may not have an active subscription. |
| active_price_id | [string](#string) | optional | active_price_id is the id of the active price for the customer. It is optional as the customer may not have an active subscription. |






<a name="organisation_service-v1-GetCustomerBillingSessionRequest"></a>

### GetCustomerBillingSessionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |






<a name="organisation_service-v1-GetCustomerBillingSessionResponse"></a>

### GetCustomerBillingSessionResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| session_secret | [string](#string) |  |  |






<a name="organisation_service-v1-GetCustomerDefaultPaymentMethodAndIntentRequest"></a>

### GetCustomerDefaultPaymentMethodAndIntentRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |






<a name="organisation_service-v1-GetCustomerDefaultPaymentMethodAndIntentResponse"></a>

### GetCustomerDefaultPaymentMethodAndIntentResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| default_payment_method_id | [string](#string) | optional | default_payment_method_id is the id of the default payment method if it exists |
| default_payment_method_intent | [string](#string) | optional | default_payment_method_intent is the id of the payment intent for the default payment method if it exists |






<a name="organisation_service-v1-GetOrganisationRequest"></a>

### GetOrganisationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |






<a name="organisation_service-v1-GetOrganisationResponse"></a>

### GetOrganisationResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation | [Organisation](#organisation_service-v1-Organisation) |  |  |






<a name="organisation_service-v1-GetProjectRequest"></a>

### GetProjectRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| project_name | [string](#string) |  |  |






<a name="organisation_service-v1-GetProjectResponse"></a>

### GetProjectResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project | [Project](#organisation_service-v1-Project) |  |  |






<a name="organisation_service-v1-GetProjectsForOrganisationRequest"></a>

### GetProjectsForOrganisationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |






<a name="organisation_service-v1-GetProjectsForOrganisationResponse"></a>

### GetProjectsForOrganisationResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| projects | [Project](#organisation_service-v1-Project) | repeated |  |






<a name="organisation_service-v1-GetUsersOrganisationRequest"></a>

### GetUsersOrganisationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| user_id | [string](#string) |  |  |






<a name="organisation_service-v1-InvalidateAPIKeyRequest"></a>

### InvalidateAPIKeyRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| project_name | [string](#string) |  | project_name is the name of the project that the api key belongs to |
| id | [string](#string) |  |  |






<a name="organisation_service-v1-InviteUserToOrganisationRequest"></a>

### InviteUserToOrganisationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| email | [string](#string) |  |  |






<a name="organisation_service-v1-IsOrganisationPermittedToGrantRequest"></a>

### IsOrganisationPermittedToGrantRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |






<a name="organisation_service-v1-IsOrganisationPermittedToGrantResponse"></a>

### IsOrganisationPermittedToGrantResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| permitted | [bool](#bool) |  |  |






<a name="organisation_service-v1-ListAPIKeysRequest"></a>

### ListAPIKeysRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| project_name | [string](#string) |  | project_name is the name of the project to list the api keys for |






<a name="organisation_service-v1-ListAPIKeysResponse"></a>

### ListAPIKeysResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| api_keys | [APIKey](#organisation_service-v1-APIKey) | repeated |  |






<a name="organisation_service-v1-Organisation"></a>

### Organisation



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| name | [string](#string) |  |  |
| users | [User](#organisation_service-v1-User) | repeated |  |
| created_at | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |  |  |
| updated_at | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |  |  |
| billing_customer | [BillingCustomer](#organisation_service-v1-BillingCustomer) |  |  |






<a name="organisation_service-v1-Project"></a>

### Project



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  |  |
| name | [string](#string) |  |  |
| created_at | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |  |  |






<a name="organisation_service-v1-SetUsersOrganisationRequest"></a>

### SetUsersOrganisationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| user_id | [string](#string) |  |  |
| email | [string](#string) |  |  |






<a name="organisation_service-v1-UpdateOrganisationRequest"></a>

### UpdateOrganisationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| name | [string](#string) |  |  |






<a name="organisation_service-v1-UpdateOrganisationResponse"></a>

### UpdateOrganisationResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation | [Organisation](#organisation_service-v1-Organisation) |  |  |






<a name="organisation_service-v1-User"></a>

### User



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| email | [string](#string) |  |  |





 

 

 


<a name="organisation_service-v1-OrganisationService"></a>

### OrganisationService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| CreateOrganisation | [CreateOrganisationRequest](#organisation_service-v1-CreateOrganisationRequest) | [CreateOrganisationResponse](#organisation_service-v1-CreateOrganisationResponse) |  |
| GetOrganisation | [GetOrganisationRequest](#organisation_service-v1-GetOrganisationRequest) | [GetOrganisationResponse](#organisation_service-v1-GetOrganisationResponse) |  |
| UpdateOrganisation | [UpdateOrganisationRequest](#organisation_service-v1-UpdateOrganisationRequest) | [UpdateOrganisationResponse](#organisation_service-v1-UpdateOrganisationResponse) | UpdateOrganisation updates the provided organisation. Required Permissions: - organisation.update on /organisation/{organisation_id} |
| SetUsersOrganisation | [SetUsersOrganisationRequest](#organisation_service-v1-SetUsersOrganisationRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | SetUsersOrganisation sets the provided users organisation. Required Permissions: - user.organisation.set on /user/{user_id} |
| InviteUserToOrganisation | [InviteUserToOrganisationRequest](#organisation_service-v1-InviteUserToOrganisationRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) |  |
| GetUsersOrganisation | [GetUsersOrganisationRequest](#organisation_service-v1-GetUsersOrganisationRequest) | [GetOrganisationResponse](#organisation_service-v1-GetOrganisationResponse) | GetUsersOrganisation returns the organisation for the user. Required Permissions: - user.organisation.get on /user/{user_id} |
| CreateAPIKey | [CreateAPIKeyRequest](#organisation_service-v1-CreateAPIKeyRequest) | [CreateAPIKeyResponse](#organisation_service-v1-CreateAPIKeyResponse) |  |
| ListAPIKeys | [ListAPIKeysRequest](#organisation_service-v1-ListAPIKeysRequest) | [ListAPIKeysResponse](#organisation_service-v1-ListAPIKeysResponse) | ListAPIKeys returns a list of apiKeys for an organisation. Required Permissions: - apiKeys.list on /organisation/{organisation_id} |
| InvalidateAPIKey | [InvalidateAPIKeyRequest](#organisation_service-v1-InvalidateAPIKeyRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) |  |
| CreateProject | [CreateProjectRequest](#organisation_service-v1-CreateProjectRequest) | [CreateProjectResponse](#organisation_service-v1-CreateProjectResponse) | SetUniquePrincipalCountForOrganisation is an internal method to set the unique principal count for an organisation. rpc SetUniquePrincipalCountForOrganisation(permissions_service.v1.PrincipalCountUpdatedEvent) returns (google.protobuf.Empty) { option (google.api.http) = { post: &#34;/organisation-service/v1/organisation/unique-principal-count&#34; body: &#34;*&#34; }; } CreateProject creates a new project for an organisation. Required Permissions: - project.create on /organisation/{organisation_id} |
| GetProject | [GetProjectRequest](#organisation_service-v1-GetProjectRequest) | [GetProjectResponse](#organisation_service-v1-GetProjectResponse) | GetProject returns the project given the organisation and project id. Required Permissions: - project.get on /organisation/{organisation_id}/project/{project_name} |
| GetProjectsForOrganisation | [GetProjectsForOrganisationRequest](#organisation_service-v1-GetProjectsForOrganisationRequest) | [GetProjectsForOrganisationResponse](#organisation_service-v1-GetProjectsForOrganisationResponse) | GetProjectsForOrganisation returns the project given the organisation and project id. Required Permissions: - project.get on /organisation/{organisation_id} |
| DeleteProject | [DeleteProjectRequest](#organisation_service-v1-DeleteProjectRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | DeleteProject deletes the project for the organisation. Required Permissions: - project.delete on /organisation/{organisation_id}/project/{project_name} |
| GetCustomerBillingSession | [GetCustomerBillingSessionRequest](#organisation_service-v1-GetCustomerBillingSessionRequest) | [GetCustomerBillingSessionResponse](#organisation_service-v1-GetCustomerBillingSessionResponse) | GetCustomerBillingSession is an internal method and returns a new billing session for the customer to change plan configurations. Required Permissions: - billing.manage on /organisation/{organisation_id} |
| GetCustomerActiveSubscription | [GetCustomerActiveSubscriptionRequest](#organisation_service-v1-GetCustomerActiveSubscriptionRequest) | [GetCustomerActiveSubscriptionResponse](#organisation_service-v1-GetCustomerActiveSubscriptionResponse) | GetCustomerActiveSubscription is an internal method and returns the active subscription for the customer. Required Permissions: - billing.manage on /organisation/{organisation_id} |
| GetCustomerDefaultPaymentMethodAndIntent | [GetCustomerDefaultPaymentMethodAndIntentRequest](#organisation_service-v1-GetCustomerDefaultPaymentMethodAndIntentRequest) | [GetCustomerDefaultPaymentMethodAndIntentResponse](#organisation_service-v1-GetCustomerDefaultPaymentMethodAndIntentResponse) | GetCustomerDefaultPaymentMethodAndIntent is an internal method which returns the payment method and intent for the customer. Required Permissions: - billing.manage on /organisation/{organisation_id} |
| ActivateBillingSubscription | [ActivateBillingSubscriptionRequest](#organisation_service-v1-ActivateBillingSubscriptionRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | ActivateBillingSubscription is an internal method to activate a billing subscription for the customer. Required Permissions: - billing.manage on /organisation/{organisation_id} |
| IsOrganisationPermittedToGrant | [IsOrganisationPermittedToGrantRequest](#organisation_service-v1-IsOrganisationPermittedToGrantRequest) | [IsOrganisationPermittedToGrantResponse](#organisation_service-v1-IsOrganisationPermittedToGrantResponse) | IsOrganisationPermittedToGrant is an internal method to check if the organisation can grant more principals. Required Permissions: - organisation.grant.check.permitted on /organisation/{organisation_id} |
| AddEmailToMailingList | [AddEmailToMailingListRequest](#organisation_service-v1-AddEmailToMailingListRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) |  |

 



<a name="v1_permissions_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## v1/permissions_service.proto



<a name="permissions_service-v1-Assignment"></a>

### Assignment
an Assignment is a set of permissions and roles assigned to a principal on a resource.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| resource_uri | [string](#string) |  | ResourceURI is the URI of the resource to which the principal is assigned permissions. |
| permissions | [Permission](#permissions_service-v1-Permission) | repeated | Permissions is a list of permissions that the principal has. |
| roles | [Role](#permissions_service-v1-Role) | repeated | Roles is a list of roles that the principal has. |






<a name="permissions_service-v1-CheckPermissionRequest"></a>

### CheckPermissionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project to check permissions in. |
| principal_id | [string](#string) |  | PrincipalID is the unique identifier of the principal. |
| resource_uris | [string](#string) | repeated | ResourceURIs is a list of URIs of the resources to check. |
| permissions | [string](#string) | repeated | Permissions is a list of permission names that the principal should have. |






<a name="permissions_service-v1-CheckPermissionResponse"></a>

### CheckPermissionResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| passed | [bool](#bool) |  | passed is true if the principal has all of the specified permissions on the specified resources. |
| missing_permissions | [MissingPermissions](#permissions_service-v1-MissingPermissions) | repeated | missing_permissions is a list of resources and the permissions that the principal does not have on them. |






<a name="permissions_service-v1-CreatePermissionRequest"></a>

### CreatePermissionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the permission will belong to. |
| name | [string](#string) |  | Name is the name of the permission. |
| description | [string](#string) |  | Description is the description of the permission. |






<a name="permissions_service-v1-CreateRoleRequest"></a>

### CreateRoleRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the role belongs to. |
| name | [string](#string) |  | Name is the name of the role. |
| description | [string](#string) |  | Description is the description of the role. |
| permissions | [string](#string) | repeated | Permissions is a list of permission IDs that the role has. |






<a name="permissions_service-v1-DeletePermissionRequest"></a>

### DeletePermissionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the permission belongs to. |
| id | [string](#string) |  | ID is the unique identifier of the permission. |






<a name="permissions_service-v1-DeleteRoleRequest"></a>

### DeleteRoleRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the role belongs to. |
| id | [string](#string) |  | ID is the unique identifier of the role. |






<a name="permissions_service-v1-GetAllAssignmentsForPrincipalRequest"></a>

### GetAllAssignmentsForPrincipalRequest
GetAllAssignmentsForPrincipalRequest is the request to get all assignments for a principal.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that principal belongs to. |
| principal_id | [string](#string) |  | PrincipalID is the unique identifier of the principal. |






<a name="permissions_service-v1-GetAllAssignmentsForPrincipalResponse"></a>

### GetAllAssignmentsForPrincipalResponse
GetAllAssignmentsForPrincipalResponse is the response to the GetAllAssignmentsForPrincipal request.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| assignments | [Assignment](#permissions_service-v1-Assignment) | repeated | Assignments is a list of assignments for the principal. |






<a name="permissions_service-v1-GetPermissionRequest"></a>

### GetPermissionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the permission belongs to. |
| id | [string](#string) |  | ID is the unique identifier of the permission. |






<a name="permissions_service-v1-GetRoleRequest"></a>

### GetRoleRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the role belongs to. |
| id | [string](#string) |  | ID is the unique identifier of the role. |






<a name="permissions_service-v1-GetUserPermissionsAndRolesOnResourceRequest"></a>

### GetUserPermissionsAndRolesOnResourceRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the grant will belong to. |
| user_id | [string](#string) |  | UserID is the unique identifier of the user. |
| resource_uri | [string](#string) |  | ResourceURI is the URI of the resource to which the user is being assigned permissions. |






<a name="permissions_service-v1-GetUserPermissionsAndRolesOnResourceResponse"></a>

### GetUserPermissionsAndRolesOnResourceResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  |  |
| user_id | [string](#string) |  | UserID is the unique identifier of the user. |
| resource_uri | [string](#string) |  | ResourceURI is the URI of the resource to which the user is being assigned permissions. |
| permissions | [string](#string) | repeated | Permissions is a list of permission IDs that should be assigned to the user. |
| roles | [string](#string) | repeated | Roles is a list of role IDs that should be assigned to the user. |






<a name="permissions_service-v1-GrantUserPermissionsAndRolesOnResourceRequest"></a>

### GrantUserPermissionsAndRolesOnResourceRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the grant will belong to. |
| user_id | [string](#string) |  | UserID is the unique identifier of the user. |
| resource_uri | [string](#string) |  | ResourceURI is the URI of the resource to which the user is being assigned permissions. |
| permissions | [string](#string) | repeated | Permissions is a list of permission IDs that should be assigned to the user. |
| roles | [string](#string) | repeated | Roles is a list of role IDs that should be assigned to the user. |






<a name="permissions_service-v1-InheritedPermission"></a>

### InheritedPermission
an InheritedPermission is a permission that a principal has inherited from a role.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| permission | [Permission](#permissions_service-v1-Permission) |  |  |
| inherited_from | [string](#string) |  |  |






<a name="permissions_service-v1-InheritedRole"></a>

### InheritedRole
an InheritedRole is a role that a principal has inherited.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| role | [Role](#permissions_service-v1-Role) |  |  |
| inherited_from | [string](#string) |  |  |






<a name="permissions_service-v1-ListPermissionsRequest"></a>

### ListPermissionsRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the permissions belong to. |






<a name="permissions_service-v1-ListPermissionsResponse"></a>

### ListPermissionsResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| permissions | [Permission](#permissions_service-v1-Permission) | repeated |  |






<a name="permissions_service-v1-ListPrincipalsRequest"></a>

### ListPrincipalsRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the principals belong to. |






<a name="permissions_service-v1-ListPrincipalsResponse"></a>

### ListPrincipalsResponse
ListPrincipalsResponse is the response to the ListPrincipals request.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| principals | [string](#string) | repeated |  |






<a name="permissions_service-v1-ListRolesRequest"></a>

### ListRolesRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the roles belong to. |






<a name="permissions_service-v1-ListRolesResponse"></a>

### ListRolesResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| roles | [Role](#permissions_service-v1-Role) | repeated |  |






<a name="permissions_service-v1-MissingPermissions"></a>

### MissingPermissions



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| resource_uri | [string](#string) |  |  |
| missing_permissions | [string](#string) | repeated |  |






<a name="permissions_service-v1-Permission"></a>

### Permission
a Permission identifies an action that can be performed on a resource.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | ID is the unique identifier of the permission. |
| organisation_id | [string](#string) |  | OrganisationID is the unique identifier of the organisation that owns the permission. |
| name | [string](#string) |  | Name is the name of the permission. |
| description | [string](#string) |  | Description is the description of the permission. |
| project_name | [string](#string) |  | project_name is the name of the project that the permission belongs to. |






<a name="permissions_service-v1-PrincipalCountUpdatedEvent"></a>

### PrincipalCountUpdatedEvent
PrincipalCountUpdatedEvent is an event that is published when the number of unique principals in an organisation is updated.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| organisation_id | [string](#string) |  | OrganisationID is the unique identifier of the organisation that the principal count was updated for. |
| unique_principal_count | [int64](#int64) |  | UniquePrincipalCount is the new number of unique principals in the organisation. |






<a name="permissions_service-v1-RevokeUserPermissionsAndRolesOnResourceRequest"></a>

### RevokeUserPermissionsAndRolesOnResourceRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that grant belongs to. |
| user_id | [string](#string) |  | UserID is the unique identifier of the user. |
| resource_uri | [string](#string) |  | ResourceURI is the URI of the resource from which the user&#39;s permissions should be revoked. |
| permissions | [string](#string) | repeated | Permissions is a list of permission IDs that should be revoked from the user. |
| roles | [string](#string) | repeated | Roles is a list of role IDs that should be revoked from the user. |






<a name="permissions_service-v1-Role"></a>

### Role
a Role is a collection of permissions.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | ID is the unique identifier of the role. |
| organisation_id | [string](#string) |  | OrganisationID is the unique identifier of the organisation that owns the role. |
| name | [string](#string) |  | Name is the name of the role. |
| description | [string](#string) |  | Description is the description of the role. |
| permissions | [Permission](#permissions_service-v1-Permission) | repeated | Permissions is a list of permissions that the role contains. |
| project_name | [string](#string) |  | project_name is the name of the project that the role belongs to. |






<a name="permissions_service-v1-UpdatePermissionRequest"></a>

### UpdatePermissionRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the permission belongs to. |
| id | [string](#string) |  | ID is the unique identifier of the permission. |
| name | [string](#string) |  | Name is the name of the permission. |
| description | [string](#string) |  | Description is the description of the permission. |






<a name="permissions_service-v1-UpdateRoleRequest"></a>

### UpdateRoleRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| project_name | [string](#string) |  | project_name is the name of the project that the role belongs to. |
| id | [string](#string) |  | ID is the unique identifier of the role. |
| name | [string](#string) |  | Name is the name of the role. |
| description | [string](#string) |  | Description is the description of the role. |
| permissions | [string](#string) | repeated | Permissions is a list of permission IDs that the role has. |





 

 

 


<a name="permissions_service-v1-PermissionsService"></a>

### PermissionsService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| CreatePermission | [CreatePermissionRequest](#permissions_service-v1-CreatePermissionRequest) | [Permission](#permissions_service-v1-Permission) | CreatePermission creates a new permission. It is idempotent and will update the permission if it already exists. Required Permissions: - permission.create on /organisation/{organisation_id} |
| GetPermission | [GetPermissionRequest](#permissions_service-v1-GetPermissionRequest) | [Permission](#permissions_service-v1-Permission) | GetPermission returns a permission by ID. Required Permissions: - permission.get on /organisation/{organisation_id}/permission/{id} |
| UpdatePermission | [UpdatePermissionRequest](#permissions_service-v1-UpdatePermissionRequest) | [Permission](#permissions_service-v1-Permission) | UpdatePermission updates a permission. It will return not found if the permission does not exist. Required Permissions: - permission.update on /organisation/{organisation_id}/permission/{id} |
| DeletePermission | [DeletePermissionRequest](#permissions_service-v1-DeletePermissionRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | DeletePermission deletes a permission. It is idempotent and will return ok whether the permission existed or not. Required Permissions: - permission.delete on /organisation/{organisation_id}/permission/{id} |
| ListPermissions | [ListPermissionsRequest](#permissions_service-v1-ListPermissionsRequest) | [ListPermissionsResponse](#permissions_service-v1-ListPermissionsResponse) | ListPermissions returns a list of permissions. Required Permissions: - permission.list on /organisation/{organisation_id} |
| CreateRole | [CreateRoleRequest](#permissions_service-v1-CreateRoleRequest) | [Role](#permissions_service-v1-Role) | CreateRole creates a new role. It is idempotent and will update the role if it already exists. Required Permissions: - role.create on /organisation/{organisation_id} - permission.get on /organisation/{organisation_id}/permission/{permission_id} for each permission in the role |
| GetRole | [GetRoleRequest](#permissions_service-v1-GetRoleRequest) | [Role](#permissions_service-v1-Role) | GetRole returns a role by ID. Required Permissions: - role.get on /organisation/{organisation_id}/role/{id} |
| UpdateRole | [UpdateRoleRequest](#permissions_service-v1-UpdateRoleRequest) | [Role](#permissions_service-v1-Role) | UpdateRole updates a role. It will return not found if the role does not exist. Required Permissions: - role.update on /organisation/{organisation_id}/role/{id} |
| DeleteRole | [DeleteRoleRequest](#permissions_service-v1-DeleteRoleRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | DeleteRole deletes a role. It is idempotent and will return ok whether the role existed or not. Required Permissions: - role.delete on /organisation/{organisation_id}/role/{id} |
| ListRoles | [ListRolesRequest](#permissions_service-v1-ListRolesRequest) | [ListRolesResponse](#permissions_service-v1-ListRolesResponse) | ListRoles returns a list of roles. Required Permissions: - role.list on /organisation/{organisation_id} |
| GrantUserPermissionsAndRolesOnResource | [GrantUserPermissionsAndRolesOnResourceRequest](#permissions_service-v1-GrantUserPermissionsAndRolesOnResourceRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | GrantUserPermissionsAndRolesOnResource assigns permissions and roles to a user on a resource. It is additive and will not remove existing permissions or roles. Required Permissions: - permission.get on /organisation/{organisation_id}/permission/{permission_id} for each permission - role.get on /organisation/{organisation_id}/role/{role_id} for each role - principal.assignment.create on /organisation/{organisation_id}/principal/{user_id} |
| RevokeUserPermissionsAndRolesOnResource | [RevokeUserPermissionsAndRolesOnResourceRequest](#permissions_service-v1-RevokeUserPermissionsAndRolesOnResourceRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | RevokeUserPermissionsAndRolesOnResource revokes permissions and roles from a user on a resource. Required Permissions: - principal.assignment.delete on RevokeUserPermissionsAndRolesOnResourceRequest.resource_uri |
| GetUserPermissionsAndRolesOnResource | [GetUserPermissionsAndRolesOnResourceRequest](#permissions_service-v1-GetUserPermissionsAndRolesOnResourceRequest) | [GetUserPermissionsAndRolesOnResourceResponse](#permissions_service-v1-GetUserPermissionsAndRolesOnResourceResponse) | GetUserPermissionsAndRolesOnResource returns the permissions and roles assigned to a user on a resource. Required Permissions: - principal.assignment.get on GetUserPermissionsAndRolesOnResourceRequest.resource_uri |
| ListPrincipals | [ListPrincipalsRequest](#permissions_service-v1-ListPrincipalsRequest) | [ListPrincipalsResponse](#permissions_service-v1-ListPrincipalsResponse) | ListPrincipals returns a list of principals. Required Permissions: - principal.list on /organisation/{organisation_id} |
| GetAllAssignmentsForPrincipal | [GetAllAssignmentsForPrincipalRequest](#permissions_service-v1-GetAllAssignmentsForPrincipalRequest) | [GetAllAssignmentsForPrincipalResponse](#permissions_service-v1-GetAllAssignmentsForPrincipalResponse) | GetAllAssignmentsForPrincipal returns all assignments for a principal within an organisation. Required Permissions: - principal.assignment.list on /organisation/{organisation_id}/principal/{principal_id} |
| Check | [CheckPermissionRequest](#permissions_service-v1-CheckPermissionRequest) | [CheckPermissionResponse](#permissions_service-v1-CheckPermissionResponse) | Check checks if a principal has the specified permissions on the specified resources |

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

