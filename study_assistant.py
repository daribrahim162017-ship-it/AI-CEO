import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
import json
import base64
import urllib.request
import urllib.error
import threading
import uuid
import os
from datetime import datetime


# ============================================================
# AI CEO
# FAST IMAGE + GEOMETRY AI
# ============================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS = "http://127.0.0.1:11434/api/tags"

CHAT_FILE = Path("ibrahim_chats.json")

# 3B is used for image reading because it is considerably lighter.
# Change to qwen2.5vl:7b later when everything is working.
VISION_MODEL = "qwen2.5vl:3b"

# Strong text model for explanations.
TEXT_MODEL = "qwen2.5:7b"


# ============================================================
# CORE INSTRUCTIONS
# ============================================================

IMAGE_PROMPT = r"""
You are AI CEO's geometry image reader.

Inspect the ENTIRE uploaded image.

Your job is to extract the mathematics from the image accurately.

Return ONLY structured information in this format:

QUESTION:
[exact question or requested part]

MEASUREMENTS:
[list every visible measurement]

ANGLES:
[list every visible angle]

SHAPES:
[list shapes]

RELATIONSHIPS:
[list useful geometry relationships]

INSTRUCTIONS:
[list rounding/unit instructions]

UNCLEAR:
[list anything genuinely unreadable]

IMPORTANT:
- Do not invent numbers.
- Do not guess unreadable labels.
- Do not solve the problem yet.
- Read the whole image.
- If the user asks for 9(b), identify 9(b).
"""


SOLVER_PROMPT = r"""
You are Ibrahim, an expert mathematics and geometry tutor.

Use the extracted information below to solve the COMPLETE requested problem.

Do not invent information.

Use correct geometry rules.

Important rules include:

Triangle angles = 180°
Angles on a straight line = 180°
Angles around a point = 360°
Quadrilateral angles = 360°
Vertically opposite angles are equal.
Corresponding angles are equal for parallel lines.
Alternate angles are equal for parallel lines.
Co-interior angles add to 180°.
Pythagoras: a² + b² = c²
Circle area = πr²
Circle circumference = 2πr
Semicircle area = 1/2 πr²
Semicircle arc = πr
Rectangle area = length × width
Triangle area = 1/2 × base × perpendicular height

Solve every requested part.

Show:
1. Given information
2. Formula/rule
3. Substitution
4. Calculation
5. Final answer

Use clear English.

Do not output raw LaTeX.

Trust your reasoning, check your work carefully.

Then put your trust in Allah and continue with confidence.
"""


CHECK_PROMPT = r"""
You are AI CEO's final mathematics checker.

Check the proposed solution against the extracted information.

Check:
- every number
- every angle
- every formula
- every calculation
- every unit
- every requested part
- rounding

If anything is wrong, correct it.

If anything is missing, complete it.

Return the COMPLETE corrected solution in clear English.

Do not discuss the checking process.
"""


# ============================================================
# OLLAMA HELPERS
# ============================================================

def get_models():

    try:

        req = urllib.request.Request(
            OLLAMA_TAGS,
            method="GET"
        )

        with urllib.request.urlopen(
            req,
            timeout=10
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        return [
            item["name"]
            for item in data.get("models", [])
            if item.get("name")
        ]

    except Exception:

        return []


def call_ollama(
    model,
    messages,
    timeout=900
):

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "temperature": 0,
            "num_ctx": 8192,
            "num_predict": 3000
        }
    }

    body = json.dumps(
        payload
    ).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=body,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=timeout
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return (
            result
            .get("message", {})
            .get("content", "")
            .strip()
        )

    except urllib.error.HTTPError as error:

        try:
            details = error.read().decode("utf-8")
        except Exception:
            details = str(error)

        return (
            f"OLLAMA ERROR {error.code}\n\n"
            + details
        )

    except Exception as error:

        return (
            "OLLAMA TIMEOUT/CONNECTION ERROR\n\n"
            + str(error)
        )


def encode_image(path):

    with open(
        path,
        "rb"
    ) as file:

        return base64.b64encode(
            file.read()
        ).decode("utf-8")


