import tkinter.ttk as ttk
import tkinter as tk
import asyncio
import tk_tooltip
import core
import sys
from PIL import Image, ImageTk


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Boolean Generator")
        self.event_loop = asyncio.get_event_loop()
        self.bool_entry_dict = {}
        self.how_many_match = tk.StringVar(value="2")
        self.option_frame = ttk.Frame(self.root)
        self.option_frame.grid(row=0, column=0, pady=2)
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.grid(row=1, column=0, pady=5, padx=5)
        self.boolean_frame = ttk.Labelframe(self.input_frame, text="Boolean Search Terms")
        self.boolean_frame.pack()
        self.bool_output_strvar = tk.StringVar()
        self.bool_button_frame = ttk.Frame(self.input_frame)
        self.bool_button_frame.pack()
        self.bool_output_frame = ttk.Labelframe(self.input_frame, text="Boolean Output")
        self.bool_output_frame.pack()
        self.bool_output_entry = ttk.Entry(self.bool_output_frame, textvariable=self.bool_output_strvar,
                                           state="readonly", width=55)
        self.bool_output_entry.grid(row=0, column=0, sticky="WE", padx=3, pady=3)
        tk_tooltip.Tooltip(self.bool_output_entry, text="Output box for boolean search, "
                                                        "automatically sent to clipboard.")
        self.any_n_of_entry = ttk.Entry()
        self.any_n_of_entry.destroy()
        self.generate_bool_button = ttk.Button()
        self.root.resizable(0, 0)
        self.is_refreshing = False
        self.inputs_list = []
        delete_image = Image.open("./icons/win_delete_cross.ico").resize((16, 16), Image.ANTIALIAS)
        self.delete_cross_image = ImageTk.PhotoImage(delete_image)
        refresh_image = Image.open("./icons/refresh_symbol.ico").resize((16, 16), Image.ANTIALIAS)
        self.refresh_arrows_image = ImageTk.PhotoImage(refresh_image)
        add_new_image = Image.open("./icons/green_plus.ico").resize((16, 16), Image.ANTIALIAS)
        self.add_new_image = ImageTk.PhotoImage(add_new_image)
        green_arrow_right = Image.open("./icons/green_arrow_right.ico").resize((16, 16), Image.ANTIALIAS)
        self.green_arrow_right = ImageTk.PhotoImage(green_arrow_right)
        self.bool_output_entry.bind("<FocusIn>", func=self.__bool_output_highlight_all_callback)
        asyncio.run(self.gen_option_frame())
        asyncio.run(self.gen_input_frame())
        asyncio.run(self.main_loop())
        self.event_loop.run_forever()

    async def gen_option_frame(self):
        modes_info_1 = ttk.Label(self.option_frame, text="Any ")
        modes_info_2 = ttk.Label(self.option_frame, text=" must match. ")
        self.any_n_of_entry = ttk.Entry(self.option_frame, textvariable=self.how_many_match,
                                        width=2, exportselection=0)
        self.how_many_match.trace_add("write",
                                      lambda *args: asyncio.create_task(self.update_how_many_match(
                                          self.any_n_of_entry)))
        modes_info_1.grid(row=0, column=0)
        self.any_n_of_entry.grid(row=0, column=1)
        modes_info_2.grid(row=0, column=2)
        tk_tooltip.Tooltip(self.any_n_of_entry, text="How many booleans must match\n(More than 2, "
                                                     "less than or equal to number of inputs, integer type).")

    async def update_how_many_match(self, any_n_of_entry):
        try:
            if 2 <= int(self.how_many_match.get()) <= await self.num_bool_rows():
                any_n_of_entry.config(foreground="black")
                self.generate_bool_button.config(state=tk.NORMAL)
            else:
                any_n_of_entry.config(foreground="red")
                self.generate_bool_button.config(state=tk.DISABLED)
        except ValueError:
            any_n_of_entry.config(foreground="red")
            self.generate_bool_button.config(state=tk.DISABLED)
        except AttributeError:
            pass
        except NameError:
            pass

    async def gen_input_frame(self):
        await self.gen_new_input_row(no_delete=True, gen_refresh_button=True)
        await self.gen_new_input_row(no_delete=True, gen_add_row_button=True)
        self.generate_bool_button.destroy()
        self.generate_bool_button = ttk.Button(self.bool_button_frame, text="Generate Boolean",
                                               image=self.green_arrow_right, compound="left",
                                               command=lambda: asyncio.create_task(self.draw_bool_out()))
        self.generate_bool_button.grid(column=0, pady=2, sticky="W")
        tk_tooltip.Tooltip(self.generate_bool_button, text="Generate boolean search term based "
                                                           "on text entries. Deletes all empty rows.")

    async def gen_new_input_row(self, no_delete=False, gen_add_row_button=False, gen_refresh_button=False):
        row_bool_stringvar = tk.StringVar()
        # Schema for this [ttk.Frame, tk.StringVar]
        row_storage_struct = [ttk.Frame(self.boolean_frame), row_bool_stringvar]
        self.inputs_list.append(row_storage_struct)
        # print(await self.num_bool_rows())
        # i = 0
        # while self.boolean_frame.grid_slaves(row=i):
        #     i += 1
        row_storage_struct[0].grid(row=len(self.inputs_list), sticky="WE")
        boolean_entry = ttk.Entry(row_storage_struct[0], width=50, textvariable=row_storage_struct[1])
        if not no_delete:
            deletion_button = ttk.Button(row_storage_struct[0], image=self.delete_cross_image,
                                         command=lambda: asyncio.create_task(self.delete_bool_row(row_storage_struct)))
            deletion_button.image = self.delete_cross_image  # Used to avoid garbage collection
            deletion_button.grid(row=0, column=1, padx=3, pady=2)
            boolean_entry.grid(row=0, column=0, pady=3, padx=3)
            tk_tooltip.Tooltip(deletion_button, text="Delete row.")
        else:
            boolean_entry.grid(row=0, column=0, sticky="W", pady=3, padx=3)
        if gen_add_row_button:
            add_new_row_button = ttk.Button(row_storage_struct[0], image=self.add_new_image,
                                            command=lambda: asyncio.create_task(self.gen_new_input_row()))
            add_new_row_button.grid(row=0, column=1, padx=3, pady=2)
            tk_tooltip.Tooltip(add_new_row_button, text="Add new row at bottom.")
        if gen_refresh_button:
            refresh_window_button = ttk.Button(row_storage_struct[0], image=self.refresh_arrows_image,
                                               command=lambda: asyncio.create_task(self.refresh_entry_boxes()))
            refresh_window_button.grid(row=0, column=1, padx=3, pady=2)
            tk_tooltip.Tooltip(refresh_window_button, text="Regenerate boolean term entry area.")
        await self.update_how_many_match(self.any_n_of_entry)

    async def delete_bool_row(self, row_storage_struct):
        row_storage_struct[0].grid_remove()
        row_storage_struct[0].destroy()
        self.inputs_list[self.inputs_list.index(row_storage_struct)] = ["EMPTY", "EMPTY"]
        await self.update_how_many_match(self.any_n_of_entry)
        # print(await self.num_bool_rows())

    async def num_bool_rows(self):
        row_num = 0
        for row_obj in self.inputs_list:
            if row_obj[0] == "EMPTY":
                pass
            else:
                row_num += 1

        return row_num

    async def refresh_entry_boxes(self):
        self.is_refreshing = True
        self.input_frame.destroy()
        self.input_frame = ttk.Labelframe(self.root, text="Boolean Search Terms")
        self.input_frame.grid(row=1, column=0, pady=5, padx=5)
        self.boolean_frame = ttk.Frame(self.input_frame)
        self.boolean_frame.pack()
        self.bool_button_frame = ttk.Frame(self.input_frame)
        self.bool_button_frame.pack()
        self.bool_output_frame = ttk.Labelframe(self.input_frame, text="Boolean Output")
        self.bool_output_frame.pack()
        self.bool_output_entry = ttk.Entry(self.bool_output_frame, textvariable=self.bool_output_strvar,
                                           state="readonly", width=55)
        self.bool_output_entry.grid(row=0, column=0, sticky="WE")
        self.bool_output_strvar.set("")
        self.inputs_list = []
        await self.gen_input_frame()
        self.is_refreshing = False

    async def draw_bool_out(self):
        self.generate_bool_button.config(state=tk.DISABLED)
        for row in self.inputs_list:
            try:
                if row[1].get() == "":
                    if self.inputs_list.index(row) not in [0, 1]:
                        await self.delete_bool_row(row)
            except AttributeError:
                pass
        output_boolean = await core.generate_bool(int(self.how_many_match.get()), self.inputs_list)
        # print(output_boolean)
        self.root.clipboard_clear()
        self.root.clipboard_append(output_boolean)
        if len(output_boolean) > 20000:
            self.bool_output_strvar.set("Search too long, sent to clipboard.")
        else:
            self.bool_output_strvar.set(output_boolean)
        self.generate_bool_button.config(state=tk.NORMAL)

    def __bool_output_highlight_all_callback(self, event):
        self.bool_output_entry.selection_range(0, tk.END)

    async def main_loop(self):
        while True:
            try:
                if not self.is_refreshing:
                    self.root.update()
            except tk.TclError:
                exit()
            await asyncio.sleep(0.0001)


if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Minimum Python version: 3.7.0"
    test_gui = MainGUI()
