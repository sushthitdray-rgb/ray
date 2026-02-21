 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/cute_cartoon_video.py b/cute_cartoon_video.py
new file mode 100644
index 0000000000000000000000000000000000000000..1f886978fd97ba2f17c00ce6a6eb73412f9c9a6b
--- /dev/null
+++ b/cute_cartoon_video.py
@@ -0,0 +1,123 @@
+from pathlib import Path
+import importlib.util
+import sys
+
+
+def missing_packages():
+    required = ("moviepy", "numpy", "PIL")
+    return [pkg for pkg in required if importlib.util.find_spec(pkg) is None]
+
+
+def main() -> int:
+    missing = missing_packages()
+    if missing:
+        print(
+            "Missing required packages: "
+            + ", ".join(missing)
+            + ". Install them with: pip install moviepy numpy pillow"
+        )
+        return 1
+
+    from moviepy.editor import AudioClip, AudioFileClip, VideoClip
+    import numpy as np
+    from PIL import Image, ImageDraw, ImageFont, ImageFilter
+
+    # FILES
+    image_path = "your_image.png"     # Replace with your image
+    music_path = "firfirey.mp3"       # Add song file yourself
+    output_path = "Cute_Cartoon_Love.mp4"
+
+    duration = 15
+    fps = 24
+    resolution = (1080, 1080)  # Instagram square
+
+    def ensure_demo_image(path: Path) -> None:
+        """Create a simple fallback image when no input image is provided."""
+        if path.exists():
+            return
+
+        img = Image.new("RGB", (800, 600), (255, 206, 226))
+        draw = ImageDraw.Draw(img)
+        draw.ellipse((180, 110, 620, 550), fill=(255, 173, 204), outline=(255, 105, 180), width=8)
+        draw.text((230, 250), "Your Love Photo", fill=(255, 255, 255))
+        img.save(path)
+
+    def ensure_demo_audio(path: Path, clip_duration: int) -> None:
+        """Create a soft fallback soundtrack when no music file is provided."""
+        if path.exists():
+            return
+
+        def tone(t):
+            return 0.05 * np.sin(2 * np.pi * 220 * t)
+
+        tone_clip = AudioClip(tone, duration=clip_duration, fps=44100)
+        tone_clip.write_audiofile(path.as_posix(), fps=44100, logger=None)
+        tone_clip.close()
+
+    ensure_demo_image(Path(image_path))
+    ensure_demo_audio(Path(music_path), duration)
+
+    base_image = Image.open(image_path).convert("RGBA")
+    base_image = base_image.resize((800, 600))
+
+    def make_frame(t):
+        zoom = 1 + 0.02 * np.sin(t)
+        img = base_image.resize((int(800 * zoom), int(600 * zoom)))
+
+        # Cartoon soft blur glow
+        img = img.filter(ImageFilter.SMOOTH_MORE)
+
+        frame = Image.new("RGBA", resolution, (255, 220, 235))
+        x = (resolution[0] - img.width) // 2
+        y = (resolution[1] - img.height) // 2
+        frame.paste(img, (x, y))
+
+        draw = ImageDraw.Draw(frame)
+
+        try:
+            font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
+            font_small = ImageFont.truetype("DejaVuSans-Bold.ttf", 45)
+        except OSError:
+            font_big = ImageFont.load_default()
+            font_small = ImageFont.load_default()
+
+        # Dialogue timing
+        if 2 < t < 6:
+            draw.text(
+                (150, 100),
+                "Will we be together\\nwhen we grow up? 💭",
+                fill="white",
+                font=font_small,
+            )
+
+        if 7 < t < 12:
+            draw.text(
+                (120, 800),
+                "Let destiny decide.\\nI will ask you again someday 💍✨",
+                fill=(255, 105, 180),
+                font=font_big,
+            )
+
+        # Floating hearts
+        for i in range(8):
+            heart_x = int((t * 100 + i * 120) % resolution[0])
+            heart_y = int(resolution[1] - (t * 80 + i * 60) % resolution[1])
+            draw.text((heart_x, heart_y), "💖", fill=(255, 120, 170), font=font_small)
+
+        return np.array(frame)
+
+    video = VideoClip(make_frame, duration=duration)
+
+    # Add music (trim to video duration)
+    audio = AudioFileClip(music_path).subclip(0, duration)
+    video = video.set_audio(audio)
+
+    video.write_videofile(output_path, fps=fps)
+
+    video.close()
+    audio.close()
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
 
EOF
)
