!!! info "API hosts"

    | Environment | Base URL |
    | --- | --- |
    | Production | `https://temp-api.perms.io` |
    | Development | `https://dev-api.perms.io` |

    Production will move to `https://api.perms.io`. The examples on this site read the host from a
    `PERMIO_API` shell variable, so you only need to change it in one place:

    ```bash
    export PERMIO_API=https://temp-api.perms.io
    export PERMIO_API_KEY=perms_...   # your API key
    ```