# ============================================================
# CHAT STORAGE
# ============================================================

def load_chats():

    if not CHAT_FILE.exists():
        return []

    try:

        with open(
            CHAT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

    except Exception:
        pass

    return []


def save_chats(chats):

    try:

        with open(
            CHAT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                chats,
                file,
                indent=2,
                ensure_ascii=False
            )

    except Exception:
        pass


# ============================================================
# APP
# ============================================================

class IbrahimApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "🤖 AI CEO"
        )

        self.root.geometry(
            "1350x850"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.configure(
            bg="#090909"
        )

        self.chats = load_chats()

        self.current_chat_id = None
        self.current_image = None
        self.busy = False

        self.build_ui()

        if self.chats:

            self.current_chat_id = self.chats[0]["id"]

            self.refresh_chat_list()

            self.open_chat_by_id(
                self.current_chat_id
            )

        else:

            self.create_new_chat()


    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        # ---------------- SIDEBAR ----------------

        sidebar = tk.Frame(
            self.root,
            bg="#101010",
            width=280
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(
            False
        )

        tk.Label(
            sidebar,
            text="🤖 AI CEO",
            bg="#101010",
            fg="#00ff88",
            font=("Helvetica", 24, "bold")
        ).pack(
            pady=(25, 20)
        )

        tk.Button(
            sidebar,
            text="＋ NEW CHAT",
            command=self.create_new_chat,
            bg="#eeeeee",
            fg="#111111",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            pady=11
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 20)
        )

        tk.Label(
            sidebar,
            text="CHAT HISTORY",
            bg="#101010",
            fg="#777777",
            font=("Helvetica", 10, "bold")
        ).pack(
            anchor="w",
            padx=18
        )

        history_frame = tk.Frame(
            sidebar,
            bg="#101010"
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=8
        )

        self.chat_list = tk.Listbox(
            history_frame,
            bg="#171717",
            fg="#dddddd",
            selectbackground="#00aa66",
            selectforeground="white",
            font=("Helvetica", 11),
            relief="flat",
            highlightthickness=0
        )

        self.chat_list.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll = tk.Scrollbar(
            history_frame,
            command=self.chat_list.yview
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        self.chat_list.configure(
            yscrollcommand=scroll.set
        )

        self.chat_list.bind(
            "<<ListboxSelect>>",
            self.open_selected_chat
        )

        actions = tk.Frame(
            sidebar,
            bg="#101010"
        )

        actions.pack(
            fill="x",
            padx=14,
            pady=15
        )

        tk.Button(
            actions,
            text="✏ Rename",
            command=self.rename_chat,
            bg="#eeeeee",
            fg="#111111",
            relief="flat",
            pady=9
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 4)
        )

        tk.Button(
            actions,
            text="🗑 Delete",
            command=self.delete_chat,
            bg="#eeeeee",
            fg="#111111",
            relief="flat",
            pady=9
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 0)
        )

        # ---------------- MAIN ----------------

        main = tk.Frame(
            self.root,
            bg="#090909"
        )

        main.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.title_label = tk.Label(
            main,
            text="🤖 AI CEO",
            bg="#090909",
            fg="#00ff88",
            font=("Helvetica", 25, "bold")
        )

        self.title_label.pack(
            pady=(20, 3)
        )

        tk.Label(
            main,
            text="Fast local AI • Maths • Geometry • Study • Image solving",
            bg="#090909",
            fg="#999999",
            font=("Helvetica", 11)
        ).pack(
            pady=(0, 10)
        )

        # ---------------- ANSWER ----------------

        answer_frame = tk.Frame(
            main,
            bg="#111111",
            highlightbackground="#444444",
            highlightthickness=1
        )

        answer_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=8
        )

        self.answer_box = tk.Text(
            answer_frame,
            bg="#111111",
            fg="#eeeeee",
            insertbackground="white",
            font=("Helvetica", 14),
            wrap="word",
            relief="flat",
            padx=18,
            pady=18
        )

        self.answer_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        answer_scroll = tk.Scrollbar(
            answer_frame,
            command=self.answer_box.yview
        )

        answer_scroll.pack(
            side="right",
            fill="y"
        )

        self.answer_box.configure(
            yscrollcommand=answer_scroll.set
        )

        # ---------------- IMAGE ----------------

        self.image_status = tk.Label(
            main,
            text="📷 No image selected",
            bg="#181818",
            fg="#888888",
            pady=7
        )

        self.image_status.pack(
            fill="x",
            padx=18
        )

        buttons = tk.Frame(
            main,
            bg="#090909"
        )

        buttons.pack(
            fill="x",
            padx=18,
            pady=8
        )

        self.upload_btn = tk.Button(
            buttons,
            text="📷 UPLOAD IMAGE",
            command=self.upload_image,
            font=("Helvetica", 11, "bold"),
            bg="#eeeeee",
            fg="#111111",
            relief="flat",
            padx=15,
            pady=10
        )

        self.upload_btn.pack(
            side="left",
            padx=(0, 7)
        )

        self.solve_btn = tk.Button(
            buttons,
            text="🚀 SOLVE",
            command=self.solve,
            font=("Helvetica", 11, "bold"),
            bg="#eeeeee",
            fg="#111111",
            relief="flat",
            padx=20,
            pady=10
        )

        self.solve_btn.pack(
            side="left",
            padx=7
        )

        tk.Button(
            buttons,
            text="❌ REMOVE IMAGE",
            command=self.remove_image,
            font=("Helvetica", 11, "bold"),
            bg="#eeeeee",
            fg="#111111",
            relief="flat",
            padx=15,
            pady=10
        ).pack(
            side="left",
            padx=7
        )

        # ---------------- INPUT ----------------

        input_frame = tk.Frame(
            main,
            bg="#090909"
        )

        input_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        self.question_box = tk.Text(
            input_frame,
            height=4,
            bg="#151515",
            fg="white",
            insertbackground="white",
            font=("Helvetica", 14),
            wrap="word",
            relief="flat",
            padx=12,
            pady=12
        )

        self.question_box.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Button(
            input_frame,
            text="🚀 SEND",
            command=self.solve,
            font=("Helvetica", 12, "bold"),
            bg="#eeeeee",
            fg="#111111",
            relief="flat",
            padx=22,
            pady=12
        ).pack(
            side="right",
            fill="y"
        )

        # ---------------- STATUS ----------------

        self.status = tk.Label(
            main,
            text="Ready",
            bg="#090909",
            fg="#00cc77",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )


    # ========================================================
    # CHAT
    # ========================================================

    def create_new_chat(
        self,
        show=True
    ):

        chat = {
            "id": str(uuid.uuid4()),
            "title": "New Chat",
            "messages": []
        }

        self.chats.insert(
            0,
            chat
        )

        self.current_chat_id = chat["id"]

        save_chats(
            self.chats
        )

        self.refresh_chat_list()

        self.clear_screen()

        if show:

            self.answer_box.insert(
                "1.0",
                "🤖 AI CEO IS READY\n\n"
                "Upload a geometry image or type a question."
            )

    def current_chat(self):

        for chat in self.chats:

            if chat["id"] == self.current_chat_id:

                return chat

        return None

    def refresh_chat_list(self):

        self.chat_list.delete(
            0,
            "end"
        )

        for chat in self.chats:

            self.chat_list.insert(
                "end",
                "💬 " + chat.get(
                    "title",
                    "New Chat"
                )
            )

    def open_selected_chat(
        self,
        event=None
    ):

        selection = self.chat_list.curselection()

        if not selection:
            return

        if selection[0] >= len(self.chats):
            return

        chat = self.chats[
            selection[0]
        ]

        self.open_chat_by_id(
            chat["id"]
        )

    def open_chat_by_id(
        self,
        chat_id
    ):

        self.current_chat_id = chat_id

        chat = self.current_chat()

        if not chat:
            return

        self.title_label.configure(
            text="🤖 " + chat.get(
                "title",
                "New Chat"
            )
        )

        self.answer_box.delete(
            "1.0",
            "end"
        )

        for message in chat.get(
            "messages",
            []
        ):

            if message["role"] == "user":

                self.answer_box.insert(
                    "end",
                    "\n👤 YOU\n"
                    + message["content"]
                    + "\n\n"
                )

            else:

                self.answer_box.insert(
                    "end",
                    "🤖 AI CEO\n"
                    + message["content"]
                    + "\n\n"
                )

        self.answer_box.see(
            "end"
        )

    def rename_chat(self):

        chat = self.current_chat()

        if not chat:
            return

        name = simpledialog.askstring(
            "Rename Chat",
            "Chat name:",
            initialvalue=chat.get(
                "title",
                "New Chat"
            )
        )

        if not name:
            return

        chat["title"] = name.strip()

        save_chats(
            self.chats
        )

        self.refresh_chat_list()

        self.title_label.configure(
            text="🤖 " + chat["title"]
        )

    def delete_chat(self):

        chat = self.current_chat()

        if not chat:
            return

        confirm = messagebox.askyesno(
            "Delete Chat",
            "Delete this chat?"
        )

        if not confirm:
            return

        self.chats = [
            c for c in self.chats
            if c["id"] != self.current_chat_id
        ]

        save_chats(
            self.chats
        )

        if self.chats:

            self.current_chat_id = self.chats[0]["id"]

            self.refresh_chat_list()

            self.open_chat_by_id(
                self.current_chat_id
            )

        else:

            self.create_new_chat()


    # ========================================================
    # IMAGE
    # ========================================================

    def upload_image(self):

        path = filedialog.askopenfilename(
            title="Choose Geometry Image",
            filetypes=[
                (
                    "Images",
                    "*.png *.jpg *.jpeg *.webp *.bmp"
                )
            ]
        )

        if not path:
            return

        self.current_image = path

        self.image_status.configure(
            text="📷 " + Path(path).name,
            fg="#00ff88"
        )

        self.status.configure(
            text="Image ready."
        )

    def remove_image(self):

        self.current_image = None

        self.image_status.configure(
            text="📷 No image selected",
            fg="#888888"
        )


    # ========================================================
    # SOLVE
    # ========================================================

    def solve(self):

        if self.busy:
            return

        question = self.question_box.get(
            "1.0",
            "end"
        ).strip()

        if not question and not self.current_image:

            messagebox.showinfo(
                "Ibrahim",
                "Type a question or upload an image."
            )

            return

        self.busy = True

        self.solve_btn.configure(
            state="disabled"
        )

        self.upload_btn.configure(
            state="disabled"
        )

        self.status.configure(
            text="🤖 AI CEO is working..."
        )

        self.answer_box.delete(
            "1.0",
            "end"
        )

        self.answer_box.insert(
            "1.0",
            "🤖 Reading and solving...\n\n"
            "Please wait."
        )

        thread = threading.Thread(
            target=self.solve_worker,
            args=(
                question,
                self.current_image
            ),
            daemon=True
        )

        thread.start()


    # ========================================================
    # SOLVER
    # ========================================================

    def solve_worker(
        self,
        question,
        image_path
    ):

        try:

            models = get_models()

            if not models:

                self.finish(
                    "❌ Ollama is not running or no model is installed."
                )

                return

            # =================================================
            # IMAGE MODE
            # =================================================

            if image_path:

                vision_model = None

                for name in models:

                    if name.lower() == VISION_MODEL.lower():

                        vision_model = name
                        break

                if not vision_model:

                    vision_model = next(
                        (
                            name
                            for name in models
                            if (
                                "vl" in name.lower()
                                or "vision" in name.lower()
                                or "llava" in name.lower()
                            )
                        ),
                        None
                    )

                if not vision_model:

                    self.finish(
                        "❌ No vision model was found.\n\n"
                        "Install qwen2.5vl:3b or another "
                        "Ollama vision model."
                    )

                    return

                encoded = encode_image(
                    image_path
                )

                # -------------------------------------------
                # PASS 1: READ IMAGE
                # -------------------------------------------

                extraction = call_ollama(
                    vision_model,
                    [
                        {
                            "role": "system",
                            "content": IMAGE_PROMPT
                        },
                        {
                            "role": "user",
                            "content": (
                                question
                                if question
                                else
                                "Read this geometry question completely."
                            ),
                            "images": [
                                encoded
                            ]
                        }
                    ],
                    timeout=900
                )

                if (
                    extraction.startswith(
                        "OLLAMA ERROR"
                    )
                    or
                    extraction.startswith(
                        "OLLAMA TIMEOUT"
                    )
                ):

                    self.finish(
                        extraction
                    )

                    return

                # -------------------------------------------
                # PASS 2: SOLVE FROM EXTRACTED DATA
                # -------------------------------------------

                solver_models = [
                    x for x in models
                    if x.lower() == TEXT_MODEL.lower()
                ]

                if solver_models:

                    solver_model = solver_models[0]

                else:

                    solver_model = models[0]

                solution = call_ollama(
                    solver_model,
                    [
                        {
                            "role": "system",
                            "content": SOLVER_PROMPT
                        },
                        {
                            "role": "user",
                            "content": (
                                "User request:\n"
                                + (
                                    question
                                    if question
                                    else
                                    "Solve the requested question."
                                )
                                + "\n\n"
                                "EXTRACTED IMAGE INFORMATION:\n\n"
                                + extraction
                            )
                        }
                    ],
                    timeout=600
                )

                # -------------------------------------------
                # PASS 3: CHECK SOLUTION USING TEXT
                # -------------------------------------------

                checked = call_ollama(
                    solver_model,
                    [
                        {
                            "role": "system",
                            "content": CHECK_PROMPT
                        },
                        {
                            "role": "user",
                            "content": (
                                "EXTRACTED INFORMATION:\n"
                                + extraction
                                + "\n\n"
                                "PROPOSED SOLUTION:\n"
                                + solution
                            )
                        }
                    ],
                    timeout=600
                )

                final_answer = (
                    checked
                    if checked
                    and not checked.startswith(
                        "OLLAMA"
                    )
                    else solution
                )

            # =================================================
            # TEXT MODE
            # =================================================

            else:

                model = TEXT_MODEL

                if model not in models:

                    model = models[0]

                final_answer = call_ollama(
                    model,
                    [
                        {
                            "role": "system",
                            "content": SOLVER_PROMPT
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    timeout=600
                )

            # =================================================
            # SAVE
            # =================================================

            chat = self.current_chat()

            if chat:

                chat["messages"].append(
                    {
                        "role": "user",
                        "content": (
                            "📷 Image question\n"
                            if image_path
                            else question
                        )
                    }
                )

                chat["messages"].append(
                    {
                        "role": "assistant",
                        "content": final_answer
                    }
                )

                if chat["title"] == "New Chat":

                    title = (
                        question
                        if question
                        else
                        Path(image_path).name
                    )

                    chat["title"] = title[:40]

                save_chats(
                    self.chats
                )

            self.finish(
                final_answer
            )

        except Exception as error:

            self.finish(
                "❌ ERROR\n\n"
                + str(error)
            )


    # ========================================================
    # FINISH
    # ========================================================

    def finish(
        self,
        answer
    ):

        self.root.after(
            0,
            lambda: self.finish_ui(
                answer
            )
        )

    def finish_ui(
        self,
        answer
    ):

        self.answer_box.delete(
            "1.0",
            "end"
        )

        self.answer_box.insert(
            "1.0",
            answer
        )

        self.answer_box.see(
            "1.0"
        )

        self.refresh_chat_list()

        self.busy = False

        self.solve_btn.configure(
            state="normal"
        )

        self.upload_btn.configure(
            state="normal"
        )

        self.status.configure(
            text="✅ Complete solution ready."
        )

    def clear_screen(self):

        self.current_image = None

        self.image_status.configure(
            text="📷 No image selected",
            fg="#888888"
        )

        self.answer_box.delete(
            "1.0",
            "end"
        )

        self.question_box.delete(
            "1.0",
            "end"
        )

        self.title_label.configure(
            text="🤖 New Chat"
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = IbrahimApp(
        root
    )

    root.mainloop()