from PIL import Image, ImageDraw
from Season import Season
from math import *
import sys




"""
Uses code skeleton stubs from https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar
and http://theory.stanford.edu/~amitp/GameProgramming/ImplementationNotes.html
with a general public usage license
"""

class Grid:
    # grid is completed, need to think bout the cost and pixel
    def __init__(self, width, height, pixel_data, elevation_data, goal_points):
        """
        Initialization of Parameter
        :param width: width of image
        :param height: height of image
        :param pixel_data: pixel data
        :param elevation_data: elevation data
        :param goal_points: points to travel
        """
        self.width = width
        self.height = height
        self.pix_copy = pixel_data
        self.ele_copy = elevation_data
        self.goal_points = goal_points
        self.speed_values = {}

    def speed_set(self):
        """
        Setting speeds over terrain, hardcoded
        :return:
        """
        # Out Bound
        self.speed_values[(205, 0, 101)] = 0.01
        # FootPath
        self.speed_values[(0, 0, 0)] = 15
        # Paved road
        self.speed_values[(71, 51, 3)] = 12
        # lake/swap
        self.speed_values[(0, 0, 255)] = 2
        # vegetation
        self.speed_values[(5, 73, 24)] = 2
        # forest walk
        self.speed_values[(2, 136, 40)] = 4
        # slow Run forest
        self.speed_values[(2, 208, 60)] = 5
        # ez movement forest
        self.speed_values[(255, 255, 255)] = 6.5
        # rough meadow
        self.speed_values[(255, 192, 0)] = 4
        # open land
        self.speed_values[(248, 148, 18)] = 8

    def in_bounds(self, id):
        """
        Checks if a grid point is in the bounds of image
        :param id: x,y coordinates
        :return: True if in bound , else false
        """
        (x, y) = id
        # add condition that pixels[x,y]!=(205,0,101)
        return 0 <= x < self.width and 0 <= y < self.height and self.pix_copy[x, y] != (205, 0, 101)

    def neighbors(self, x1, y1):
        """
        Creates a list of neighbors for current x and y
        :param x1: x coordinate
        :param y1: y coordinate
        :return: list of neighbors
        """
        x = x1
        y = y1
        x_next = x1 + 1
        x_prev = x1 - 1
        y_next = y1 + 1
        y_prev = y1 - 1
        list_of_neighbors = [(x, y_next), (x_next, y), (x_prev, y), (x, y_prev)]
        list_of_neighbors = filter(self.in_bounds, list_of_neighbors)
        return list_of_neighbors


class GridWithWeights(Grid):

    def __init__(self, width, height, pixel_data, elevation_data, goal_points):
        """
        Initialization of a weighted grid
        :param width: width of image
        :param height: height of image
        :param pixel_data: pixel data
        :param elevation_data: elevation data
        :param goal_points: points to visit
        """
        super().__init__(width, height, pixel_data, elevation_data, goal_points)
        self.weights = {}

    def cost_g(self, x1_p, y1_p, x2_n, y2_n):
        """
        Cost of moving from one node to its immediate neighbor
        :param x1_p: previous x
        :param y1_p: previous y
        :param x2_n: neighbor x
        :param y2_n: neighbor y
        :return:
        """
        return 1

    def heuristic(self, x1_p, y1_p, x2_n, y2_n):
        """
        Heuristic function, distance between two nodes in 3D space
        :param x1_p: node x
        :param y1_p: node y
        :param x2_n: next x
        :param y2_n: next y
        :return:
        """
        x1 = int(x1_p)
        y1 = int(y1_p)
        z1 = float(self.ele_copy[x1][y1_p])
        x2 = int(x2_n)
        y2 = int(y2_n)
        z2 = float(self.ele_copy[x2_n][y2_n])
        if (x2 == (x1 + 1) or x2 == (x1 - 1)) and y2 == y1:
            cost = 10.29
        elif (y2 == (y1 + 1) or y2 == (y1 - 1)) and y2 == y1:
            cost = 7.55
        else:
            cost = sqrt(((x2 - x1) * 10.29) ** 2 + ((y2 - y1) * 7.55) ** 2)
            cost = sqrt(cost ** 2 + (z2 - z1) ** 2)
        # change speed
        speed = self.speed_values[self.pix_copy[x1_p, y1_p]]
        time = cost / speed
        return time


