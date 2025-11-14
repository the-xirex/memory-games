"""
Memory Games - Train your memory and cognitive skills
"""
import customtkinter as ctk
from utils import get_icon_path
from games.spatial_memory_game import SpatialMemoryGame
from games.corsi_block_test import CorsiBlockTest
from games.memory_span_game import MemorySpanGame
from menu import MainMenu


def main():
    """Initialize and run the Memory Games application"""
    # Set appearance mode and color theme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Create main application window
    app = ctk.CTk()
    app.title("Memory Games")
    app.geometry("800x600")
    app.resizable(False, False)
    
    # Set window icon
    icon_path = get_icon_path()
    if icon_path:
        try:
            app.iconbitmap(icon_path)
        except Exception:
            pass  # Icon loading failed, continue without it
    
    # Initialize main menu (will be set up after games are created)
    main_menu = None
    
    def show_main_menu():
        """Show the main menu"""
        if main_menu:
            main_menu.show()
    
    # Initialize games
    spatial_game = SpatialMemoryGame(app, show_main_menu)
    corsi_game = CorsiBlockTest(app, show_main_menu)
    span_game = MemorySpanGame(app, show_main_menu)
    
    # Create main menu with game callbacks
    game_callbacks = {
        'spatial': spatial_game.start,
        'corsi': corsi_game.start,
        'span': span_game.start
    }
    main_menu = MainMenu(app, game_callbacks)
    
    # Show main menu
    main_menu.show()
    
    # Start the application
    app.mainloop()


if __name__ == "__main__":
    main()
