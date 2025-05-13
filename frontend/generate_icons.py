from PIL import Image, ImageDraw, ImageFont
import os

def create_icon_placeholder(title, size=(200, 200), bg_color="#222831", text_color="#FFFFFF"):
    """Create a placeholder icon with text"""
    # Create a new image with a dark background
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    font_size = 20
    try:
        font = ImageFont.truetype("Arial", font_size)
    except:
        font = ImageFont.load_default()
    
    # Center the text
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), title, fill=text_color, font=font)
    
    return img

def main():
    # Create icons
    icons = {
        "ML Analytics": "ML for\nPredictive\nAnalytics",
        "Algorithms": "Algorithmic\nStrategies",
        "Reporting": "Automated\nReporting",
        "Metrics": "Important\nMetrics",
        "Security": "Data Protection\nStandards"
    }
    
    # Ensure assets directory exists
    os.makedirs("frontend/assets", exist_ok=True)
    
    # Generate and save icons
    for key, title in icons.items():
        icon = create_icon_placeholder(title)
        img_path = f"frontend/assets/{key.lower().replace(' ', '_')}_icon.png"
        icon.save(img_path)
        print(f"Generated: {img_path}")

if __name__ == "__main__":
    main() 