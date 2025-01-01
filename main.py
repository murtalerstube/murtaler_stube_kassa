import tkinter as tk
from tkinter import messagebox


class Kassensystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Murtaler Stube Kassensystem")
        self.root.geometry("1000x800")  # Größeres Fenster für mobile Geräte

        # Tabelle der Tische mit Bestellungen und Kundenkarten
        self.tische = {
            f"Tisch {i}": {
                "bestellungen": [],
                "kundenkarte": None,
                "punkte": 0,
                "kellner_id": None
            }
            for i in range(1, 11)
        }

        # Essenskategorien und Produkte mit Preisen
        self.kategorien = {
            "Getränke": [("Cola", 2.50), ("Fanta", 2.50), ("Apfelsaft", 2.50),
                         ("Orangensaft", 2.50), ("Wasser", 2.50),
                         ("Bier", 3.00), ("Radler", 3.00), ("Rotwein", 6.00),
                         ("Sekt", 12.00), ("Jägermeister", 1.50),
                         ("RedBull", 5.00), ("Weißwein", 18.00),
                         ("Eistee", 4.00), ("Espresso", 2.70),
                         ("Verlängerten", 3.40), ("Kaffee Latte", 4.00),
                         ("Cappuccino", 4.50), ("Kakao", 3.50)],
            "Snacks": [("Schnitzelsemmel", 5.00), ("Toast", 2.60),
                       ("Frankfurter/Käsekrainer mit Gebäck", 3.50),
                       ("Gebackene Mäuse", 4.20)],
            "Desserts": [("Tiramisu", 5.00),
                         ("Apfelstrudel/Topfenstrudel", 7.50),
                         ("Schokoküchlein", 5.50), ("Sachertorte", 3.00),
                         ("Eispalatschinken", 4.20)]
        }

        # UI für Tische
        self.create_table_buttons()

        # Kellner Dropdown und Kassa schließen Button
        self.create_kellner_dropdown()
        self.create_kassa_close_button()

        # Anzeige für den Tisch
        self.table_window = None
        self.table_total_label = None
        self.table_payment_entry = None
        self.table_kundenkarte_label = None

    def create_kellner_dropdown(self):
        # Dropdown für Kellner-IDs
        self.kellner_ids = {"001": "Florian", "002": "Emily"}
        self.kellner_var = tk.StringVar()
        self.kellner_var.set("Kellner auswählen")

        kellner_dropdown = tk.OptionMenu(self.root, self.kellner_var,
                                         *self.kellner_ids.values())
        kellner_dropdown.pack(pady=10)

    def create_kassa_close_button(self):
        # Kassa schließen Button
        close_button = tk.Button(self.root,
                                 text="Kassa schließen",
                                 command=self.close_kassa,
                                 font=("Arial", 12),
                                 bg="lightyellow")
        close_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_table_buttons(self):
        frame = tk.Frame(self.root, bg="lightgrey")
        frame.pack(pady=10)

        # Erste Reihe für Tische (Tisch 1 bis Tisch 5)
        first_row = tk.Frame(self.root, bg="lightgrey")
        first_row.pack(pady=5)

        # Zweite Reihe für Tische (Tisch 6 bis Tisch 10)
        second_row = tk.Frame(self.root, bg="lightgrey")
        second_row.pack(pady=5)

        # Erstelle Buttons für 10 Tische, 5 Tische in jeder Reihe
        for i, tisch in enumerate(self.tische, start=1):
            btn = tk.Button(first_row if i <= 5 else second_row,
                            text=f"Tisch {i}",
                            width=12,
                            height=3,
                            command=lambda t=f"Tisch {i}": self.open_table(t),
                            bg="skyblue",
                            font=("Arial", 12, "bold"))
            btn.pack(side=tk.LEFT, padx=10, pady=10)

    def open_table(self, tisch_name):
        # Wenn schon ein Fenster für den Tisch geöffnet ist, schließen
        if self.table_window:
            self.table_window.destroy()

        # Neues Fenster für den Tisch
        self.table_window = tk.Toplevel(self.root)
        self.table_window.title(f"{tisch_name} Bestellungen")

        # Anzeige für die Bestellungen
        tk.Label(self.table_window,
                 text=f"Bestellungen für {tisch_name}",
                 font=("Arial", 14, "bold"),
                 bg="lightblue").grid(row=0, column=0, columnspan=2, pady=10)

        # Tabs für Kategorien
        categories_frame = tk.Frame(self.table_window, bg="lightgray")
        categories_frame.grid(row=1, column=0, pady=10)

        for index, category in enumerate(self.kategorien):
            category_button = tk.Button(categories_frame,
                                        text=category,
                                        width=15,
                                        command=lambda c=category: self.
                                        show_category_items(c, tisch_name),
                                        bg="lightgreen",
                                        font=("Arial", 12))
            category_button.grid(row=0, column=index, padx=10)

        # Gesamtbetrag und Kundenkarte für den Tisch
        self.table_total_label = tk.Label(self.table_window,
                                          text="Gesamt: € 0.00",
                                          font=("Arial", 14),
                                          bg="lightgray")
        self.table_total_label.grid(row=2, column=0, pady=10)

        self.table_kundenkarte_label = tk.Label(
            self.table_window,
            text="Kundenkarte: Nicht vorhanden",
            font=("Arial", 12),
            bg="lightgray")
        self.table_kundenkarte_label.grid(row=3, column=0, pady=10)

        if not self.tische[tisch_name]["kundenkarte"]:
            tk.Button(self.table_window,
                      text="Kundenkarte hinzufügen",
                      command=lambda: self.add_kundenkarte(tisch_name),
                      font=("Arial", 12),
                      bg="lightcoral").grid(row=4, column=0, pady=10)

        # Bezahlbutton
        tk.Button(self.table_window,
                  text="Bezahlen & Neues Fenster",
                  command=lambda: self.pay_and_reset(tisch_name),
                  font=("Arial", 12),
                  bg="lightyellow").grid(row=5, column=0, pady=10)

        # Bestellungen laden (falls bereits Bestellungen vorhanden sind)
        self.update_order(tisch_name)

    def show_category_items(self, category, tisch_name):
        # Löschen der bestehenden Widgets (falls schon Bestellungen für eine andere Kategorie angezeigt werden)
        for widget in self.table_window.winfo_children():
            widget.grid_forget()

        # Bestellungen für die gewählte Kategorie anzeigen
        tk.Label(self.table_window,
                 text=f"Bestellungen für {category}",
                 font=("Arial", 12, "bold"),
                 bg="lightblue").grid(row=0, column=0, columnspan=2, pady=10)

        row = 1
        for item, price in self.kategorien[category]:
            item_button = tk.Button(
                self.table_window,
                text=f"{item} - € {price:.2f}",
                width=30,
                command=lambda item=item, price=price, t=tisch_name: self.
                add_item_to_order(item, price, t),
                bg="lightpink")
            item_button.grid(row=row, column=0, pady=5)
            row += 1

        # Gesamtbetrag für den Tisch
        self.table_total_label.grid(row=row, column=0, pady=10)

    def add_item_to_order(self, item, price, tisch_name):
        # Bestellung zum Tisch hinzufügen
        self.tische[tisch_name]["bestellungen"].append((item, price))

        # Punkte für Kundenkarte aktualisieren
        self.tische[tisch_name][
            "punkte"] += 1  # Beispiel: 1 Punkt pro Bestellung

        self.update_order(tisch_name)

    def update_order(self, tisch_name):
        # Berechnung des Gesamtbetrags für den Tisch
        total = sum(item[1]
                    for item in self.tische[tisch_name]["bestellungen"])
        self.table_total_label.config(text=f"Gesamt: € {total:.2f}")

        # Aktualisierung der Kundenkarte
        kundenkarte = self.tische[tisch_name]["kundenkarte"]
        if kundenkarte:
            self.table_kundenkarte_label.config(
                text=
                f"Kundenkarte: {kundenkarte} (Punkte: {self.tische[tisch_name]['punkte']})"
            )
        else:
            self.table_kundenkarte_label.config(
                text="Kundenkarte: Nicht vorhanden")

    def add_kundenkarte(self, tisch_name):
        # Eingabefeld für Kundenkarte
        def save_kundenkarte():
            kunden_id = kundenkarte_entry.get()
            if kunden_id:
                self.tische[tisch_name]["kundenkarte"] = kunden_id
                self.tische[tisch_name]["punkte"] = 0
                kundenkarte_entry.delete(0, tk.END)
                messagebox.showinfo("Erfolg",
                                    f"Kundenkarte {kunden_id} hinzugefügt!")
                new_window.destroy()
                self.update_order(tisch_name)
            else:
                messagebox.showerror(
                    "Fehler", "Bitte eine gültige Kundenkarte eingeben.")

        new_window = tk.Toplevel(self.root)
        new_window.title("Kundenkarte hinzufügen")

        tk.Label(new_window, text="Kundenkarte ID:",
                 font=("Arial", 12)).pack(pady=10)
        kundenkarte_entry = tk.Entry(new_window, font=("Arial", 12))
        kundenkarte_entry.pack(pady=5)

        tk.Button(new_window,
                  text="Speichern",
                  command=save_kundenkarte,
                  font=("Arial", 12),
                  bg="lightgreen").pack(pady=10)

    def pay_and_reset(self, tisch_name):
        # Berechnung und Anzeige für Bezahlung
        total = sum(item[1]
                    for item in self.tische[tisch_name]["bestellungen"])
        messagebox.showinfo(
            "Bezahlung", f"Der Betrag für {tisch_name} beträgt € {total:.2f}.")

        # Zurücksetzen der Bestellungen und Fenster für den nächsten Gast
        self.tische[tisch_name]["bestellungen"].clear()
        self.tische[tisch_name]["punkte"] = 0  # Punkte zurücksetzen
        self.update_order(tisch_name)

        # Schließen des Fensters
        self.table_window.destroy()

    def close_kassa(self):
        # Berechnung des Gesamtbetrags für alle Tische
        total_all = sum(
            sum(item[1] for item in tisch["bestellungen"])
            for tisch in self.tische.values())
        messagebox.showinfo("Kassa schließen",
                            f"Gesamtbetrag des Tages: € {total_all:.2f}")


# Hauptprogramm starten
root = tk.Tk()
app = Kassensystem(root)
root.mainloop()
