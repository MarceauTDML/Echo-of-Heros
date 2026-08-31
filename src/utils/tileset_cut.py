import os
from PIL import Image

def slice_tileset(image_path: str, tile_size: int = 32, output_dir: str = "tiles_output", skip_empty: bool = False):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    os.makedirs(output_dir, exist_ok=True)
    
    tile_count = 0
    cols = width // tile_size
    rows = height // tile_size
    
    for row in range(rows):
        for col in range(cols):
            x = col * tile_size
            y = row * tile_size
            
            tile = img.crop((x, y, x + tile_size, y + tile_size))
            
            if skip_empty:
                alpha_extrema = tile.getchannel("A").getextrema()
                if alpha_extrema == (0, 0):
                    continue
            
            filename = f"tile_r{row}_c{col}.png"
            tile.save(os.path.join(output_dir, filename), "PNG")
            tile_count += 1
            
    print(f"Découpage terminé : {tile_count} tuiles générées dans '{output_dir}'.")

if __name__ == "__main__":
    slice_tileset("World2_Cliff_Tileset.png", tile_size=16, skip_empty=False)