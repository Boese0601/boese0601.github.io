#!/usr/bin/env python3
"""Compress video files using moviepy while maintaining quality."""

import os
from pathlib import Path
from moviepy.editor import VideoFileClip

# Paths
input_dir = Path("/Users/dichang0601/Downloads/CVPR_2026_Meta/Supp/Submit_Final/hairweaver_page/static/sorted_videos_compressed_ori")
output_dir = Path("/Users/dichang0601/Downloads/CVPR_2026_Meta/Supp/Submit_Final/hairweaver_page/static/sorted_videos_compressed")

# Create output directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

# Get all mp4 files
video_files = sorted(input_dir.glob("*.mp4"))

print(f"Found {len(video_files)} video files to compress")

for video_path in video_files:
    output_path = output_dir / video_path.name
    print(f"\nProcessing: {video_path.name}")

    try:
        # Load video
        clip = VideoFileClip(str(video_path))

        # Get original file size
        original_size = video_path.stat().st_size / (1024 * 1024)  # MB

        # Write compressed video with optimized settings
        # bitrate controls the compression - lower = smaller file, less quality
        # Using a reasonable bitrate for good quality compression
        clip.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac',
            bitrate='2000k',  # 2 Mbps - good balance of quality and size
            preset='medium',  # encoding speed vs compression ratio
            ffmpeg_params=['-crf', '23'],  # Constant Rate Factor (18-28 is good, lower = better quality)
        )

        # Close the clip to free resources
        clip.close()

        # Get compressed file size
        compressed_size = output_path.stat().st_size / (1024 * 1024)  # MB
        reduction = (1 - compressed_size / original_size) * 100

        print(f"  Original: {original_size:.2f} MB -> Compressed: {compressed_size:.2f} MB ({reduction:.1f}% reduction)")

    except Exception as e:
        print(f"  Error processing {video_path.name}: {e}")

print("\n✓ Compression complete!")
