"""Corsi Block Test - Remember sequence of randomly positioned blocks."""
import customtkinter as ctk
import random
from .base_game import BaseGame
from utils import load_records, update_record


class CorsiBlockTest(BaseGame):
    """Corsi Block Test implementation."""
    
    GAME_NAME = "Corsi Block Test"
    
    def start(self):
        """Start the Corsi Block Test game."""
        for widget in self.app.winfo_children():
            widget.destroy()
        
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        self.game_started = False
        self.block_positions = []
        
        self.create_top_frame(
            "Corsi Block Test",
            "Remember the sequence of randomly\npositioned blocks.\n\n"
            "Develops:\n"
            "• Spatial working memory\n"
            "• Visual attention\n"
            "• Cognitive flexibility"
        )
        
        self.header = ctk.CTkLabel(
            self.app,
            text="Press 'Start' to begin",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=30
        )
        self.header.pack(pady=5)
        
        self.game_canvas = ctk.CTkFrame(self.app, width=650, height=420, fg_color="gray90")
        self.game_canvas.pack(pady=5, padx=25)
        self.game_canvas.pack_propagate(False)
        
        self._generate_random_blocks()
        
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
    
    def _generate_random_blocks(self):
        """Generate randomly positioned blocks."""
        self.corsi_buttons = []
        self.block_positions = []
        button_size = 70
        canvas_width = 650
        canvas_height = 420
        margin = 10
        padding = 12
        
        num_blocks = 12
        max_attempts = 1000
        
        for block_idx in range(num_blocks):
            placed = False
            attempts = 0
            
            while not placed and attempts < max_attempts:
                x = random.randint(margin, canvas_width - button_size - margin)
                y = random.randint(margin, canvas_height - button_size - margin)
                
                overlaps = False
                for existing_pos in self.block_positions:
                    ex, ey = existing_pos
                    if not (x + button_size + padding < ex or x > ex + button_size + padding or
                            y + button_size + padding < ey or y > ey + button_size + padding):
                        overlaps = True
                        break
                
                if not overlaps:
                    self.block_positions.append((x, y))
                    
                    btn = ctk.CTkButton(
                        self.game_canvas,
                        text="",
                        width=button_size,
                        height=button_size,
                        corner_radius=10,
                        fg_color="gray85",
                        hover_color="gray75",
                        command=lambda idx=block_idx: self._button_clicked(idx)
                    )
                    btn.place(x=x, y=y)
                    self.corsi_buttons.append(btn)
                    placed = True
                
                attempts += 1
    
    def _button_clicked(self, index):
        """Handle button click."""
        if not self.game_started or not self.is_playing or not self.is_showing:
            return
        
        self.user_sequence.append(index)
        
        self._highlight_button(index, "#1f6aa5")
        
        if self.user_sequence[-1] != self.sequence[len(self.user_sequence)-1]:
            self.app.after(300, lambda: self._game_over())
        elif len(self.user_sequence) == len(self.sequence):
            self.app.after(300, lambda: self._level_complete())
        else:
            self.app.after(300, lambda: self._reset_button(index))
    
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
        
        self.sequence.extend([random.randint(0, 11) for _ in range(1)])
        
        self.header.configure(text="Watch the sequence...")
        
        self._show_sequence()
    
    def _show_sequence(self):
        """Show the sequence to memorize."""
        delay = max(400, 800 - (self.level * 30))
        
        def show_next(index=0):
            if index < len(self.sequence):
                pos = self.sequence[index]
                
                self._highlight_button(pos, "#4a9eff")
                
                self.app.after(delay, lambda: self._reset_button(pos))
                self.app.after(delay + 200, lambda: show_next(index + 1))
            else:
                self.is_showing = False
                self.header.configure(text="Repeat the sequence!")
        
        show_next()
    
    def _highlight_button(self, index, color):
        """Highlight a button with given color."""
        try:
            if hasattr(self, 'corsi_buttons') and self.corsi_buttons and index < len(self.corsi_buttons):
                self.corsi_buttons[index].configure(fg_color=color)
        except Exception:
            pass
    
    def _reset_button(self, index):
        """Reset button to default color."""
        try:
            if hasattr(self, 'corsi_buttons') and self.corsi_buttons and index < len(self.corsi_buttons):
                self.corsi_buttons[index].configure(fg_color="gray85")
        except Exception:
            pass
    
    def _level_complete(self):
        """Handle level completion."""
        for btn in self.corsi_buttons:
            btn.configure(fg_color="gray85")
        
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
        
        for btn in self.corsi_buttons:
            btn.configure(fg_color="#8b0000")
        
        self.app.after(500, self._show_game_over_screen)
    
    def _show_game_over_screen(self):
        """Show game over screen."""
        for btn in self.corsi_buttons:
            btn.configure(fg_color="gray85")
        
        self.header.configure(text="Game Over!")
        
        score = self.level - 1
        self.show_game_over_modal(self.GAME_NAME, score, self.start)