class project1:
    def __init__(self, map_image, elevation_file, path_file, season,output_image):
        """
        Initialization of the input parser class
        :param map_image: image file
        :param elevation_file: elevation file
        :param path_file: path file
        :param season: season
        :param output_image: outputimage file
        """
        self.map_image = map_image
        self.path_file = path_file
        self.grid = None
        self.elevation_file = elevation_file
        self.goal_points = []
        self.width = None
        self.height = None
        self.pixel_data = None
        self.elevation_data = []
        self.output_image = output_image
        self.season = season

    def read_goal(self):
        """
        Reads the points needed to traverse
        :return: list of points to travel
        """
        with open(self.path_file) as f:
            for line in f:
                state = line.split()
                self.goal_points.append(state)
        return self.goal_points

    def read_image(self):
        """
        Reads image
        :return: pixel data array
        """
        open_image = Image.open(self.map_image)
        open_image = open_image.convert('RGB')
        self.width, self.height = open_image.size
        self.pixel_data = open_image.load()

    def read_elevation(self):
        """
        Reads and changes dimension of elevation data array
        :return: elevation data array
        """
        with open(self.elevation_file) as f:
            for i in f:
                self.elevation_data.append(i.split())
        self.elevation_data = [[self.elevation_data[i][j] for i in range(len(self.elevation_data))] for j in
                               range(len(self.elevation_data[0]) - 5)]
        return self.elevation_data

    def create_grid(self):
        """
        Creates a weighted Grid and sets the speeds at pixels
        :return: weighted Grid
        """
        self.grid = GridWithWeights(self.width, self.height,
                                    self.pixel_data, self.elevation_data, self.goal_points)
        self.grid.speed_set()

    def create_image(self, map_image,output_image, final_path, color):
        """
        Creates output images from the updated season map
        :param map_image: original image
        :param output_image: output image
        :param final_path: the final path
        :param color: color with which we draw on the map
        :return: output image
        """
        im = Image.open(map_image)
        draw = ImageDraw.Draw(im)
        draw.line(final_path, fill=color, width=1)
        im.show()
        im.save(output_image)


def main():
    image_file = sys.argv[1]
    elevation_file = sys.argv[2]
    path_file = sys.argv[3]
    season = sys.argv[4]
    output_file = sys.argv[5]
    driver_project(image_file,elevation_file,path_file,season,output_file)


def driver_project(image_file,elevation_file,path_file,season,output_file):
    """
    Driver function of the project
    :param image_file: image file
    :param elevation_file: elevation file
    :param path_file: path file
    :param season: season
    :param output_file: outputfile
    :return: None
    """
    drive = project1(image_file,elevation_file,path_file,season,output_file)
    drive.read_goal()
    drive.read_image()
    drive.read_elevation()
    drive.create_grid()
    drive_season = Season(drive.grid,image_file,output_file,season)
    driver_season(drive_season,drive,image_file,output_file)


def driver_season(drive_season,drive,image_file,output_file):
    """
    Driver function for the season class
    :param drive_season: season object
    :param drive: project object
    :param image_file: image file
    :param output_file: output file
    :return:
    """
    created_path = []
    if drive_season.season == "summer":
        print("Entering Astar")
        for i in range(len(drive.goal_points)-1):
            start_point = drive.goal_points[i]
            current_end_point = drive.goal_points[i+1]
            start_point_txt = (int(start_point[0]),int(start_point[1]))
            end_point_txt = (int(current_end_point[0]), int(current_end_point[1]))
            created_path = created_path + drive_season.a_star(start_point_txt,end_point_txt)
        drive.create_image(image_file, output_file,created_path, (255, 0, 0))
        drive_season.total_cost_2D(created_path)
    else:
        boundaries = drive_season.season_limits()
        drive_season.bfs_season(boundaries)
        for i in range(len(drive.goal_points)-1):
            start_point = drive.goal_points[i]
            current_end_point = drive.goal_points[i+1]
            start_point_txt = (int(start_point[0]),int(start_point[1]))
            end_point_txt = (int(current_end_point[0]), int(current_end_point[1]))
            created_path = created_path + drive_season.a_star(start_point_txt,end_point_txt)
        if drive_season.season=="winter":
            drive.create_image("temp_winter.png", output_file, created_path, (255, 0, 0))
            drive_season.total_cost_2D(created_path)
        elif drive_season.season=="spring":
            drive.create_image("temp_spring.png", output_file, created_path, (255, 0, 0))
            drive_season.total_cost_2D(created_path)
        else:
            drive.create_image("temp_fall.png", output_file, created_path, (255, 0, 0))
            drive_season.total_cost_2D(created_path)
    return created_path


if __name__ == "__main__":
    main()

