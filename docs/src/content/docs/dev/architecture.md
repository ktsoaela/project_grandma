---
title: Architecture
description: High-level architecture of Project Grandma
---

Project Grandma uses Electron for UI and Python for the recording engine. Communications flow through an HTTP API between the Electron frontend and Python backend.

```mermaid
flowchart LR
  subgraph Frontend["Electron (grandama)"]
    A[Main Process]
    B[Renderer / UI]
    C[Click Circle UI]
  end

  subgraph Backend["Python (recorder)"]
    D[Flask API]
    E[Capture / Screenshots]
    F[Click Circle on Screenshot]
  end

  A <-->|HTTP| D
  B --> C
  E --> F
  D --> E
```

See [Building from Source](/dev/build/) for implementation details.
