# Animated technology icons — authentic logos

All **28 icons** are embedded locally in this repository. The **original, recognizable brand logos** (27 assets) were sourced from [Skill Icons by tandpfun](https://github.com/tandpfun/skill-icons), distributed under the MIT license. The REST API icon is a local pictogram created for this profile.

## Design

- The brand artwork, colors, proportions and original logo tile backgrounds are preserved.
- Animation lives around the logo: a small floating movement, breathing glow, gentle shine, and a tiny revolving highlight on the outer border.
- Every icon is a single self-contained SVG containing its own original logo artwork, rather than requesting any image from a CDN.
- The HTML table in the profile README references `./assets/animated/*.svg` and displays them at 48 x 48.

## Customization

Each icon's SVG uses declarative SVG `animate` / `animateTransform`, without any JavaScript. Edit `dur` (seconds) for animation speed, `begin` for a start offset, `stroke-opacity` for the orbit's subtlety, and `opacity` on the shine overlay for brightness. The nested 56x56 SVG holds the original logo. **Do not edit it** if you want to preserve logo fidelity.

## Browser & GitHub support

Modern browsers support these animations, but GitHub's image proxy and some clients may render SVGs differently or show a still frame. Reduced-motion preferences or browser settings can also suppress animation. If motion is not displayed in your GitHub client, pre-render local GIF/APNG assets using the same original SVGs rather than depending on an outside animation service.

## Attribution

See [SKILL-ICONS-LICENSE.txt](./SKILL-ICONS-LICENSE.txt) for the MIT license and required copyright notice. All third-party brand logos belong to their respective owners. The extra motion composition in this repository is custom work.
