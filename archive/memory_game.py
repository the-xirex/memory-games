import customtkinter as ctk
import random
import os
import sys
import json


class MemoryGame:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Memory Games")
        self.app.geometry("800x600")
        self.app.resizable(False, False)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        if sys.platform == 'win32':
            app_data = os.getenv('APPDATA')
            app_folder = os.path.join(app_data, 'MemoryGames')
        else:
            app_folder = os.path.join(os.path.expanduser('~'), '.memorygames')
        
        if not os.path.exists(app_folder):
            os.makedirs(app_folder)
        
        self.records_file = os.path.join(app_folder, 'records.json')
        self.records = self.load_records()
        
        try:
            if getattr(sys, 'frozen', False):
                icon_base_path = sys._MEIPASS
            else:
                icon_base_path = os.path.dirname(__file__)
            
            icon_path = os.path.join(icon_base_path, 'brainstorm.ico')
            
            if os.path.exists(icon_path):
                self.app.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.app.geometry(f"800x600+{x}+{y}")
        
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        
        self.show_main_menu()
    
    def load_records(self):
        """Загрузка рекордов из JSON файла"""
        try:
            if os.path.exists(self.records_file):
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading records: {e}")
        
        return {
            'Spatial Memory Game': 0,
            'Corsi Block Test': 0,
            'Memory Span': 0
        }
    
    def save_records(self):
        """Сохранение рекордов в JSON файл"""
        try:
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving records: {e}")
    
    def update_record(self, game_name, score):
        """Обновление рекорда если новый результат лучше"""
        if score > self.records.get(game_name, 0):
            self.records[game_name] = score
            self.save_records()
            return True
        return False
    
    def reset_records(self):
        """Сброс всех рекордов"""
        self.records = {
            'Spatial Memory Game': 0,
            'Corsi Block Test': 0,
            'Memory Span': 0
        }
        self.save_records()
        self.show_main_menu()
    
    def show_help_tooltip(self, widget, title, description):
        self.help_tooltip = ctk.CTkFrame(self.app, fg_color="white", corner_radius=10, border_width=2, border_color="#4a9eff")
        
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
        if hasattr(self, 'help_tooltip'):
            self.help_tooltip.destroy()
    
    def show_main_menu(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        
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
        help_btn.bind("<Enter>", lambda e: self.show_help_tooltip(help_btn, 
            "Memory Games",
            "Train your memory and cognitive skills\nwith these scientifically-based games.\n\n"
            "Created by:\n"
            "Volokitin Vladyslav"))
        help_btn.bind("<Leave>", lambda e: self.hide_help_tooltip())
        
        main_container = ctk.CTkFrame(self.app, fg_color="transparent")
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
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
            command=self.start_spatial_game
        )
        game1_btn.pack(pady=12)
        
        game2_btn = ctk.CTkButton(
            button_frame,
            text="Corsi Block Test",
            font=ctk.CTkFont(size=16),
            width=280,
            height=50,
            command=self.start_corsi_game
        )
        game2_btn.pack(pady=12)
        
        game3_btn = ctk.CTkButton(
            button_frame,
            text="Memory Span",
            font=ctk.CTkFont(size=16),
            width=280,
            height=50,
            command=self.start_memory_span_game
        )
        game3_btn.pack(pady=12)
        
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
        
        games = [
            ("Spatial Memory", "Spatial Memory Game"),
            ("Corsi Block", "Corsi Block Test"),
            ("Memory Span", "Memory Span")
        ]
        
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
            
            score = self.records.get(game_key, 0)
            score_label = ctk.CTkLabel(
                record_frame,
                text=f"Level {score}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#1f6aa5"
            )
            score_label.pack(side="right", padx=15, pady=12)
        
        reset_btn = ctk.CTkButton(
            right_frame,
            text="Reset Records",
            font=ctk.CTkFont(size=12),
            width=150,
            height=30,
            fg_color="gray70",
            hover_color="gray60",
            command=self.reset_records
        )
        reset_btn.pack(pady=(10, 20))
        
    def start_spatial_game(self):
        for widget in self.app.winfo_children():
            widget.destroy()
            
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        self.game_started = False
        
        top_frame = ctk.CTkFrame(self.app, height=50, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)
        top_frame.pack_propagate(False)
        
        back_btn = ctk.CTkButton(
            top_frame,
            text="Back",
            width=80,
            height=30,
            command=self.show_main_menu
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
        help_btn.bind("<Enter>", lambda e: self.show_help_tooltip(help_btn, 
            "Spatial Memory Game",
            "Remember the sequence of highlighted squares.\n\n"
            "Develops:\n"
            "• Visual-spatial memory\n"
            "• Pattern recognition\n"
            "• Sequential memory"))
        help_btn.bind("<Leave>", lambda e: self.hide_help_tooltip())
        
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
                    command=lambda idx=i*3+j: self.button_clicked(idx)
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
            command=self.start_level
        )
        self.start_btn.place(in_=button_spacer, relx=0.5, rely=0.5, anchor="center")
        
    def button_clicked(self, index):
        if not self.game_started or not self.is_playing or self.is_showing:
            return
            
        self.user_sequence.append(index)
        
        row, col = index // 3, index % 3
        self.highlight_button(row, col, "#1f6aa5")
        
        if self.user_sequence[-1] != self.sequence[len(self.user_sequence)-1]:
            self.app.after(300, lambda: self.game_over())
        elif len(self.user_sequence) == len(self.sequence):
            self.app.after(300, lambda: self.level_complete())
        else:
            self.app.after(300, lambda: self.reset_button(row, col))
            
    def start_level(self):
        self.game_started = True
        self.start_btn.place_forget()
        
        def countdown(count):
            if count > 0:
                self.header.configure(text=f"{count}")
                self.app.after(1000, lambda: countdown(count - 1))
            else:
                self.begin_level()
        
        if self.level == 1:
            countdown(3)
        else:
            self.begin_level()
    
    def begin_level(self):
        self.is_playing = True
        self.is_showing = True
        self.user_sequence = []
        
        self.sequence.extend([random.randint(0, 8) for _ in range(1)])
        
        self.header.configure(text="Watch the sequence...")
        
        self.show_sequence()
        
    def show_sequence(self):
        delay = max(400, 800 - (self.level * 30))
        
        def show_next(index=0):
            if index < len(self.sequence):
                pos = self.sequence[index]
                row, col = pos // 3, pos % 3
                
                self.highlight_button(row, col, "#4a9eff")
                
                self.app.after(delay, lambda: self.reset_button(row, col))
                self.app.after(delay + 200, lambda: show_next(index + 1))
            else:
                self.is_showing = False
                self.header.configure(text="Repeat the sequence!")
                
        show_next()
        
    def highlight_button(self, row, col, color):
        try:
            if hasattr(self, 'buttons') and self.buttons and row < len(self.buttons) and col < len(self.buttons[row]):
                self.buttons[row][col].configure(fg_color=color)
        except Exception:
            pass
        
    def reset_button(self, row, col):
        try:
            if hasattr(self, 'buttons') and self.buttons and row < len(self.buttons) and col < len(self.buttons[row]):
                self.buttons[row][col].configure(fg_color="gray85")
        except Exception:
            pass
        
    def level_complete(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(fg_color="gray85")
        
        self.level += 1
        self.update_record('Spatial Memory Game', self.level - 1)
        self.level_label.configure(text=f"Level: {self.level}")
        self.header.configure(text="Great! Next level...")
        self.is_playing = False
        
        self.app.after(1500, self.start_level)
        
    def game_over(self):
        self.is_playing = False
        self.is_showing = False
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(fg_color="#8b0000")
        
        self.app.after(500, self.show_game_over_screen)
        
    def show_game_over_screen(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(fg_color="gray85")
        
        self.header.configure(text="Game Over!")
        
        score = self.level - 1
        
        overlay = ctk.CTkFrame(self.app, fg_color="gray40")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        overlay.configure(corner_radius=0)
        
        modal_frame = ctk.CTkFrame(overlay, fg_color="white", corner_radius=15, width=400, height=300)
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
            command=lambda: [overlay.destroy(), self.restart_game()]
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="No",
            width=120,
            height=40,
            command=lambda: [overlay.destroy(), self.show_main_menu()]
        ).pack(side="left", padx=10)
        
    def restart_game(self):
        self.start_spatial_game()
        
    def start_corsi_game(self):
        for widget in self.app.winfo_children():
            widget.destroy()
            
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        self.game_started = False
        self.block_positions = []
        
        top_frame = ctk.CTkFrame(self.app, height=50, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)
        top_frame.pack_propagate(False)
        
        back_btn = ctk.CTkButton(
            top_frame,
            text="Back",
            width=80,
            height=30,
            command=self.show_main_menu
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
        help_btn.bind("<Enter>", lambda e: self.show_help_tooltip(help_btn, 
            "Corsi Block Test",
            "Remember the sequence of randomly\npositioned blocks.\n\n"
            "Develops:\n"
            "• Spatial working memory\n"
            "• Visual attention\n"
            "• Cognitive flexibility"))
        help_btn.bind("<Leave>", lambda e: self.hide_help_tooltip())
        
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
        
        self.generate_random_blocks()
        
        button_spacer = ctk.CTkFrame(self.app, fg_color="transparent", height=45)
        button_spacer.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            self.app,
            text="START",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=180,
            height=45,
            command=self.start_corsi_level
        )
        self.start_btn.place(in_=button_spacer, relx=0.5, rely=0.5, anchor="center")
        
    def generate_random_blocks(self):
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
                        command=lambda idx=block_idx: self.corsi_button_clicked(idx)
                    )
                    btn.place(x=x, y=y)
                    self.corsi_buttons.append(btn)
                    placed = True
                
                attempts += 1
                
    def corsi_button_clicked(self, index):
        if not self.game_started or not self.is_playing or self.is_showing:
            return
            
        self.user_sequence.append(index)
        
        self.highlight_corsi_button(index, "#1f6aa5")
        
        if self.user_sequence[-1] != self.sequence[len(self.user_sequence)-1]:
            self.app.after(300, lambda: self.corsi_game_over())
        elif len(self.user_sequence) == len(self.sequence):
            self.app.after(300, lambda: self.corsi_level_complete())
        else:
            self.app.after(300, lambda: self.reset_corsi_button(index))
            
    def start_corsi_level(self):
        self.game_started = True
        self.start_btn.place_forget()
        
        def countdown(count):
            if count > 0:
                self.header.configure(text=f"{count}")
                self.app.after(1000, lambda: countdown(count - 1))
            else:
                self.begin_corsi_level()
        
        if self.level == 1:
            countdown(3)
        else:
            self.begin_corsi_level()
    
    def begin_corsi_level(self):
        self.is_playing = True
        self.is_showing = True
        self.user_sequence = []
        
        self.sequence.extend([random.randint(0, 11) for _ in range(1)])
        
        self.header.configure(text="Watch the sequence...")
        
        self.show_corsi_sequence()
        
    def show_corsi_sequence(self):
        delay = max(400, 800 - (self.level * 30))
        
        def show_next(index=0):
            if index < len(self.sequence):
                pos = self.sequence[index]
                
                self.highlight_corsi_button(pos, "#4a9eff")
                
                self.app.after(delay, lambda: self.reset_corsi_button(pos))
                self.app.after(delay + 200, lambda: show_next(index + 1))
            else:
                self.is_showing = False
                self.header.configure(text="Repeat the sequence!")
                
        show_next()
        
    def highlight_corsi_button(self, index, color):
        try:
            if hasattr(self, 'corsi_buttons') and self.corsi_buttons and index < len(self.corsi_buttons):
                self.corsi_buttons[index].configure(fg_color=color)
        except Exception:
            pass
        
    def reset_corsi_button(self, index):
        try:
            if hasattr(self, 'corsi_buttons') and self.corsi_buttons and index < len(self.corsi_buttons):
                self.corsi_buttons[index].configure(fg_color="gray85")
        except Exception:
            pass
        
    def corsi_level_complete(self):
        for btn in self.corsi_buttons:
            btn.configure(fg_color="gray85")
        
        self.level += 1
        self.update_record('Corsi Block Test', self.level - 1)
        self.level_label.configure(text=f"Level: {self.level}")
        self.header.configure(text="Great! Next level...")
        self.is_playing = False
        
        self.app.after(1500, self.start_corsi_level)
        
    def corsi_game_over(self):
        self.is_playing = False
        self.is_showing = False
        
        for btn in self.corsi_buttons:
            btn.configure(fg_color="#8b0000")
        
        self.app.after(500, self.show_corsi_game_over_screen)
        
    def show_corsi_game_over_screen(self):
        for btn in self.corsi_buttons:
            btn.configure(fg_color="gray85")
        
        self.header.configure(text="Game Over!")
        
        score = self.level - 1
        
        overlay = ctk.CTkFrame(self.app, fg_color="gray40")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        overlay.configure(corner_radius=0)
        
        modal_frame = ctk.CTkFrame(overlay, fg_color="white", corner_radius=15, width=400, height=300)
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
            command=lambda: [overlay.destroy(), self.restart_corsi_game()]
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="No",
            width=120,
            height=40,
            command=lambda: [overlay.destroy(), self.show_main_menu()]
        ).pack(side="left", padx=10)
        
    def restart_corsi_game(self):
        self.start_corsi_game()
        
    def start_memory_span_game(self):
        for widget in self.app.winfo_children():
            widget.destroy()
            
        self.sequence = []
        self.user_sequence = []
        self.level = 1
        self.is_playing = False
        self.is_showing = False
        self.game_started = False
        
        top_frame = ctk.CTkFrame(self.app, height=50, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)
        top_frame.pack_propagate(False)
        
        back_btn = ctk.CTkButton(
            top_frame,
            text="Back",
            width=80,
            height=30,
            command=self.show_main_menu
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
        help_btn.bind("<Enter>", lambda e: self.show_help_tooltip(help_btn, 
            "Memory Span",
            "Remember the sequence of digits shown.\n\n"
            "Develops:\n"
            "• Numerical working memory\n"
            "• Short-term memory capacity\n"
            "• Concentration"))
        help_btn.bind("<Leave>", lambda e: self.hide_help_tooltip())
        
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
        
        self.grid_frame = ctk.CTkFrame(game_area, fg_color="transparent")
        
        self.number_buttons = []
        button_size = 90
        
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
                    command=lambda num=number: self.span_button_clicked(num)
                )
                btn.grid(row=i, column=j, padx=6, pady=6)
                row.append(btn)
            self.number_buttons.append(row)
        
        zero_btn = ctk.CTkButton(
            self.grid_frame,
            text="0",
            width=button_size,
            height=button_size,
            corner_radius=10,
            fg_color="gray85",
            hover_color="gray75",
            font=ctk.CTkFont(size=28, weight="bold"),
            command=lambda: self.span_button_clicked(0)
        )
        zero_btn.grid(row=3, column=1, padx=6, pady=6)
        self.number_buttons.append([None, zero_btn, None])
        
        button_spacer = ctk.CTkFrame(self.app, fg_color="transparent", height=45)
        button_spacer.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            self.app,
            text="START",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=180,
            height=45,
            command=self.start_span_level
        )
        self.start_btn.place(in_=button_spacer, relx=0.5, rely=0.5, anchor="center")
        
    def span_button_clicked(self, number):
        if not self.game_started or not self.is_playing or self.is_showing:
            return
            
        self.user_sequence.append(number)
        
        self.highlight_span_button(number, "#1f6aa5")
        
        if self.user_sequence[-1] != self.sequence[len(self.user_sequence)-1]:
            self.app.after(300, lambda: self.span_game_over())
        elif len(self.user_sequence) == len(self.sequence):
            self.app.after(300, lambda: self.span_level_complete())
        else:
            self.app.after(300, lambda: self.reset_span_button(number))
            
    def start_span_level(self):
        self.game_started = True
        self.start_btn.place_forget()
        self.digit_label.configure(text="")
        
        def countdown(count):
            if count > 0:
                self.header.configure(text=f"{count}")
                self.app.after(1000, lambda: countdown(count - 1))
            else:
                self.begin_span_level()
        
        if self.level == 1:
            countdown(3)
        else:
            self.begin_span_level()
    
    def begin_span_level(self):
        self.is_playing = True
        self.is_showing = True
        self.user_sequence = []
        
        self.sequence.extend([random.randint(0, 9) for _ in range(1)])
        
        self.header.configure(text="Watch the sequence...")
        
        self.show_span_sequence()
        
    def show_span_sequence(self):
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
                
                self.digit_label.pack_forget()
                self.grid_frame.place(relx=0.5, rely=0.5, anchor="center")
                
        show_next()
        
    def highlight_span_button(self, number, color):
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
        
    def reset_span_button(self, number):
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
        
    def span_level_complete(self):
        for i in range(3):
            for j in range(3):
                self.number_buttons[i][j].configure(fg_color="gray85")
        self.number_buttons[3][1].configure(fg_color="gray85")
        
        self.level += 1
        self.update_record('Memory Span', self.level - 1)
        self.level_label.configure(text=f"Level: {self.level}")
        self.header.configure(text="Great! Next level...")
        self.is_playing = False
        
        self.grid_frame.place_forget()
        self.digit_label.pack()
        
        self.app.after(1500, self.start_span_level)
        
    def span_game_over(self):
        self.is_playing = False
        self.is_showing = False
        
        for i in range(3):
            for j in range(3):
                self.number_buttons[i][j].configure(fg_color="#8b0000")
        self.number_buttons[3][1].configure(fg_color="#8b0000")
        
        self.app.after(500, self.show_span_game_over_screen)
        
    def show_span_game_over_screen(self):
        for i in range(3):
            for j in range(3):
                self.number_buttons[i][j].configure(fg_color="gray85")
        self.number_buttons[3][1].configure(fg_color="gray85")
        
        self.header.configure(text="Game Over!")
        
        score = self.level - 1
        
        overlay = ctk.CTkFrame(self.app, fg_color="gray40")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        overlay.configure(corner_radius=0)
        
        modal_frame = ctk.CTkFrame(overlay, fg_color="white", corner_radius=15, width=400, height=300)
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
            command=lambda: [overlay.destroy(), self.restart_span_game()]
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="No",
            width=120,
            height=40,
            command=lambda: [overlay.destroy(), self.show_main_menu()]
        ).pack(side="left", padx=10)
        
    def restart_span_game(self):
        self.start_memory_span_game()
        
    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    game = MemoryGame()
    game.run()
