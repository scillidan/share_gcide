# Authors: DeepSeek🧙‍♂️, scillidan🤡
# Usage: python file.py <input_file> <output_file>

import os
import sys
import glob
import logging
import chardet

def setup_logging():
    """Setup logging configuration for conversion process"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('_cide2tabfile.log', 'w', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('cide_converter')

def detect_encoding(file_path):
    """Detect file encoding using chardet"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']

            # If confidence is low or encoding is None, default to common encodings
            if not encoding or confidence < 0.7:
                return 'us-ascii', confidence
            return encoding.lower(), confidence
    except Exception as e:
        logging.warning(f"Error detecting encoding for {file_path}: {e}")
        return 'us-ascii', 0.0

def convert_special_characters(text, filename, logger):
    """Convert specific special characters to custom representations"""
    # Track conversions for logging
    conversions = {
        'ç': 0,
        '¹': 0,
        'other_non_ascii': 0
    }

    # Replace common problematic characters and normalize line endings
    replacements = {
        '\r\n': '\n',  # Normalize Windows line endings
        '\r': '\n',    # Normalize old Mac line endings
    }

    for old, new in replacements.items():
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            logger.info(f"Replaced {count} '{repr(old)}' with '{repr(new)}' in {filename}")

    # Process each character for special conversions
    cleaned_text = ''
    problematic_chars = []

    for i, char in enumerate(text):
        # Special handling for specific characters
        if char == 'ç':
            # Convert ç to <cced/
            cleaned_text += '<cced/'
            conversions['ç'] += 1
            continue
        elif char == '¹':
            # Convert ¹ to <sup>1</sup>
            cleaned_text += '<sup>1</sup>'
            conversions['¹'] += 1
            continue

        # Check if character is ASCII
        try:
            char.encode('ascii')
            cleaned_text += char
        except UnicodeEncodeError:
            # Character is non-ASCII, replace with placeholder and log
            problematic_chars.append((i, char, ord(char)))
            cleaned_text += '?'  # Placeholder for other non-ASCII characters
            conversions['other_non_ascii'] += 1

    # Log special character conversions
    if conversions['ç'] > 0:
        logger.info(f"Converted {conversions['ç']} 'ç' characters to '<cced/' in {filename}")
    if conversions['¹'] > 0:
        logger.info(f"Converted {conversions['¹']} '¹' characters to '<sup>1</sup>' in {filename}")

    # Log other problematic characters
    if problematic_chars:
        logger.warning(f"Found {len(problematic_chars)} other non-ASCII characters in {filename}:")
        for pos, char, code in problematic_chars[:10]:  # Log first 10 problematic chars
            logger.warning(f"  Position {pos}: Character '{char}' (Unicode: U+{code:04X})")
        if len(problematic_chars) > 10:
            logger.warning(f"  ... and {len(problematic_chars) - 10} more non-ASCII characters")

    return cleaned_text

def read_file_with_fallback(filename, logger):
    """Read file with encoding fallback mechanism"""
    encodings_to_try = ['us-ascii', 'utf-8', 'latin-1', 'iso-8859-1', 'gbk', 'cp1252']

    # First, detect encoding
    detected_encoding, confidence = detect_encoding(filename)
    logger.info(f"Detected encoding for {filename}: {detected_encoding} (confidence: {confidence:.2f})")

    # Try detected encoding first, then fallbacks
    if detected_encoding not in encodings_to_try:
        encodings_to_try.insert(0, detected_encoding)

    for i, encoding in enumerate(encodings_to_try):
        try:
            with open(filename, 'r', encoding=encoding) as infile:
                content = infile.read()

            logger.info(f"Successfully read {filename} with {encoding} encoding")

            # Convert special characters
            converted_content = convert_special_characters(content, os.path.basename(filename), logger)
            return converted_content, encoding

        except UnicodeDecodeError as e:
            if i == len(encodings_to_try) - 1:  # Last attempt failed
                logger.error(f"Failed to read {filename} with all attempted encodings: {encodings_to_try}")
                raise e
            logger.warning(f"Failed to read {filename} with {encoding}: {e}. Trying next encoding...")
        except Exception as e:
            logger.error(f"Unexpected error reading {filename}: {e}")
            raise e

    # This should not be reached, but for safety
    raise UnicodeDecodeError("All encoding attempts failed", b"", 0, 0, "No suitable encoding found")

def merge_cide_files(input_dir, output_file):
    """
    Merge CIDE.* files in alphabetical order into a single UTF-8 encoded file
    with comprehensive encoding handling and logging
    """
    logger = setup_logging()

    try:
        # Build file pattern matching path
        file_pattern = os.path.join(input_dir, "CIDE.[A-Z]")
        file_list = glob.glob(file_pattern)

        # Sort in alphabetical order
        file_list.sort()

        if not file_list:
            logger.error(f"No CIDE.[A-Z] files found in directory {input_dir}")
            return False

        logger.info(f"Found {len(file_list)} files, starting merge...")
        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output file: {output_file}")

        # Statistics
        stats = {
            'total_files': len(file_list),
            'successful_files': 0,
            'failed_files': 0,
            'encoding_issues': 0,
            'ç_conversions': 0,
            '¹_conversions': 0
        }

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, filename in enumerate(file_list, 1):
                file_basename = os.path.basename(filename)
                logger.info(f"Processing file {i}/{len(file_list)}: {file_basename}")

                try:
                    # Read file with encoding detection and character conversion
                    content, used_encoding = read_file_with_fallback(filename, logger)

                    # Count special character conversions for this file
                    stats['ç_conversions'] += content.count('<cced/')
                    stats['¹_conversions'] += content.count('<sup>1</sup>')

                    # Write content to output file
                    outfile.write(content)

                    # Add newline separator between files (not after last file)
                    if i < len(file_list):
                        outfile.write('\n')

                    stats['successful_files'] += 1

                    # Log if non-default encoding was used
                    if used_encoding != 'us-ascii':
                        stats['encoding_issues'] += 1
                        logger.info(f"File {file_basename} required {used_encoding} encoding")

                except UnicodeDecodeError as e:
                    logger.error(f"Unicode decode error for {file_basename}: {e}")
                    stats['failed_files'] += 1
                except Exception as e:
                    logger.error(f"Error processing {file_basename}: {e}")
                    stats['failed_files'] += 1

        # Log final statistics
        logger.info("Merge process completed!")
        logger.info(f"Files processed: {stats['total_files']}")
        logger.info(f"Successful: {stats['successful_files']}")
        logger.info(f"Failed: {stats['failed_files']}")
        logger.info(f"Files with encoding issues: {stats['encoding_issues']}")
        logger.info(f"Total 'ç' to '<cced/' conversions: {stats['ç_conversions']}")
        logger.info(f"Total '¹' to '<sup>1</sup>' conversions: {stats['¹_conversions']}")
        logger.info(f"Output file created: {output_file}")

        return stats['failed_files'] == 0

    except Exception as e:
        logger.error(f"Error during merge process: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_file>")
        print("Example: python script.py ./input _gcide.txt")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)

    success = merge_cide_files(input_dir, output_file)

    if success:
        print(f"\nMerge completed successfully! Check _cide2tabfile.log for details.")
    else:
        print(f"\nMerge completed with errors. Check _cide2tabfile.log for details.")

    sys.exit(0 if success else 1)