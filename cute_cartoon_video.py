from moviepy.editor import AudioFileClip, VideoClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# FILES
image_path = "your_image.png"     # Replace with your image
music_path = "firfirey.mp3"       # Add song file yourself
output_path = "Cute_Cartoon_Love.mp4"

duration = 15
fps = 24
resolution = (1080, 1080)  # Instagram square

base_image = Image.open(image_path).convert("RGBA")
base_image = base_image.resize((800, 600))


def make_frame(t):
    zoom = 1 + 0.02 * np.sin(t)
    img = base_image.resize((int(800 * zoom), int(600 * zoom)))

    # Cartoon soft blur glow
    img = img.filter(ImageFilter.SMOOTH_MORE)

    frame = Image.new("RGBA", resolution, (255, 220, 235))
    x = (resolution[0] - img.width) // 2
    y = (resolution[1] - img.height) // 2
    frame.paste(img, (x, y))

    draw = ImageDraw.Draw(frame)

    try:
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        font_small = ImageFont.truetype("DejaVuSans-Bold.ttf", 45)
    except OSError:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Dialogue timing
    if 2 < t < 6:
        draw.text(
            (150, 100),
            "Will we be together\nwhen we grow up? 💭",
            fill="white",
            font=font_small,
        )

    if 7 < t < 12:
        draw.text(
            (120, 800),
            "Let destiny decide.\nI will ask you again someday 💍✨",
            fill=(255, 105, 180),
            font=font_big,
        )

    # Floating hearts
    for i in range(8):
        heart_x = int((t * 100 + i * 120) % resolution[0])
        heart_y = int(resolution[1] - (t * 80 + i * 60) % resolution[1])
        draw.text((heart_x, heart_y), "💖", fill=(255, 120, 170), font=font_small)

    return np.array(frame)


video = VideoClip(make_frame, duration=duration)

# Add music (trim to video duration)
audio = AudioFileClip(music_path).subclip(0, duration)
video = video.set_audio(audio)

video.write_videofile(output_path, fps=fps)
