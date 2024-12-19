import re
from dataclasses import dataclass
from collections import defaultdict
import os
from PIL import Image

SAMPLE = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

PATTERN = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int
    width: int
    height: int

    def take_steps(self, step_count):
        self.x = (self.x + self.dx*step_count) % self.width
        self.y = (self.y + self.dy*step_count) % self.height

    @property
    def quadrant(self):
        halfwidth = self.width//2
        halfheight = self.height//2
        right = self.x>halfwidth
        bottom = self.y>halfheight
        left = self.x<halfwidth
        top = self.y<halfheight
        if left and top: return "topleft"
        if right and top: return "topright"
        if left and bottom: return "bottomleft"
        if right and bottom: return "bottomright"
        return None


def main_1(text_input: str, width: int, height) -> int:
    inputs = re.findall(PATTERN,text_input)
    quads = defaultdict(int)
    for entry in inputs:
        x,y,dx,dy = [int(e) for e in entry]
        robot = Robot(x, y, dx, dy, width, height)
        robot.take_steps(100)
        quads[robot.quadrant] += 1
    return quads["topleft"]*quads["topright"]*quads["bottomleft"]*quads["bottomright"]

def main_2(text_input: str, width: int, height) -> int:
    inputs = re.findall(PATTERN,text_input)
    robot_list = []
    for entry in inputs:
        x,y,dx,dy = [int(e) for e in entry]
        robot = Robot(x, y, dx, dy, width, height)
        robot_list.append(robot)
    steps=0
    while steps < 10000:
        canvas = [[0 for i in range(width)] for j in range(height)]
        for robot in robot_list:
            canvas[robot.y][robot.x] = 255
            robot.take_steps(1)
        
        flat = [value for row in canvas for value in row]
        image = Image.new("L",(width,height))
        image.putdata(flat)
        image.save(f"{steps}_day14.png")
        steps += 1

        
        

if __name__ == "__main__":
    
    with open("input14.txt","r") as f: real_input = f.read()
    
    # print(f"{main_1(SAMPLE,11,7) = }")
    # print(f"{main_1(real_input,101,103) = }")

    main_2(real_input,101,103)