from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor
import random
import math

class MatrixBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAutoFillBackground(False)
        
        if parent:
            self.resize(parent.size())
        
        self.points = []
        self.lines = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_points)
        self.timer.start(30)
        self.glow_points = []
        self.particle_age = {}
        self.pulse_animation = 0

    def update_points(self):
        width = self.width()
        height = self.height()
        
        # Agregar nuevos puntos
        if len(self.points) < 100:
            new_point = [
                random.randint(0, width), 
                random.randint(0, height),
                random.uniform(-2.5, 2.5),
                random.uniform(-2.5, 2.5),
            ]
            self.points.append(new_point)
            self.particle_age[id(new_point)] = 0

        # Actualizar movimiento de puntos
        for point in self.points[:]:
            point[0] += point[2]
            point[1] += point[3]
            
            # Rebote suave en bordes
            if point[0] < 0 or point[0] > width:
                point[2] *= -1
                point[0] = max(0, min(width, point[0]))
            if point[1] < 0 or point[1] > height:
                point[3] *= -1
                point[1] = max(0, min(height, point[1]))
            
            # Envejecimiento
            pid = id(point)
            if pid in self.particle_age:
                self.particle_age[pid] += 1

        # Limpiar puntos viejos
        self.points = [p for p in self.points if id(p) in self.particle_age and self.particle_age[id(p)] < 600]
        
        # Actualizar líneas de conexión
        self.lines = []
        for i, point1 in enumerate(self.points):
            for point2 in self.points[i+1:]:
                dx = point1[0] - point2[0]
                dy = point1[1] - point2[1]
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < 180:
                    self.lines.append((point1, point2, distance))

        # Seleccionar puntos con glow
        self.glow_points = random.sample(self.points, min(len(self.points), 20))
        
        # Animación de pulso
        self.pulse_animation = (self.pulse_animation + 0.05) % (2 * math.pi)
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Fondo muy transparente para ver los puntos
        painter.fillRect(self.rect(), QColor(0, 0, 0, 5))
        
        # Dibujar líneas de conexión
        for line in self.lines:
            opacity = max(0.15, min(0.7, 1 - (line[2] / 180)))
            color = QColor(46, 204, 113)
            color.setAlphaF(opacity * 0.8)
            painter.setPen(QPen(color, 1.8))
            painter.drawLine(int(line[0][0]), int(line[0][1]),
                           int(line[1][0]), int(line[1][1]))
        
        # Dibujar puntos principales
        for point in self.points:
            brightness = max(0.4, min(1.0, 1 - (self.particle_age.get(id(point), 0) / 600)))
            color = QColor(46, 204, 113)
            color.setAlphaF(0.85 * brightness)
            painter.setPen(QPen(color, 2.5))
            painter.drawPoint(int(point[0]), int(point[1]))
        
        # Dibujar puntos con mega glow (brillan más)
        for point in self.glow_points:
            pid = id(point)
            brightness = max(0.4, min(1.0, 1 - (self.particle_age.get(pid, 0) / 600)))
            pulse = 0.5 + 0.5 * math.sin(self.pulse_animation)
            
            # Glow externo - muy visible
            glow_outer = QColor(46, 204, 113)
            glow_outer.setAlphaF((0.25 * brightness * pulse))
            painter.setPen(QPen(glow_outer, 28))
            painter.drawPoint(int(point[0]), int(point[1]))
            
            # Glow medio - vibrante
            glow_mid = QColor(46, 204, 113)
            glow_mid.setAlphaF((0.5 * brightness * pulse))
            painter.setPen(QPen(glow_mid, 16))
            painter.drawPoint(int(point[0]), int(point[1]))
            
            # Centro brillante
            center = QColor(46, 204, 113)
            center.setAlphaF(0.98 * brightness)
            painter.setPen(QPen(center, 7))
            painter.drawPoint(int(point[0]), int(point[1]))
