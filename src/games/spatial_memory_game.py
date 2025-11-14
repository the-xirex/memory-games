"""Spatial Memory Game - Remember sequence of highlighted squares."""
import customtkinter as ctk
import random
from .base_game import BaseGame
from utils import load_records, update_record


class SpatialMemoryGame(BaseGame):
    """Spatial Memory Game implementation."""
    
    GAME_NAME = "Spatial Memory Game"
    
    def start(self):
        """Start the spatial memory game."""
        for widget in self.app.winfo_children():
            widget.destroy()
        
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        self.game_started = False
        
        self.create_top_frame(
            "Spatial Memory Game",
            "Remember the sequence of highlighted squares.\n\n"
            "Develops:\n"
            "• Visual-spatial memory\n"
            "• Pattern recognition\n"
            "• Sequential memory"
        )
        
        self.header = ctk.CTkLabel(
            self.app,
            text="Press 'Start' to begin",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=30
        )
        self.header.pack(pady=5)
        
        game_area = ctk.CTkFrame(self.app, fg_color="transparent", height=420)
        game_area.pack(fill="x", padx=25, pady=5)
        game_area.pack_propagate(False)
        
        grid_frame = ctk.CTkFrame(game_area, fg_color="transparent")
        grid_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.buttons = []
        button_size = 110
        
        for i in range(3):
            row = []
            for j in range(3):
                btn = ctk.CTkButton(
                    grid_frame,
                    text="",
                    width=button_size,
                    height=button_size,
                    corner_radius=10,
                    fg_color="gray85",
                    hover_color="gray75",
                    command=lambda idx=i*3+j: self._button_clicked(idx)
                )
                btn.grid(row=i, column=j, padx=8, pady=8)
                row.append(btn)
            self.buttons.append(row)
        
        button_spacer = ctk.CTkFrame(self.app, fg_color="transparent", height=45)
        button_spacer.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            self.app,
            text="START",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=180,
            height=45,
            command=self._start_level
        )
        self.start_btn.place(in_=button_spacer, relx=0.5, rely=0.5, anchor="center")
    
    def _button_clicked(self, index):
        """Handle button click."""
        if not self.game_started or not self.is_playing or self.is_showing:
            return
        
        self.user_sequence.append(index)
        
        row, col = index // 3, index % 3
        self._highlight_button(row, col, "#1f6aa5")
        
        if self.user_sequence[-1] != self.sequence[len(self.user_sequence)-1]:
            self.app.after(300, lambda: self._game_over())
        elif len(self.user_sequence) == len(self.sequence):
            self.app.after(300, lambda: self._level_complete())
        else:
            self.app.after(300, lambda: self._reset_button(row, col))
    
    def _start_level(self):
        """Start a new level."""
        self.game_started = True
        self.start_btn.place_forget()
        
        def countdown(count):
            if count > 0:
                self.header.configure(text=f"{count}")
                self.app.after(1000, lambda: countdown(count - 1))
            else:
                self._begin_level()
        
        if self.level == 1:
            countdown(3)
        else:
            self._begin_level()
    
    def _begin_level(self):
        """Begin the level sequence."""
        self.is_playing = True
        self.is_showing = True
        self.user_sequence = []
        
        self.sequence.extend([random.randint(0, 8) for _ in range(1)])
        
        self.header.configure(text="Watch the sequence...")
        
        self._show_sequence()
    
    def _show_sequence(self):
        """Show the sequence to memorize."""
        delay = max(400, 800 - (self.level * 30))
        
        def show_next(index=0):
            if index < len(self.sequence):
                pos = self.sequence[index]
                row, col = pos // 3, pos % 3
                
                self._highlight_button(row, col, "#4a9eff")
                
                self.app.after(delay, lambda: self._reset_button(row, col))
                self.app.after(delay + 200, lambda: show_next(index + 1))
            else:
                self.is_showing = False
                self.header.configure(text="Repeat the sequence!")
        
        show_next()
    
    def _highlight_button(self, row, col, color):
        """Highlight a button with given color."""
        try:
            if hasattr(self, 'buttons') and self.buttons and row < len(self.buttons) and col < len(self.buttons[row]):
                self.buttons[row][col].configure(fg_color=color)
        except Exception:
            pass
    
    def _reset_button(self, row, col):
        """Reset button to default color."""
        try:
            if hasattr(self, 'buttons') and self.buttons and row < len(self.buttons) and col < len(self.buttons[row]):
                self.buttons[row][col].configure(fg_color="gray85")
        except Exception:
            pass
    
    def _level_complete(self):
        """Handle level completion."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(fg_color="gray85")
        
        self.level += 1
        records = load_records()
        update_record(records, self.GAME_NAME, self.level - 1)
        self.level_label.configure(text=f"Level: {self.level}")
        self.header.configure(text="Great! Next level...")
        self.is_playing = False
        
        self.app.after(1500, self._start_level)
    
    def _game_over(self):
        """Handle game over."""
        self.is_playing = False
        self.is_showing = False
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(fg_color="#8b0000")
        
        self.app.after(500, self._show_game_over_screen)
    
    def _show_game_over_screen(self):
        """Show game over screen."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(fg_color="gray85")
        
        self.header.configure(text="Game Over!")
        
        score = self.level - 1
        self.show_game_over_modal(self.GAME_NAME, score, self.start)
