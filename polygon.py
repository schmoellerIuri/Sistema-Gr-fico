from ursina import *
from transformationMatrixes import TransformationMatrixes as tm
import numpy as np

class Polygon(Entity):
    transformationMode = False

    def __init__(self, points, color=color.white, world_origin=(0, 0), parent=None):
        super().__init__()
        self.points = points
        self.world_origin = world_origin
        positions = [vertex.position for vertex in self.points] + [points[0].position]
        self.model = Mesh(vertices=positions,  mode='line', thickness=3)
        self.color = color
        self.menu = None  
        self.collider = 'box'

    def triangulate(self, vertices):
        return [(0, i, i + 1) for i in range(1, len(vertices) - 1)]
    
    def get_centroid(self):
        x = sum([point.coordinates[0] for point in self.points])/len(self.points)
        y = sum([point.coordinates[1] for point in self.points])/len(self.points)
        return x, y
    
    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                self.show_menu()

    def show_menu(self):
        Polygon.transformationMode = True

        if self.menu:
            self.menu.disable()  

        self.menu = Entity(parent=camera.ui, position=mouse.position, model=Quad(scale=(.3, .35), radius=.05), color=color.gray)
        
        options = ['Escala', 'Cisalhamento', 'Rotação', 'Translação', 'Reflexão']
        for i, option in enumerate(options):
            button = Button(text=option, parent=self.menu, scale=(0.18, 0.05), position=(0, .1 -i*0.06))
            button.on_click = Func(self.on_option_selected, i)
        
    def on_option_selected(self, option):
        self.menu.disable()

        self.operationScreen = Entity(parent=camera.ui, model=Quad(scale=(.5, .3), radius=.05), color=color.gray, slider = None, input_x = None, input_y = None, check = None)

        fieldText = False
        text = ''
        if option == 0:
            fieldText = True
            text = 'Fator de escala'
        if option == 1:
            fieldText = True
            text = 'Fator de cisalhamento'
        if option == 2:
            Text('Ângulo de rotação:', parent=self.operationScreen, position=(-.225, .1))
            self.operationScreen.slider = Slider(parent=self.operationScreen, min=-180, max=180, step=1, value=0, position=(-.225, 0), scale = (.9, 1))
        if option == 3:
            fieldText = True
            text = 'Translação'
        if option == 4:
            Text('Horizontal(x)/Vertical():', parent=self.operationScreen, position=(-.225, .1), scale=(1, 1))
            self.operationScreen.check = CheckBox(parent=self.operationScreen, position=(.2, .09))
            
        if fieldText:
            Text(text + ' em x:', parent=self.operationScreen, position=(-.225, .1), scale=(.8, 1))
            Text(text + ' em y:', parent=self.operationScreen, position=( 0, .1), scale=(.8, 1))
            self.operationScreen.input_x = InputField(parent=self.operationScreen, position=(-.125, 0), scale=(.2, .05))
            self.operationScreen.input_y = InputField(parent=self.operationScreen, position=(.1, 0), scale=(.2, .05))

        button_apply = Button('Aplicar', parent=self.operationScreen, position=(.18, -.1), scale=(.1, .05))
        button_apply.on_click = Func(self.apply_operation, option)
        button_cancel = Button('Cancelar', parent=self.operationScreen, position=(.03, -.1), scale=(.1, .05))
        button_cancel.on_click = Func(self.cancel_operation)

    def apply_operation(self, option):
        if option == 0:
            x = float(self.operationScreen.input_x.text)
            y = float(self.operationScreen.input_y.text)
            self.scale(x, y)
        if option == 1:
            x = float(self.operationScreen.input_x.text)
            y = float(self.operationScreen.input_y.text)
            self.shear(x, y)
        if option == 2:
            angle = float(self.operationScreen.slider.value)
            self.rotate(angle)
        if option == 3:
            x = float(self.operationScreen.input_x.text)/10
            y = float(self.operationScreen.input_y.text)/10
            self.translate(x, y)
        if option == 4:
            sense = 'x' if self.operationScreen.check.value else 'y'
            self.reflect(sense)
        
        destroy(self.operationScreen)
        Polygon.transformationMode = False


    def cancel_operation(self):
        destroy(self.operationScreen)
        Polygon.transformationMode = False

    def scale(self, x, y):
        c_x, c_y = self.get_centroid()
        operations = tm.concatenate_operations(
            tm.translation_matrix(-c_x, -c_y),
            tm.scale_matrix(x, y),
            tm.translation_matrix(c_x, c_y)
        )
        self.update_points(operations)
        self.update_figure()

    def shear(self, x, y):
        c_x, c_y = self.get_centroid()
        operations = tm.concatenate_operations(
            tm.translation_matrix(-c_x, -c_y),
            tm.shear_matrix(x, y),
            tm.translation_matrix(c_x, c_y)
        )
        self.update_points(operations)
        self.update_figure()

    def rotate(self, angle):
        c_x, c_y = self.get_centroid()
        print(angle)
        operations = tm.concatenate_operations(
            tm.translation_matrix(-c_x, -c_y),
            tm.rotation_matrix(np.radians(angle)),
            tm.translation_matrix(c_x, c_y)
        )
        self.update_points(operations)
        self.update_figure()

    def translate(self, x, y):
        operations = tm.translation_matrix(x, y)
        self.update_points(operations)
        self.update_figure()

    def reflect(self, sense):
        c_x, c_y = self.get_centroid()
        operations = tm.concatenate_operations(
            tm.translation_matrix(-c_x, -c_y),
            tm.reflection_matrix(sense),
            tm.translation_matrix(c_x, c_y)
        )
        self.update_points(operations)
        self.update_figure()


    def update_points(self, operations):
        for point in self.points:
            new_coordinate = np.dot(operations, np.array([point.coordinates[0], point.coordinates[1], 1]))
            point.coordinates = (new_coordinate[0], new_coordinate[1])
            
            point.position = (new_coordinate[0] + self.world_origin[0], new_coordinate[1] + self.world_origin[1])

        
    def update_figure(self):
        self.model.clear()
        positions = [vertex.position for vertex in self.points] + [self.points[0].position]
        self.model = Mesh(vertices=positions,  mode='line', thickness=3)
        self.collider.enabled = False
        self.collider = None
        self.collider = 'box'

        self.enable()