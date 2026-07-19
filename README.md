# dcc-ai-openai-image

<p align="center">
  <img src="docs/assets/dcc-ai-openai-image.svg" alt="DCC-MCP · OPENAI-IMAGE" width="600">
</p>

## Agent workflow

AI agents should use installed package skills through the shared gateway. IDE
users may continue to use the MCP endpoint.

### Install or update the CLI

`dcc-mcp-cli` is the preferred control path for every shell-capable agent. If
it is missing, ask the user before installing the latest official release:

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/dcc-mcp/dcc-mcp-core/main/scripts/install-cli.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/dcc-mcp/dcc-mcp-core/main/scripts/install-cli.ps1 | iex"
```

Keep an official build current through the release manifest:

```bash
dcc-mcp-cli update check
dcc-mcp-cli update apply
```

`update apply` downloads and stages the latest CLI for the next launch. It
does not update a running `dcc-mcp-server`; update that server in its own
environment.

```bash
dcc-mcp-cli dcc-types
dcc-mcp-cli list
dcc-mcp-cli search --query "<task>" --dcc-type <host>
dcc-mcp-cli describe <tool-slug>
dcc-mcp-cli call <tool-slug> --json '{"key":"value"}'
```

If the package skill is not active, call
`dcc-mcp-cli load-skill <skill-name> --dcc-type <host>`. After the task,
query `dcc-mcp-cli stats --range 24h --session-id <task-id>` and pass only
bounded evidence to the `review_skill_improvement` prompt from
`dcc-mcp-skills-creator`.


OpenAI image generation and editing for DCC texture workflows. The skill stays
DCC-neutral: it writes an image and returns an `AssetDescriptor`; Maya,
Blender, Houdini, 3ds Max, Unreal, or another adapter owns UVs, baking, material
creation, and scene import.

![Generated texture source handed off for DCC material binding](docs/images/dcc-ai-openai-image-showcase.webp)

## Workflow

```mermaid
flowchart LR
    P[Prompt or reference] --> G[GPT Image]
    G --> A[AssetDescriptor]
    A --> U[DCC UV and bake]
    U --> M[Material binding]
```

## Install

```bash
pip install -e .
set OPENAI_API_KEY=your-key
```

Load `skill/openai-image-textures`, then call:

- `openai-image-textures__generate_texture_source`
- `openai-image-textures__edit_texture_source`

Generated images are creative source material. Derive normal, roughness,
metalness, height, and other physically meaningful maps through DCC baking or
a deterministic texture pipeline.

