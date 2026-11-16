#!/usr/bin/env python3
"""Check the 28 standalone animated brand SVGs (Python standard library only)."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parents[1] / "assets" / "animated"
IDS = ["c","cpp","csharp","go","python","rust","kotlin","next","nodejs","java","typescript","react","html","css","javascript","vue","tensorflow","docker","mysql","postgres","mongodb","graphql","sqlite","git","linux","postman","fastapi","rest-api"]
SVG = "{http://www.w3.org/2000/svg}"
BAD = {"script", "foreignObject", "image"}
errors = []
assets = sorted(p.stem for p in BASE.glob("*.svg"))
if sorted(IDS) != assets:
    errors.append(f"SVG inventory mismatch. Missing: {sorted(set(IDS)-set(assets))}; Extra: {sorted(set(assets)-set(IDS))}")
descriptions = set()
for name in IDS:
    path = BASE / f"{name}.svg"
    if not path.exists():
        continue
    source = path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        errors.append(f"{name}: invalid XML: {exc}")
        continue
    if root.tag != SVG+"svg" or root.get("viewBox") != "0 0 64 64":
        errors.append(f"{name}: SVG root or viewBox is incorrect")
    brands = [child for child in root if child.tag == SVG+"svg"]
    effects = [child for child in root if child.tag == SVG+"g" and child.get("class") == "tech-effect"]
    if len(brands) != 1 or len(effects) != 1:
        errors.append(f"{name}: expected one unchanged nested brand SVG and one tech-effect group")
        continue
    desc = root.find(SVG+"desc")
    if desc is None or not (desc.text or "").strip():
        errors.append(f"{name}: missing accessible description")
    elif desc.text in descriptions:
        errors.append(f"{name}: description reused")
    else:
        descriptions.add(desc.text)
    style = root.find(SVG+"style")
    if style is None or "prefers-reduced-motion:reduce" not in (style.text or "") or ":root:hover" not in (style.text or ""):
        errors.append(f"{name}: reduced-motion or interactive visibility CSS absent")
    animated = [n for n in effects[0].iter() if n.tag in {SVG+"animate",SVG+"animateMotion",SVG+"animateTransform"}]
    if not animated:
        errors.append(f"{name}: no animated semantic layer")
    if name == "react":
        if len(list(effects[0].iter(SVG+"animateMotion"))) != 6:
            errors.append("react: require exactly 3 electron+halo pairs following atomic ellipses")
        if any("21.86 8.34" not in (n.get("path") or "") for n in effects[0].iter(SVG+"animateMotion")):
            errors.append("react: electron path does not match branded ellipse")
    if name != "react" and "electron" in (desc.text or "").lower():
        errors.append(f"{name}: React-only electron language appears outside React")
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] in BAD:
            errors.append(f"{name}: disallowed SVG node {node.tag}")
        for value in node.attrib.values():
            if "javascript:" in value.lower() or "http://" in value.lower() or "https://" in value.lower():
                errors.append(f"{name}: external or unsafe reference detected")
if errors:
    print("\n".join("FAIL: " + e for e in errors), file=sys.stderr)
    sys.exit(1)
print(f"PASS: {len(IDS)} branded SVGs, unique overlays, reduced motion, React-only electron orbits.")
