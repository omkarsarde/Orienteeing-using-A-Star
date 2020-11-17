from PIL import Image, ImageDraw
from queue import PriorityQueue
from math import *


class Season:
    def __init__(self, grid, image_file, output_file, season):
        """
        Initialization
        :param grid: weighted grid
        :param image_file: image file
        :param output_file: output file
        :param season: season
        """
        self.path_color = None
        self.grid = grid
        self.grid.speed_set()
        self.image_file = image_file
        self.output_file = output_file
        self.processed_file = None
        self.season = season
        if season == "spring":
            self.path_color = (86, 54, 0)
        elif season == "winter":
            self.path_color = (178, 255, 255)
        elif season == "fall":
            self.path_color = (0, 255, 255)
        else:
            self.path_color = (255, 0, 255)

    def season_limits(self):
        """
        Finds the changes in original map with respect to given season
        :return: edges of boundaries which needed a change
        """
        if self.season == "summer":
            return
        neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        points_list = []
        season_pixels = []
        season_edges = []
        width = self.grid.width
        height = self.grid.height
        x = 0
        while x < width:
            y = 0
            while y < height:
                points_list.append((x, y))
                if self.season == "spring" or self.season == "winter":
                    if self.grid.pix_copy[x, y] == (0, 0, 255):
                        season_pixels.append((x, y))
                else:
                    if self.grid.pix_copy[x, y] == (255, 255, 255):
                        season_pixels.append((x, y))
                y += 1
            x += 1
        for points in points_list:
            k = 0
            while k < (len(neighbors)):
                xp = points[0] + neighbors[k][0]
                yp = points[1] + neighbors[k][1]
                condition = self.filter_edges_one(points[0], points[1], xp, yp, season_edges)
                if condition:
                    season_edges.append((xp, yp))
                k += 1
        return season_edges

    def filter_edges_one(self, x1, y1, xp, yp, season_edges):
        """
        Basic filter on deciding the bounds of the given two pixels
        :param x1:current node x
        :param y1:current node y
        :param xp:next node x
        :param yp:next node y
        :param season_edges: boundary lise
        :return:
        """
        if self.season == "winter" or self.season == "spring":
            if xp >= 0 and xp < self.grid.width and yp >= 0 and yp < self.grid.height:
                if self.grid.pix_copy[x1, y1] == (0, 0, 255) and self.grid.pix_copy[xp, yp] != (0, 0, 255) and \
                        ((xp, yp) not in season_edges):
                    return True
        elif self.season == "fall":
            if xp >= 0 and xp < self.grid.width and yp >= 0 and yp < self.grid.height:
                if self.grid.pix_copy[x1, y1] == (255, 255, 255) and self.grid.pix_copy[xp, yp] != (255, 255, 255) and \
                        ((xp, yp) not in season_edges):
                    return True

    def speed_setting_season(self):
        """
        Update speeds with respect to created paths
        :return:
        """
        if self.season == "spring":
            self.grid.speed_values[self.path_color] = 4
            self.grid.speed_values[(0, 0, 255)] = 0.1
        elif self.season == "winter":
            self.grid.speed_values[self.path_color] = 3
            self.grid.speed_values[(0, 0, 255)] = 0.1
        elif self.season == "fall":
            self.grid.speed_values[self.path_color] = 6
        elif self.season == "summer":
            pass

    def bfs_season(self, season_edges):
        """
        Generic implementation of a BFS, travers in the list of season edges
        :param season_edges:
        :return: None
        """
        if self.season == "summer":
            return
        pixel_neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        season_boundaries = []
        depth_parameters = None
        if self.season == "spring":
            depth_parameters = 15
        elif self.season == "winter":
            depth_parameters = 7
        elif self.season == "fall":
            depth_parameters = 1
        elif self.season == "summer":
            depth_parameters = 0
        for points in season_edges:
            parent_elevation = float(self.grid.ele_copy[points[0]][points[1]])
            if self.season == "winter":
                if self.grid.pix_copy[points[0], points[1]] == (0, 0, 255):
                    season_boundaries.append((points[0], points[1]))
            queue = []
            explored_set = {}
            queue.append((points[0], points[1]))

            # BFS Implementation
            while len(queue) != 0:
                current_node = queue.pop(0)
                if current_node[0] == points[0] + depth_parameters or \
                        current_node[1] == points[1] + depth_parameters or \
                        current_node[0] == points[0] - depth_parameters or \
                        current_node[1] == points[1] - depth_parameters:
                    break
                if current_node not in explored_set:
                    explored_set[(current_node[0], current_node[1])] = 0
                else:
                    continue
                for k in range(len(pixel_neighbors)):
                    x_value = current_node[0] + pixel_neighbors[k][0]
                    y_value = current_node[1] + pixel_neighbors[k][1]
                    if self.season == "spring":
                        if x_value >= 0 and x_value < self.grid.width and y_value >= 0 and y_value < self.grid.height:
                            if (x_value, y_value) not in queue and (x_value, y_value) not in explored_set:
                                if (not (float(self.grid.ele_copy[x_value][y_value]) - parent_elevation > 1)):
                                    if self.grid.pix_copy[x_value, y_value] != (205, 0, 101):
                                        queue.append((x_value, y_value))
                                    if self.grid.pix_copy[x_value, y_value] != (0, 0, 255):
                                        season_boundaries.append((x_value, y_value))
                    elif self.season == "winter":
                        if x_value >= 0 and x_value < self.grid.width and y_value >= 0 and y_value < self.grid.height:
                            if (x_value, y_value) not in queue and (x_value, y_value) not in explored_set:
                                queue.append((x_value, y_value))
                                if self.grid.pix_copy[x_value, y_value] == (0, 0, 255):
                                    season_boundaries.append((x_value, y_value))
                    elif self.season == "fall":
                        if x_value >= 0 and x_value < self.grid.width and y_value >= 0 and y_value < self.grid.height:
                            if (x_value, y_value) not in queue and (x_value, y_value) not in explored_set:
                                queue.append((x_value, y_value))
                                if self.grid.pix_copy[x_value, y_value] == (248, 148, 18) \
                                        or self.grid.pix_copy[x_value, y_value] == (0, 0, 0):
                                    season_boundaries.append((x_value, y_value))
            while len(queue) != 0:
                current_node = queue.pop(0)
                xc = current_node[0]
                yc = current_node[1]
                if self.season == "spring":
                    if xc >= 0 and xc < self.grid.width and yc >= 0 and yc < self.grid.height:
                        if self.grid.pix_copy[xc, yc] != (0, 0, 255):
                            if (not (float(self.grid.ele_copy[xc][yc]) - parent_elevation >= 1)):
                                season_boundaries.append((xc, yc))
                elif self.season == "winter":
                    if xc >= 0 and xc < self.grid.width and yc >= 0 and yc < self.grid.height:
                        if self.grid.pix_copy[xc, yc] == (0, 0, 255):
                            season_boundaries.append((xc, yc))
                elif self.season == "fall":
                    if xc >= 0 and xc < self.grid.width and yc >= 0 and yc < self.grid.height:
                        if self.grid.pix_copy[xc, yc] == (248, 148, 18) \
                                or self.grid.pix_copy[xc, yc] == (0, 0, 0):
                            season_boundaries.append((xc, yc))
        self.update_map(season_boundaries)
        print("map updated for season")
        print("Entering Astar")

    def update_map(self, boundaries):
        """
        Upadates the map for the required season, also stores a temporary map
        so that I can atleast get some points in this lab
        :param boundaries: boundaries that need to change with the season
        :return: None
        """
        image = Image.open(self.image_file)
        update_pixels = ImageDraw.Draw(image)
        for i in range(len(boundaries) - 1):
            update_pixels.point(boundaries[i], fill=self.path_color)
        if self.season =="winter":
            image.save("temp_winter.png")
        elif self.season =="spring":
            image.save("temp_spring.png")
        else:
            image.save("temp_fall.png")

    def a_star(self, start, final):
        """
        Generic Astar created from the skeleton stubs from
        https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar
        :param start: starting node
        :param final: ending node
        :return: node list containing points on grid required to travel from one goal to another
        """
        self.speed_setting_season()
        cost_so_far = {}
        frontier = PriorityQueue()
        parents = {}
        frontier.put(start, 0)
        cost_so_far[start] = 0
        f_value = {}
        f_value[start] = self.grid.heuristic(start[0], start[1], final[0], final[1])
        final_path_list = []
        while not frontier.empty():
            actual_node = frontier.get()
            final_path_list = []
            if actual_node == final:
                curr = final
                while curr != start:
                    final_path_list.insert(0, curr)
                    curr = parents[curr]
                final_path_list.insert(0, start)
                break
            potential_neighbors = self.grid.neighbors(int(actual_node[0]), int(actual_node[1]))
            for neighbor in potential_neighbors:
                g_value = cost_so_far[actual_node] + self.grid.cost_g(actual_node[0], actual_node[1],
                                                                      neighbor[0],
                                                                      neighbor[1])
                h_value = self.grid.heuristic(neighbor[0], neighbor[1], final[0], final[1])
                if neighbor not in cost_so_far or g_value + h_value < f_value[neighbor]:
                    cost_so_far[neighbor] = g_value
                    f_value[neighbor] = g_value + h_value
                    frontier.put(neighbor, g_value + h_value)
                    parents[neighbor] = actual_node
        print("found path from: " + str(start) + " to: " + str(final))
        return final_path_list

    def total_cost_2D(self, final_list):
        """
        Compute total 2D  distance between the start and end paths
        :param final_list:
        :return:
        """
        total_cost = 0
        for i in range(len(final_list) - 1):
            temp = self.pairwise_distance(final_list[i], final_list[i + 1])
            total_cost = total_cost + temp
        print("Total distance: " + str(total_cost))

    def pairwise_distance(self, start, end):
        """
        distance between two points, 2D
        :param start: start point
        :param end: end point
        :return: distance between them
        """
        x1 = start[0]
        y1 = start[1]
        x2 = end[0]
        y2 = end[1]
        pairwise_dist = sqrt(((x2 - x1) * 10.29) ** 2 + ((y2 - y1) * 7.55) ** 2)
        return pairwise_dist
