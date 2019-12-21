''' Experiments for how figure out how to tell whether an object is on the left or right of another one.'''

SIZE = 600
color_mode = HSB
heading = 0
w = PI / 60 / 2

def sign(x):
    if x < 0:
        return -1
    else:
        return 1

def draw_tangents(move_to_avg_heading=True):
    global heading
    
    fill(0)
    rect(0, 0, width, height)
    
    # clock face
    translate(width / 2, height / 2)
    fill(255)
    circle(0, 0, 600 / 2)
    
    # x-axis
    fill(0)
    rect(-width / 2, -1, 600, 2)
    
    # tangent
    rel_x = mouseX - width / 2 + 0.000001
    rel_y = mouseY - height / 2
    length = sqrt(sq(rel_x) + sq(rel_y))
    tangent = atan(rel_y / rel_x)
    stroke(0)
    noFill()
    if tangent < 0:
        start = tangent
        end = 0
    else:
        start = 0
        end = tangent
    arc(0, 0, 30, 30, start, end)
    
    # cursor heading
    stroke(50, 255, 255)
    cursor_heading = tangent
    if rel_x > 0 and tangent < 0:
        # top right
        cursor_heading = tangent + 2 * PI
    elif rel_x < 0:
        # top and bottom left
        cursor_heading = tangent + PI
    arc(0, 0, 50, 50, 0, cursor_heading)
    
    # heading
    stroke(0, 255, 255)
    arc(0, 0, 70, 70, 0, heading)
    
    # difference
    difference = cursor_heading - heading
    stroke(90, 255, 255)
    if difference < 0:
        start = heading + difference
        end = heading
    else:
        start = heading
        end = heading + difference
    arc(0, 0, 90, 90, start, end)
    
    # cropped difference
    stroke(120, 255, 255)
    cropped = difference
    if cropped < -PI:
        cropped += 2*PI
    if cropped > PI:
        cropped -= 2*PI
    if cropped < 0:
        start = heading + cropped
        end = heading
    else:
        start = heading
        end = heading + cropped
    arc(0, 0, 110, 110, start, end)
    noStroke()
    
    # line to cursor
    rotate(tangent)
    fill(50, 255, 255)
    rect(0, -2, length * sign(rel_x), 4)
    rotate(-tangent)
    
    # clock arm
    rotate(heading)
    fill(0, 255, 255)
    rect(0, -2, 600 / 4, 4)
    rotate(-heading)
    
    translate(-width / 2, -height / 2)
    fill(255)
    text('tangent (-PI/2, PI/2): ' + str(tangent), 0, 10)
    fill(0, 255, 255)
    text('heading (0, 2PI): ' + str(heading), 0, 25)
    fill(50, 255, 255)
    text('cursor heading (0, 2PI): ' + str(cursor_heading), 0, 40)
    fill(90, 255, 255)
    text('difference  (-2PI, 2PI): ' + str(difference), 0, 55)
    fill(120, 255, 255)
    text('cropped difference (-PI, PI): ' + str(cropped), 0, 70)
    fill(255)
    direction = 'right'
    if cropped < 0:
        direction = 'left'
    text('direction: ' + direction, 0, 85)
    
    if move_to_avg_heading:
        if direction == 'left':
            heading -= w
        else:
            heading += w
    else:
        heading += w
        if heading > 2 * PI:
            heading -= 2 * PI
