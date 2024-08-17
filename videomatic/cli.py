import argparse
from .scene import Scene
from .video import make_scenes


def main():
    parser = argparse.ArgumentParser(description="Manage video scenes generation.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Build command
    build_parser = subparsers.add_parser("create_frames", help="Build all scenes, images")
    build_parser = subparsers.add_parser("create_videos", help="Build all fideos from frames")
    build_parser = subparsers.add_parser("reformat_video", help="Rebuild Video to correct time length")
    build_parser = subparsers.add_parser("build", help="Put it all togeather into a single video")

    # Redo command
    redo_parser = subparsers.add_parser("redo", help="Redo specific scenes")
    redo_parser.add_argument("frames", nargs="+", type=int, help="Indexes of the scenes to redo")

    args = parser.parse_args()

    if args.command == "create_frames":
        scene=make_scenes()
        scene.create_fragments("frames")
    if args.command == "create_videos":
        scene=make_scenes()
        scene.create_fragments("video")
    if args.command == "reformat_video":
        scene=make_scenes()
        scene.correct_fragments()
    if args.command == "build":
        scene=make_scenes()
        scene.build_video()
    elif args.command == "redo":
        scene=make_scenes()
        scene.create_fragments("frames",redo=True,indexes=args.frames)
        scene.create_fragments("video",redo=True,indexes=args.frames)

if __name__ == "__main__":
    main()
 
