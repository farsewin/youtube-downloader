import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
from threading import Thread

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader by faris bouziane")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Configure grid weights for centering
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create a container frame
        self.container = ttk.Frame(root, padding="10")
        self.container.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Configure the container grid for centering the content
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        # Create main frame inside the container
        self.main_frame = ttk.Frame(self.container, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="")

        # Center the main frame inside the container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Add widgets to main_frame
        self.create_widgets()

    def create_widgets(self):
        # URL Entry
        ttk.Label(self.main_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.main_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Download Type
        ttk.Label(self.main_frame, text="Download Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.download_type = tk.StringVar(value="video")
        ttk.Radiobutton(self.main_frame, text="Video", variable=self.download_type, 
                       value="video", command=self.toggle_quality).grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(self.main_frame, text="Audio", variable=self.download_type,
                       value="audio", command=self.toggle_quality).grid(row=1, column=2, sticky=tk.W)
        
        # Quality Selection
        ttk.Label(self.main_frame, text="Quality:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="720p")
        self.quality_combo = ttk.Combobox(self.main_frame, textvariable=self.quality_var,
                                        values=["480p", "720p", "1080p", "best"])
        self.quality_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Playlist Option
        self.is_playlist = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.main_frame, text="Playlist", variable=self.is_playlist).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        
        # Output Directory
        ttk.Label(self.main_frame, text="Save to:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar(value=os.getcwd())
        ttk.Entry(self.main_frame, textvariable=self.output_path, width=50).grid(
            row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_output).grid(
            row=4, column=3, sticky=tk.W, pady=5)
        
        # Progress Bar
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(self.main_frame, textvariable=self.progress_var).grid(
            row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        self.progress_bar = ttk.Progressbar(self.main_frame, length=400, mode='determinate')
        self.progress_bar.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # Download Button
        self.download_btn = ttk.Button(self.main_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=7, column=0, columnspan=4, pady=20)

    def toggle_quality(self):
        if self.download_type.get() == "audio":
            self.quality_combo.set("")
            self.quality_combo["state"] = "disabled"
        else:
            self.quality_combo["state"] = "normal"
            self.quality_combo.set("720p")

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def update_progress(self, d):
        if d['status'] == 'downloading':
            # Update progress bar
            if '_percent_str' in d:
                percent = float(d['_percent_str'].replace('%', ''))
                self.progress_bar['value'] = percent
                self.progress_var.set(f"Downloading: {d['_percent_str']} at {d.get('_speed_str', '0 B/s')} ETA: {d.get('_eta_str', 'N/A')}")
                self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.progress_var.set("Download completed!")
            self.progress_bar['value'] = 100

    def download(self):
        try:
            url = self.url_var.get()
            output_path = self.output_path.get()
            is_playlist = self.is_playlist.get()
            download_type = self.download_type.get()
            
            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return
                
            # Configure yt-dlp options
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.update_progress],
            }
            
            if download_type == "video":
                quality = self.quality_var.get()
                ydl_opts['format'] = f'best[height<={quality[:-1]}]' if quality != 'best' else 'best'
            else:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            if is_playlist:
                ydl_opts['outtmpl'] = os.path.join(output_path, '%(playlist)s/%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("Success", "Download completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        finally:
            self.download_btn["state"] = "normal"
            self.progress_var.set("Ready")
            self.progress_bar['value'] = 0

    def start_download(self):
        self.download_btn["state"] = "disabled"
        self.progress_var.set("Starting download...")
        self.progress_bar['value'] = 0
        Thread(target=self.download, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()