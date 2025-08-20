import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any

from core.numeric_generator import NumericGenerator

class NumericFrame(ttk.Frame):
    """Frame para configuración del generador numérico."""
    
    def __init__(self, parent, numeric_generator: NumericGenerator, 
                 on_config_changed: Callable):
        super().__init__(parent)
        self.numeric_generator = numeric_generator
        self.on_config_changed = on_config_changed
        
        self._create_widgets()
        self._setup_bindings()
        
    def _create_widgets(self):
        """Crear widgets del frame."""
        # Título
        title_label = ttk.Label(self, text="Generador Numérico", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(10, 20))
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Panel de configuración básica
        self._create_basic_config(main_frame)
        
        # Panel de configuración de matrícula
        self._create_matricula_config(main_frame)
        
        # Panel de vista previa
        self._create_preview_panel(main_frame)
        
    def _create_basic_config(self, parent):
        """Crear configuración básica."""
        basic_frame = ttk.LabelFrame(parent, text="⚙️ Configuración Básica", padding=15)
        basic_frame.pack(fill='x', pady=(0, 10))
        
        # Tipo de generación
        type_frame = ttk.Frame(basic_frame)
        type_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(type_frame, text="Tipo de Generación:").pack(side='left')
        
        self.generation_type = tk.StringVar(value="simple")
        ttk.Radiobutton(type_frame, text="Simple", variable=self.generation_type, 
                       value="simple").pack(side='left', padx=(20, 10))
        ttk.Radiobutton(type_frame, text="Agrupado", variable=self.generation_type, 
                       value="grouped").pack(side='left', padx=10)
        ttk.Radiobutton(type_frame, text="Matrícula", variable=self.generation_type, 
                       value="matricula").pack(side='left', padx=10)
        
        # Configuración simple/agrupado
        config_frame = ttk.Frame(basic_frame)
        config_frame.pack(fill='x', pady=10)
        
        # Número inicial
        start_frame = ttk.Frame(config_frame)
        start_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(start_frame, text="Número Inicial:").pack(anchor='w')
        self.start_number = tk.IntVar(value=1)
        ttk.Entry(start_frame, textvariable=self.start_number, width=10).pack(anchor='w')
        
        # Incremento
        increment_frame = ttk.Frame(config_frame)
        increment_frame.pack(side='left', fill='x', expand=True, padx=(20, 0))
        
        ttk.Label(increment_frame, text="Incremento:").pack(anchor='w')
        self.increment = tk.IntVar(value=1)
        ttk.Entry(increment_frame, textvariable=self.increment, width=10).pack(anchor='w')
        
        # Padding
        padding_frame = ttk.Frame(config_frame)
        padding_frame.pack(side='left', fill='x', expand=True, padx=(20, 0))
        
        ttk.Label(padding_frame, text="Relleno (dígitos):").pack(anchor='w')
        self.padding = tk.IntVar(value=4)
        ttk.Entry(padding_frame, textvariable=self.padding, width=10).pack(anchor='w')
        
        # Prefijo y sufijo
        prefix_suffix_frame = ttk.Frame(basic_frame)
        prefix_suffix_frame.pack(fill='x', pady=10)
        
        # Prefijo
        prefix_frame = ttk.Frame(prefix_suffix_frame)
        prefix_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(prefix_frame, text="Prefijo:").pack(anchor='w')
        self.prefix = tk.StringVar()
        ttk.Entry(prefix_frame, textvariable=self.prefix, width=15).pack(anchor='w')
        
        # Sufijo
        suffix_frame = ttk.Frame(prefix_suffix_frame)
        suffix_frame.pack(side='left', fill='x', expand=True, padx=(20, 0))
        
        ttk.Label(suffix_frame, text="Sufijo:").pack(anchor='w')
        self.suffix = tk.StringVar()
        ttk.Entry(suffix_frame, textvariable=self.suffix, width=15).pack(anchor='w')
        
    def _create_matricula_config(self, parent):
        """Crear configuración específica para matrícula."""
        self.matricula_frame = ttk.LabelFrame(parent, text="🎓 Configuración de Matrícula", 
                                            padding=15)
        # NO empaquetar aquí, se hará dinámicamente
        
        # Año académico
        year_frame = ttk.Frame(self.matricula_frame)
        year_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(year_frame, text="Año Académico:").pack(side='left')
        self.academic_year = tk.StringVar(value="2024")
        ttk.Entry(year_frame, textvariable=self.academic_year, width=10).pack(side='left', padx=(10, 0))
        
        # Tipo de matrícula
        type_frame = ttk.Frame(self.matricula_frame)
        type_frame.pack(fill='x', pady=10)
        
        ttk.Label(type_frame, text="Tipo de Matrícula:").pack(side='left')
        self.matricula_type = tk.StringVar(value="01")
        
        type_combo = ttk.Combobox(type_frame, textvariable=self.matricula_type, 
                                 values=["01", "02", "03", "04", "05"], width=8)
        type_combo.pack(side='left', padx=(10, 0))
        
        # Descripción de tipos
        desc_frame = ttk.Frame(self.matricula_frame)
        desc_frame.pack(fill='x', pady=10)
        
        desc_text = """Tipos de Matrícula:
    01 - Regular    02 - Especial    03 - Transferencia
    04 - Reingreso  05 - Visitante"""
        
        ttk.Label(desc_frame, text=desc_text, foreground='gray', 
                 font=('Arial', 8)).pack(anchor='w')
        
        # El frame se mostrará/ocultará dinámicamente
        
        # Configuración inicial
        self.matricula_frame.pack_forget()  # Ocultar inicialmente
        
    def _create_preview_panel(self, parent):
        """Crear panel de vista previa."""
        preview_frame = ttk.LabelFrame(parent, text="👁️ Vista Previa", padding=15)
        preview_frame.pack(fill='both', expand=True)
        
        # Controles de vista previa
        controls_frame = ttk.Frame(preview_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(controls_frame, text="Cantidad a generar:").pack(side='left')
        self.preview_count = tk.IntVar(value=10)
        ttk.Entry(controls_frame, textvariable=self.preview_count, width=8).pack(side='left', padx=(10, 0))
        
        ttk.Button(controls_frame, text="Generar Vista Previa", 
                  command=self._generate_preview).pack(side='left', padx=(20, 0))
        
        ttk.Button(controls_frame, text="Aplicar Configuración", 
                  command=self._apply_config).pack(side='right')
        
        # Lista de vista previa
        list_frame = ttk.Frame(preview_frame)
        list_frame.pack(fill='both', expand=True)
        
        self.preview_listbox = tk.Listbox(list_frame, height=8)
        preview_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', 
                                        command=self.preview_listbox.yview)
        self.preview_listbox.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_listbox.pack(side='left', fill='both', expand=True)
        preview_scrollbar.pack(side='right', fill='y')
        
    def _setup_bindings(self):
        """Configurar eventos y bindings."""
        self.generation_type.trace('w', self._on_type_changed)
        
        # Bindings para actualización automática
        for var in [self.start_number, self.increment, self.padding, 
                   self.prefix, self.suffix, self.academic_year, self.matricula_type]:
            if hasattr(var, 'trace'):
                var.trace('w', self._on_config_changed)
                
    def _on_type_changed(self, *args):
        """Callback cuando cambia el tipo de generación."""
        gen_type = self.generation_type.get()
        
        if gen_type == "matricula":
            # Verificar que el frame no esté ya empaquetado
            if not self.matricula_frame.winfo_manager():
                self.matricula_frame.pack(fill='x', pady=(0, 10))
        else:
            self.matricula_frame.pack_forget()
            
        self._generate_preview()
        
    def _on_config_changed(self, *args):
        """Callback cuando cambia la configuración."""
        # Regenerar vista previa automáticamente
        self._generate_preview()
        
    def _generate_preview(self):
        """Generar vista previa de números."""
        try:
            gen_type = self.generation_type.get()
            count = min(self.preview_count.get(), 50)  # Limitar a 50
            
            if gen_type == "simple":
                numbers = self.numeric_generator.generate_simple_sequence(
                    count=count,
                    start=self.start_number.get(),
                    increment=self.increment.get(),
                    padding=self.padding.get(),
                    prefix=self.prefix.get(),
                    suffix=self.suffix.get()
                )
            elif gen_type == "matricula":
                numbers = self.numeric_generator.generate_matricula_sequence(
                    count=count,
                    academic_year=self.academic_year.get(),
                    matricula_type=self.matricula_type.get(),
                    start_number=self.start_number.get()
                )
            else:  # grouped
                # Para agrupado, necesitamos datos de ejemplo
                numbers = self.numeric_generator.generate_simple_sequence(
                    count=count,
                    start=self.start_number.get(),
                    increment=self.increment.get(),
                    padding=self.padding.get(),
                    prefix=self.prefix.get() + "GRP",
                    suffix=self.suffix.get()
                )
                
            # Actualizar listbox
            self.preview_listbox.delete(0, tk.END)
            for i, number in enumerate(numbers, 1):
                self.preview_listbox.insert(tk.END, f"{i:2d}. {number}")
                
        except Exception as e:
            self.preview_listbox.delete(0, tk.END)
            self.preview_listbox.insert(tk.END, f"Error: {str(e)}")
            
    def _apply_config(self):
        """Aplicar configuración actual."""
        try:
            config = self._get_current_config()
            self.numeric_generator.set_config(config)
            self.on_config_changed(config)
            messagebox.showinfo("Éxito", "Configuración aplicada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar configuración: {str(e)}")
            
    def _get_current_config(self) -> Dict[str, Any]:
        """Obtener configuración actual."""
        config = {
            'type': self.generation_type.get(),
            'start_number': self.start_number.get(),
            'increment': self.increment.get(),
            'padding': self.padding.get(),
            'prefix': self.prefix.get(),
            'suffix': self.suffix.get()
        }
        
        if self.generation_type.get() == "matricula":
            config.update({
                'academic_year': self.academic_year.get(),
                'matricula_type': self.matricula_type.get()
            })
            
        return config