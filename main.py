from canvas import Canvas
from scribe import TerminalScribe, WobbleScribe
from drawing import Drawing, ParallelDrawing
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=False, help='The input Canvas file to draw on',default=None)
args = vars(parser.parse_args())

canvas = Canvas(30, 30)

if args['input']:
    canvas.load(args['input'])

scribe = TerminalScribe(canvas, framerate=0.1)
wobbly_scribe = WobbleScribe(canvas, wobbly_proba=0.3, fancy=True)

scribe.mark = "#"

pos = (0, 0)
# right direction
degree = 90
inst = [('right', 3),
        ('change_direction', 150),
        ('step_forward', 70)]

#pic = Drawing(pos, degree)

# pic.paint(scribe=scribe, instructions=inst)
# pic.plot(scribe=scribe, func=lambda x: x ** 2, range_x=(0, 10))
# pic.plot(scribe=wobbly_scribe, func=lambda x: x ** 2, range_x=(0, 10))

func = lambda x: x**2
sim_scribe = ParallelDrawing([(func, (0, 10)),
                inst])
sim_scribe.execute(canvas)

canvas.save("save.canvas")
canvas.load("save.canvas")
canvas.clear()
time.sleep(1)
canvas.print()