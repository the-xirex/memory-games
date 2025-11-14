import customtkinter as ctk
from utils import load_records, reset_records


class MainMenu:
    """Main menu UI for Memory Games application"""
    
    def __init__(self, app, game_callbacks):
        """
        Initialize the main menu
        
        Args:
            app: The main CTk application window
            game_callbacks: Dictionary with keys 'spatial', 'corsi', 'span' pointing to game start functions
        """
        self.app = app
        self.game_callbacks = game_callbacks
        self.tooltip_window = None
        
    def show(self):
        """Display the main menu"""
        for widget in self.app.winfo_children():
            widget.destroy()
        
        # Top frame with help button
        top_frame = ctk.CTkFrame(self.app, height=50, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)
        top_frame.pack_propagate(False)
        
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
        help_btn.bind("<Enter>", lambda e: self._show_help_tooltip(help_btn, 
            "Memory Games",
            "Train your memory and cognitive skills\nwith these scientifically-based games.\n\n"
            "Created by:\n"
            "Volokitin Vladyslav"))
        help_btn.bind("<Leave>", lambda e: self._hide_help_tooltip())
        
        # Main container with left (games) and right (records) sections
        main_container = ctk.CTkFrame(self.app, fg_color="transparent")
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Left frame - Game buttons
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent", width=320)
        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)
        
        button_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        button_frame.pack(expand=True)
        
        game1_btn = ctk.CTkButton(
            button_frame,
            text="Spatial Memory Game",
            font=ctk.CTkFont(size=16),
            width=280,
            height=50,
            command=self.game_callbacks['spatial']
        )
        game1_btn.pack(pady=12)
        
        game2_btn = ctk.CTkButton(
            button_frame,
            text="Corsi Block Test",
            font=ctk.CTkFont(size=16),
            width=280,
            height=50,
            command=self.game_callbacks['corsi']
        )
        game2_btn.pack(pady=12)
        
        game3_btn = ctk.CTkButton(
            button_frame,
            text="Memory Span",
            font=ctk.CTkFont(size=16),
            width=280,
            height=50,
            command=self.game_callbacks['span']
        )
        game3_btn.pack(pady=12)
        
        # Right frame - Records table
        right_frame = ctk.CTkFrame(main_container, fg_color="gray90", corner_radius=10, width=320, height=350)
        right_frame.pack(side="right", fill="none")
        right_frame.pack_propagate(False)
        
        records_title = ctk.CTkLabel(
            right_frame,
            text="🏆 Session Records",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="gray20"
        )
        records_title.pack(pady=(20, 10))
        
        records_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        records_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Display records for each game
        games = [
            ("Spatial Memory", "Spatial Memory Game"),
            ("Corsi Block", "Corsi Block Test"),
            ("Memory Span", "Memory Span")
        ]
        
        records = load_records()
        
        for display_name, game_key in games:
            record_frame = ctk.CTkFrame(records_container, fg_color="white", corner_radius=8)
            record_frame.pack(fill="x", pady=8, padx=5)
            
            game_label = ctk.CTkLabel(
                record_frame,
                text=display_name,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="gray30",
                anchor="w"
            )
            game_label.pack(side="left", padx=15, pady=12)
            
            score = records.get(game_key, 0)
            score_label = ctk.CTkLabel(
                record_frame,
                text=f"Level {score}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#1f6aa5"
            )
            score_label.pack(side="right", padx=15, pady=12)
        
        # Reset records button
        reset_btn = ctk.CTkButton(
            right_frame,
            text="Reset Records",
            font=ctk.CTkFont(size=12),
            width=150,
            height=30,
            fg_color="gray70",
            hover_color="gray60",
            command=self._reset_records
        )
        reset_btn.pack(pady=(10, 20))
        
    def _show_help_tooltip(self, widget, title, description):
        """Show a help tooltip near the widget"""
        self._hide_help_tooltip()
        
        x = widget.winfo_rootx() - 300
        y = widget.winfo_rooty() + 40
        
        self.tooltip_window = ctk.CTkToplevel(self.app)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        tooltip_frame = ctk.CTkFrame(
            self.tooltip_window,
            fg_color="white",
            corner_radius=10,
            border_width=2,
            border_color="gray70"
        )
        tooltip_frame.pack(padx=2, pady=2)
        
        title_label = ctk.CTkLabel(
            tooltip_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray20"
        )
        title_label.pack(pady=(10, 5), padx=15, anchor="w")
        
        desc_label = ctk.CTkLabel(
            tooltip_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="gray40",
            justify="left"
        )
        desc_label.pack(pady=(0, 10), padx=15, anchor="w")
        
    def _hide_help_tooltip(self):
        """Hide the help tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
            
    def _reset_records(self):
        """Reset all game records to 0"""
        reset_records()
        self.show()  # Refresh the menu to show updated records
