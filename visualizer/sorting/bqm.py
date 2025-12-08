import pygame
import sys
import random
import time
import threading

# ==============================
# KONFIGURASI
# ==============================
WIDTH, HEIGHT = 1400, 600
BAR_WIDTH = 3
N = 500  # Ubah sesuai kebutuhan
FPS = 60

# Warna
BG = (30, 30, 40)
GRID_COLOR = (50, 50, 60)
COMPARE_COLOR = (255, 215, 0)    # emas
SWAP_COLOR = (255, 80, 80)      # merah muda
DONE_BG = (40, 60, 40)          # hijau gelap
TEXT_COLOR = (220, 220, 220)

# ==============================
# IMPLEMENTASI ALGORITMA (UNTUK ANIMASI - DENGAN CALLBACK & SLEEP)
# ==============================

def bubble_sort(arr, on_compare, on_swap, on_done):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            on_compare(j, j + 1)
            time.sleep(0.0001)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                on_swap(j, j + 1)
                time.sleep(0.0001)
    on_done()

def partition(arr, low, high, on_compare, on_swap):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        on_compare(j, high)
        time.sleep(0.0001)
        if arr[j] <= pivot:
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                on_swap(i, j)
                time.sleep(0.0001)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    on_swap(i + 1, high)
    return i + 1

def quick_sort(arr, low, high, on_compare, on_swap, on_done):
    if low < high:
        pi = partition(arr, low, high, on_compare, on_swap)
        quick_sort(arr, low, pi - 1, on_compare, on_swap, lambda: None)
        quick_sort(arr, pi + 1, high, on_compare, on_swap, lambda: None)
    if low == 0 and high == len(arr) - 1:
        on_done()

def merge(arr, l, m, r, on_compare, on_write):
    left = arr[l:m+1]
    right = arr[m+1:r+1]
    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        on_compare(l + i, m + 1 + j)
        time.sleep(0.0001)
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        on_write(k)
        time.sleep(0.0001)
        k += 1
    while i < len(left):
        arr[k] = left[i]
        on_write(k)
        time.sleep(0.0001)
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        on_write(k)
        time.sleep(0.0001)
        j += 1
        k += 1

def merge_sort(arr, l, r, on_compare, on_write, on_done):
    if l < r:
        m = (l + r) // 2
        merge_sort(arr, l, m, on_compare, on_write, lambda: None)
        merge_sort(arr, m+1, r, on_compare, on_write, lambda: None)
        merge(arr, l, m, r, on_compare, on_write)
    if l == 0 and r == len(arr) - 1:
        on_done()

# ==============================
# IMPLEMENTASI ALGORITMA (UNTUK BENCHMARK CPU - TANPA SLEEP/CALLBACK)
# ==============================

