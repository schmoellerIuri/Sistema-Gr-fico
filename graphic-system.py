from ursina import *
from ursina.prefabs.file_browser import FileBrowser
from ObjReader import GetObjectFromFile
from polygon import Polygon

app = Ursina()

window.size = (800, 800)
window.color = color.rgb(255, 255, 255)
window.title = "Sistema Gráfico"
camera.orthographic = True
camera.fov = 1

def on_submit(path):
    global points
    path = path[0]
    vertices = []
    vertices = GetObjectFromFile(path)

    for vertex in vertices:
        points.append(Entity(model='circle', scale=.01, color = color.black, position=(origin[0] + vertex[0]*.1,origin[1] + vertex[1]*.1,-1), coordinates=(vertex[0]*.1, vertex[1]*.1)))

    figures.append(Polygon(points=points[:], color=color.random_color(), world_origin=origin))

    points.clear()

    fileBrowser.enabled = False

fileBrowser = FileBrowser(file_types=('.obj'), enabled=False)
fileBrowser.on_submit = on_submit

def open_file_browser():
    fileBrowser.enabled = not fileBrowser.enabled

addFileButton = Button(text='File', scale=(0.1, 0.05), color=color.rgb(0, 0, 0), x=-.85, y=0.5, z=-1, origin=(-.5, .5))
addFileButton.on_click = open_file_browser

verticalLine = Entity(model='quad', scale=(1/200, 1), origin_x=0.5, x=0, color=color.rgb(0, 0, 0), z=-1)
horizontalLine = Entity(model='quad', scale=(1, 1/200), origin_y=0.5, y=0, color=color.rgb(0, 0, 0), z=-1)

verticalLines = []
horizontalLines = []
origin = (0, 0)
lastOrigin = (0, 0)
startPosition = (0, 0)

dx = 0
dy = 0

i = -0.5
while i <= 0.5:
    verticalLines.append(Entity(model='quad', scale=(1/300, 1), origin_x=0.5, x=i, color=color.rgb(195/255, 195/255, 195/255), last_x=i))
    horizontalLines.append(Entity(model='quad', scale=(1, 1/300), origin_y=0.5, y=i, color=color.rgb(195/255, 195/255, 195/255), last_y=i))
    i += 1/10

cooldown = 0.15
pressing = False
createMode = False
points = []
figures = []

def update():
    global cooldown, scale, origin, pressing, lastOrigin, dx, dy, createMode, createFromFile
    cooldown -= time.dt

    if pressing and not createMode:
        dx = mouse.x - startPosition[0]
        dy = mouse.y - startPosition[1]

        new_origin_x = lastOrigin[0] + dx
        new_origin_y = lastOrigin[1] + dy

        if -0.5 <= new_origin_x <= 0.5 and -0.5 <= new_origin_y <= 0.5:
            origin = (new_origin_x, new_origin_y)

            verticalLine.x = origin[0]
            horizontalLine.y = origin[1]

            for line in verticalLines:
                line.x = (line.last_x + dx) % 1
                if line.x > 0.5:
                    line.x -= 1
                elif line.x < -0.5:
                    line.x += 1

            for line in horizontalLines:
                line.y = (line.last_y + dy) % 1
                if line.y > 0.5:
                    line.y -= 1
                elif line.y < -0.5:
                    line.y += 1
        for figure in figures:
            for point in figure.points:
                point.position = (origin[0] + point.coordinates[0], origin[1] + point.coordinates[1])
            figure.world_origin = origin
            figure.update_figure()
            
    if cooldown > 0:
        return
        
    if createMode:
        if mouse.left:
            cooldown = 0.15
            points.append(Entity(model='circle', scale=.01, color = color.black, position=(mouse.x, mouse.y, -1), coordinates=(mouse.x - origin[0], mouse.y - origin[1])))


def input(key):
    global scale, redraw, pressing, startPosition, lastOrigin, origin, createMode

    if Polygon.transformationMode:
        return

    if key == 'left mouse down':
        startPosition = (mouse.x, mouse.y)
        pressing = True

    if key == 'left mouse up':
        lastOrigin = origin
        for line in verticalLines:
            line.last_x = line.x
        for line in horizontalLines:
            line.last_y = line.y
        pressing = False

    if key == 'enter':
        lastMode = createMode
        createMode = not createMode
        if lastMode and not createMode:
            if len(points) > 2:
                print(points[0].coordinates)
                figures.append(Polygon(points=points[:], color=color.random_color(), world_origin=origin))
            else:
                for point in points:
                    destroy(point)
            points.clear()
                
app.run()