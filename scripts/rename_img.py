from pathlib import Path

for filepath in Path("images_jpgs").iterdir():
    if filepath.is_file():
        old_name = filepath.stem
        old_extension = filepath.suffix
        directory = filepath.parent

        name = old_name.split('_')
        name[-1] = f'I{int(name[-1]):05d}'
        name = "_".join(name)
        new_name = name + old_extension
        filepath.rename(Path(directory, new_name))
