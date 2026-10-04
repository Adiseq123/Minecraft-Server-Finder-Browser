import asyncio
import json
import os
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from mcstatus import JavaServer


class MCScannerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Server Finder & Browser")
        self.root.geometry("1000x650")

        self.all_servers = []  # Pełna lista znalezionych serwerów
        self.is_scanning = False

        self._build_ui()

    def _build_ui(self):
        # --- PANELS / TABS ---
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Zakładka 1: Skanowanie
        scan_tab = ttk.Frame(notebook, padding=10)
        notebook.add(scan_tab, text="🔍 Skanowanie")

        # --- KONFIGURACJA SKANERA ---
        # Opcja A: Skanowanie zakresem IP (Masscan)
        masscan_frame = ttk.LabelFrame(
            scan_tab, text=" Skanowanie zakresem IP (Masscan CLI) ", padding=10
        )
        masscan_frame.pack(fill="x", pady=5)

        ttk.Label(masscan_frame, text="Zakres IP (CIDR / zakres):").grid(
            row=0, column=0, sticky="w"
        )
        self.ip_range_var = tk.StringVar(value="185.0.0.0/16")
        ttk.Entry(masscan_frame, textvariable=self.ip_range_var, width=30).grid(
            row=0, column=1, padx=5, sticky="w"
        )

        ttk.Label(masscan_frame, text="Port:").grid(
            row=0, column=2, sticky="e", padx=5
        )
        self.port_var = tk.StringVar(value="25565")
        ttk.Entry(masscan_frame, textvariable=self.port_var, width=8).grid(
            row=0, column=3, sticky="w"
        )

        ttk.Label(masscan_frame, text="Rate (pakietów/s):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.rate_var = tk.StringVar(value="3000")
        ttk.Entry(masscan_frame, textvariable=self.rate_var, width=15).grid(
            row=1, column=1, padx=5, sticky="w"
        )

        # Opcja B: Plik JSON
        file_frame = ttk.LabelFrame(
            scan_tab, text=" Lub wczytaj gotowy plik z Masscan JSON ", padding=10
        )
        file_frame.pack(fill="x", pady=5)

        self.file_path_var = tk.StringVar(value="")
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(
            side="left", padx=5
        )
        ttk.Button(file_frame, text="Przeglądaj...", command=self.browse_file).pack(
            side="left"
        )

        # Wydajność Pythona
        perf_frame = ttk.LabelFrame(
            scan_tab, text=" Parametry weryfikacji MC ", padding=10
        )
        perf_frame.pack(fill="x", pady=5)

        ttk.Label(perf_frame, text="Maks. wątków (Concurrency):").grid(
            row=0, column=0, sticky="w"
        )
        self.limit_var = tk.StringVar(value="200")
        ttk.Entry(perf_frame, textvariable=self.limit_var, width=10).grid(
            row=0, column=1, padx=5, sticky="w"
        )

        ttk.Label(perf_frame, text="Timeout (s):").grid(
            row=0, column=2, sticky="e", padx=5
        )
        self.timeout_var = tk.StringVar(value="3.0")
        ttk.Entry(perf_frame, textvariable=self.timeout_var, width=10).grid(
            row=0, column=3, sticky="w"
        )

        # Przycisk start
        self.btn_start = ttk.Button(
            scan_tab, text="🚀 URUCHOM SKANOWANIE", command=self.start_scan_thread
        )
        self.btn_start.pack(fill="x", pady=10)

        self.status_var = tk.StringVar(value="Status: Gotowy do uruchomienia.")
        ttk.Label(scan_tab, textvariable=self.status_var, font=("Arial", 10, "bold")).pack(
            anchor="w"
        )

        # --- BROWSER / WYSZUKIWARKA (GŁÓWNY PANEL) ---
        browser_frame = ttk.Frame(self.root, padding=10)
        browser_frame.pack(fill="both", expand=True)

        # Wyszukiwarka i Filtry
        filter_frame = ttk.LabelFrame(
            browser_frame, text=" Wyszukiwarka i Filtry ", padding=10
        )
        filter_frame.pack(fill="x", pady=5)

        ttk.Label(filter_frame, text="Szukaj (IP / Wersja / MOTD):").pack(
            side="left", padx=5
        )
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_table)
        ttk.Entry(filter_frame, textvariable=self.search_var, width=30).pack(
            side="left", padx=5
        )

        self.only_players_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            filter_frame,
            text="Tylko z graczami online",
            variable=self.only_players_var,
            command=self.filter_table,
        ).pack(side="left", padx=15)

        ttk.Button(
            filter_frame, text="📋 Kopiuj Zaznaczony IP", command=self.copy_selected_ip
        ).pack(side="right", padx=5)

        # Tabela wyników
        columns = ("ip", "port", "version", "players", "ping", "motd")
        self.tree = ttk.Treeview(
            browser_frame, columns=columns, show="headings", selectmode="browse"
        )

        self.tree.heading("ip", text="Adres IP", command=lambda: self.sort_col("ip"))
        self.tree.heading("port", text="Port")
        self.tree.heading("version", text="Wersja")
        self.tree.heading(
            "players",
            text="Gracze (Online/Max)",
            command=lambda: self.sort_col("players"),
        )
        self.tree.heading(
            "ping", text="Ping (ms)", command=lambda: self.sort_col("ping")
        )
        self.tree.heading("motd", text="MOTD / Opis serwera")

        self.tree.column("ip", width=130)
        self.tree.column("port", width=60)
        self.tree.column("version", width=120)
        self.tree.column("players", width=100)
        self.tree.column("ping", width=80)
        self.tree.column("motd", width=400)

        scrollbar = ttk.Scrollbar(
            browser_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self.copy_selected_ip())

    # --- LOGIKA APLIKACJI ---

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            self.file_path_var.set(filename)

    def start_scan_thread(self):
        if self.is_scanning:
            return
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        self.is_scanning = True
        self.btn_start.config(state="disabled")
        targets = []

        json_file = self.file_path_var.get().strip()
        ip_range = self.ip_range_var.get().strip()

        # 1. Pozyskiwanie celów (Masscan lub Plik JSON)
        if json_file:
            self.status_var.set(f"Status: Wczytywanie pliku {json_file}...")
            targets = self.parse_json_file(json_file)
        elif ip_range:
            if not shutil.which("masscan"):
                messagebox.showerror(
                    "Błąd",
                    "Nie znaleziono programu Masscan w systemie PATH!\nZainstaluj"
                    " Masscan lub użyj opcji wczytania pliku JSON.",
                )
                self.reset_ui()
                return

            self.status_var.set(
                f"Status: Skanowanie portów z Masscan ({ip_range})..."
            )
            temp_output = "temp_scan.json"
            cmd = [
                "masscan",
                ip_range,
                f"-p{self.port_var.get()}",
                f"--rate={self.rate_var.get()}",
                "-oJ",
                temp_output,
            ]

            try:
                subprocess.run(cmd, check=True)
                targets = self.parse_json_file(temp_output)
                if os.path.exists(temp_output):
                    os.remove(temp_output)
            except Exception as e:
                messagebox.showerror("Błąd Masscan", f"Skanowanie nie powiodło się:\n{e}")
                self.reset_ui()
                return

        if not targets:
            messagebox.showwarning("Brak celów", "Nie znaleziono otwartych portów.")
            self.reset_ui()
            return

        # 2. Asynchroniczne odpytywanie serwerów Minecraft
        self.status_var.set(
            f"Status: Weryfikowanie protokołem MC dla {len(targets)} adresów..."
        )

        # Czyszczenie tabeli przed nowym skanem
        self.root.after(0, self.clear_results)

        try:
            limit = int(self.limit_var.get())
            timeout = float(self.timeout_var.get())
        except ValueError:
            limit, timeout = 200, 3.0

        asyncio.run(self.scan_minecraft_servers(targets, limit, timeout))

        self.status_var.set(
            f"Status: Zakończono! Znaleziono {len(self.all_servers)} serwerów MC."
        )
        self.reset_ui()

    def parse_json_file(self, filepath):
        targets = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    ip = item.get("ip")
                    for p in item.get("ports", []):
                        targets.append((ip, p.get("port", 25565)))
        except Exception as e:
            print(f"Błąd odczytu pliku JSON: {e}")
        return targets

    async def scan_minecraft_servers(self, targets, limit, timeout):
        semaphore = asyncio.Semaphore(limit)
        tasks = [
            self.check_server(ip, port, semaphore, timeout) for ip, port in targets
        ]
        await asyncio.gather(*tasks)

    async def check_server(self, ip, port, semaphore, timeout):
        async with semaphore:
            try:
                server = await asyncio.wait_for(
                    JavaServer.async_lookup(f"{ip}:{port}"), timeout=timeout
                )
                status = await asyncio.wait_for(
                    server.async_status(), timeout=timeout
                )

                motd = status.description
                if isinstance(motd, dict):
                    motd = motd.get("text", str(motd))

                res = {
                    "ip": ip,
                    "port": port,
                    "version": status.version.name,
                    "players_online": status.players.online,
                    "players_max": status.players.max,
                    "players_str": f"{status.players.online}/{status.players.max}",
                    "ping": round(status.latency),
                    "ping_str": f"{round(status.latency)} ms",
                    "motd": str(motd).strip().replace("\n", " "),
                }

                self.root.after(0, self.add_server_result, res)
            except Exception:
                pass

    def add_server_result(self, res):
        self.all_servers.append(res)
        self.filter_table()

    def clear_results(self):
        self.all_servers.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)

    def filter_table(self, *args):
        search_query = self.search_var.get().lower().strip()
        only_players = self.only_players_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for s in self.all_servers:
            if only_players and s["players_online"] == 0:
                continue

            match_text = (
                search_query in s["ip"].lower()
                or search_query in s["version"].lower()
                or search_query in s["motd"].lower()
            )

            if not search_query or match_text:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        s["ip"],
                        s["port"],
                        s["version"],
                        s["players_str"],
                        s["ping_str"],
                        s["motd"],
                    ),
                )

    def copy_selected_ip(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            ip = item["values"][0]
            port = item["values"][1]
            full_addr = f"{ip}:{port}" if port != 25565 else str(ip)

            self.root.clipboard_clear()
            self.root.clipboard_append(full_addr)
            self.status_var.set(f"Skopiowano do schowka: {full_addr}")

    def reset_ui(self):
        self.is_scanning = False
        self.btn_start.config(state="normal")

    def sort_col(self, col):
        if col == "ping":
            self.all_servers.sort(key=lambda x: x["ping"])
        elif col == "players":
            self.all_servers.sort(key=lambda x: x["players_online"], reverse=True)
        elif col == "ip":
            self.all_servers.sort(key=lambda x: x["ip"])
        self.filter_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = MCScannerApp(root)
    root.mainloop()