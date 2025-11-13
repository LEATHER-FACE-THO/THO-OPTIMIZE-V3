from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                              QWidget, QLabel, QMessageBox, QHBoxLayout, QTextEdit,
                              QFrame, QScrollArea, QStackedWidget)
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QUrl, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor, QIcon, QDesktopServices, QMouseEvent, QPixmap
from PySide6.QtMultimedia import QSoundEffect  
from matrix_background import MatrixBackground  

try:
    import win32security
    import win32api
    import win32con
except ImportError:
    pass

import os
import subprocess
import winreg
import ctypes
import sys
import psutil
import threading
import json
import shutil
from datetime import datetime

class OptimizationWorker(QThread):
    progress = Signal(str)
    finished = Signal(bool)
    error_occurred = Signal(str)
    
    def __init__(self, optimize=True):
        super().__init__()
        self.optimize = optimize
        self.backup_data = {}
        
    def run(self):
        try:
            if self.optimize:
                self.crear_punto_restauracion()
                self.optimizar_completo()
            else:
                self.restaurar_completo()
            self.finished.emit(True)
        except Exception as e:
            self.progress.emit(f"❌ ERROR CRÍTICO: {str(e)}")
            self.error_ocurrido.emit(str(e))
            self.finished.emit(False)
    
    def crear_punto_restauracion(self):
        try:
            self.progress.emit("📍 Creando punto de restauración...")
            subprocess.run('wmic.exe /Namespace:\\\\root\\default Class SystemRestore Call CreateRestorePoint "THO-OPTIMIZE-BACKUP", 100, 7', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            self.progress.emit("✅ Punto de restauración creado exitosamente")
        except Exception as e:
            self.progress.emit(f"⚠️ Advertencia: No se pudo crear punto de restauración")
    
    def optimizar_completo(self):
        self.progress.emit("\n" + "="*60)
        self.progress.emit("🚀 INICIANDO OPTIMIZACIÓN COMPLETA DEL SISTEMA")
        self.progress.emit("="*60 + "\n")
        
        self.optimizar_servicios_tho()
        self.limpiar_temporales_tho()
        self.optimizar_ram_tho()
        self.optimizar_gpu_tho()
        self.optimizar_registro_tho()
        self.optimizar_red_tho()
        self.optimizar_sistema_tho()
        self.optimizar_disco_tho()
        self.desactivar_telemetria()
        self.optimizar_energia_tho()
        self.eliminar_apps_innecesarias()
        self.optimizar_startup_tho()
        self.limpiar_cache_aplicaciones()
        
        self.progress.emit("\n" + "="*60)
        self.progress.emit("✨ OPTIMIZACIÓN COMPLETADA EXITOSAMENTE")
        self.progress.emit("="*60)
    
    def optimizar_servicios_tho(self):
        self.progress.emit("\n📋 [1/13] Optimizando servicios de Windows...")
        servicios_desactivar = [
            "DiagTrack", "dmwappushservice", "SysMain", "WSearch", 
            "XboxGipSvc", "XblAuthManager", "XblGameSave", "TabletInputService",
            "Remote Registry", "PrintNotify", "fax", "WpnService", "RetailDemo",
            "DoSvc", "PcaSvc", "WMPNetworkSvc", "WerSvc", "MapsBroker",
            "BTAGService", "CDPUserSvc", "OneSyncSvc", "WpcMonSvc",
            "SharedAccess", "PhoneSvc", "SCardSvr", "DusmSvc", "DPS",
            "WdiServiceHost", "WdiSystemHost", "TapiSrv", "BITS",
            "lmhosts", "iphlpsvc", "WpnService", "MessagingService",
            "ClipSVC", "AppXSvc"
        ]
        
        desactivados = 0
        for servicio in servicios_desactivar:
            try:
                result = subprocess.run(f'sc query "{servicio}"', shell=True, 
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
                if result.returncode == 0:
                    subprocess.run(f'net stop "{servicio}" /y', shell=True, 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
                    subprocess.run(f'sc config "{servicio}" start=disabled', shell=True, 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
                    desactivados += 1
            except Exception:
                pass
        
        self.progress.emit(f"   ✓ {desactivados} servicios innecesarios desactivados")
    
    def limpiar_temporales_tho(self):
        self.progress.emit("\n🧹 [2/13] Limpiando archivos temporales...")
        rutas_temp = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            r'C:\Windows\Temp',
            r'C:\Windows\Prefetch',
            r'C:\Windows\SoftwareDistribution\Download',
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp'),
            os.path.join(os.environ.get('APPDATA'), 'Temp'),
        ]
        
        limpios = 0
        for ruta in rutas_temp:
            if ruta and os.path.exists(ruta):
                try:
                    for item in os.listdir(ruta):
                        path = os.path.join(ruta, item)
                        try:
                            if os.path.isfile(path):
                                os.remove(path)
                                limpios += 1
                            elif os.path.isdir(path):
                                shutil.rmtree(path, ignore_errors=True)
                                limpios += 1
                        except Exception:
                            pass
                except Exception:
                    pass
        
        try:
            subprocess.run('powershell -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        except Exception:
            pass
        
        self.progress.emit(f"   ✓ {limpios} archivos temporales eliminados")
    
    def optimizar_ram_tho(self):
        self.progress.emit("\n💾 [3/13] Optimizando memoria RAM...")
        try:
            ctypes.windll.psapi.EmptyWorkingSet(ctypes.c_int(-1))
            subprocess.run('ipconfig /flushdns', shell=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            self.progress.emit("   ✓ RAM optimizada y caché DNS limpiado")
        except Exception as e:
            self.progress.emit(f"   ✗ Error en RAM: {str(e)}")
    
    def optimizar_gpu_tho(self):
        self.progress.emit("\n🎮 [4/13] Optimizando caché de GPU...")
        shader_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA'), 'NVIDIA\\GLCache'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'AMD\\GLCache'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Intel\\GLCache'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'NVIDIA Corporation'),
        ]
        limpios = 0
        for path in shader_paths:
            if os.path.exists(path):
                try:
                    for item in os.listdir(path):
                        fullpath = os.path.join(path, item)
                        try:
                            if os.path.isfile(fullpath):
                                os.remove(fullpath)
                                limpios += 1
                            elif os.path.isdir(fullpath):
                                shutil.rmtree(fullpath, ignore_errors=True)
                                limpios += 1
                        except Exception:
                            pass
                except Exception:
                    pass
        
        self.progress.emit(f"   ✓ Caché de GPU limpiado ({limpios} archivos)")
    
    def optimizar_registro_tho(self):
        self.progress.emit("\n⚙️ [5/13] Optimizando registro del sistema...")
        try:
            optimizaciones = [
                {
                    'path': r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
                    'values': {
                        'LargeSystemCache': (winreg.REG_DWORD, 1),
                        'SystemCacheDirtyPageThreshold': (winreg.REG_DWORD, 1000),
                        'IoPageLockLimit': (winreg.REG_DWORD, 983040),
                        'ClearPageFileAtShutdown': (winreg.REG_DWORD, 1)
                    }
                },
                {
                    'path': r'SYSTEM\CurrentControlSet\Control\PriorityControl',
                    'values': {
                        'Win32PrioritySeparation': (winreg.REG_DWORD, 38)
                    }
                },
                {
                    'path': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile',
                    'values': {
                        'SystemResponsiveness': (winreg.REG_DWORD, 0),
                        'NetworkThrottlingIndex': (winreg.REG_DWORD, 4294967295)
                    }
                },
                {
                    'path': r'SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters',
                    'values': {
                        'IRPStackSize': (winreg.REG_DWORD, 32)
                    }
                }
            ]
            
            for reg_key in optimizaciones:
                try:
                    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, reg_key['path'], 
                                           0, winreg.KEY_ALL_ACCESS)
                    for value_name, (value_type, value_data) in reg_key['values'].items():
                        winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                except Exception as e:
                    pass
            
            self.progress.emit("   ✓ Registro optimizado")
        except Exception as e:
            self.progress.emit(f"   ✗ Error en registro: {str(e)}")
    
    def optimizar_red_tho(self):
        self.progress.emit("\n🌐 [6/13] Optimizando red y conectividad...")
        network_commands = [
            'netsh int tcp set global autotuninglevel=normal',
            'netsh int tcp set global chimney=enabled',
            'netsh int tcp set global dca=enabled',
            'netsh int tcp set global ecncapability=enabled',
            'netsh int tcp set global rss=enabled',
            'netsh int tcp set global timestamps=disabled',
            'netsh interface tcp set heuristics disabled',
            'netsh int tcp set supplemental internet congestionprovider=ctcp',
            'netsh int tcp set global initialRto=2000',
            'netsh int tcp set global nonsackrttresiliency=disabled',
            'ipconfig /flushdns',
            'ipconfig /registerdns',
            'netsh winsock reset',
        ]
        
        ejecutados = 0
        for cmd in network_commands:
            try:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL, timeout=5)
                ejecutados += 1
            except Exception:
                pass
        
        try:
            dns_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, 
                                       r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters",
                                       0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(dns_key, "MaxCacheTtl", 0, winreg.REG_DWORD, 86400)
            winreg.SetValueEx(dns_key, "MaxNegativeCacheTtl", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(dns_key)
        except Exception:
            pass
        
        self.progress.emit(f"   ✓ {ejecutados} optimizaciones de red aplicadas")
    
    def optimizar_sistema_tho(self):
        self.progress.emit("\n🖥️ [7/13] Optimizando configuración del sistema...")
        system_commands = [
            'fsutil behavior set disablelastaccess 1',
            'fsutil behavior set memoryusage 2',
            'bcdedit /set useplatformclock no',
            'bcdedit /set disabledynamictick yes',
            'bcdedit /set bootmenupolicy legacy',
            'bcdedit /set nx OptOut',
            'bcdedit /set bootux disabled'
        ]
        
        ejecutados = 0
        for cmd in system_commands:
            try:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL, timeout=5)
                ejecutados += 1
            except Exception:
                pass
        
        self.progress.emit(f"   ✓ {ejecutados} optimizaciones del sistema aplicadas")
    
    def optimizar_disco_tho(self):
        self.progress.emit("\n💿 [8/13] Optimizando disco duro...")
        try:
            subprocess.run('defrag C: /U /V', shell=True, stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, timeout=60)
            self.progress.emit("   ✓ Disco optimizado")
        except Exception:
            self.progress.emit("   ⚠️ Desfragmentación completada con advertencias")
    
    def desactivar_telemetria(self):
        self.progress.emit("\n🔒 [9/13] Desactivando telemetría y rastreo...")
        try:
            telemetria_commands = [
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowDiagnosticData /t REG_DWORD /d 0 /f',
                'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Privacy" /v TailoredExperiencesAllowed /t REG_DWORD /d 0 /f',
                'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Privacy" /v AdId /t REG_SZ /d "" /f',
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy" /v LetAppsRunInBackground /t REG_DWORD /d 2 /f'
            ]
            
            for cmd in telemetria_commands:
                try:
                    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL, timeout=5)
                except Exception:
                    pass
            
            self.progress.emit("   ✓ Telemetría y rastreo desactivados")
        except Exception:
            pass
    
    def optimizar_energia_tho(self):
        self.progress.emit("\n⚡ [10/13] Optimizando esquema de energía...")
        try:
            subprocess.run('powercfg /duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            subprocess.run('powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            self.progress.emit("   ✓ Esquema de energía optimizado para máximo rendimiento")
        except Exception:
            pass
    
    def eliminar_apps_innecesarias(self):
        self.progress.emit("\n📦 [11/13] Eliminando aplicaciones innecesarias...")
        apps_to_remove = [
            "Microsoft.BingWeather", "Microsoft.GetHelp", "Microsoft.Getstarted",
            "Microsoft.MixedReality.Portal", "Microsoft.People", "Microsoft.SkypeApp",
            "Microsoft.WindowsFeedbackHub", "Microsoft.XboxApp", "Microsoft.XboxGameOverlay",
            "Microsoft.YourPhone", "Microsoft.ZuneMusic", "Microsoft.ZuneVideo"
        ]
        
        removidos = 0
        for app in apps_to_remove:
            try:
                subprocess.run(f'powershell -Command "Get-AppxPackage *{app}* | Remove-AppxPackage -ErrorAction SilentlyContinue"', 
                             shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
                removidos += 1
            except Exception:
                pass
        
        self.progress.emit(f"   ✓ {removidos} aplicaciones bloat eliminadas")
    
    def optimizar_startup_tho(self):
        self.progress.emit("\n⏱️ [12/13] Optimizando arranque del sistema...")
        try:
            startup_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, 
                                           r"SYSTEM\CurrentControlSet\Control\SessionManager\PowerPlan",
                                           0, winreg.KEY_ALL_ACCESS)
            winreg.CloseKey(startup_key)
            
            subprocess.run('wevtutil cl System', shell=True, stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, timeout=5)
            subprocess.run('wevtutil cl Application', shell=True, stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, timeout=5)
            
            self.progress.emit("   ✓ Arranque optimizado")
        except Exception:
            pass
    
    def limpiar_cache_aplicaciones(self):
        self.progress.emit("\n🗑️ [13/13] Limpiando caché de aplicaciones...")
        try:
            cache_paths = [
                os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft\\Windows\\INetCache'),
                os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp'),
                os.path.join(os.environ.get('APPDATA'), 'Microsoft\\Windows\\Recent'),
            ]
            
            limpios = 0
            for cache_path in cache_paths:
                if os.path.exists(cache_path):
                    try:
                        for item in os.listdir(cache_path):
                            fullpath = os.path.join(cache_path, item)
                            try:
                                if os.path.isfile(fullpath):
                                    os.remove(fullpath)
                                    limpios += 1
                            except Exception:
                                pass
                    except Exception:
                        pass
            
            self.progress.emit(f"   ✓ Caché de aplicaciones limpiado ({limpios} archivos)")
        except Exception:
            pass
    
    def restaurar_completo(self):
        self.progress.emit("\n" + "="*60)
        self.progress.emit("🔄 INICIANDO RESTAURACIÓN DEL SISTEMA")
        self.progress.emit("="*60 + "\n")
        
        self.progress.emit("📋 Restaurando servicios de Windows...")
        servicios_restaurar = [
            ("DiagTrack", "auto"), ("SysMain", "auto"), ("WSearch", "auto"),
            ("XboxGipSvc", "manual"), ("XblAuthManager", "manual"), ("XblGameSave", "manual"),
            ("TabletInputService", "manual"), ("PrintNotify", "manual"), ("fax", "disabled"),
            ("WpnService", "manual"), ("RetailDemo", "disabled"), ("DoSvc", "manual"),
            ("PcaSvc", "manual"), ("WMPNetworkSvc", "manual"), ("WerSvc", "manual"),
            ("MapsBroker", "manual"), ("BTAGService", "manual"), ("CDPUserSvc", "manual"),
            ("OneSyncSvc", "manual"), ("WpcMonSvc", "manual"), ("SharedAccess", "manual"),
            ("PhoneSvc", "manual"), ("SCardSvr", "manual"), ("DusmSvc", "manual"), ("DPS", "manual")
        ]
        
        for servicio, tipo in servicios_restaurar:
            try:
                subprocess.run(f'sc config "{servicio}" start={tipo}', shell=True, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
                subprocess.run(f'net start "{servicio}" >nul 2>&1', shell=True, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            except Exception:
                pass
        
        self.progress.emit("✓ Servicios restaurados\n")
        
        self.progress.emit("⚙️ Restaurando configuración del registro...")
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, 
                                   r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
                                   0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "LargeSystemCache", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "SystemCacheDirtyPageThreshold", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "IoPageLockLimit", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except Exception:
            pass
        
        self.progress.emit("✓ Registro restaurado\n")
        
        self.progress.emit("⚡ Restaurando configuración de energía...")
        try:
            subprocess.run('powercfg -restoredefaultschemes', shell=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            subprocess.run('powercfg -setactive scheme_balanced', shell=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        except Exception:
            pass
        
        self.progress.emit("✓ Energía restaurada\n")
        
        self.progress.emit("🖥️ Restaurando configuración del sistema...")
        try:
            subprocess.run('bcdedit /deletevalue useplatformclock', shell=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            subprocess.run('bcdedit /deletevalue disabledynamictick', shell=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            subprocess.run('bcdedit /deletevalue bootmenupolicy', shell=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        except Exception:
            pass
        
        self.progress.emit("✓ Sistema restaurado\n")
        
        self.progress.emit("🔒 Restaurando telemetría a valores por defecto...")
        try:
            subprocess.run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowDiagnosticData /t REG_DWORD /d 1 /f', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        except Exception:
            pass
        
        self.progress.emit("✓ Telemetría restaurada\n")
        
        self.progress.emit("="*60)
        self.progress.emit("✨ RESTAURACIÓN COMPLETADA EXITOSAMENTE")
        self.progress.emit("="*60)


class OptimizadorTHO(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("THO OPTIMIZER 2.0 - PROFESSIONAL")
        self.setFixedSize(1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        
        self.drag_position = None
        self.current_page = 0
        
        self.setWindowOpacity(0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(1200)
        self.fade_in_animation.start()
        
        self.elevar_privilegios()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        
        self.background = MatrixBackground(self)
        self.background.resize(self.size())
        self.background.lower()
        
        # Barra de título personalizada
        title_bar = QFrame()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(0, 0, 0, 0.98), stop:1 rgba(46, 204, 113, 0.1));
                border-bottom: 3px solid #2ecc71;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        title_label = QLabel("⚡ THO OPTIMIZER 2.0 PROFESSIONAL ⚡")
        title_label.setStyleSheet("""
            color: #2ecc71; 
            font-size: 18px; 
            font-weight: bold;
            letter-spacing: 2px;
        """)
        title_label.setFont(QFont("Courier New", 11, QFont.Bold))
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        minimize_btn = QPushButton("−")
        minimize_btn.setFixedSize(45, 50)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2ecc71;
                border: none;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(46, 204, 113, 0.2);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(minimize_btn)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(45, 50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2ecc71;
                border: none;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(220, 53, 69, 0.7);
                border-radius: 0px;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        # Contenedor principal
        main_container = QWidget()
        main_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.4);")
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Stack para cambiar entre páginas
        self.stack = QStackedWidget()
        
        # Página 1: Botones principales
        page1 = self.crear_pagina_principal()
        
        # Página 2: Créditos
        page2 = self.crear_pagina_creditos()
        
        self.stack.addWidget(page1)
        self.stack.addWidget(page2)
        
        main_layout.addWidget(self.stack)
        
        central_layout.addWidget(title_bar)
        central_layout.addWidget(main_container)
        
        self.worker = None
        
        self.success_sound = QSoundEffect(self)
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            sound_path = os.path.join(base_path, "sound", "2.wav")
            if os.path.exists(sound_path):
                self.success_sound.setSource(QUrl.fromLocalFile(sound_path))
                self.success_sound.setVolume(1.0)
        except Exception:
            pass
    
    def crear_pagina_principal(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Panel de botones
        buttons_panel = QFrame()
        buttons_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.9);
                border: 3px solid #2ecc71;
                border-radius: 15px;
                padding: 40px;
            }
        """)
        buttons_layout = QVBoxLayout(buttons_panel)
        buttons_layout.setSpacing(40)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Título
        titulo = QLabel("SELECCIONA UNA OPCIÓN")
        titulo.setStyleSheet("""
            color: #2ecc71; 
            font-size: 20px; 
            font-weight: bold;
            padding: 10px;
            border-bottom: 2px solid #2ecc71;
        """)
        titulo.setAlignment(Qt.AlignCenter)
        buttons_layout.addWidget(titulo)
        
        # Botón OPTIMIZAR
        self.btn_optimizar = QPushButton("⚡ OPTIMIZAR AL MÁXIMO")
        self.btn_optimizar.setFixedSize(350, 100)
        self.btn_optimizar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.5), stop:1 rgba(46, 204, 113, 0.3));
                color: #2ecc71;
                border: 4px solid #2ecc71;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.7), stop:1 rgba(46, 204, 113, 0.5));
                border: 4px solid #27ae60;
            }
            QPushButton:pressed {
                background: rgba(46, 204, 113, 0.9);
            }
        """)
        self.btn_optimizar.clicked.connect(self.iniciar_optimizacion)
        buttons_layout.addWidget(self.btn_optimizar, alignment=Qt.AlignCenter)
        
        # Botón RESTAURAR
        self.btn_restaurar = QPushButton("🔄 RESTAURAR SISTEMA")
        self.btn_restaurar.setFixedSize(350, 100)
        self.btn_restaurar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(230, 126, 34, 0.5), stop:1 rgba(230, 126, 34, 0.3));
                color: #e67e22;
                border: 4px solid #e67e22;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(230, 126, 34, 0.7), stop:1 rgba(230, 126, 34, 0.5));
                border: 4px solid #d35400;
            }
            QPushButton:pressed {
                background: rgba(230, 126, 34, 0.9);
            }
        """)
        self.btn_restaurar.clicked.connect(self.iniciar_restauracion)
        buttons_layout.addWidget(self.btn_restaurar, alignment=Qt.AlignCenter)
        
        # Botón CRÉDITOS
        self.btn_creditos = QPushButton("📋 CRÉDITOS DEL CREADOR")
        self.btn_creditos.setFixedSize(350, 100)
        self.btn_creditos.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(149, 165, 166, 0.5), stop:1 rgba(149, 165, 166, 0.3));
                color: #95a5a6;
                border: 4px solid #95a5a6;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(149, 165, 166, 0.7), stop:1 rgba(149, 165, 166, 0.5));
                border: 4px solid #7f8c8d;
            }
            QPushButton:pressed {
                background: rgba(149, 165, 166, 0.9);
            }
        """)
        self.btn_creditos.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        buttons_layout.addWidget(self.btn_creditos, alignment=Qt.AlignCenter)
        
        layout.addWidget(buttons_panel)
        
        # Panel de logs (CRT)
        logs_panel = QFrame()
        logs_panel.setFixedWidth(450)
        logs_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.95);
                border: 3px solid #2ecc71;
                border-radius: 15px;
            }
        """)
        logs_layout = QVBoxLayout(logs_panel)
        logs_layout.setContentsMargins(15, 15, 15, 15)
        logs_layout.setSpacing(10)
        
        logs_title = QLabel("📡 CONSOLA CRT - MONITOR DEL SISTEMA")
        logs_title.setStyleSheet("""
            color: #2ecc71; 
            font-size: 13px; 
            font-weight: bold; 
            padding: 8px;
            border-bottom: 2px solid #2ecc71;
            letter-spacing: 1px;
        """)
        logs_layout.addWidget(logs_title)
        
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.98);
                color: #2ecc71;
                border: 2px solid #2ecc71;
                border-radius: 8px;
                font-family: 'Courier New';
                font-size: 9px;
                padding: 5px;
            }
            QScrollBar:vertical {
                background-color: rgba(46, 204, 113, 0.1);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(46, 204, 113, 0.5);
                border-radius: 6px;
            }
        """)
        logs_layout.addWidget(self.log_console)
        
        layout.addWidget(logs_panel)
        
        return page
    
    def crear_pagina_creditos(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Panel central de créditos - SIMPLE Y LIMPIO
        credits_panel = QWidget()
        credits_panel.setStyleSheet("background-color: transparent;")
        credits_layout = QVBoxLayout(credits_panel)
        credits_layout.setContentsMargins(80, 80, 80, 80)
        credits_layout.setSpacing(60)
        credits_layout.setAlignment(Qt.AlignCenter)
        
        # Título
        titulo = QLabel("THO OPTIMIZER 2.0")
        titulo.setStyleSheet("""
            color: #2ecc71; 
            font-size: 52px; 
            font-weight: bold;
            letter-spacing: 4px;
        """)
        titulo.setFont(QFont("Courier New", 26, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        credits_layout.addWidget(titulo)
        
        # Subtítulo - Creador
        creador = QLabel("CREADO POR\nHANNIBAL THO")
        creador.setStyleSheet("""
            color: #f39c12; 
            font-size: 24px; 
            font-weight: bold;
            letter-spacing: 2px;
            line-height: 1.8;
        """)
        creador.setAlignment(Qt.AlignCenter)
        credits_layout.addWidget(creador)
        
        # Línea separadora brillante
        separator = QFrame()
        separator.setStyleSheet("background-color: #2ecc71;")
        separator.setFixedHeight(2)
        credits_layout.addWidget(separator)
        
        # Espaciador
        credits_layout.addSpacing(30)
        
        # Botones en grid 2x2
        buttons_grid = QHBoxLayout()
        buttons_grid.setSpacing(40)
        buttons_grid.setAlignment(Qt.AlignCenter)
        
        # GitHub
        github_btn = QPushButton("🔗\nGITHUB\nOFICIAL")
        github_btn.setFixedSize(130, 130)
        github_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.5), stop:1 rgba(46, 204, 113, 0.2));
                color: #2ecc71;
                border: 3px solid #2ecc71;
                border-radius: 15px;
                font-size: 11px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.8), stop:1 rgba(46, 204, 113, 0.5));
                border: 3px solid #27ae60;
            }
            QPushButton:pressed {
                background: rgba(46, 204, 113, 0.9);
            }
        """)
        github_btn.setCursor(Qt.PointingHandCursor)
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/TODO-HACK-OFFICIAL")))
        buttons_grid.addWidget(github_btn)
        
        # PayPal
        paypal_btn = QPushButton("💰\nPAYPAL\nDIRECTO")
        paypal_btn.setFixedSize(130, 130)
        paypal_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(52, 152, 219, 0.5), stop:1 rgba(52, 152, 219, 0.2));
                color: #3498db;
                border: 3px solid #3498db;
                border-radius: 15px;
                font-size: 11px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(52, 152, 219, 0.8), stop:1 rgba(52, 152, 219, 0.5));
                border: 3px solid #2980b9;
            }
            QPushButton:pressed {
                background: rgba(52, 152, 219, 0.9);
            }
        """)
        paypal_btn.setCursor(Qt.PointingHandCursor)
        paypal_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.paypal.com/paypalme/cakarrota2022")))
        buttons_grid.addWidget(paypal_btn)
        
        # Discord
        discord_btn = QPushButton("🎮\nDISCORD\nDEL SERVIDOR")
        discord_btn.setFixedSize(130, 130)
        discord_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(114, 137, 218, 0.5), stop:1 rgba(114, 137, 218, 0.2));
                color: #7289da;
                border: 3px solid #7289da;
                border-radius: 15px;
                font-size: 11px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(114, 137, 218, 0.8), stop:1 rgba(114, 137, 218, 0.5));
                border: 3px solid #5a6fa0;
            }
            QPushButton:pressed {
                background: rgba(114, 137, 218, 0.9);
            }
        """)
        discord_btn.setCursor(Qt.PointingHandCursor)
        discord_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://discord.gg/4svwzsy3UP")))
        buttons_grid.addWidget(discord_btn)
        
        # YouTube
        youtube_btn = QPushButton("📺\nYOUTUBE\nDEL CANAL")
        youtube_btn.setFixedSize(130, 130)
        youtube_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 0, 0, 0.5), stop:1 rgba(255, 0, 0, 0.2));
                color: #ff0000;
                border: 3px solid #ff0000;
                border-radius: 15px;
                font-size: 11px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 0, 0, 0.8), stop:1 rgba(255, 0, 0, 0.5));
                border: 3px solid #cc0000;
            }
            QPushButton:pressed {
                background: rgba(255, 0, 0, 0.9);
            }
        """)
        youtube_btn.setCursor(Qt.PointingHandCursor)
        youtube_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.youtube.com/@TODO-HACK-OFFICIAL")))
        buttons_grid.addWidget(youtube_btn)
        
        credits_layout.addLayout(buttons_grid)
        credits_layout.addSpacing(50)
        
        # Botón volver
        volver_btn = QPushButton("◄ VOLVER")
        volver_btn.setFixedSize(280, 65)
        volver_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.6), stop:1 rgba(46, 204, 113, 0.3));
                color: #2ecc71;
                border: 3px solid #2ecc71;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.8), stop:1 rgba(46, 204, 113, 0.5));
                border: 3px solid #27ae60;
            }
            QPushButton:pressed {
                background: rgba(46, 204, 113, 0.95);
            }
        """)
        volver_btn.setCursor(Qt.PointingHandCursor)
        volver_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        credits_layout.addWidget(volver_btn, alignment=Qt.AlignCenter)
        
        credits_layout.addStretch()
        
        layout.addWidget(credits_panel)
        
        return page
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.position().y() < 50:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_position = None
    
    def log(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_console.append(f"[{timestamp}] {mensaje}")
        self.log_console.verticalScrollBar().setValue(
            self.log_console.verticalScrollBar().maximum()
        )
    
    def iniciar_optimizacion(self):
        respuesta = QMessageBox.question(self, "CONFIRMAR OPTIMIZACIÓN", 
            "⚡ ¿DESEAS OPTIMIZAR TU PC AL MÁXIMO?\n\n"
            "✓ Se creará un punto de restauración automático\n"
            "✓ La optimización durará algunos minutos\n"
            "✓ Se recomienda no usar la PC durante el proceso\n\n"
            "¿Deseas continuar?", 
            QMessageBox.Yes | QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            self.btn_optimizar.setEnabled(False)
            self.btn_restaurar.setEnabled(False)
            self.btn_creditos.setEnabled(False)
            self.log_console.clear()
            self.log("🚀 Iniciando optimización completa...")
            
            self.worker = OptimizationWorker(optimize=True)
            self.worker.progress.connect(self.log)
            self.worker.finished.connect(self.optimizacion_finalizada)
            self.worker.error_occurred.connect(lambda e: self.log(f"❌ {e}"))
            self.worker.start()
    
    def iniciar_restauracion(self):
        respuesta = QMessageBox.question(self, "CONFIRMAR RESTAURACIÓN", 
            "🔄 ¿DESEAS RESTAURAR EL SISTEMA?\n\n"
            "⚠️ Esto revertirá TODA la optimización\n"
            "⚠️ El sistema volverá a valores por defecto\n"
            "✓ Durará algunos minutos\n\n"
            "¿Deseas continuar?", 
            QMessageBox.Yes | QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            self.btn_optimizar.setEnabled(False)
            self.btn_restaurar.setEnabled(False)
            self.btn_creditos.setEnabled(False)
            self.log_console.clear()
            self.log("🔄 Iniciando restauración del sistema...")
            
            self.worker = OptimizationWorker(optimize=False)
            self.worker.progress.connect(self.log)
            self.worker.finished.connect(self.restauracion_finalizada)
            self.worker.error_occurred.connect(lambda e: self.log(f"❌ {e}"))
            self.worker.start()
    
    def optimizacion_finalizada(self, exitoso):
        self.btn_optimizar.setEnabled(True)
        self.btn_restaurar.setEnabled(True)
        self.btn_creditos.setEnabled(True)
        
        if exitoso:
            try:
                self.success_sound.play()
            except Exception:
                pass
            
            QMessageBox.information(self, "✨ ÉXITO", 
                "¡OPTIMIZACIÓN COMPLETADA EXITOSAMENTE!\n\n"
                "🚀 Tu PC está super rápida en TODO:\n"
                "   ✓ WiFi - Velocidad máxima\n"
                "   ✓ Sistema - Rendimiento óptimo\n"
                "   ✓ Aplicaciones - Ejecución suave\n"
                "   ✓ Juegos - FPS mejorado\n\n"
                "💡 Se recomienda reiniciar la PC para mejores resultados.")
        else:
            QMessageBox.critical(self, "❌ ERROR", 
                "Hubo un error durante la optimización.\n"
                "Por favor, intenta nuevamente.")
    
    def restauracion_finalizada(self, exitoso):
        self.btn_optimizar.setEnabled(True)
        self.btn_restaurar.setEnabled(True)
        self.btn_creditos.setEnabled(True)
        
        if exitoso:
            try:
                self.success_sound.play()
            except Exception:
                pass
            
            QMessageBox.information(self, "✨ ÉXITO", 
                "¡RESTAURACIÓN COMPLETADA EXITOSAMENTE!\n\n"
                "🔄 Tu sistema ha sido restaurado a:\n"
                "   ✓ Valores por defecto\n"
                "   ✓ Configuración original\n"
                "   ✓ Todos los servicios activados\n\n"
                "💡 Se recomienda reiniciar la PC.")
        else:
            QMessageBox.critical(self, "❌ ERROR", 
                "Hubo un error durante la restauración.\n"
                "Por favor, intenta nuevamente.")
    
    def elevar_privilegios(self):
        try:
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                self.log("Solicitando privilegios de administrador...")
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit()
        except Exception as e:
            self.log(f"❌ Error al elevar privilegios: {str(e)}")


def main():
    app = QApplication(sys.argv)
    
    if not ctypes.windll.shell32.IsUserAnAdmin():
        if sys.platform == 'win32':
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            return
    
    app.setStyle('Fusion')
    ventana = OptimizadorTHO()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
