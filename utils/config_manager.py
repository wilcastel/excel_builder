# -*- coding: utf-8 -*-
"""
Gestor de configuraciones de la aplicación
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import asdict

from config.settings import AppSettings
from .exceptions import ConfigurationError

class ConfigManager:
    """Gestor para cargar, guardar y gestionar configuraciones"""
    
    def __init__(self, config_dir: str = "config_files"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Archivos de configuración
        self.app_config_file = self.config_dir / "app_config.json"
        self.user_config_file = self.config_dir / "user_config.json"
        self.project_config_file = self.config_dir / "project_config.json"
        
        # Configuraciones en memoria
        self.app_settings: Optional[AppSettings] = None
        self.user_config: Dict[str, Any] = {}
        self.project_config: Dict[str, Any] = {}
    
    def load_app_settings(self) -> AppSettings:
        """Cargar configuración de la aplicación"""
        try:
            if self.app_config_file.exists():
                with open(self.app_config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Crear AppSettings con los datos cargados
                self.app_settings = AppSettings(**config_data)
            else:
                # Usar configuración por defecto
                self.app_settings = AppSettings()
                self.save_app_settings()
            
            return self.app_settings
            
        except Exception as e:
            self.logger.error(f"Error cargando configuración de aplicación: {e}")
            # Usar configuración por defecto en caso de error
            self.app_settings = AppSettings()
            return self.app_settings
    
    def save_app_settings(self) -> bool:
        """Guardar configuración de la aplicación"""
        try:
            if not self.app_settings:
                raise ConfigurationError("No hay configuración de aplicación para guardar")
            
            config_data = asdict(self.app_settings)
            
            with open(self.app_config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            
            self.logger.info("Configuración de aplicación guardada")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración de aplicación: {e}")
            return False
    
    def load_user_config(self) -> Dict[str, Any]:
        """Cargar configuración de usuario"""
        try:
            if self.user_config_file.exists():
                with open(self.user_config_file, 'r', encoding='utf-8') as f:
                    self.user_config = json.load(f)
            else:
                # Configuración por defecto de usuario
                self.user_config = {
                    'recent_files': [],
                    'last_export_dir': '',
                    'window_state': {},
                    'ui_preferences': {
                        'show_tooltips': True,
                        'auto_save_config': True,
                        'confirm_before_export': True
                    }
                }
                self.save_user_config()
            
            return self.user_config
            
        except Exception as e:
            self.logger.error(f"Error cargando configuración de usuario: {e}")
            return {}
    
    def save_user_config(self) -> bool:
        """Guardar configuración de usuario"""
        try:
            with open(self.user_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_config, f, indent=4, ensure_ascii=False)
            
            self.logger.debug("Configuración de usuario guardada")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración de usuario: {e}")
            return False
    
    def load_project_config(self, project_name: str = "default") -> Dict[str, Any]:
        """Cargar configuración de proyecto"""
        try:
            project_file = self.config_dir / f"project_{project_name}.json"
            
            if project_file.exists():
                with open(project_file, 'r', encoding='utf-8') as f:
                    self.project_config = json.load(f)
            else:
                # Configuración por defecto de proyecto
                self.project_config = {
                    'project_name': project_name,
                    'column_configs': [],
                    'numeric_config': {},
                    'mapping_config': {},
                    'export_config': {},
                    'created_at': None,
                    'modified_at': None
                }
            
            return self.project_config
            
        except Exception as e:
            self.logger.error(f"Error cargando configuración de proyecto: {e}")
            return {}
    
    def save_project_config(self, project_name: str = "default") -> bool:
        """Guardar configuración de proyecto"""
        try:
            from datetime import datetime
            
            # Actualizar timestamp
            self.project_config['modified_at'] = datetime.now().isoformat()
            if not self.project_config.get('created_at'):
                self.project_config['created_at'] = datetime.now().isoformat()
            
            project_file = self.config_dir / f"project_{project_name}.json"
            
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(self.project_config, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Configuración de proyecto '{project_name}' guardada")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración de proyecto: {e}")
            return False
    
    def update_user_preference(self, key: str, value: Any) -> bool:
        """Actualizar preferencia de usuario"""
        try:
            if 'ui_preferences' not in self.user_config:
                self.user_config['ui_preferences'] = {}
            
            self.user_config['ui_preferences'][key] = value
            return self.save_user_config()
            
        except Exception as e:
            self.logger.error(f"Error actualizando preferencia de usuario: {e}")
            return False
    
    def add_recent_file(self, file_path: str, max_recent: int = 10) -> bool:
        """Agregar archivo a la lista de recientes"""
        try:
            if 'recent_files' not in self.user_config:
                self.user_config['recent_files'] = []
            
            recent_files = self.user_config['recent_files']
            
            # Remover si ya existe
            if file_path in recent_files:
                recent_files.remove(file_path)
            
            # Agregar al inicio
            recent_files.insert(0, file_path)
            
            # Limitar cantidad
            self.user_config['recent_files'] = recent_files[:max_recent]
            
            return self.save_user_config()
            
        except Exception as e:
            self.logger.error(f"Error agregando archivo reciente: {e}")
            return False
    
    def get_recent_files(self) -> list:
        """Obtener lista de archivos recientes"""
        return self.user_config.get('recent_files', [])
    
    def export_all_configs(self, export_path: str) -> bool:
        """Exportar todas las configuraciones"""
        try:
            export_data = {
                'app_settings': asdict(self.app_settings) if self.app_settings else {},
                'user_config': self.user_config,
                'project_config': self.project_config,
                'export_timestamp': datetime.now().isoformat()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Configuraciones exportadas a: {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exportando configuraciones: {e}")
            return False
    
    def import_configs(self, import_path: str) -> bool:
        """Importar configuraciones desde archivo"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Importar configuración de aplicación
            if 'app_settings' in import_data:
                self.app_settings = AppSettings(**import_data['app_settings'])
                self.save_app_settings()
            
            # Importar configuración de usuario
            if 'user_config' in import_data:
                self.user_config.update(import_data['user_config'])
                self.save_user_config()
            
            # Importar configuración de proyecto
            if 'project_config' in import_data:
                self.project_config.update(import_data['project_config'])
                self.save_project_config()
            
            self.logger.info(f"Configuraciones importadas desde: {import_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importando configuraciones: {e}")
            return False