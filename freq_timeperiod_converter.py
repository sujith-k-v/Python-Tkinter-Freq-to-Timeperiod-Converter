#!/usr/bin/python3

from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import logging
import sys

class Freq_Timeperiod_Converter:    
    def config_logger(self):
        # Basic logger config       
        logging.basicConfig(filename="", 
                            format="%(levelname)-5s: %(filename)s(Func:%(funcName)-32s, Line:%(lineno)-3d): %(message)s")
        
        self.logger = logging.getLogger()  # Creating an object
        self.logger.setLevel(logging.INFO) # Setting the threshold of logger to DEBUG
        logging.StreamHandler(sys.stdout)  # Print logging to console output as well

    def __init__(self, master):
        # Configure logger
        self.config_logger()
        
        # Main window config
        master.title('Freq ⇔ Timeperiod Converter')
        master.resizable(False, False)
        #master.configure(background = '#d7718a')

        self.window_icon = PhotoImage(file='images/window_icon.png')
        master.iconphoto(True, self.window_icon)

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1d8b9')
        self.style.configure('TButton', background = '#e1d8b9')
        self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 11), padding=(2,2))
        self.style.configure('TCombobox', padding=(2,2))
        self.style.configure('TEntry', padding=(2,2))
        self.style.configure('Header.TLabel', font = ('Arial', 15, 'bold'))

        # Padding for widgets inside the content frame
        self.padding_x = 2
        self.padding_y = 2      

        # Frames inside the main window
        # Header
        self.frame_header = ttk.Frame(master, relief='flat') # borderwidth=10, padding=(10,10,10,10)
        self.frame_header.pack(fill=X) # fill=X, expand=False, anchor=CENTER
        self.frame_header.columnconfigure(index=1, weight=1,)
                
        self.logo_left  = PhotoImage(file = 'images/wave_left.png' ).subsample( 4, 4) 
        self.logo_right = PhotoImage(file = 'images/wave_right.png').subsample(12,12) 
        
        ttk.Label(self.frame_header, image = self.logo_left , justify=CENTER).grid(row = 0, column = 0, rowspan = 2, sticky='nsew')
        ttk.Label(self.frame_header, image = self.logo_right, justify=CENTER).grid(row = 0, column = 2, rowspan = 2, sticky='nsew')
        # to-fro symbols: ⇔, ⇌, ↔
        ttk.Label(self.frame_header, text = 'Frequency ⇔ Time-period', justify='center',
                    style = 'Header.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, wraplength = 300, justify='center',
                    text = ("Convert frequency to time-period and vice-versa")).grid(row = 1, column = 1)
        
        # Content
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack(fill=X, padx=3, pady=3)

        # Usage Selection
        self.usage_choice_dict = {  'freq_to_timeperiod': 'Frequency    → Time-period',
                                    'timeperiod_to_freq': 'Time-period → Frequency'     }      
        self.row_id = 0 # This makes rearranging hassle-free

        ttk.Label(self.frame_content, text = 'Select Usage').grid(row = self.row_id, column = 0, sticky='w', 
                                                                    padx=self.padding_x, pady=self.padding_y)

        self.usage_choice = StringVar(value=self.usage_choice_dict['freq_to_timeperiod'])        
        self.combobox_usage_choice = ttk.Combobox(self.frame_content, textvariable=self.usage_choice,
                                                    values=list(self.usage_choice_dict.values()))
        self.combobox_usage_choice.grid(row=self.row_id, column=1, columnspan=2, sticky='nsew',
                                        padx=self.padding_x, pady=self.padding_y)
        self.combobox_usage_choice.bind("<<ComboboxSelected>>", self.combobox_usage_choice_callback)

        # Freq list
        self.freq_list = (  'Hertz (Hz)',  
                            'Kilo-Hertz (kHz)', 
                            'Mega-Hertz (MHz)',
                            'Giga-Hertz (GHz)',
                            'Tera-Hertz (THz)'  )
    
        # Time-period list
        self.timeperiod_list = ('Seconds (s)',
                                'Milli-Seconds (ms)',
                                'Micro-Seconds (us)', 
                                'Nano-Seconds (ns)',
                                'Pico-Seconds (ps)',
                                'Femto-Seconds (fs)' )
    
        # Row 1
        self.row_id += 2

        # Enter source input
        self.label_input = ttk.Label(self.frame_content, text = 'Enter Frequency')
        self.label_input.grid(row = self.row_id, column = 0, sticky='w', 
                                padx=self.padding_x, pady=self.padding_y)

        validate_cmd = master.register(self.validate_int_or_float)
        self.entry_input = ttk.Entry(self.frame_content, validate='key', validatecommand=(validate_cmd, '%P'))
        self.entry_input.grid(row=self.row_id, column=1, sticky='nsew', 
                                padx=self.padding_x, pady=self.padding_y)

        self.source_unit = StringVar()
        self.combobox_source_unit = ttk.Combobox(self.frame_content, textvariable=self.source_unit, values=self.freq_list)
        self.combobox_source_unit.grid(row=self.row_id, column=2, sticky='nsew', 
                                        padx=self.padding_x, pady=self.padding_y)

        # Row 1
        self.row_id += 1

        # Output Unit
        ttk.Label(self.frame_content, text = 'Output unit').grid(row = self.row_id, column = 0, sticky='w', 
                                                                padx=self.padding_x, pady=self.padding_y)

        self.output_unit = StringVar()        
        self.combobox_output_unit = ttk.Combobox(self.frame_content, textvariable=self.output_unit,
                                                    values=self.timeperiod_list)
        self.combobox_output_unit.grid(row=self.row_id, column=1, sticky='nsew', 
                                        padx=self.padding_x, pady=self.padding_y)
        self.combobox_output_unit.bind("<<ComboboxSelected>>", self.combobox_output_unit_callback)

        # Row 1
        # Choose number of decimal places to display in result
        self.num_decimal_places = IntVar(value=10)
        # self.row_id += 1
        # ttk.Label(self.frame_content, text = 'Decimal places').grid(row = self.row_id, column = 0, sticky='w', 
        #                                                             padx=self.padding_x, pady=self.padding_y)
        
        # self.spinbox_num_decimal_places = Spinbox(self.frame_content, from_=1, to=10, textvariable=self.num_decimal_places)
        # self.spinbox_num_decimal_places.grid(row=self.row_id, column=1, sticky='nsew', 
        #                                         padx=self.padding_x, pady=self.padding_y)   

        # Row 2
        self.row_id += 1

        # Output result
        self.result = DoubleVar()
        ttk.Label(self.frame_content, text = 'Result').grid(row = self.row_id, column = 0, sticky='w', 
                                                            padx=self.padding_x, pady=self.padding_y)
        self.entry_result = ttk.Entry(self.frame_content, textvariable=self.result, state='readonly', justify=CENTER)
        self.entry_result.grid(row=self.row_id, column=1, sticky='nsew', 
                                padx=self.padding_x, pady=self.padding_y)
        
        # Refresh result
        self.logo_refresh = PhotoImage(file = 'images/logo_refresh.gif').subsample(30,30)
        self.button_refresh = ttk.Button(self.frame_content, text = "Refresh", command=self.refresh_result, state='disabled',
                    image=self.logo_refresh, compound=LEFT)
        self.button_refresh.grid(row=self.row_id, column=2, sticky='nsw',
                                    padx=self.padding_x, pady=self.padding_y)

    def validate_int_or_float(self, text):
        ''' Validate that only integer and floating point numbers can be entered into an Entry widget. 
            The character will not be input into the Entry widget
        '''
        try:
            if(text == ""):
                return True
                # Without this condition the entry widget wont allow to clear the input completely.

            float(text)
            return True
        except ValueError:
            return False
        
    def combobox_usage_choice_callback(self, event):
        self.logger.debug(f"Usage = {event.widget.get()}")
        choice = self.combobox_usage_choice.current() # Get the index of current selection
        # choice = self.usage_choice.get()
        self.logger.info( f"Usage = {choice}({list(self.usage_choice_dict)[choice]}) ") #self.usage_choice.get()
        
        # Change the souce and output unit drop-down menu list appropriately
        if  (list(self.usage_choice_dict)[choice] == 'freq_to_timeperiod'):
            self.label_input.config(text = "Enter Frequency:")
            self.combobox_source_unit.config(values=self.freq_list)
            self.combobox_output_unit.config(values=self.timeperiod_list)
        elif(list(self.usage_choice_dict)[choice] == "timeperiod_to_freq"):
            self.label_input.config(text = "Enter Time-period:")  
            self.combobox_source_unit.config(values=self.timeperiod_list)
            self.combobox_output_unit.config(values=self.freq_list)

        # Clear all fields when reselecting the mode
        self.clear_fields()

    def clear_fields(self, **field_type): # TODO: have a switch statement to clear the fields based on widget type
        self.logger.debug("Clearing all fields")
        self.entry_input.delete(0, END)
        self.combobox_source_unit.set('')
        self.combobox_output_unit.set('')
        self.result.set(0.0)    

        self.button_refresh.config(state='disabled')

    def refresh_result(self):
        self.calculate_result()

    def combobox_output_unit_callback(self, event):
        self.logger.debug(f"Output unit = {event.widget.get()}")
        self.calculate_result()

    def calculate_result(self):
        try:
            input_val          = float(self.entry_input.get())
            input_unit         = self.source_unit.get()        
            output_unit        = self.output_unit.get()  
            num_decimal_places = int(self.num_decimal_places.get())  
        except:
            messagebox.showerror(title = "Invalid Entry", message = 'Invalid input. Please Retry after entering all valid inputs')
            self.clear_fields()
            return 0
            
        self.logger.debug(f"Input       = {input_val} {input_unit}")    
        self.logger.debug(f"Output unit = {output_unit}")

        input_unit_mulitplier  = self.get_multiplier(input_unit)
        output_unit_multiplier = self.get_multiplier(output_unit)

        if((input_unit_mulitplier == 0) or (output_unit_multiplier == 0)):
            messagebox.showerror(title = "Invalid Entry", message = 'Please enter a valid unit from the drop-down menu')
            self.clear_fields()
            return 0
        
        # Enable refresh button
        #self.button_refresh.config(state='active')
        self.button_refresh.state(['!disabled'])

        reciprocal = 1.0 / (input_val * input_unit_mulitplier)   
        output_val = reciprocal / output_unit_multiplier
        
        self.logger.debug(f"Reciprocal  = {reciprocal}")
        self.logger.info( f"Output      = {output_val}")

        # Set the result to the textvariable of entry_result widget
        self.result.set(f"{output_val:,.{num_decimal_places}f}")

    def get_multiplier(self, unit):
        # For frequency
        if  (unit == 'Hertz (Hz)'      ): unit_mulitplier = 1
        elif(unit == 'Kilo-Hertz (kHz)'): unit_mulitplier = 10**(3)
        elif(unit == 'Mega-Hertz (MHz)'): unit_mulitplier = 10**(6)
        elif(unit == 'Giga-Hertz (GHz)'): unit_mulitplier = 10**(9)
        elif(unit == 'Tera-Hertz (THz)'): unit_mulitplier = 10**(12)

        # For time-period
        elif(unit == 'Seconds (s)'       ): unit_mulitplier = 1
        elif(unit == 'Milli-Seconds (ms)'): unit_mulitplier = 10**(-3)
        elif(unit == 'Micro-Seconds (us)'): unit_mulitplier = 10**(-6)
        elif(unit == 'Nano-Seconds (ns)' ): unit_mulitplier = 10**(-9)
        elif(unit == 'Pico-Seconds (ps)' ): unit_mulitplier = 10**(-12)
        elif(unit == 'Femto-Seconds (fs)'): unit_mulitplier = 10**(-15)

        else:
            # print(f"Unit = {unit}")
            # messagebox.showerror(title = "Invalid Entry", message = 'Please enter a valid unit from the drop-down menu')
            # self.clear_fields()
            return 0
        
        return unit_mulitplier

def main():                
    root = Tk()
    converter = Freq_Timeperiod_Converter(root)
    root.mainloop()
    
if __name__ == "__main__": main()