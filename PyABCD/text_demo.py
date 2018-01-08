# text_demo.py
#
# experiment with drawing some text to get the ABCD text_display module to work right

# References:
#
# Psychopy TextStim documentation:
# http://www.psychopy.org/api/visual/textstim.html
#
# Psychopy TextStim example
# http://www.psychopy.org/coder/codeStimuli.html
#
# Windows point size:
# https://msdn.microsoft.com/en-us/library/windows/desktop/ff684173(v=vs.85).aspx
#
# Types of line breaks on Windows, Mac and Linux
# http://texthandler.com/info/remove-line-breaks-python/

from psychopy import visual, core


start_point_size = 18

text_gap_pixels = 10

# TODO: Verify this converstion by comparing images
# TODO: Verify that aliasing matches original E-Prime stimulus
def points_to_pixels(points):
    pixels_per_inch = 96.0
    points_per_inch = 72.0
    size_pixels = points / points_per_inch * pixels_per_inch
    return size_pixels



# Match ABCD text formatting except for the the parameter hight
def make_abcd_text(win, message_txt, height_pix):
    message_stim = visual.TextStim(win,
                                   font="verdana",
                                   color='Black',
                                   units='pix',
                                   alignHoriz='left',
                                   alignVert='top',
                                   height=height_pix,
                                   pos=(-960, 540),
                                   text=message_txt)
    bounds= message_stim.boundingBox
    print("bounds: %s" % str(bounds))
    return message_stim




class PositionedLine:

    def __init__(self, window, text, font_name, font_height_pixels):
        self.window_size = window.size
        self.text = text
        self.font_name = font_name
        self.font_height_pixels = font_height_pixels
        self.x_position = None
        self.y_position = None
        self.text_stim = visual.TextStim(window,
                                         font=self.font_name,
                                         color='Black',
                                         units='pix',
                                         height=font_height_pixels,
                                         text=self.text)

    @property
    def width_pixels(self):
        #return self.text_stim.size[0]
        return self.text_stim.boundingBox[0]


    @property
    def height_pixels(self):
        #return self.text_stim.size[1]
        return self.text_stim.boundingBox[1]


    # def center_x(self):
    #     x= self.window_size[0]
    #     #sz= self.text_stim.size
    #     sz= self.text_stim.boundingBox
    #     y=sz[0]
    #     offset_pixels = (x-y) / 2
    #     #self.x_position = (self.window_size[0] - self.text_stim.size[0]) / 2
    #     self.x_position = offset_pixels

    def offset_y(self, offset_pixels):
        self.y_position = offset_pixels
        #new_offset = self.y_position + self.text_stim.size[1]
        new_offset = self.y_position + self.text_stim.boundingBox[1]
        return new_offset

    def draw(self):
        self.text_stim.pos = (0, self.y_position)
        #self.text_stim.pos = (-500, 0)
        #print(self.text_stim.posPix)
        self.text_stim.draw()
        # foo_text_stim = visual.TextStim(self.text_stim.win,
        #                                  font="verdana",
        #                                  color='Black',
        #                                  units='pix',
        #                                  height=20,
        #                                  text="TEST TEST TEST")
        # foo_text_stim.draw()

    def __str__(self):
        txt = ""
        txt += "text: %s\n" % self.text
        txt += "width: %d\n" % self.width_pixels
        txt += "height: %d\n" % self.height_pixels
        txt += "x_position %d\n" % self.x_position
        txt += "y_position %d\n" % self.y_position
        return txt


class TextBlock:

    def __init__(self, window, text, font_name, font_height_pixels):
        # retain arguments
        self.window = window
        self.text = text
        self.font_name = font_name
        self.font_height_pixels = font_height_pixels
        # init instance variables
        self.positioned_lines = []

    def format(self):
        broken_lines = self.break_lines(self.text)
        # create positioned lines
        self.positioned_lines = [PositionedLine(self.window, line, self.font_name, self.font_height_pixels) for line in broken_lines]
        # for line in broken_lines:
        #     p_line = PositionedLine(self.window, line, self.font_name, self.font_height_pixels)
        #     self.positioned_lines.append(p_line)
        #     p_line.center_x()
        # find the vertical offset of the text block and offset each line accordingly
        block_height_pixels = sum(line.height_pixels for line in self.positioned_lines)
        #y_offset_pixels_temp = self.window.size[1]  - block_height_pixels
        y_offset_pixels_temp = int(-block_height_pixels * 0.5)
        for pline in self.positioned_lines:
            y_offset_pixels_temp = pline.offset_y(y_offset_pixels_temp)

    def draw(self):
        # tell each text line to draw itself at set coordinates
        for pline in self.positioned_lines:
            pline.draw()

    @staticmethod
    def break_lines(txt):
        # Replace any Windows (CRLF) and Mac (CR) style line break with Linux (LF) line breaks.
        norm_out_crlf = txt.replace('\r\n', '\n')         # Windows
        norm_out_cr = norm_out_crlf.replace('\r', '\n')   # Mac
        # Split lines on LF then replace the empty lines "" with a single character for correct Y spacing
        lines = norm_out_cr.split('\n')
        lines_nl_fixed = [line if line !='' else ' ' for line in lines]
        return lines_nl_fixed

    def __str__(self):
        lines_txt = [line.__str__() for line in self.positioned_lines]
        txt= "\n".join(lines_txt)
        return txt


# Open the window and draw the sample text
win = visual.Window(screen=1, fullscr=True, units='pix')
message = "Hello\n\nTree\n\nBanana"
font_size_points = 40
font_size_pixels = points_to_pixels(font_size_points)
block = TextBlock(win, message, "verdana", font_size_pixels)
block.format()
block.draw()
win.flip()
core.wait(5.0)
win.close()


# message = make_abcd_text(win, "Hello\n\nTree\n\nBanana", 50)
# message.draw()
# win.flip()
# core.wait(5.0)
# win.close()


