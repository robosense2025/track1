import argparse
import json
from pathlib import Path
from typing import Dict, Any, List
from nuscenes.nuscenes import NuScenes
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json(file_path: str) -> Dict[str, Any]:
    """Load a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data: Dict[str, Any], file_path: str):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_image_paths(nusc: NuScenes, frame_token: str, corruption_root: str) -> Dict[str, str]:
    """Get image paths for all cameras for a given frame."""
    sample = nusc.get('sample', frame_token)
    img_paths = {}
    
    for cam in ['CAM_FRONT', 'CAM_FRONT_RIGHT', 'CAM_FRONT_LEFT',
                'CAM_BACK', 'CAM_BACK_RIGHT', 'CAM_BACK_LEFT']:
        cam_token = sample['data'][cam]
        cam_data = nusc.get('sample_data', cam_token)
        img_paths[cam] = os.path.join(corruption_root, cam_data['filename'])
    
    return img_paths

def get_temporal_frames(nusc: NuScenes, frame_token: str, num_frames: int) -> List[str]:
    """Get previous frame tokens for temporal context."""
    frames = []
    current_sample = nusc.get('sample', frame_token)
    
    # Get previous frames
    for _ in range(num_frames):
        if current_sample['prev']:
            current_sample = nusc.get('sample', current_sample['prev'])
            frames.append(current_sample['token'])
        else:
            break
    
    return frames

def convert_format(input_file: str, output_file: str, corruption_root: str, nusc: NuScenes, use_temporal: bool = False, num_frames: int = 0):
    """Convert the QA data format."""
    # Load input data
    logger.info(f"Loading input file: {input_file}")
    data = load_json(input_file)
    
    # Initialize output data
    output_data = []
    
    # Process each scene
    for scene_token, scene_data in data.items():
        logger.info(f"Processing scene: {scene_token}")
        
        # Process each frame
        for frame_token, frame_data in scene_data['key_frames'].items():
            # Get image paths for current frame
            img_paths = get_image_paths(nusc, frame_token, corruption_root)
            
            # Get temporal context if requested
            history_frames = None
            if use_temporal and num_frames > 0:
                prev_frames = get_temporal_frames(nusc, frame_token, num_frames)
                if prev_frames:
                    history_frames = {
                        frame: get_image_paths(nusc, frame, corruption_root)
                        for frame in prev_frames
                    }
            
            # Process each QA pair
            if 'QA' in frame_data:
                for category, qa_list in frame_data['QA'].items():
                    for qa_item in qa_list:
                        sample = {
                            'scene_token': scene_token,
                            'frame_token': frame_token,
                            'question': qa_item['Q'],
                            'answer': qa_item.get('A', ''),  # Handle cases where answer might be missing
                            'category': category,
                            'img_paths': img_paths
                        }
                        
                        # Add temporal context if available
                        if history_frames:
                            sample['history_frames'] = history_frames
                        
                        output_data.append(sample)
    
    # Save output data
    logger.info(f"Saving {len(output_data)} samples to: {output_file}")
    save_json(output_data, output_file)

def parse_args():
    parser = argparse.ArgumentParser(description='Convert QA data format')
    parser.add_argument('input', type=str, help='Input JSON file path')
    parser.add_argument('output', type=str, help='Output JSON file path')
    parser.add_argument('corruption_root', type=str, help='Robosense corruption data root')
    parser.add_argument('--dataroot', type=str, default='data/nuscenes', help='NuScenes data root')
    parser.add_argument('--use-temporal', action='store_true', help='Whether to include temporal context')
    parser.add_argument('--num-frames', type=int, default=5, help='Number of previous frames to include if use_temporal is True')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Initialize NuScenes
    logger.info("Initializing NuScenes...")
    nusc = NuScenes(version='v1.0-trainval', 
                    dataroot=args.dataroot,
                    verbose=True)
    
    # Convert format
    convert_format(
        args.input,
        args.output,
        args.corruption_root,
        nusc,
        use_temporal=args.use_temporal,
        num_frames=args.num_frames
    )

if __name__ == '__main__':
    main()