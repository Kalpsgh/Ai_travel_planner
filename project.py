from typing import TypedDict, Annotated, List
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from google.generativeai import configure, GenerativeModel

# Configure Gemini API (Replace with your own API key securely)
configure(api_key="AIzaSyDLxG3KmUq1QLcWN327LOWlZeOkPbrJ3YA")  
gemini_model = GenerativeModel("gemini-2.0-flash")

class PlannerState(TypedDict):
    messages: Annotated[List[str], "the messages in the conversation"]
    city: str
    interests: List[str]
    days: int
    itinerary: str

# Generate itinerary using AI
def generate_itinerary(city: str, interests: List[str], days: int) -> str:
    interest_str = ", ".join(interests) if interests else "general sightseeing"

    prompt = f"""
    Create a unique {days}-day travel itinerary for {city} based on these interests: {interest_str}.
    Each day's plan should include:
    - Morning: Activities like sightseeing, nature walks, or cultural visits.
    - Afternoon: Adventure activities, historical tours, or food experiences.
    - Evening: Entertainment, nightlife, or relaxation options.

    Ensure variety across days. Format it in an easy-to-read structure.
    """

    try:
        response = gemini_model.generate_content(prompt)
        return response.text if response else "⚠️ Could not generate itinerary. Please try again."
    except Exception as e:
        return f"⚠️ Error generating itinerary: {str(e)}"

# UI Setup
def create_ui():
    def get_itinerary():
        city = city_entry.get().strip()
        interests = interests_entry.get().strip().split(", ") if interests_entry.get().strip() else []
        
        try:
            days = int(days_entry.get().strip())
            if not city or days <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid city and number of days.")
            return

        generate_btn.config(state=tk.DISABLED)
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "⏳ Generating itinerary, please wait...\n", "loading")
        result_text.config(state=tk.DISABLED)

        def fetch_data():
            itinerary = generate_itinerary(city, interests, days)
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)

            # Add formatted title
            add_colored_text(result_text, f"🌍 {days}-Day Travel Plan for {city} 🌍\n", "title")
            result_text.insert(tk.END, "\n")

            # Formatting AI response
            for line in itinerary.split("\n"):
                if "📅 Day" in line:
                    add_colored_text(result_text, f"\n{line}\n", "day_title")
                elif "🌅 Morning:" in line:
                    add_colored_text(result_text, "🌅 Morning: ", "morning")
                    result_text.insert(tk.END, line.replace("🌅 Morning:", "").strip() + "\n")
                elif "🌞 Afternoon:" in line:
                    add_colored_text(result_text, "🌞 Afternoon: ", "afternoon")
                    result_text.insert(tk.END, line.replace("🌞 Afternoon:", "").strip() + "\n")
                elif "🌙 Evening:" in line:
                    add_colored_text(result_text, "🌙 Evening: ", "evening")
                    result_text.insert(tk.END, line.replace("🌙 Evening:", "").strip() + "\n")
                else:
                    result_text.insert(tk.END, line + "\n")

            result_text.config(state=tk.DISABLED)
            generate_btn.config(state=tk.NORMAL)

        # Run API call in a separate thread to avoid freezing the UI
        threading.Thread(target=fetch_data, daemon=True).start()

    def add_colored_text(widget, text, tag):
        widget.insert(tk.END, text, tag)

    root = tk.Tk()
    root.title("🌍 AI Travel Planner")
    root.geometry("800x600")
    root.configure(bg="#f0f8ff")

    # Layout Configuration
    root.columnconfigure(1, weight=1)

    # Title Label
    tk.Label(root, text="AI Travel Planner", font=("Arial", 18, "bold"), bg="#0047AB", fg="white", pady=10).grid(row=0, column=0, columnspan=2, sticky="ew")

    # Labels and Inputs
    tk.Label(root, text="Enter City:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    city_entry = tk.Entry(root, font=("Arial", 12), width=30)
    city_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Enter Number of Days:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    days_entry = tk.Entry(root, font=("Arial", 12), width=30)
    days_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Enter Interests (comma separated):", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    interests_entry = tk.Entry(root, font=("Arial", 12), width=30)
    interests_entry.grid(row=3, column=1, padx=10, pady=5)

    # Generate Button
    generate_btn = tk.Button(root, text="✨ Generate AI Itinerary ✨", font=("Arial", 12, "bold"), bg="#ff4500", fg="white", command=get_itinerary)
    generate_btn.grid(row=4, column=0, columnspan=2, pady=10)

    # Scrollable Output Box
    result_text = scrolledtext.ScrolledText(root, font=("Arial", 12), height=18, width=70, state=tk.DISABLED, wrap=tk.WORD, bg="#fffafa", fg="#333")
    result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Text Formatting
    result_text.tag_configure("title", font=("Arial", 16, "bold"), foreground="#0047AB")
    result_text.tag_configure("day_title", font=("Arial", 14, "bold"), foreground="#228B22")
    result_text.tag_configure("morning", font=("Arial", 12, "bold"), foreground="#ff4500")
    result_text.tag_configure("afternoon", font=("Arial", 12, "bold"), foreground="#D2691E")
    result_text.tag_configure("evening", font=("Arial", 12, "bold"), foreground="#800080")
    result_text.tag_configure("loading", font=("Arial", 12, "italic"), foreground="#777")

    root.mainloop()

# Run the UI
create_ui()
