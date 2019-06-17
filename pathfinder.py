from PIL import Image
import random

class ElevationMap:

    def __init__ (self, height, width):
        self.height = height
        self.width = width

    def total_lines(self):
        with open("elevation_small.txt") as textFile:
            line_total = 0
            for lines in textFile:
                line_total +=1

        return line_total


    def get_lists(self):
        with open("elevation_small.txt") as textFile:
            coordinate = [line.split() for line in textFile]
        return coordinate
    
    
    def max_coordinate(self):
        """
        Gets the maximum coordinate in a list of numbers.
        """
        max_num = 0;
        with open("elevation_small.txt") as textFile:
            coordinate = [line.split() for line in textFile]

        for y in range(self.height):
            for x in range(self.width):
                if int(coordinate[y][x]) >= max_num:
                    max_num = int(coordinate[y][x])

        
        return max_num

    def min_coordinate(self):
        """
        Get the minimum coordinate in a list of numbers.
        """
        min_num = self.max_coordinate()
        with open("elevation_small.txt") as textFile:
            coordinate = [line.split() for line in textFile]

        for y in range(self.height):
            for x in range(self.width):
                if int(coordinate[y][x]) <= min_num:
                    min_num = int(coordinate[y][x])

        
        return min_num
    
    def draw(self, y_start=300):
        """
        Draws the map. First sets up the image, calculates the difference between the min and max points,
        and determines the appropriate incremenent along the RGB scale to determine the right
        amount of gray to produce.
        """
        pathfinder_map = Image.new('RGBA', (self.width, self.height))
        difference = self.max_coordinate() - self.min_coordinate()
        adjust_color = 255 / difference
        min_value = self.min_coordinate()

        with open("elevation_small.txt") as textFile:
            coordinate = [line.split() for line in textFile]

        """Cycles through each pixel by column, then by row."""
        for y in range(self.height):
            for x in range(self.width):
                value = int(((int(coordinate[y][x]) - min_value) * adjust_color))
                pathfinder_map.putpixel((x, y), (value, value, value))

        return pathfinder_map
        
        
        

    def draw_all_lines(self):
        """
        Draw all lines starting at every y coordinate
        """
        coordinate = self.get_lists()
        pathfinder_map = self.draw()
        best_total = 9999
        best_y = 0
        y_total = 0

        for y in range(self.height):
            
            y_total = 0
            new_y = y
            
            current_step = int((coordinate[new_y][0]))
            x = 1
        
            for x in range(self.width):
                
                coin_flip = False
                flip = 0

                y_above = new_y - 1 
                y_middle = new_y 
                y_below = new_y + 1 

                if y_above < 0:
                    y_above = 0

                if y_below >= self.height:
                    y_below = self.height - 1
                
                step_above = abs(int(coordinate[y_above][x]) - current_step)
                step_middle = abs(int(coordinate[y_middle][x]) - current_step)
                step_below = abs(int(coordinate[y_below][x]) - current_step)

                
                if step_above < step_middle and step_above < step_below:
                    pathfinder_map.putpixel((x, y_above), (0, 0, 255))
                    y_total += step_above
                    new_y = y_above

                elif step_middle < step_above and step_middle < step_below:
                    pathfinder_map.putpixel((x, y_middle), (0, 0, 255))
                    y_total += step_middle
                    new_y = y_middle

                elif step_below < step_above and step_below < step_middle:
                    pathfinder_map.putpixel((x, y_below), (0, 0, 255))
                    y_total += step_below
                    new_y = y_below

                else:

                    while coin_flip == False:
                        
                        flip = random.randint(1,3)

                        if flip == 1 and step_above <= step_middle and step_above <= step_below:
                            pathfinder_map.putpixel((x, y_above), (0, 0, 255))
                            y_total += step_above
                            new_y = y_above
                            coin_flip = True
                        elif flip == 2 and step_middle <= step_above and step_middle <= step_below:
                            pathfinder_map.putpixel((x, y_middle), (0, 0, 255))
                            y_total += step_middle
                            new_y = y_middle
                            coin_flip = True
                        elif flip == 3 and step_below <= step_above and step_below <= step_middle:
                            pathfinder_map.putpixel((x, y_below), (0, 0, 255))
                            y_total += step_below
                            new_y = y_below
                            coin_flip = True



                
                current_step = int((coordinate[new_y][x]))
            
                
                
            if y_total < best_total:
                best_total = y_total
                best_y = y
                


        """
        Draw greedy path
        """
        new_y = best_y
        for x in range(self.width):
            
            y_above = new_y - 1 
            y_middle = new_y 
            y_below = new_y + 1 

            if y_above < 0:
                y_above = 0

            if y_below >= self.height:
                y_below = self.height - 1
            
            step_above = abs(int(coordinate[y_above][x]) - current_step)
            step_middle = abs(int(coordinate[y_middle][x]) - current_step)
            step_below = abs(int(coordinate[y_below][x]) - current_step)

            
            if step_above < step_middle and step_above < step_below:
                pathfinder_map.putpixel((x, y_above), (0, 255, 255))
                new_y = y_above

            elif step_middle < step_above and step_middle < step_below:
                pathfinder_map.putpixel((x, y_middle), (0, 255, 255))
                new_y = y_middle

            elif step_below < step_above and step_below < step_middle:
                pathfinder_map.putpixel((x, y_below), (0, 255, 255))
                new_y = y_below
            
            current_step = int((coordinate[new_y][x]))

        pathfinder_map.save('bob_map.png')


elevation_map = ElevationMap(600,600)
elevation_map.draw_all_lines()