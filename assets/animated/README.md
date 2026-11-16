# Premium Technology Motion Lab — 28 authentic SVG animations

Each technology retains its **original official brand paths, colors and proportions**. The logo is uniformly scaled inside its own `<g class="brand-art">` for composition; no nested brand SVG elements are changed. React uses the original unscaled logo. The technical vignette is a separate `<g class="tech-effect">` in the same 64 × 64 SVG.

## Motion system

- **Ambient (including GitHub README):** each icon carries its own low-intensity live SMIL/SVG process animation; the technology mark remains identifiable. GitHub's `<img>` does **not** forward hover into the SVG.
- **Gallery hover / keyboard focus:** `<object>` embedding supports document-local interactive state. The gallery mirrors parent card hover, keyboard focus, and pressed state into the embedded SVG root without animation loops.
- **Reduced motion:** CSS hides the entire moving effect layer, leaving the original logo visible. This prevents SMIL animation from causing motion to sensitive viewers.
- **Rendering:** no external network assets, scripts inside SVG, GIFs, videos, animation libraries or unbounded JavaScript loops. The 28 SVGs remain fully self-contained.

## Design inventory

| Brand | Dedicated technical vignette | Layout |
| --- | --- | --- |
| [C](./c.svg) | Low-level register addressing and instruction decode | left |
| [C++](./cpp.svg) | Parallel vector execution with an explicit synchronization barrier | top |
| [C#](./csharp.svg) | Component contracts are linked through a dependency architecture | right |
| [Go](./go.svg) | Three goroutines converge at a channel synchronization point | top |
| [Python](./python.svg) | An interpreter transforms parsed input through evaluation to output | right |
| [Rust](./rust.svg) | Owner value moves A→B; immutable borrow returns safely | left |
| [Kotlin](./kotlin.svg) | Coroutine flow suspends then resumes across a gradient transition | top |
| [Next.js](./next.svg) | Request passes through a router, selects a page and renders HTML | top |
| [Node.js](./nodejs.svg) | FIFO task queue feeds an event-loop dispatch and callback | right |
| [Java](./java.svg) | JVM executes bytecode by pushing and popping stack frames | left |
| [TypeScript](./typescript.svg) | Compile-time typed declaration passes validation before emitting JavaScript | top |
| [React Native](./react.svg) | Three calibrated elliptic electron trajectories aligned to the official React atom | center |
| [HTML](./html.svg) | A document tree expands from html to head/body elements | left |
| [CSS](./css.svg) | Cascade resolves overlapping rules into a computed visual style | right |
| [JavaScript](./javascript.svg) | The JavaScript runtime evaluates 5 + 10 into its result | right |
| [Vue](./vue.svg) | Reactive source propagates via computed state into an updated view | bottom |
| [TensorFlow](./tensorflow.svg) | A weighted neural net processes inputs across three inference layers | right |
| [Docker](./docker.svg) | Image layers stack into a container and transition to RUN | bottom |
| [MySQL](./mysql.svg) | SQL SELECT scans table rows and returns matching tuples | right |
| [PostgreSQL](./postgres.svg) | ACID transaction progresses BEGIN, WRITE, COMMIT and confirmation | bottom |
| [MongoDB](./mongodb.svg) | JSON-style documents stack; a selected document opens and returns | top |
| [GraphQL](./graphql.svg) | A typed graph query follows only selected field nodes | top |
| [SQLite](./sqlite.svg) | An embedded database writes then reads a local flash-memory region | left |
| [Git](./git.svg) | A clean commit DAG: main branch, feature divergence, commits and merge | bottom |
| [Linux](./linux.svg) | A true terminal prompt types ls and displays a directory listing | bottom |
| [Postman](./postman.svg) | Two-panel HTTP testing console with GET, request, response and 200 status | bottom |
| [FastAPI](./fastapi.svg) | An endpoint router matches GET /v1 and serializes a fast JSON reply | right |
| [REST API](./rest-api.svg) | Client/server topology with distinct request and response packets | bottom |

## Eight priority scenes

**Git:** directed acyclic commit graph with a persistent main branch, animated divergence, feature commits, and a true merge node. The branch highlight follows the merge path and uses a different accent from main.

**Postman:** a request editor with `GET`, a distinct response inspector, directional request/return lines, and an eventual `200` status. This is an API testing UI, deliberately unlike REST's architecture diagram.

**REST API:** a recognizable client box and server hardware endpoint, different request/response packet geometries, plus a server acknowledgement. The endpoint architecture is separate from Postman's testing interface.

**Linux:** a terminal window with title bar/traffic lights, a real `$ ls` prompt, character-by-character command reveal, a blinking block cursor, and directory output.

**JavaScript:** a yellow/black interpreter HUD that evaluates the exact expression `5+10` and produces `15` as a later runtime result. It is not Node's FIFO event loop.

**TypeScript:** typed source declaration with blue annotation, typed compiler stage, deferred check mark and JavaScript emission. It is separate from JavaScript's execution timeline.

**Rust:** structured owner A / owner B scopes, an ownership move, explicit immutable borrow and successful memory-safety acknowledgement.

**Next.js:** a request enters a deterministic routing selector, selects an application route and generates a page response via an SSR stage.

**React is the exclusive Electron Orbit.** Its ellipses are calibrated to the actual atom geometry (`rx≈21.875`, `ry≈8.34`, ±60°), with three electron+halo pairs on independent timelines. No other brand uses this trajectory.

## Preview and quality gates

Run the local gallery (from repository root):

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/assets/animated/preview.html`. Search/category filtering, responsive cards, a 48/64 px size switch and keyboard Tab/Enter/Space interactions are supported. Then run:

```bash
python3 tools/validate_animations.py
python3 -m pip install playwright pillow
python3 tools/visual_qa.py
```

The second command drives a real Chrome/Chromium browser to test **all 28** SVG embeds, ambient animation without hover, eight critical logos at **48 and 64 pixels**, hover, focus, active interaction, mobile overflow and `prefers-reduced-motion`. The CI workflow uploads a visual contact sheet and detailed test results as GitHub Actions artifacts. Visual output is never committed to the profile's production assets.

## Limitations

At 48 px, detailed labels are intentionally abbreviated; inspect the 64 px gallery for legibility and full diagrams. GitHub Profile README `img` embeds render the ambient loop only; a GitHub-hosted static README cannot forward pointer or keyboard events into external SVGs. Native SMIL/CSS support depends on the rendering environment; evergreen Chromium-based browsers support the preview, while some SVG converters produce only the static SVG state.

The original brand artwork retains its original license terms in [SKILL-ICONS-LICENSE.txt](./SKILL-ICONS-LICENSE.txt).
