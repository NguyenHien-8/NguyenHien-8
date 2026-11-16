# Meaningful animated icons

The **28 brand logos stay unchanged**, while every icon now has its **own animation** inspired by the technology's function. The README uses locally hosted SVG files, with no animated icon service, JavaScript, or remote runtime dependency.

## Individual motion designs

| Icon | Motion metaphor |
|---|---|
| C | Compiler scans instruction blocks |
| C++ | Plus symbols increment and a build indicator advances |
| C# | Four sharp grid lines light up in succession |
| Go | Fast horizontal motion streaks |
| Python | Blue/yellow data trails intertwine like two snakes |
| Rust | A mechanical outer gear rotates |
| Kotlin | A diagonal, colorful multiplatform transition |
| Next.js | Screen/page transition sliding in |
| Node.js | Asynchronous event packet visiting connected nodes |
| Java | Rising steam from a cup |
| TypeScript | Typing cursor and compiled editor tokens |
| React Native | An electron orbits the component atom |
| HTML | Markup angle brackets are drawn in |
| CSS | Style layers cascade in sequence |
| JavaScript | Runtime console executes and the cursor blinks |
| Vue | Nested V-shaped layers expand progressively |
| TensorFlow | Data tensors flow through a branching compute graph |
| Docker | Shipping containers stack above a dock |
| MySQL | Water current and bubbles by the dolphin |
| PostgreSQL | Query rows arrive and are committed |
| MongoDB | Leaf stem grows and leaf gently sways |
| GraphQL | Query signals flow around connected graph vertices |
| SQLite | Quill draws a writing/query stroke |
| Git | Commit dots diverge and merge across branches |
| Linux | Shell prompt types a command |
| Postman | Request and response arrows go in opposite directions |
| FastAPI | A lightning pulse runs down a bolt |
| REST API | Two-way HTTP packets and an activity/status trace |

## Files and customization

- All icon files: `assets/animated/*.svg`.
- Each icon displays at 48x48 in the profile README but has a native 64x64 SVG canvas.
- The original brand logo is a nested `<svg x="4" width="56" y="4" height="56" ...>` element. Preserve this embedded element for authentic branding.
- Change the `dur` values on `<animate>`, `<animateTransform>`, and `<animateMotion>` to tune the specific motion.
- To make an animation more understated, reduce stroke or fill `opacity` on the *overlay* elements.
- The animations are powered by native SVG SMIL syntax and require no JavaScript.

## Compatibility

The profile README embeds the SVGs using `<img>`. Modern browsers generally support SVG SMIL animation, but GitHub's image proxy and some clients can display a still frame. Reduced-motion or animation-blocking settings can also suppress movement. If guaranteed playback in all GitHub surfaces is required, rasterize these SVGs to locally hosted animated GIF/APNG assets.

## Attribution

The 27 original skill logos are from [tandpfun/skill-icons](https://github.com/tandpfun/skill-icons), MIT-licensed. The REST API pictogram is local. See [SKILL-ICONS-LICENSE.txt](./SKILL-ICONS-LICENSE.txt) for the source license. The custom function-inspired effects added here are separate from the original logos; logos and marks remain the property of their respective owners.
