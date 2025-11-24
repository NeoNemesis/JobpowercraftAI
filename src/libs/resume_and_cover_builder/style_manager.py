import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


class StyleManager:
    def __init__(self):
        self.selected_style: Optional[str] = None
        self.selected_style_path: Optional[Path] = None
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent
        self.styles_directory = project_root / "src" / "libs" / "resume_and_cover_builder" / "resume_style"
        
        # Lägg till de nya moderna design-mapparna
        self.moderndesign1_directory = project_root / "src" / "libs" / "resume_and_cover_builder" / "moderndesign1"
        self.moderndesign2_directory = project_root / "src" / "libs" / "resume_and_cover_builder" / "moderndesign2"

        logging.debug(f"Project root determined as: {project_root}")
        logging.debug(f"Styles directory set to: {self.styles_directory}")
        logging.debug(f"ModernDesign1 directory set to: {self.moderndesign1_directory}")
        logging.debug(f"ModernDesign2 directory set to: {self.moderndesign2_directory}")

    def get_styles(self) -> Dict[str, Tuple[str, str]]:
        """
        Retrieve the available styles from all style directories.
        Returns:
            Dict[str, Tuple[str, str]]: A dictionary mapping style names to their file paths and directory info.
        """
        styles_to_files = {}
        
        # Lista över alla mappar att söka i
        directories_to_search = [
            (self.styles_directory, "resume_style"),
            (self.moderndesign1_directory, "moderndesign1"), 
            (self.moderndesign2_directory, "moderndesign2")
        ]
        
        for directory, dir_name in directories_to_search:
            if not directory or not directory.exists():
                logging.warning(f"Directory {directory} not found, skipping.")
                continue
                
            logging.debug(f"Reading directory: {directory}")
            try:
                files = [f for f in directory.iterdir() if f.is_file() and f.suffix == '.css']
                logging.debug(f"CSS files found in {dir_name}: {[f.name for f in files]}")
                
                for file_path in files:
                    logging.debug(f"Processing file: {file_path}")
                    try:
                        with file_path.open("r", encoding="utf-8") as file:
                            first_line = file.readline().strip()
                            logging.debug(f"First line of file {file_path.name}: {first_line}")
                            if first_line.startswith("/*") and first_line.endswith("*/"):
                                content = first_line[2:-2].strip()
                                style_name = content.strip()
                                # Spara både filnamn och fullständig sökväg
                                styles_to_files[style_name] = (file_path.name, str(file_path))
                                logging.info(f"Added style: {style_name} from {dir_name}")
                    except Exception as file_error:
                        logging.error(f"Error reading file {file_path}: {file_error}")
                        
            except Exception as dir_error:
                logging.error(f"Error accessing directory {directory}: {dir_error}")
        
        return styles_to_files

    def format_choices(self, styles_to_files: Dict[str, Tuple[str, str]]) -> List[str]:
        """
        Format the style choices for user presentation.
        Args:
            styles_to_files (Dict[str, Tuple[str, str]]): A dictionary mapping style names to their file names.
        Returns:
            List[str]: A list of formatted style choices.
        """
        return [f"{style_name}" for style_name, (file_name, _) in styles_to_files.items()]

    def set_selected_style(self, selected_style: str):
        """
        Directly set the selected style.
        Args:
            selected_style (str): The name of the style to select.
        """
        self.selected_style = selected_style
        logging.info(f"Selected style set to: {self.selected_style}")

    def get_style_path(self) -> Optional[Path]:
        """
        Get the path to the selected style.
        Returns:
            Path: A Path object representing the path to the selected style file, or None if not found.
        """
        try:
            styles = self.get_styles()
            if self.selected_style not in styles:
                raise ValueError(f"Style '{self.selected_style}' not found.")
            file_name, full_path = styles[self.selected_style]
            
            # Om vi har en fullständig sökväg, använd den
            if full_path:
                return Path(full_path)
            else:
                # Fallback till gamla metoden
                return self.styles_directory / file_name
        except Exception as e:
            logging.error(f"Error retrieving selected style: {e}")
            return None
