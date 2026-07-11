---
name: openai-image-textures
description: Asset-provider skill for generating and editing DCC texture source images with OpenAI. Use for albedo concepts, decals, and local texture repair. Not for physically accurate PBR map derivation.
license: MIT
compatibility: "dcc-mcp-core 0.19+, Python 3.9+"
metadata:
  dcc-mcp:
    dcc: python
    layer: domain
    stage: authoring
    version: "0.1.0"
    tags: [openai, image, texture, albedo, decal, asset-provider]
    search-hint: "generate texture source, edit texture, create albedo concept, texture decal, OpenAI image"
    produces: [asset_descriptor]
    tools: tools.yaml
---

# OpenAI Image Textures

Generate or edit a texture source image, then pass the returned
`asset_descriptor` to the target DCC. Keep PBR channel derivation, UV layout,
baking, and scene mutation in deterministic host or texture-pipeline skills.

