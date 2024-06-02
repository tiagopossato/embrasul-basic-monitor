"""
The point group definition element provides a way to logically group a set of points. There are
three reasons to group points:
    • The top-level model organization construct is always a point group. The first element in a
model definition is the top-level point group and includes all the point and point group
definitions in the model.
    • A repeating set of points can be grouped, creating multiple instances of the point group
that can be accessed as an array of point groups.
    • A set of points with synchronous operational requirements can be grouped, indicating
that the points in the group must be read and written atomically.

"""
from . import group_type, Point
from typing import List
import re

class PointGroup():
    def __init__(self,id:str, label:str, description: str, points: List[Point], 
                 gp_type: group_type = group_type.gt_group) -> None:
        """
        Initializes a Group object.

        Parameters:
        - id (str): The ID of the group.
        - label (str): A short label associated with the group.
        - description (str): A brief description of the group.
        - points (List[Point]): List of Point objects associated with the group.
        - gp_type (group_type): The type of the group (default is gt_group).
        """
        # Validate id using regular expression
        if not re.match(r'^[a-zA-Z0-9_]+$', id):
            raise ValueError("Invalid id format. ID must consist of only alphanumeric characters and underscores.")
        
        # Validate label
        if not isinstance(label, str):
            raise TypeError("Label must be a string.")
        
        # Validate description
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        
        # Validate points
        if not isinstance(points, list) or not all(isinstance(p, Point) for p in points):
            raise TypeError("Points must be a list of Point objects.")
        
        # Validate gp_type
        if not isinstance(gp_type, group_type):
            raise TypeError("gp_type must be of type group_type.")
        
        self.__id = id
        self.__label = label
        self.__description = description
        self.__points = points
        self.__gp_type = gp_type
    
    def get_id(self) -> str:
        return self.__id

    def get_label(self) -> str:
        return self.__label

    def get_description(self) -> str:
        return self.__description

    def get_points(self) -> List[Point]:
        return self.__points

    def get_gp_type(self) -> group_type:
        return self.__gp_type
    
    def add_point(self, point: Point) -> None:
        """
        Add a Point object to the list of points associated with the group.

        Parameters:
        - point (Point): The Point object to be added.
        """
        if not isinstance(point, Point):
            raise TypeError("point must be a Point object.")
        
        self.__points.append(point)