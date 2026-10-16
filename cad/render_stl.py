#!/usr/bin/env python3
"""
Dependency-light STL renderer for product, section and exploded views (numpy + PIL).

Per-pixel depth buffer (correct for thin fins and overlapping parts), per-triangle flat
shading with two lights, 2x supersampling, orthographic projection.

Usage (as a library):
    from render_stl import Scene
    s = Scene(width=1600, height=1100, view=(35, 30))          # azimuth, elevation in degrees
    s.add("core.stl", color=(184, 115, 51))                     # copper
    s.add("cap.stl", color=(200, 130, 70), offset=(0, 0, 25))   # exploded upward
    s.render("exploded.png", caption="PRISM-15 Rev A, exploded")
"""
from __future__ import annotations

import math
import struct
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def read_stl(path: str) -> np.ndarray:
    """Return (n, 3, 3) float32 triangle vertices from a binary or ASCII STL."""
    with open(path, "rb") as f:
        head = f.read(84)
        if len(head) < 84:
            raise ValueError("STL too short")
        n = struct.unpack("<I", head[80:84])[0]
        f.seek(0, 2)
        size = f.tell()
        if size == 84 + 50 * n:
            f.seek(84)
            data = np.frombuffer(f.read(50 * n), dtype=np.uint8).reshape(n, 50)
            tri = data[:, 12:48].copy().view("<f4").reshape(n, 3, 3)
            return tri.astype(np.float32)
    verts = []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if s.startswith("vertex"):
                verts.append([float(v) for v in s.split()[1:4]])
    return np.array(verts, dtype=np.float32).reshape(-1, 3, 3)


def view_matrix(azimuth_deg: float, elevation_deg: float) -> np.ndarray:
    """World (x right, y back, z up) -> camera. Camera looks along -y_cam; screen = (x_cam, z_cam)."""
    az, el = math.radians(azimuth_deg), math.radians(elevation_deg)
    rz = np.array([[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]])
    rx = np.array([[1, 0, 0], [0, math.cos(el), -math.sin(el)], [0, math.sin(el), math.cos(el)]])
    return rx @ rz


