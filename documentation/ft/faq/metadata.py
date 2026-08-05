import os
import re

def file_exists_and_readable(filepath):
    return os.path.isfile(filepath) and os.access(filepath, os.R_OK)

def comment_out_special_blocks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    inside_env_block = False
    inside_glightbox_block = False
    inside_plantuml_block = False

    for line in lines:
        # Check for start of glightbox block
        if '- glightbox:' in line.strip():
            inside_glightbox_block = True
            output_lines.append('# ' + line)
        # Check for end of glightbox block
        elif inside_glightbox_block and '- macros: {}' in line.strip():
            output_lines.append('# ' + line)
            inside_glightbox_block = False
        # Check for start of plantuml block
        elif '- plantuml_markdown:' in line.strip():
            inside_plantuml_block = True
            output_lines.append('# ' + line)
        # Check for end of plantuml block
        elif inside_plantuml_block and 'remove_inline_svg_size: false' in line.strip():
            output_lines.append('# ' + line)
            inside_plantuml_block = False
        # Comment out lines inside blocks
        elif inside_glightbox_block or inside_plantuml_block:
            output_lines.append('# ' + line)
        # Handle !ENV blocks
        elif re.search(r'!ENV', line):
            if line.strip().endswith(']'):
                output_lines.append('# ' + line)
            else:
                inside_env_block = True
                output_lines.append('# ' + line)
        elif re.search(r'!!', line):
            output_lines.append('# ' + line)
        elif inside_env_block:
            output_lines.append('# ' + line)
            if re.search(r'\]', line.strip()):  # End of the !ENV block
                inside_env_block = False
        else:
            output_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)

# Step 1: Verify and read the metadata.yml file
metadata_filepath = 'tools/ft/faq/metadata.yml'
if file_exists_and_readable(metadata_filepath):
    with open(metadata_filepath, 'r') as file:
        metadata_content = file.read()
else:
    print(f"Error: '{metadata_filepath}' does not exist or is not readable.")
    exit(1)

# Step 2: Verify and read the mkdocs.yml file
mkdocs_filepath = 'mkdocs.yml'
if file_exists_and_readable(mkdocs_filepath):
    with open(mkdocs_filepath, 'r') as file:
        mkdocs_content = file.read()
else:
    print(f"Error: '{mkdocs_filepath}' does not exist or is not readable.")
    exit(1)

# Step 3: Verify and read the mkdocs.yml file for faq
faq_nav_filepath = 'tools/mkdocs/mkdocs_faq.yml'
if file_exists_and_readable(faq_nav_filepath):
    with open(faq_nav_filepath, 'r') as file:
        lines = file.readlines()
        nav_start_index = next((i for i, line in enumerate(lines) if line.strip().startswith('nav:')), None)
        if nav_start_index is not None:
            faq_nav_content = ''.join(lines[nav_start_index:])
        else:
            print(f"Error: 'nav:' not found in '{faq_nav_filepath}'.")
            exit(1)
else:
    print(f"Error: '{faq_nav_filepath}' does not exist or is not readable.")
    exit(1)

# Step 4: Check if 'ft_metadata' is already present in mkdocs.yml
if 'ft_metadata' in mkdocs_content:
    print("Error: 'ft_metadata' is already present in mkdocs.yml. Aborting.")
    exit(1)

# Step 5: Append the content of metadata.yml to mkdocs.yml
with open(mkdocs_filepath, 'a') as file:
    file.write("\n" + metadata_content)
print("mkdocs.yml has been successfully updated.")

# Step 6: Append the FAQ navigation content to mkdocs.yml
with open(mkdocs_filepath, 'a') as file:
    file.write("\n" + faq_nav_content)

# Step 7: Comment out the !ENV lines in metadata.yml
comment_out_special_blocks(mkdocs_filepath)

# Step 8: Update site name
with open(mkdocs_filepath, 'r') as file:
    content = file.read()

content = re.sub(r'site_name:.*', 'site_name: AI SDK FAQ', content)

with open(mkdocs_filepath, 'w') as file:
    file.write(content)