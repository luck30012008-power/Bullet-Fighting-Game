import tkinter as tk
import random

# Game setup
WIDTH = 600
HEIGHT = 700
PLAYER_SPEED = 10
BULLET_SPEED = 15
ENEMY_SPEED = 5
ENEMY_SPAWN_RATE = 2000  # ms

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Space Shooter")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.score = 0
        self.game_over = False

        # Player
        self.player = self.canvas.create_rectangle(WIDTH//2 - 20, HEIGHT - 40,
                                                   WIDTH//2 + 20, HEIGHT - 10,
                                                   fill="cyan")

        self.bullets = []
        self.enemies = []

        # Score text
        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  fill="white", font=("Arial", 16),
                                                  text="Score: 0")

        # Key states
        self.keys = {"Left": False, "Right": False, "space": False}

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.spawn_enemy()
        self.update()

    def on_key_press(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = True

    def on_key_release(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = False

    def handle_input(self):
        if self.keys["Left"]:
            x1, y1, x2, y2 = self.canvas.coords(self.player)
            if x1 > 0:
                self.canvas.move(self.player, -PLAYER_SPEED, 0)
        if self.keys["Right"]:
            x1, y1, x2, y2 = self.canvas.coords(self.player)
            if x2 < WIDTH:
                self.canvas.move(self.player, PLAYER_SPEED, 0)
        if self.keys["space"]:
            self.shoot()

    def shoot(self):
        if not self.game_over:
            # limit firing rate
            if not hasattr(self, "can_shoot") or self.can_shoot:
                x1, y1, x2, y2 = self.canvas.coords(self.player)
                bullet = self.canvas.create_rectangle((x1+x2)//2 - 2, y1 - 10,
                                                      (x1+x2)//2 + 2, y1,
                                                      fill="yellow")
                self.bullets.append(bullet)
                self.can_shoot = False
                # allow shooting again after 200ms
                self.root.after(200, self.enable_shoot)

    def enable_shoot(self):
        self.can_shoot = True

    def spawn_enemy(self):
        if not self.game_over:
            x = random.randint(20, WIDTH - 20)
            enemy = self.canvas.create_rectangle(x-15, 0, x+15, 30, fill="red")
            self.enemies.append(enemy)
            self.root.after(ENEMY_SPAWN_RATE, self.spawn_enemy)

    def update(self):
        if self.game_over:
            return

        # Handle inputs every frame
        self.handle_input()

        # Move bullets
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -BULLET_SPEED)
            if self.canvas.coords(bullet)[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

        # Move enemies
        for enemy in self.enemies[:]:
            self.canvas.move(enemy, 0, ENEMY_SPEED)
            if self.canvas.coords(enemy)[3] > HEIGHT:
                self.game_over_screen()
                return

        # Check collisions
        for bullet in self.bullets[:]:
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            for enemy in self.enemies[:]:
                ex1, ey1, ex2, ey2 = self.canvas.coords(enemy)
                if bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1:
                    # hit
                    self.canvas.delete(bullet)
                    self.canvas.delete(enemy)
                    if bullet in self.bullets: self.bullets.remove(bullet)
                    if enemy in self.enemies: self.enemies.remove(enemy)
                    self.score += 10
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    break

        self.root.after(30, self.update)

    def game_over_screen(self):
        self.game_over = True
        self.canvas.create_text(WIDTH//2, HEIGHT//2, fill="red",
                                font=("Arial", 30, "bold"), text="GAME OVER")
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 50, fill="white",
                                font=("Arial", 20), text=f"Final Score: {self.score}")


root = tk.Tk()
game = Game(root)
root.mainloop()
