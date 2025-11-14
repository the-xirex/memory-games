import customtkinter as ctk
import random
from .base_game import BaseGame
from utils import load_records, update_record


class MemorySpanGame(BaseGame):
    """Memory Span Game - remember and reproduce sequences of digits"""
    
    GAME_NAME = "Memory Span"
    
    def __init__(self, app, on_back):
        super().__init__(app, on_back)
        self.digit_label = None
        self.display_frame = None
        self.grid_frame = None
        self.number_buttons = []
        self.start_btn = None
        
    def start(self):
        """Initialize and display the Memory Span game"""
        for widget in self.app.winfo_children():
            widget.destroy()
            
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        self.game_started = False
        
        self.create_top_frame(
            "Memory Span",
            "Remember the sequence of digits shown.\n\n"
            "Develops:\n"
            "• Numerical working memory\n"
            "• Short-term memory capacity\n"
            "• Concentration"
        )
        
        # Header text
        self.header = ctk.CTkLabel(
            self.app,
            text="Press 'Start' to begin",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=30
        )
        self.header.pack(pady=5)
        
        # Game area
        game_area = ctk.CTkFrame(self.app, fg_color="transparent", height=420)
        game_area.pack(fill="x", padx=25, pady=5)
        game_area.pack_propagate(False)
        
        # Display frame for showing digits
        self.display_frame = ctk.CTkFrame(game_area, fg_color="transparent")
        self.display_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.digit_label = ctk.CTkLabel(
            self.display_frame,
            text="?",
            font=ctk.CTkFont(size=120, weight="bold"),
            width=200,
            height=200,
            text_color="#4a9eff"
        )
        self.digit_label.pack()
        
        # Grid frame for number pad (0-9)
        self.grid_frame = ctk.CTkFrame(game_area, fg_color="transparent")
        
        self.number_buttons = []
        button_size = 90
        
        # Create 3x3 grid for digits 1-9
        for i in range(3):
            row = []
            for j in range(3):
                number = i * 3 + j + 1
                btn = ctk.CTkButton(
                    self.grid_frame,
                    text=str(number),
                    width=button_size,
                    height=button_size,
                    corner_radius=10,
                    fg_color="gray85",
                    hover_color="gray75",
                    font=ctk.CTkFont(size=28, weight="bold"),
                    command=lambda num=number: self._button_clicked(num)
                )
                btn.grid(row=i, column=j, padx=6, pady=6)
                row.append(btn)
            self.number_buttons.append(row)
        
        # Add 0 button at bottom center
        zero_btn = ctk.CTkButton(
            self.grid_frame,
            text="0",
            width=button_size,
            height=button_size,
            corner_radius=10,
            fg_color="gray85",
            hover_color="gray75",
            font=ctk.CTkFont(size=28, weight="bold"),
            command=lambda: self._button_clicked(0)
        )
        zero_btn.grid(row=3, column=1, padx=6, pady=6)
        self.number_buttons.append([None, zero_btn, None])
        
        # Start button area
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
        
    def _button_clicked(self, number):
        """Handle number button click"""
        if not self.game_started or not self.is_playing or self.is_showing:
            return
            
        self.user_sequence.append(number)
        
        self._highlight_button(number, "#1f6aa5")
        
        # Check if the input is correct
        if self.user_sequence[-1] != self.sequence[len(self.user_sequence)-1]:
            self.app.after(300, lambda: self._game_over())
        elif len(self.user_sequence) == len(self.sequence):
            self.app.after(300, lambda: self._level_complete())
        else:
            self.app.after(300, lambda: self._reset_button(number))
            
    def _start_level(self):
        """Start a new level with countdown"""
        self.game_started = True
        self.start_btn.place_forget()
        self.digit_label.configure(text="")
        
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
        """Initialize level and start showing sequence"""
        self.is_playing = True
        self.is_showing = True
        self.user_sequence = []
        
        # Add one more digit to the sequence
        self.sequence.extend([random.randint(0, 9) for _ in range(1)])
        
        self.header.configure(text="Watch the sequence...")
        
        self._show_sequence()
        
    def _show_sequence(self):
        """Display the sequence of digits one by one"""
        delay = max(400, 800 - (self.level * 30))
        
        def show_next(index=0):
            if index < len(self.sequence):
                digit = self.sequence[index]
                
                self.digit_label.configure(text=str(digit), text_color="#4a9eff")
                
                def clear_and_next():
                    self.digit_label.configure(text="")
                    self.app.after(200, lambda: show_next(index + 1))
                
                self.app.after(delay, clear_and_next)
            else:
                self.is_showing = False
                self.header.configure(text="Enter the sequence!")
                
                # Switch from digit display to number pad
                self.digit_label.pack_forget()
                self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")
                
        show_next()
        
    def _highlight_button(self, number, color):
        """Highlight a number button with the specified color"""
        try:
            if not hasattr(self, 'number_buttons') or not self.number_buttons:
                return
            if number == 0:
                self.number_buttons[3][1].configure(fg_color=color)
            else:
                row = (number - 1) // 3
                col = (number - 1) % 3
                self.number_buttons[row][col].configure(fg_color=color)
        except Exception:
            pass
        
    def _reset_button(self, number):
        """Reset a number button to default color"""
        try:
            if not hasattr(self, 'number_buttons') or not self.number_buttons:
                return
            if number == 0:
                self.number_buttons[3][1].configure(fg_color="gray85")
            else:
                row = (number - 1) // 3
                col = (number - 1) % 3
                self.number_buttons[row][col].configure(fg_color="gray85")
        except Exception:
            pass
        
    def _level_complete(self):
        """Handle successful level completion"""
        # Reset all buttons to default color
        for i in range(3):
            for j in range(3):
                self.number_buttons[i][j].configure(fg_color="gray85")
        self.number_buttons[3][1].configure(fg_color="gray85")
        
        # Update level and record
        self.level += 1
        records = load_records()
        update_record(records, self.GAME_NAME, self.level - 1)
        self.level_label.configure(text=f"Level: {self.level}")
        self.header.configure(text="Great! Next level...")
        self.is_playing = False
        
        # Switch back to digit display
        self.grid_frame.place_forget()
        self.digit_label.pack()
        
        self.app.after(1500, self._start_level)
        
    def _game_over(self):
        """Handle game over"""
        self.is_playing = False
        self.is_showing = False
        
        # Flash all buttons red
        for i in range(3):
            for j in range(3):
                self.number_buttons[i][j].configure(fg_color="#8b0000")
        self.number_buttons[3][1].configure(fg_color="#8b0000")
        
        self.app.after(500, self._show_game_over_screen)
        
    def _show_game_over_screen(self):
        """Display game over modal"""
        # Reset button colors first
        for i in range(3):
            for j in range(3):
                self.number_buttons[i][j].configure(fg_color="gray85")
        self.number_buttons[3][1].configure(fg_color="gray85")
        
        # Show game over modal
        self.show_game_over_modal(self.GAME_NAME, self.level - 1, self.start)
