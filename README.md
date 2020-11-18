# Orienteering using A Star
In this project I implement my own version of googlemaps !
<br> Primary aim of this project is to find the shortest route between two points given the constraints of distance, elevations and change in seasons.
<br>
# Approach
The primary terrain is given in the terrain.png file and the elevations are stored in the elevations.txt file.
<br> The seasons can be specified through arguments.
<br> Run the program as
```python
main.py terrain.png elevations.txt path1.txt winter output.png
```
<br> I induce season changes through freezing waters (I live in Rochester duh !), indicated through a cyan color on water body egdes and make them traversible albeit with a slow speed.
<br> In Spring areas near water bodies towards inlands become marshy, reduce speed and are depicted brown. Other changes are made for fall (leaves on ground through yellow) and Summer (No change). 
<br> The pathfinder takes into account all these variables and finds the shortest route given points to traverse and plots a path in red!
 <table>
  <tr>
    <td>Original Terrain</td>
     <td>Winter Terrain</td>
     <td>Spring Terrain</td>
  </tr>
  <tr>
    <td valign="top"><img src="/terrain.png",width="33%"></td>
    <td valign="top"><img src="/winter.png",width="33%"></td>
    <td valign="top"><img src="/spring.png",width="33%"></td>
  </tr>
 </table>
