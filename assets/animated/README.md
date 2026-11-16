# Semantic Technology Logo Animations

All **28 original brand marks** are retained inside their original nested SVG elements. The surrounding independent SVG layer named `tech-effect` contains the domain-specific visual motion. No external animation assets, JavaScript frame loops, GIFs, fonts or external network dependencies are used.

## Animation inventory

| Technology | Motion concept |
| --- | --- |
| [C](./c.svg) | Binary memory registers and instruction bus |
| [C++](./cpp.svg) | Directed high-performance execution lanes |
| [C#](./csharp.svg) | Layered software dependency architecture |
| [Go](./go.svg) | Concurrent goroutines rendezvous |
| [Python](./python.svg) | Sequential data transformation pipeline |
| [Rust](./rust.svg) | Ownership and borrow boundaries |
| [Kotlin](./kotlin.svg) | Modern gradient language flow |
| [Next.js](./next.svg) | Server routing and content distribution |
| [Node.js](./nodejs.svg) | Event-loop dispatch and callbacks |
| [Java](./java.svg) | JVM bytecode stack execution |
| [TypeScript](./typescript.svg) | Static type checks and validation |
| [React Native](./react.svg) | Electron orbit aligned to official atomic logo |
| [HTML](./html.svg) | Top-down document rendering |
| [CSS](./css.svg) | Cascading styles and interface layers |
| [JavaScript](./javascript.svg) | Dynamic instruction evaluation |
| [Vue](./vue.svg) | Reactive state-to-view propagation |
| [TensorFlow](./tensorflow.svg) | Neural-network forward inference |
| [Docker](./docker.svg) | Container image lifecycle |
| [MySQL](./mysql.svg) | Relational query row selection |
| [PostgreSQL](./postgres.svg) | Ordered transaction and commit |
| [MongoDB](./mongodb.svg) | Document-oriented storage |
| [GraphQL](./graphql.svg) | Selective graph query traversal |
| [SQLite](./sqlite.svg) | Embedded data read and write |
| [Git](./git.svg) | Version branching and merge |
| [Linux](./linux.svg) | Terminal command execution |
| [Postman](./postman.svg) | HTTP request, response and acknowledgement |
| [FastAPI](./fastapi.svg) | Fast API endpoint processing |
| [REST API](./rest-api.svg) | Client-server request and response |

**React is the only electron-orbit design.** Its three moving electrons follow ellipses matching the original logo's scaled radii and orientations (0°, +60°, −60°), instead of an unrelated circle outside the brand artwork. Node.js uses a distinct event-loop processing indicator, never an electron.

## Interaction and accessibility

- **Default:** Lightweight, deliberately low-opacity SVG motion; the logo remains visually dominant.
- **Hover/focus:** `tech-effect` fades toward full visibility without resizing the official artwork, where the embed environment delivers these events.
- **Active:** Higher visibility without any layout shift, where supported.
- **Reduced motion:** `prefers-reduced-motion: reduce` suppresses the animated effect layer; the official brand stays visible.
- **No hover inside GitHub README images:** GitHub Profile READMEs render embedded SVGs as `<img>`; the image cannot forward pointer events into its internal SVG. Therefore the README uses subtle ambient motion. This limitation cannot be eliminated with CSS inside an externally embedded image.

## Interactive gallery (local)

To inspect all 28 hover states, serve this repository locally (from the repository root):

```bash
python3 -m http.server 8000
```

Then visit **http://localhost:8000/assets/animated/preview.html**. The gallery uses native `<object>` embedding, supports keyboard focus, search, categories and responsive layout. No application framework is required.

## Maintenance

- Edit the **effect overlay** after the original nested brand `<svg>`; never edit the original brand paths or brand colors.
- Each SVG has its own self-contained timing and semantic choreography.
- Keep logo dimensions and 64×64 `viewBox` consistent.
- Validate before committing with `python3 tools/validate_animations.py`.

Brand SVG artwork is covered by [the preserved asset license](./SKILL-ICONS-LICENSE.txt). The added animation overlays are project-specific code.
