#!/usr/bin/env python3
"""
Directory to Markdown Converter using Microsoft markitdown
Converts all supported files in a directory to markdown format.
"""

import os
import sys
import argparse
from pathlib import Path
from markitdown import MarkItDown

def convert_directory_to_markdown(input_dir, output_dir=None):
    """
    Convert all supported files in a directory to markdown format.
    
    Args:
        input_dir (str): Path to input directory
        output_dir (str, optional): Path to output directory. If None, creates 'markdown_output' in input_dir
    """
    input_path = Path(input_dir)
    
    # Validate input directory
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return False
    
    if not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        return False
    
    # Set up output directory
    if output_dir is None:
        output_path = input_path / "markdown_output"
    else:
        output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_path}")
    
    # Initialize MarkItDown
    md = MarkItDown()
    
    # Supported file extensions (adjust based on markitdown capabilities)
    supported_extensions = {
        '.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls',
        '.html', '.htm', '.xml', '.csv', '.json', '.txt', '.rtf'
    }
    
    converted_count = 0
    error_count = 0
    
    # Process all files in the directory
    for file_path in input_path.rglob('*'):
        if file_path.is_file():
            file_extension = file_path.suffix.lower()
            
            # Skip files that are already markdown
            if file_extension in ['.md', '.markdown']:
                print(f"Skipping markdown file: {file_path.name}")
                continue
            
            # Check if file extension is supported
            if file_extension not in supported_extensions:
                print(f"Skipping unsupported file: {file_path.name}")
                continue
            
            try:
                print(f"Converting: {file_path.name}")
                
                # Convert file to markdown
                result = md.convert(str(file_path))
                
                # Create output filename
                relative_path = file_path.relative_to(input_path)
                output_filename = relative_path.with_suffix('.md')
                output_file_path = output_path / output_filename
                
                # Create subdirectories if needed
                output_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write markdown content to file
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(result.text_content)
                
                print(f"✓ Converted: {file_path.name} -> {output_filename}")
                converted_count += 1
                
            except Exception as e:
                print(f"✗ Error converting {file_path.name}: {str(e)}")
                error_count += 1
    
    # Summary
    print(f"\n--- Conversion Summary ---")
    print(f"Files converted: {converted_count}")
    print(f"Errors encountered: {error_count}")
    print(f"Output location: {output_path}")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Convert all files in a directory to markdown using Microsoft markitdown"
    )
    parser.add_argument(
        "input_directory",
        help="Path to the input directory containing files to convert"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory for markdown files (default: creates 'markdown_output' in input directory)"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Process files recursively in subdirectories (default behavior)"
    )
    
    args = parser.parse_args()
    
    try:
        success = convert_directory_to_markdown(args.input_directory, args.output)
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nConversion interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
