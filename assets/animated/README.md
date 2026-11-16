# Custom animated technology icons

These 28 SVGs are original, locally hosted artwork for this GitHub profile README. Every icon contains its own vector artwork, gradient, rotating arc, pulsing accents, and subtle floating motion. No JavaScript, external images, animated-icon service, network requests, or third-party runtime dependency is used.

## Edit icons
- Open any `*.svg` in a text editor. The color appears as hexadecimal `fill` / `stroke` values.
- Adjust SVG `animateTransform` `dur`, `values` and `begin` to customize motion. They use native browser SMIL animation.
- The README references these files locally as `./assets/animated/<name>.svg`.
- Every SVG is 64 × 64 and is displayed at 48 × 48 in the README.

## Compatibility
SVG motion generally works in modern browsers. GitHub and its image proxy may show a static frame for some users or environments; browsers with reduced-motion or animation-blocking settings may also suppress motion. If guaranteed autoplay across every GitHub client is a strict requirement, pre-render the animated SVG icons to GIF or APNG and point README images to those assets. No external runtime service is needed.
