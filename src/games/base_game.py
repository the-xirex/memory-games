"""Base game class for all memory games."""
import customtkinter as ctk


class BaseGame:
    """Base class for all memory games."""
    
    def __init__(self, app, on_back):
        """
        Initialize base game.
        
        Args:
            app: Main CTk application window
            on_back: Callback function to return to main menu
        """
        self.app = app
        self.on_back = on_back
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        self.game_started = False
    
    def show_help_tooltip(self, widget, title, description):
        """Display help tooltip."""
        self.help_tooltip = ctk.CTkFrame(
            self.app, 
            fg_color="white", 
            corner_radius=10, 
            border_width=2, 
            border_color="#4a9eff"
        )
        
        title_label = ctk.CTkLabel(
            self.help_tooltip,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray20"
        )
        title_label.pack(padx=15, pady=(10, 5))
        
        desc_label = ctk.CTkLabel(
            self.help_tooltip,
            text=description,
            font=ctk.CTkFont(size=12),
            justify="left",
            text_color="gray30"
        )
        desc_label.pack(padx=15, pady=(5, 10))
        
        self.app.update_idletasks()
        tooltip_width = self.help_tooltip.winfo_reqwidth()
        
        x_position = 800 - 20 - tooltip_width
        self.help_tooltip.place(x=x_position, y=60)
    
    def hide_help_tooltip(self):
        """Hide help tooltip."""
        if hasattr(self, 'help_tooltip'):
            self.help_tooltip.destroy()
    
    def show_game_over_modal(self, game_name, score, on_restart):
        """Show game over modal dialog."""
        overlay = ctk.CTkFrame(self.app, fg_color="gray40")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        overlay.configure(corner_radius=0)
        
        modal_frame = ctk.CTkFrame(
            overlay, 
            fg_color="white", 
            corner_radius=15, 
            width=400, 
            height=300
        )
        modal_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            modal_frame,
            text="Game Over!",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="gray20"
        ).pack(pady=30)
        
        ctk.CTkLabel(
            modal_frame,
            text=f"Your score: Level {score}",
            font=ctk.CTkFont(size=24),
            text_color="gray30"
        ).pack(pady=20)
        
        ctk.CTkLabel(
            modal_frame,
            text="Play again?",
            font=ctk.CTkFont(size=18),
            text_color="gray30"
        ).pack(pady=20)
        
        btn_frame = ctk.CTkFrame(modal_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Yes",
            width=120,
            height=40,
            command=lambda: [overlay.destroy(), on_restart()]
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="No",
            width=120,
            height=40,
            command=lambda: [overlay.destroy(), self.on_back()]
        ).pack(side="left", padx=10)
    
    def create_top_frame(self, help_title, help_description):
        """Create top frame with back button, level label, and help button."""
        top_frame = ctk.CTkFrame(self.app, height=50, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)
        top_frame.pack_propagate(False)
        
        back_btn = ctk.CTkButton(
            top_frame,
            text="Back",
            width=80,
            height=30,
            command=self.on_back
        )
        back_btn.pack(side="left", pady=5)
        
        self.level_label = ctk.CTkLabel(
            top_frame,
            text=f"Level: {self.level}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.level_label.place(in_=top_frame, relx=0.5, rely=0.5, anchor="center")
        
        help_btn = ctk.CTkButton(
            top_frame,
            text="?",
            width=30,
            height=30,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="gray70",
            hover_color="gray60"
        )
        help_btn.pack(side="right", pady=5)
        help_btn.bind("<Enter>", lambda e: self.show_help_tooltip(
            help_btn, help_title, help_description
        ))
        help_btn.bind("<Leave>", lambda e: self.hide_help_tooltip())
        
        return top_frame
    
    def start(self):
        """Start the game. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement start()")