class Scene:
    def __init__(self, width=1600, height=1100, view=(35.0, 28.0), background=(252, 252, 251), supersample=2):
        self.w, self.h, self.ss = width, height, supersample
        self.view = view
        self.bg = background
        self.parts = []
        # lights are defined in CAMERA space (x right, y into the screen, z up): from the upper left front
        self.light = np.array([-0.4, -0.6, 0.7]); self.light /= np.linalg.norm(self.light)
        self.light2 = np.array([0.6, -0.3, 0.3]); self.light2 /= np.linalg.norm(self.light2)
        self.fit = None   # optional (xy_min, xy_max) in camera screen units to share framing between renders

    def add(self, path_or_tris, color=(184, 115, 51), offset=(0, 0, 0), scale=1.0, clip=None):
        """clip = ((x0,y0,z0),(x1,y1,z1)) keeps only triangles whose centroid lies inside the world box."""
        tris = read_stl(path_or_tris) if isinstance(path_or_tris, str) else np.asarray(path_or_tris, dtype=np.float32)
        if clip is not None:
            lo, hi = np.asarray(clip[0], dtype=np.float32), np.asarray(clip[1], dtype=np.float32)
            inside = np.all((tris >= lo) & (tris <= hi), axis=(1, 2))      # every vertex inside: no straddling streaks
            tris = tris[inside]
        tris = tris * scale + np.asarray(offset, dtype=np.float32)
        self.parts.append((tris, tuple(color)))
        return self

    def _project(self):
        R = view_matrix(*self.view)
        lr, lr2 = self.light, self.light2
        out = []
        for tris, color in self.parts:
            if len(tris) == 0:
                continue
            cam = tris @ R.T
            nv = np.cross(cam[:, 1] - cam[:, 0], cam[:, 2] - cam[:, 0])
            nn = np.linalg.norm(nv, axis=1)
            keep = nn > 1e-9
            cam, nv = cam[keep], nv[keep] / nn[keep][:, None]
            facing = nv[:, 1] < 0            # camera sits at -y_cam looking toward +y_cam: visible normals have y_cam < 0
            cam, nv = cam[facing], nv[facing]
            lam = np.clip(nv @ lr, 0, 1) * 0.70 + np.clip(nv @ lr2, 0, 1) * 0.30 + 0.22
            rgb = np.clip(np.asarray(color, dtype=np.float32)[None, :] * np.clip(lam, 0, 1.05)[:, None], 0, 255)
            out.append((cam, rgb.astype(np.uint8)))
        return out

    def render(self, out_path: str, caption: str | None = None, margin=0.06, verbose=False):
        t0 = time.time()
        W, H = self.w * self.ss, self.h * self.ss
        proj = self._project()
        if not proj:
            raise ValueError("nothing to render")
        allxy = np.concatenate([c[:, :, [0, 2]].reshape(-1, 2) for c, _ in proj])
        if self.fit is None:
            mn, mx = allxy.min(axis=0), allxy.max(axis=0)
        else:
            mn, mx = np.asarray(self.fit[0]), np.asarray(self.fit[1])
        span = mx - mn
        sc = min((1 - 2 * margin) * W / max(span[0], 1e-6), (1 - 2 * margin) * H / max(span[1], 1e-6))
        ctr = (mn + mx) / 2
        zbuf = np.full((H, W), np.inf, dtype=np.float32)      # depth = y_cam (smaller = nearer)
        img = np.empty((H, W, 3), dtype=np.uint8); img[:] = self.bg
        ntri = 0
        for cam, rgb in proj:
            px = (cam[:, :, 0] - ctr[0]) * sc + W / 2
            py = H / 2 - (cam[:, :, 2] - ctr[1]) * sc
            dz = cam[:, :, 1]
            x0 = np.clip(np.floor(px.min(axis=1)).astype(int), 0, W - 1)
            x1 = np.clip(np.ceil(px.max(axis=1)).astype(int), 0, W - 1)
            y0 = np.clip(np.floor(py.min(axis=1)).astype(int), 0, H - 1)
            y1 = np.clip(np.ceil(py.max(axis=1)).astype(int), 0, H - 1)
            # draw larger triangles first is irrelevant with a z-buffer; iterate
            for i in range(len(cam)):
                xa, xb, ya, yb = x0[i], x1[i], y0[i], y1[i]
                if xb < xa or yb < ya:
                    continue
                xs = np.arange(xa, xb + 1, dtype=np.float32) + 0.5
                ys = np.arange(ya, yb + 1, dtype=np.float32) + 0.5
                X, Y = np.meshgrid(xs, ys)
                (ax, ay), (bx, by), (cx, cy) = (px[i, 0], py[i, 0]), (px[i, 1], py[i, 1]), (px[i, 2], py[i, 2])
                det = (bx - ax) * (cy - ay) - (cx - ax) * (by - ay)
                if abs(det) < 1e-9:
                    continue
                l1 = ((bx - X) * (cy - Y) - (cx - X) * (by - Y)) / det
                l2 = ((cx - X) * (ay - Y) - (ax - X) * (cy - Y)) / det
                l3 = 1 - l1 - l2
                eps = -1e-4
                mask = (l1 >= eps) & (l2 >= eps) & (l3 >= eps)
                if not mask.any():
                    continue
                depth = l1 * dz[i, 0] + l2 * dz[i, 1] + l3 * dz[i, 2]
                sub = zbuf[ya:yb + 1, xa:xb + 1]
                upd = mask & (depth < sub)
                if upd.any():
                    sub[upd] = depth[upd]
                    img[ya:yb + 1, xa:xb + 1][upd] = rgb[i]
                ntri += 1
        im = Image.fromarray(img).resize((self.w, self.h), Image.LANCZOS)
        if caption:
            d = ImageDraw.Draw(im)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
            except Exception:
                font = ImageFont.load_default()
            d.text((24, self.h - 40), caption, fill=(60, 60, 60), font=font)
        im.save(out_path)
        if verbose:
            print(f"rendered {out_path}: {ntri} tris in {time.time()-t0:.1f}s", flush=True)
        return out_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: render_stl.py out.png file1.stl [file2.stl ...]")
        sys.exit(1)
    s = Scene()
    for p in sys.argv[2:]:
        s.add(p)
    s.render(sys.argv[1], verbose=True)
