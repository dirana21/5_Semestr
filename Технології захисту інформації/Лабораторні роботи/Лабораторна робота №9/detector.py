"""Пошук потенційно підозрілих процесів за їхніми метаданими."""

import argparse
from collections.abc import Iterator
from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
import sys
from time import perf_counter, sleep

import psutil


DEMO_MARKER = "--lab-keylogger-demo"
PATTERNS = {
    word: re.compile(rf"(?<![a-z0-9]){word}(?![a-z0-9])")
    for word in ("keylogger", "pynput", "keyboard", "hook")
}


@dataclass(frozen=True)
class Finding:
    pid: int
    name: str
    matches: tuple[str, ...]
    demo: bool


def inspect_process(info: dict) -> Finding | None:
    name = info.get("name") or ""
    arguments = info.get("cmdline") or []
    data = " ".join((name, *arguments)).casefold()
    matches = tuple(word for word, pattern in PATTERNS.items() if pattern.search(data))
    demo = DEMO_MARKER in arguments
    if matches:
        return Finding(info["pid"], name or "(невідома назва)", matches, demo)
    return None


def iter_findings() -> Iterator[Finding]:
    for process in psutil.process_iter(["pid", "name", "cmdline"], ad_value=None):
        try:
            if process.pid == os.getpid():
                continue
            finding = inspect_process(process.info)
            if finding is not None:
                yield finding
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def scan() -> list[Finding]:
    return list(iter_findings())


def measure_demo() -> tuple[Finding, float]:
    script = Path(__file__).with_name("demo_process.py")
    started = perf_counter()
    child = subprocess.Popen([sys.executable, str(script), DEMO_MARKER])
    try:
        deadline = started + 5.0
        while perf_counter() < deadline:
            if child.poll() is not None:
                break
            for finding in iter_findings():
                if perf_counter() >= deadline:
                    break
                if finding.pid == child.pid and finding.demo:
                    return finding, (perf_counter() - started) * 1000
            sleep(0.05)
        raise RuntimeError("Демонстраційний процес не виявлено протягом 5 секунд.")
    finally:
        if child.poll() is None:
            child.terminate()
        child.wait(timeout=5)


def describe(finding: Finding) -> str:
    label = "навчальний процес" if finding.demo else "потребує перевірки"
    return f"{finding.pid:<8} {finding.name:<24} {', '.join(finding.matches)} [{label}]"


def open_gui() -> None:
    import tkinter as tk
    from tkinter import ttk
    from queue import Empty, Queue
    from threading import Thread

    window = tk.Tk()
    window.title("ЛР №9 — Аналіз процесів")
    window.geometry("750x440")
    window.minsize(620, 340)
    frame = ttk.Frame(window, padding=18)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Пошук ознак кейлогерів", font=("Segoe UI", 16, "bold")).pack(anchor="w")
    ttk.Label(frame, text="Збіг за метаданими — привід перевірити процес.").pack(anchor="w", pady=(5, 12))
    controls = ttk.Frame(frame)
    controls.pack(fill="x")
    status = tk.StringVar(value="Оберіть сканування або навчальний тест.")
    ttk.Label(frame, textvariable=status).pack(anchor="w", pady=10)
    output = tk.Text(frame, wrap="word", height=12, state="disabled", font=("Consolas", 10))
    output.pack(fill="both", expand=True)
    messages = Queue()

    def start(action):
        for button in buttons:
            button.state(["disabled"])
        status.set("Виконується перевірка…")

        def work():
            try:
                if action == "demo":
                    finding, ms = measure_demo()
                    messages.put((f"Навчальний процес виявлено за {ms:.2f} мс.", [finding]))
                else:
                    findings = scan()
                    messages.put((f"Знайдено збігів: {len(findings)}.", findings))
            except (OSError, psutil.Error, RuntimeError, subprocess.SubprocessError) as error:
                messages.put((f"Помилка: {error}", []))

        Thread(target=work, daemon=True).start()
        window.after(50, display)

    def display():
        try:
            message, findings = messages.get_nowait()
        except Empty:
            window.after(50, display)
            return
        status.set(message)
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("end", "\n".join(map(describe, findings)))
        output.configure(state="disabled")
        for button in buttons:
            button.state(["!disabled"])

    buttons = (
        ttk.Button(controls, text="Перевірити процеси", command=lambda: start("scan")),
        ttk.Button(controls, text="Навчальний тест із заміром", command=lambda: start("demo")),
    )
    for button in buttons:
        button.pack(side="left", padx=(0, 8))
    window.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="ЛР №9. Аналіз метаданих процесів")
    parser.add_argument("mode", choices=("gui", "scan", "demo"), nargs="?", default="gui")
    mode = parser.parse_args().mode
    if mode == "gui":
        open_gui()
    elif mode == "demo":
        try:
            finding, ms = measure_demo()
        except (OSError, psutil.Error, RuntimeError, subprocess.SubprocessError) as error:
            parser.exit(1, f"Помилка експерименту: {error}\n")
        print(describe(finding))
        print(f"Час від початку запуску до виявлення: {ms:.2f} мс")
    else:
        findings = scan()
        for finding in findings:
            print(describe(finding))
        print(f"Збігів за метаданими: {len(findings)}")


if __name__ == "__main__":
    main()