def bubble_sort_clean(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort_clean(arr):
    arr = arr[:]
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def qs(low, high):
        if low < high:
            pi = partition(low, high)
            qs(low, pi - 1)
            qs(pi + 1, high)

    qs(0, len(arr) - 1)
    return arr

def merge_sort_clean(arr):
    arr = arr[:]
    def merge(l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    def ms(l, r):
        if l < r:
            m = (l + r) // 2
            ms(l, m)
            ms(m + 1, r)
            merge(l, m, r)

    ms(0, len(arr) - 1)
    return arr

# ==============================
# VISUALIZER
# ==============================

class SortVisualizer:
    def __init__(self, name, y_offset, data, cpu_time):
        self.name = name
        self.y_offset = y_offset
        self.data = data[:]
        self.compare = set()
        self.highlight = set()
        self.done = False
        self.start_time = None
        self.elapsed = 0.0
        self.cpu_time = cpu_time  # waktu CPU murni

    def start_sort(self, sort_func):
        self.start_time = time.time()
        def on_compare(i, j):
            if not self.done:
                self.compare = {i, j}
        def on_swap(i, j):
            if not self.done:
                self.compare = set()
                self.highlight = {i, j}
        def on_write(i):
            if not self.done:
                self.compare = set()
                self.highlight = {i}
        def on_done():
            if not self.done:
                self.done = True
                self.elapsed = time.time() - self.start_time
                self.compare = set()
                self.highlight = set()

        if self.name == "Merge Sort":
            thread = threading.Thread(
                target=merge_sort,
                args=(self.data, 0, len(self.data)-1, on_compare, on_write, on_done)
            )
        elif self.name == "Quick Sort":
            thread = threading.Thread(
                target=quick_sort,
                args=(self.data, 0, len(self.data)-1, on_compare, on_swap, on_done)
            )
        else:  # Bubble
            thread = threading.Thread(
                target=bubble_sort,
                args=(self.data, on_compare, on_swap, on_done)
            )
        thread.daemon = True
        thread.start()

    def draw(self, screen, font):
        bg_color = DONE_BG if self.done else BG
        pygame.draw.rect(screen, bg_color, (0, self.y_offset, WIDTH, HEIGHT // 3))

        for i, val in enumerate(self.data):
            x = i * (BAR_WIDTH + 1) + 50
            y = self.y_offset + (HEIGHT // 3 - val * (HEIGHT // 3) // N)
            h = val * (HEIGHT // 3) // N
            color = SWAP_COLOR if i in self.highlight else \
                    COMPARE_COLOR if i in self.compare else \
                    (60, 60, 255) if self.name == "Bubble Sort" else \
                    (60, 255, 60) if self.name == "Quick Sort" else \
                    (255, 60, 60)
            pygame.draw.rect(screen, color, (x, y, BAR_WIDTH, h))

        # Tampilkan waktu
        if self.start_time is None:
            anim_str = "0.0000"
        elif self.done:
            anim_str = f"{self.elapsed:.4f}"
        else:
            anim_str = f"{time.time() - self.start_time:.4f}"

        if self.done:
            time_str = f"Anim: {anim_str}s | CPU: {self.cpu_time:.5f}s"
        else:
            time_str = f"Anim: {anim_str}s"

        status = "✓ Selesai" if self.done else "Memproses..."
        label = f"{self.name} | {status} | {time_str}"
        text = font.render(label, True, TEXT_COLOR)
        screen.blit(text, (10, self.y_offset + 10))

# ==============================
# MAIN
# ==============================

def main():
    random.seed(42)
    base_data = random.sample(range(1, N + 1), N)

    # Ukur waktu CPU murni
    cpu_bubble = time.perf_counter() - time.perf_counter()
    cpu_quick = cpu_bubble
    cpu_merge = cpu_bubble

    data_test = base_data[:]
    start = time.perf_counter()
    bubble_sort_clean(data_test)
    cpu_bubble = time.perf_counter() - start

    data_test = base_data[:]
    start = time.perf_counter()
    quick_sort_clean(data_test)
    cpu_quick = time.perf_counter() - start

    data_test = base_data[:]
    start = time.perf_counter()
    merge_sort_clean(data_test)
    cpu_merge = time.perf_counter() - start

    print(f"⏱️  Waktu CPU: Bubble={cpu_bubble:.5f}s, Quick={cpu_quick:.5f}s, Merge={cpu_merge:.5f}s")

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Sorting Visualizer - N = {N}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    visualizers = [
        SortVisualizer("Bubble Sort", 0, base_data, cpu_bubble),
        SortVisualizer("Quick Sort", HEIGHT // 3, base_data, cpu_quick),
        SortVisualizer("Merge Sort", 2 * HEIGHT // 3, base_data, cpu_merge),
    ]

    visualizers[0].start_sort(bubble_sort)
    visualizers[1].start_sort(quick_sort)
    visualizers[2].start_sort(merge_sort)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BG)

        for i in range(0, WIDTH, 50):
            pygame.draw.line(screen, GRID_COLOR, (i, 0), (i, HEIGHT), 1)
        for i in range(0, HEIGHT, HEIGHT // 3):
            pygame.draw.line(screen, (80, 80, 90), (0, i), (WIDTH, i), 2)

        for viz in visualizers:
            viz.draw(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    # ==============================
    # BIKIN GRAFIK SETELAH ANIMASI
    # ==============================
    pygame.quit()
    print("\n📊 Membuat grafik perbandingan kompleksitas CPU...")

    try:
        import matplotlib.pyplot as plt
        import os

        step = max(5, N // 20)
        sizes = list(range(step, N + 1, step))
        if N not in sizes:
            sizes.append(N)
        sizes = sorted(set(sizes))

        bubble_times = []
        quick_times = []
        merge_times = []
        random.seed(42)

        for n in sizes:
            data = random.sample(range(1, n * 2), n)

            start = time.perf_counter()
            bubble_sort_clean(data)
            bubble_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            quick_sort_clean(data)
            quick_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            merge_sort_clean(data)
            merge_times.append(time.perf_counter() - start)

        plt.figure(figsize=(10, 6))
        plt.plot(sizes, bubble_times, label="Bubble Sort",
                 color=(60/255, 60/255, 255/255), linewidth=2.5, marker='o')
        plt.plot(sizes, quick_times, label="Quick Sort",
                 color=(60/255, 255/255, 60/255), linewidth=2.5, marker='s')
        plt.plot(sizes, merge_times, label="Merge Sort",
                 color=(255/255, 60/255, 60/255), linewidth=2.5, marker='^')

        plt.title(f"Perbandingan Waktu CPU (n = {min(sizes)} – {N})", fontsize=14, weight='bold')
        plt.xlabel("Jumlah Data (n)", fontsize=12)
        plt.ylabel("Waktu (detik)", fontsize=12)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        filename = f"sorting_cpu_comparison_N{N}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✅ Grafik disimpan: {os.path.abspath(filename)}")

    except ImportError:
        print("⚠️  Matplotlib tidak terinstal. Lewati pembuatan grafik.")
        print("   Jalankan: pip install matplotlib")

    sys.exit()

if __name__ == "__main__":
    main()