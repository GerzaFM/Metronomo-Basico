#!/usr/bin/env python
"""
Main entry point for the Professional Metronome application.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.controllers import MetronomeController
from src.views import MetronomeWindow
from src.utils import setup_logging


def main():
    """Main application entry point."""
    # Setup logging
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    setup_logging(
        log_level=logging.INFO,
        log_file=log_dir / "metronome.log"
    )
    
    logger = logging.getLogger(__name__)
    logger.info("="*60)
    logger.info("Starting Professional Metronome Application")
    logger.info("="*60)
    
    try:
        # Create controller
        controller = MetronomeController()
        
        # Initialize
        if not controller.initialize():
            logger.error("Failed to initialize controller")
            sys.exit(1)
        
        # Create and run GUI
        window = MetronomeWindow(controller)
        window.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    main()
