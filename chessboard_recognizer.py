import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import os


class ChessboardRecognizer:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Chessboard Recognizer")
        self.root.attributes('-topmost', True)

        # Get screen width and height
        self.screen_width = self.root.winfo_screenwidth() * 2 / 3
        self.screen_height = self.root.winfo_screenheight() * 2 / 3

        # Load and resize the image to fit the screen
        self.image = Image.open(image_path)
        self.scale = min(self.screen_width / self.image.width, self.screen_height / self.image.height)
        self.scaled_image = self.image.resize((int(self.image.width * self.scale), int(self.image.height * self.scale)),
                                              Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.scaled_image)

        # Initialize canvas
        self.canvas = tk.Canvas(self.root, width=int(self.image.width * self.scale),
                                height=int(self.image.height * self.scale))
        self.canvas.pack()

        # Add image to canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Bind the mouse click event
        self.canvas.bind("<Button-1>", self.get_mouse_pos)
        self.corners = []

    def get_mouse_pos(self, event):
        # Calculate the original image coordinates
        orig_x = event.x / self.scale
        orig_y = event.y / self.scale
        self.corners.append((orig_x, orig_y))

        # Show the point on the canvas
        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill='red')

        if len(self.corners) == 2:
            self.recognize_chessboard()
            #self.root.destroy()
            self.root.quit()
    def zoom_image(self, event):
        # Zoom in or out
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.canvas_img)

        if event.delta > 0:
            if self.zoom_factor < 3:  # Limit zoom in factor to prevent image quality degradation
                self.zoom_factor *= 1.1
                self.image = self.image.resize((int(bbox[2] * 1.1), int(bbox[3] * 1.1)), Image.ANTIALIAS)
        else:
            if self.zoom_factor > 0.5:  # Limit zoom out factor to prevent image from getting too small
                self.zoom_factor /= 1.1
                self.image = self.image.resize((int(bbox[2] / 1.1), int(bbox[3] / 1.1)), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_img, image=self.photo)
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.scale("all", x, y, 1.1 if event.delta > 0 else 0.9, 1.1 if event.delta > 0 else 0.9)



    def get_mouse_pos(self, event):
        # Record the positions of two corners
        if len(self.corners) < 2:
            self.corners.append((event.x, event.y))
            self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill='red')

            if len(self.corners) == 2:
                self.recognize_chessboard()
                self.root.quit()  # 关闭窗口

    def recognize_chessboard(self):
        top_left, bottom_right = self.corners
        # Scale corners back to original image size
        top_left = (int(top_left[0] / self.scale), int(top_left[1] / self.scale))
        bottom_right = (int(bottom_right[0] / self.scale), int(bottom_right[1] / self.scale))

        grid_width = (bottom_right[0] - top_left[0]) // 8
        grid_height = (bottom_right[1] - top_left[1]) // 8
        circle_radius = int(min(grid_width, grid_height) * 0.8 / 2)  # 80% of the half of smaller dimension

        self.board = []
        self.grid_images = []
        for i in range(8):
            row = []
            for j in range(8):
                left = top_left[0] + j * grid_width
                top = top_left[1] + i * grid_height
                box = (left, top, left + grid_width, top + grid_height)
                grid = self.image.crop(box)

                # Create a circular mask to crop the circle from the grid
                mask = Image.new('L', (grid_width, grid_height), 0)
                draw = ImageDraw.Draw(mask)
                # Calculate the center and radius of the circle for mask
                center_x, center_y = grid_width // 2, grid_height // 2
                draw.ellipse((center_x - circle_radius, center_y - circle_radius, center_x + circle_radius,
                              center_y + circle_radius), fill=255)
                grid = Image.composite(grid, Image.new('RGB', (grid_width, grid_height)), mask)
                self.grid_images.append(grid)

                # Analyze the average color in the circle
                avg_color = np.mean(np.array(grid), axis=(0, 1))
                # Define a threshold for near-black or near-white recognition
                black_threshold = 30  # 1% of 255
                white_threshold = 80
                color_range = 20

                # Check if the range of color components is greater than 10
                if np.ptp(avg_color) > color_range:
                    color = 'E'  # Empty
                # Check if all color components are less than 30
                elif np.all(avg_color < black_threshold):
                    color = 'B'  # Black
                # Check if all color components are greater than 105
                elif np.all(avg_color > white_threshold):
                    color = 'W'  # White
                else:
                    #print('error')
                    color = 'E'  # Empty
                #print("avgcolor", avg_color)
                row.append(color)
            self.board.append(row)

        self.current_grid = 0
        #self.show_grid_image()
        #for row in self.board:
            #print(" ".join(row))
        return self.board

    def show_grid_image(self):
        if self.current_grid < 64:
            grid = self.grid_images[self.current_grid]
            color = self.board[self.current_grid // 8][self.current_grid % 8]
            self.current_grid += 1

            self.top = Toplevel(self.root)
            self.top.title(f"Grid {self.current_grid}")
            photo = ImageTk.PhotoImage(grid)
            label = tk.Label(self.top, image=photo)
            label.image = photo
            label.pack()

            result_label = tk.Label(self.top, text=f"Recognized as: {color}")
            result_label.pack()

            next_button = tk.Button(self.top, text="Next", command=self.show_grid_image)
            next_button.pack()

    def run(self):
        self.root.mainloop()


# Function to find the first image file in the current directory
def find_first_image(directory):
    for file in os.listdir(directory):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            return os.path.join(directory, file)
    return None


# Replace 'your_directory_path' with the path to your image directory
#image_path = find_first_image(r'D:\Users\Tianhao\Documents\GitHub\pictochess')
#current_dir = os.path.dirname(os.path.abspath(__file__))
#image_path = find_first_image(current_dir)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = find_first_image(current_dir)

    if image_path:
        recognizer = ChessboardRecognizer(image_path)
        recognizer.run()
        return recognizer.board  # 返回识别的棋盘结果
    else:
        print("No image files found in the directory.")
        return None


if __name__ == "__main__":
    recognized_board = main()
    #if recognized_board:
        #for row in recognized_board:
           #print(" ".join(row))
