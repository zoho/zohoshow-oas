# Zoho Show OpenAPI Specification (OAS) v1

OpenAPI 3.1 specifications for the [Zoho Show](https://www.zoho.com/show/) REST API.

Use these files to explore the API, generate a client SDK in your language, or
drive Show from a tool that speaks OpenAPI.

---

## Repository structure

```
openapi.json             the whole API in one document; identical to
                         v1/bundled/show-api.json

v1/
  index.json             machine-readable catalogue of every document below

  bundled/
    show-api.json        every operation, in one document
    README.md            when to use it, and when not to

  presentation.json      Create, read and manage presentations
  members-sharing.json   Sharing and member roles
  publish.json           Publish settings
  workspace.json         Workspaces available to the caller
  themes.json            Themes and templates

  slides.json            Insert, update, reorder and remove slides
  masters.json           Slide masters
  layouts.json           Master layouts
  shapes.json            Shapes in a slide, master or layout
  connectors.json        Connectors between objects
  group-shapes.json      Group and ungroup shapes
  text.json              Text content of an object
  tables.json            Tables, rows, columns and cells
  media.json             Pictures, videos and audio
  flowchart.json         Flowcharts on a slide

python/
  sample_api_runner.py   authenticate and call the API, end to end
  requirements.txt       the one dependency the sample needs
```

**Every file is a complete, standalone OpenAPI document.** It carries its own
`servers`, `securitySchemes`, and exactly the component schemas its own
operations need, so you can import any one of them on its own without
resolving references into the others.

### Which file do I want?

| You want | Use |
|---|---|
| a client for one area of the API | that area's document, e.g. `v1/slides.json` |
| a client for the whole API | `openapi.json` (same file as `v1/bundled/show-api.json`) |
| to decide without opening them | `v1/index.json`: every document with its operation and schema counts |

`bundled/show-api.json` (and the identical root `openapi.json`) is the **same
operations** as the per-resource documents, collected into one file. Generate from the bundle *or* from the per-resource
documents, not both, or you will get two copies of every shared type. That is
why it sits in its own directory rather than beside them.

---

## Concepts

Almost every path starts from a presentation. Slides, and the objects on a
slide, a master or a layout, hang below it:

```
/api/v1/presentation/{presentation_id}/slides/{slide_id}/...
/api/v1/presentation/{presentation_id}/{container_type}/{container_id}/shapes
```

`{container_type}` / `{container_id}` name the slide, master or layout that
holds the object.

---

## Getting started

### 1. Explore the spec

Import any file into [Swagger Editor](https://editor.swagger.io),
[Swagger API Hub](https://support.smartbear.com/swaggerhub/), or Postman,
paste the raw URL of the file, or upload it directly.

### 2. Pick your data centre

Every document lists one server per data centre, for example
`https://show.zoho.com` (US) and `https://show.zoho.in` (IN). Choose the one
you sign in on.

### 3. Authenticate

Show uses OAuth 2.0 (authorization code grant) through Zoho Accounts. Register
a client at the [Zoho API Console](https://api-console.zoho.com) to get a
**Client ID** and **Client Secret**, then exchange an authorization code for a
**refresh token**.

The spec's `authorizationUrl` and `tokenUrl` point at `accounts.zoho.com`, the
US data centre. For another data centre keep the paths and substitute the host.
The mapping is published on the security scheme as `x-show-accounts-hosts`, so a
client can read it rather than guess. Canada authorises at
`accounts.zohocloud.ca`, not `accounts.zoho.ca`. An OAuth client is valid only
in the data centre it was registered in, so register at your own data centre's
API console.

Scopes are named `ZohoShow.<resource>.<ACTION>`, for example
`ZohoShow.showdocslist.READ`. **Each operation declares the scopes it accepts
under `security`; request only those.** Reading them out of the spec is more
reliable than guessing from the path.

### 4. Generate an SDK

Any OpenAPI 3.1 generator works. With
[openapi-generator](https://openapi-generator.tech):

```bash
openapi-generator generate \
  -i v1/bundled/show-api.json \
  -g python \
  -o ./show-python-sdk
```

Swap `-g` for `java`, `typescript-axios`, `go`, and so on. To generate a
smaller client for one area, point `-i` at that area's file instead.

### 5. Run the sample

`python/sample_api_runner.py` shows the full loop: refresh the access token and
call the API. See the comments at the top of the file for setup.

---

## Reading the spec

**Every operation declares its type.** `x-mcp-operation-type` is published on
all 67 operations, so a tool can tell reads from writes without inferring it
from the HTTP verb.

**Errors are modelled.** Operations declare `400`, `429` and `500` responses.

**Response payloads are not typed yet.** Success responses reference a shared
`SuccessfulResponse`; the body under it is left unconstrained rather than
guessed, so a generated client returns a loosely-typed object.

---

## Versioning

Specs are versioned by directory. `v1/` tracks the v1 API; a future major
version lands beside it as `v2/` rather than replacing it.

---

## Licence

Apache License 2.0, see [LICENSE](LICENSE). You are free to use these
specifications, and any client code you generate from them, in your own
projects.

---

## Support

Full API documentation: <https://www.zoho.com/show/doc/>

Please report anything in these specifications that looks wrong against the
documentation site above.
