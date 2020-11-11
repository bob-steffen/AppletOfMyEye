import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
import math

def draw_pixels(figure, x_0, x_1, y_0, y_1):
    figure.add_shape(
                dict(
                    type="line",
                    x0=x_0,
                    y0=y_0,
                    x1=x_1,
                    y1=y_1,
                    line=dict(color="Black", width=1)
                )
            )




#variables for calulations
HEAD_RADIUS = 90 #radius in mm of an average human head
BODY_HEIGHT = 1646 #average human body height in mm



"""Tablet"""

#tablet variables from excel file
tablet_display_height = 60 #in mm
tablet_display_width = 106.7 #in mm
tablet_view_distance = 450 #in mm
tablet_pixel_pitch = (27*(10**-3)) #in mm (so 27um)
tablet_hogel_diameter = 0.07 
tablet_lossless_depth = 0.51 #in mm
tablet_view_angle = 32 #in degrees
tablet_hor_view_angel = math.radians(16) #horizontal view angle in radians
tablet_angular_resolution = 0.06
tablet_hogel_circle_diameter = tablet_view_distance * 0.75  #controls the size of the circle that represents one hogel
tablet_hogel_circle_radius = tablet_hogel_circle_diameter/2
tablet_rad_times_pixpitch = tablet_hogel_circle_diameter * tablet_pixel_pitch #variable for calculating proper pixel pitch proportations
tablet_pixel_radius_ratio = tablet_rad_times_pixpitch / tablet_hogel_diameter #pixel pitch proportional to circle diameter

#tablet graph variables

tablet_head_xpos = -tablet_view_distance
tablet_head_ypos = tablet_display_width/2
tablet_hogel_xpos = tablet_view_distance
tablet_hogel_ypos = tablet_display_width/2
tablet_axis_size = tablet_view_distance * 1.5

#variables drawing the arc that goes in between the viewing angles
y_arc = np.linspace(tablet_view_distance/2*math.tan(-tablet_hor_view_angel) + tablet_display_width/2, \
    tablet_view_distance/2*math.tan(tablet_hor_view_angel) + tablet_display_width/2, endpoint=False) #y_arc is an array that holds the y coordinates for the arc. 100 points 
x_arc = np.zeros(len(y_arc)) #x_arc is an array that holds the x coordinates for the arc
for i in range(0, len(y_arc)):
    x_arc[i] = math.sqrt((tablet_view_distance/2)**2 - (y_arc[i] - tablet_display_width/2)**2)
x_arc_size_half = int(len(x_arc)/2)
y_arc_size_half = int(len(y_arc)/2)
x_arc_mid = x_arc[x_arc_size_half]
y_arc_mid = y_arc[y_arc_size_half]

#making the figures (graph)
tablet_figure_top = go.Figure()
tablet_figure_top.update_layout(title=dict(text='Top View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
tablet_figure_top.update_xaxes(range=[-tablet_axis_size, tablet_axis_size], zeroline=False)
tablet_figure_top.update_yaxes(range=[-tablet_axis_size, tablet_axis_size])


#making the head and hogel circle respectively
tablet_figure_top.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=tablet_head_xpos-HEAD_RADIUS,
            y0=tablet_head_ypos-HEAD_RADIUS,
            x1=tablet_head_xpos+HEAD_RADIUS,
            y1=tablet_head_ypos+HEAD_RADIUS,
            line_color="Black",
            ),

        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=tablet_hogel_xpos-tablet_hogel_circle_radius,
            y0=tablet_hogel_ypos-tablet_hogel_circle_radius,
            x1=tablet_hogel_xpos+tablet_hogel_circle_radius,
            y1=tablet_hogel_ypos+tablet_hogel_circle_radius,
            line_color="Black",
            )
        ]
    )

#making the screen
tablet_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0,
                    x1=0,
                    y1=tablet_display_width,
                    line=dict(color="Black", width=3)
                )
            )

#top viewing angle line
tablet_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=tablet_display_width/2,
                    x1=-tablet_view_distance,
                    y1=tablet_view_distance*math.tan(tablet_hor_view_angel) + tablet_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

#bottom viewing angle line
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=tablet_display_width/2,
                    x1=-tablet_hogel_xpos,
                    y1=tablet_view_distance*math.tan(-tablet_hor_view_angel) + tablet_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

tablet_figure_top.add_trace(go.Scatter(x=-x_arc[1:], y=y_arc[1:], mode='lines')) #the arc between viewing angles
tablet_figure_top.add_trace(go.Scatter(x=[-(x_arc_mid + tablet_view_distance/16)], y=[y_arc_mid], text=["\u03B8"], mode="text")) #the theta next to the arc

#top hogel line
tablet_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*tablet_display_width,
                    x1=tablet_hogel_xpos - tablet_hogel_circle_radius/2,
                    y1=tablet_hogel_ypos + math.sqrt(3) * tablet_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )



#bottom hogel line
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*tablet_display_width,
                    x1=tablet_hogel_xpos - tablet_hogel_circle_radius/2,
                    y1=tablet_hogel_ypos - math.sqrt(3) * tablet_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )

#left line in pixel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y0=tablet_hogel_ypos + tablet_hogel_circle_radius+ (1/16) * tablet_hogel_circle_radius,
                    x1=tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y1=tablet_hogel_ypos + tablet_hogel_circle_radius + (1/8) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line in pixel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=2 * tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y0=tablet_hogel_ypos + tablet_hogel_circle_radius+ (1/16) * tablet_hogel_circle_radius,
                    x1=2 * tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y1=tablet_hogel_ypos + tablet_hogel_circle_radius + (1/8) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting left and right line in pixel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y0=tablet_hogel_ypos + tablet_hogel_circle_radius + (1/8) * tablet_hogel_circle_radius,
                    x1=2 * tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y1=tablet_hogel_ypos + tablet_hogel_circle_radius + (1/8) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of pixel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=1.5 * tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y0=tablet_hogel_ypos + tablet_hogel_circle_radius + (1/8) * tablet_hogel_circle_radius,
                    x1=1.5 * tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius),
                    y1=tablet_hogel_ypos + tablet_hogel_circle_radius + (1/4) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#text for the pixel label
tablet_figure_top.add_trace(go.Scatter(x=[1.5 * tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius)], y=[tablet_hogel_ypos + 1.35 * tablet_hogel_circle_radius], text=["Pixel Pitch"], mode="text"))



#left line sticking out of hogel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_hogel_xpos - tablet_hogel_circle_radius,
                    y0=tablet_hogel_ypos - tablet_hogel_circle_radius,
                    x1=tablet_hogel_xpos - tablet_hogel_circle_radius,
                    y1=tablet_hogel_ypos - tablet_hogel_circle_radius - (1/4) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line sticking out of hogel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_hogel_xpos + tablet_hogel_circle_radius,
                    y0=tablet_hogel_ypos - tablet_hogel_circle_radius,
                    x1=tablet_hogel_xpos + tablet_hogel_circle_radius,
                    y1=tablet_hogel_ypos - tablet_hogel_circle_radius - (1/4) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting the 2 lines of hogel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_hogel_xpos - tablet_hogel_circle_radius,
                    y0=tablet_hogel_ypos - tablet_hogel_circle_radius - (1/4) * tablet_hogel_circle_radius,
                    x1=tablet_hogel_xpos + tablet_hogel_circle_radius,
                    y1=tablet_hogel_ypos - tablet_hogel_circle_radius - (1/4) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of hogel label
tablet_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_hogel_xpos,
                    y0=tablet_hogel_ypos - tablet_hogel_circle_radius - (1/4) * tablet_hogel_circle_radius,
                    x1=tablet_hogel_xpos,
                    y1=tablet_hogel_ypos - tablet_hogel_circle_radius - (1/4) * tablet_hogel_circle_radius - (1/4) * tablet_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )


#text for the hogel label
tablet_figure_top.add_trace(go.Scatter(x=[tablet_hogel_xpos], y=[tablet_hogel_ypos - tablet_hogel_circle_radius - (0.6) * tablet_hogel_circle_radius], text=["Diameter of Hogel"], mode="text")) #the theta next to the arc

tablet_figure_top.update_shapes(dict(xref='x', yref='y'))


#Drawing the lines for represent the pixels in the hogel circle

tablet_num_pixel_lines = int(tablet_hogel_circle_diameter / tablet_pixel_radius_ratio)
tablet_vertical_line_pos = tablet_pixel_radius_ratio + (tablet_hogel_xpos - tablet_hogel_circle_radius) #far left of the circle + one "pixel"
tablet_horizontal_line_pos = tablet_pixel_radius_ratio + (tablet_hogel_ypos - tablet_hogel_circle_radius) #far bottom of the circle + one "pixel"


for i in range(0,tablet_num_pixel_lines):
    tablet_distance_from_center = abs(tablet_hogel_xpos - tablet_vertical_line_pos)
    tablet_curr_line_top = tablet_hogel_ypos + math.sqrt((tablet_hogel_circle_radius)**2 - (tablet_distance_from_center)**2)
    tablet_curr_line_bottom = tablet_hogel_ypos - math.sqrt((tablet_hogel_circle_radius)**2 - (tablet_distance_from_center)**2)
    draw_pixels(tablet_figure_top, tablet_vertical_line_pos, tablet_vertical_line_pos, tablet_curr_line_bottom, tablet_curr_line_top)
    tablet_vertical_line_pos = tablet_vertical_line_pos + tablet_pixel_radius_ratio

for i in range(0,tablet_num_pixel_lines):
    tablet_distance_from_center = abs(tablet_hogel_ypos - tablet_horizontal_line_pos)
    tablet_curr_line_right = tablet_hogel_xpos + math.sqrt((tablet_hogel_circle_radius)**2 - (tablet_distance_from_center)**2)
    tablet_curr_line_left = tablet_hogel_xpos - math.sqrt((tablet_hogel_circle_radius)**2 - (tablet_distance_from_center)**2)
    draw_pixels(tablet_figure_top, tablet_curr_line_left, tablet_curr_line_right, tablet_horizontal_line_pos, tablet_horizontal_line_pos)
    tablet_horizontal_line_pos = tablet_horizontal_line_pos + tablet_pixel_radius_ratio




"""Tablet Side View"""

tablet_figure_side = go.Figure()
tablet_figure_side.update_layout(title=dict(text='Side View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
tablet_figure_side.update_xaxes(range=[-tablet_axis_size, tablet_axis_size], zeroline=False)
tablet_figure_side.update_yaxes(range=[-tablet_axis_size, tablet_axis_size])

#drawing the head
tablet_figure_side.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=tablet_head_xpos-HEAD_RADIUS,
            y0=tablet_head_ypos-HEAD_RADIUS,
            x1=tablet_head_xpos+HEAD_RADIUS,
            y1=tablet_head_ypos+HEAD_RADIUS,
            line_color="Black",
            )
        ]
    )

#drawing the body line
tablet_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_head_xpos,
                    y0=tablet_head_ypos - HEAD_RADIUS,
                    x1=tablet_head_xpos,
                    y1=tablet_head_ypos - HEAD_RADIUS - BODY_HEIGHT,
                    line=dict(color="Black", width=1)
                )
            )

#drawing the display line
tablet_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=-tablet_display_height/2,
                    x1=0,
                    y1=tablet_display_height/2,
                    line=dict(color="Black", width=3)
                )
            )

#Drawing view distance representation

tablet_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=tablet_head_xpos,
                    y0=tablet_display_height/2 + 1.25 * HEAD_RADIUS,
                    x1=tablet_head_xpos,
                    y1=tablet_display_height/2 + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tablet_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=tablet_display_height/2 + 1.25 * HEAD_RADIUS,
                    x1=0,
                    y1=tablet_display_height/2 + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tablet_figure_side.add_shape(
                dict(
                    type="line",
                    x0=tablet_head_xpos,
                    y0=tablet_display_height/2 + 1.5 * HEAD_RADIUS,
                    x1=0,
                    y1=tablet_display_height/2 + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tablet_figure_side.add_shape(
                dict(
                    type="line",
                    x0=tablet_head_xpos/2,
                    y0=tablet_display_height/2 + 1.5 * HEAD_RADIUS,
                    x1=tablet_head_xpos/2,
                    y1=tablet_display_height/2 + 1.75 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tablet_figure_side.add_trace(go.Scatter(x=[tablet_head_xpos/2], y=[tablet_display_height/2 + 2 * HEAD_RADIUS], text=["View Distance"], mode="text")) #the theta next to the arc





"""Desktop"""

#desktop variables from excel file
desktop_display_height = 330 #in mm
desktop_display_width = 586.7 #in mm
desktop_view_distance = 800 #in mm
desktop_pixel_pitch = (19*(10**-3)) #in mm (so 27um)
desktop_hogel_diameter = 0.23 
desktop_lossless_depth = 5.70 #in mm
desktop_view_angle = 57.2 #in degrees
desktop_hor_view_angel = math.radians(28.62) #horizontal view angle in radians
desktop_angular_resolution = 0.21
desktop_hogel_circle_diameter = desktop_view_distance * 0.75  #controls the size of the circle that represents one hogel
desktop_hogel_circle_radius = desktop_hogel_circle_diameter/2
desktop_rad_times_pixpitch = desktop_hogel_circle_diameter * desktop_pixel_pitch #variable for calculating proper pixel pitch proportations
desktop_pixel_radius_ratio = desktop_rad_times_pixpitch / desktop_hogel_diameter #pixel pitch proportional to circle diameter

#desktop graph variables

desktop_head_xpos = -desktop_view_distance
desktop_head_ypos = desktop_display_width/2
desktop_hogel_xpos = desktop_view_distance
desktop_hogel_ypos = desktop_display_width/2
desktop_axis_size = desktop_view_distance * 1.5

#variables drawing the arc that goes in between the viewing angles
y_arc = np.linspace(desktop_view_distance/2*math.tan(-desktop_hor_view_angel) + desktop_display_width/2, \
    desktop_view_distance/2*math.tan(desktop_hor_view_angel) + desktop_display_width/2, endpoint=False) #y_arc is an array that holds the y coordinates for the arc. 100 points 
x_arc = np.zeros(len(y_arc)) #x_arc is an array that holds the x coordinates for the arc
for i in range(0, len(y_arc)):
    x_arc[i] = math.sqrt((desktop_view_distance/2)**2 - (y_arc[i] - desktop_display_width/2)**2)
x_arc_size_half = int(len(x_arc)/2)
y_arc_size_half = int(len(y_arc)/2)
x_arc_mid = x_arc[x_arc_size_half]
y_arc_mid = y_arc[y_arc_size_half]

#making the figures (graph)
desktop_figure_top = go.Figure()
desktop_figure_top.update_layout(title=dict(text='Top View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
desktop_figure_top.update_xaxes(range=[-desktop_axis_size, desktop_axis_size], zeroline=False)
desktop_figure_top.update_yaxes(range=[-desktop_axis_size, desktop_axis_size])


#making the head and hogel circle respectively
desktop_figure_top.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=desktop_head_xpos-HEAD_RADIUS,
            y0=desktop_head_ypos-HEAD_RADIUS,
            x1=desktop_head_xpos+HEAD_RADIUS,
            y1=desktop_head_ypos+HEAD_RADIUS,
            line_color="Black",
            ),

        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=desktop_hogel_xpos-desktop_hogel_circle_radius,
            y0=desktop_hogel_ypos-desktop_hogel_circle_radius,
            x1=desktop_hogel_xpos+desktop_hogel_circle_radius,
            y1=desktop_hogel_ypos+desktop_hogel_circle_radius,
            line_color="Black",
            )
        ]
    )

#making the screen
desktop_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0,
                    x1=0,
                    y1=desktop_display_width,
                    line=dict(color="Black", width=3)
                )
            )

#top viewing angle line
desktop_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=desktop_display_width/2,
                    x1=-desktop_view_distance,
                    y1=desktop_view_distance*math.tan(desktop_hor_view_angel) + desktop_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

#bottom viewing angle line
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=desktop_display_width/2,
                    x1=-desktop_hogel_xpos,
                    y1=desktop_view_distance*math.tan(-desktop_hor_view_angel) + desktop_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

desktop_figure_top.add_trace(go.Scatter(x=-x_arc[1:], y=y_arc[1:], mode='lines')) #the arc between viewing angles
desktop_figure_top.add_trace(go.Scatter(x=[-(x_arc_mid + desktop_view_distance/16)], y=[y_arc_mid], text=["\u03B8"], mode="text")) #the theta next to the arc

#top hogel line
desktop_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*desktop_display_width,
                    x1=desktop_hogel_xpos - desktop_hogel_circle_radius/2,
                    y1=desktop_hogel_ypos + math.sqrt(3) * desktop_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )



#bottom hogel line
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*desktop_display_width,
                    x1=desktop_hogel_xpos - desktop_hogel_circle_radius/2,
                    y1=desktop_hogel_ypos - math.sqrt(3) * desktop_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )

#left line in pixel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y0=desktop_hogel_ypos + desktop_hogel_circle_radius+ (1/16) * desktop_hogel_circle_radius,
                    x1=desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y1=desktop_hogel_ypos + desktop_hogel_circle_radius + (1/8) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line in pixel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=2 * desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y0=desktop_hogel_ypos + desktop_hogel_circle_radius+ (1/16) * desktop_hogel_circle_radius,
                    x1=2 * desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y1=desktop_hogel_ypos + desktop_hogel_circle_radius + (1/8) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting left and right line in pixel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y0=desktop_hogel_ypos + desktop_hogel_circle_radius + (1/8) * desktop_hogel_circle_radius,
                    x1=2 * desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y1=desktop_hogel_ypos + desktop_hogel_circle_radius + (1/8) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of pixel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=1.5 * desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y0=desktop_hogel_ypos + desktop_hogel_circle_radius + (1/8) * desktop_hogel_circle_radius,
                    x1=1.5 * desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius),
                    y1=desktop_hogel_ypos + desktop_hogel_circle_radius + (1/4) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#text for the pixel label
desktop_figure_top.add_trace(go.Scatter(x=[1.5 * desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius)], y=[desktop_hogel_ypos + 1.35 * desktop_hogel_circle_radius], text=["Pixel Pitch"], mode="text"))



#left line sticking out of hogel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_hogel_xpos - desktop_hogel_circle_radius,
                    y0=desktop_hogel_ypos - desktop_hogel_circle_radius,
                    x1=desktop_hogel_xpos - desktop_hogel_circle_radius,
                    y1=desktop_hogel_ypos - desktop_hogel_circle_radius - (1/4) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line sticking out of hogel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_hogel_xpos + desktop_hogel_circle_radius,
                    y0=desktop_hogel_ypos - desktop_hogel_circle_radius,
                    x1=desktop_hogel_xpos + desktop_hogel_circle_radius,
                    y1=desktop_hogel_ypos - desktop_hogel_circle_radius - (1/4) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting the 2 lines of hogel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_hogel_xpos - desktop_hogel_circle_radius,
                    y0=desktop_hogel_ypos - desktop_hogel_circle_radius - (1/4) * desktop_hogel_circle_radius,
                    x1=desktop_hogel_xpos + desktop_hogel_circle_radius,
                    y1=desktop_hogel_ypos - desktop_hogel_circle_radius - (1/4) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of hogel label
desktop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_hogel_xpos,
                    y0=desktop_hogel_ypos - desktop_hogel_circle_radius - (1/4) * desktop_hogel_circle_radius,
                    x1=desktop_hogel_xpos,
                    y1=desktop_hogel_ypos - desktop_hogel_circle_radius - (1/4) * desktop_hogel_circle_radius - (1/4) * desktop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )


#text for the hogel label
desktop_figure_top.add_trace(go.Scatter(x=[desktop_hogel_xpos], y=[desktop_hogel_ypos - desktop_hogel_circle_radius - (0.6) * desktop_hogel_circle_radius], text=["Diameter of Hogel"], mode="text")) #the theta next to the arc

desktop_figure_top.update_shapes(dict(xref='x', yref='y'))


#Drawing the lines for represent the pixels in the hogel circle

desktop_num_pixel_lines = int(desktop_hogel_circle_diameter / desktop_pixel_radius_ratio)
desktop_vertical_line_pos = desktop_pixel_radius_ratio + (desktop_hogel_xpos - desktop_hogel_circle_radius) #far left of the circle + one "pixel"
desktop_horizontal_line_pos = desktop_pixel_radius_ratio + (desktop_hogel_ypos - desktop_hogel_circle_radius) #far bottom of the circle + one "pixel"


for i in range(0,desktop_num_pixel_lines):
    desktop_distance_from_center = abs(desktop_hogel_xpos - desktop_vertical_line_pos)
    desktop_curr_line_top = desktop_hogel_ypos + math.sqrt((desktop_hogel_circle_radius)**2 - (desktop_distance_from_center)**2)
    desktop_curr_line_bottom = desktop_hogel_ypos - math.sqrt((desktop_hogel_circle_radius)**2 - (desktop_distance_from_center)**2)
    draw_pixels(desktop_figure_top, desktop_vertical_line_pos, desktop_vertical_line_pos, desktop_curr_line_bottom, desktop_curr_line_top)
    desktop_vertical_line_pos = desktop_vertical_line_pos + desktop_pixel_radius_ratio

for i in range(0,desktop_num_pixel_lines):
    desktop_distance_from_center = abs(desktop_hogel_ypos - desktop_horizontal_line_pos)
    desktop_curr_line_right = desktop_hogel_xpos + math.sqrt((desktop_hogel_circle_radius)**2 - (desktop_distance_from_center)**2)
    desktop_curr_line_left = desktop_hogel_xpos - math.sqrt((desktop_hogel_circle_radius)**2 - (desktop_distance_from_center)**2)
    draw_pixels(desktop_figure_top, desktop_curr_line_left, desktop_curr_line_right, desktop_horizontal_line_pos, desktop_horizontal_line_pos)
    desktop_horizontal_line_pos = desktop_horizontal_line_pos + desktop_pixel_radius_ratio




"""desktop Side View"""

desktop_figure_side = go.Figure()
desktop_figure_side.update_layout(title=dict(text='Side View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
desktop_figure_side.update_xaxes(range=[-desktop_axis_size, desktop_axis_size], zeroline=False)
desktop_figure_side.update_yaxes(range=[-desktop_axis_size, desktop_axis_size])

#drawing the head
desktop_figure_side.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=desktop_head_xpos-HEAD_RADIUS,
            y0=desktop_head_ypos-HEAD_RADIUS,
            x1=desktop_head_xpos+HEAD_RADIUS,
            y1=desktop_head_ypos+HEAD_RADIUS,
            line_color="Black",
            )
        ]
    )

#drawing the body line
desktop_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_head_xpos,
                    y0=desktop_head_ypos - HEAD_RADIUS,
                    x1=desktop_head_xpos,
                    y1=desktop_head_ypos - HEAD_RADIUS - BODY_HEIGHT,
                    line=dict(color="Black", width=1)
                )
            )

#drawing the display line
desktop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=-desktop_display_height/2,
                    x1=0,
                    y1=desktop_display_height/2,
                    line=dict(color="Black", width=3)
                )
            )

#Drawing view distance representation

desktop_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=desktop_head_xpos,
                    y0=desktop_head_ypos + 1.25 * HEAD_RADIUS,
                    x1=desktop_head_xpos,
                    y1=desktop_head_ypos + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

desktop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=desktop_head_ypos + 1.25 * HEAD_RADIUS,
                    x1=0,
                    y1=desktop_head_ypos + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

desktop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=desktop_head_xpos,
                    y0=desktop_head_ypos + 1.5 * HEAD_RADIUS,
                    x1=0,
                    y1=desktop_head_ypos + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

desktop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=desktop_head_xpos/2,
                    y0=desktop_head_ypos + 1.5 * HEAD_RADIUS,
                    x1=desktop_head_xpos/2,
                    y1=desktop_head_ypos + 1.75 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

desktop_figure_side.add_trace(go.Scatter(x=[desktop_head_xpos/2], y=[desktop_display_height/2 + 2 * HEAD_RADIUS], text=["View Distance"], mode="text")) #the theta next to the arc




"""Table Top"""

#tabletop variables from excel file
tabletop_display_height = "N/A" #in mm
tabletop_display_width = "N/A" #in mm
tabletop_view_distance = "N/A" #in mm
tabletop_pixel_pitch = (50*(10**-3)) #in mm (so 27um)
tabletop_hogel_diameter = 0.5 
tabletop_lossless_depth = 6.4 #in mm
tabletop_view_angle = 90 #in degrees
tabletop_hor_view_angel = "N/A" #horizontal view angle in radians
tabletop_angular_resolution = 0.111
"""
tabletop_hogel_circle_diameter = tabletop_view_distance * 0.75  #controls the size of the circle that represents one hogel
tabletop_hogel_circle_radius = tabletop_hogel_circle_diameter/2
tabletop_rad_times_pixpitch = tabletop_hogel_circle_diameter * tabletop_pixel_pitch #variable for calculating proper pixel pitch proportations
tabletop_pixel_radius_ratio = tabletop_rad_times_pixpitch / tabletop_hogel_diameter #pixel pitch proportional to circle diameter

#tabletop graph variables

tabletop_head_xpos = -tabletop_view_distance
tabletop_head_ypos = tabletop_display_width/2
tabletop_hogel_xpos = tabletop_view_distance
tabletop_hogel_ypos = tabletop_display_width/2
tabletop_axis_size = tabletop_view_distance * 1.5

#variables drawing the arc that goes in between the viewing angles
y_arc = np.linspace(tabletop_view_distance/2*math.tan(-tabletop_hor_view_angel) + tabletop_display_width/2, \
    tabletop_view_distance/2*math.tan(tabletop_hor_view_angel) + tabletop_display_width/2, endpoint=False) #y_arc is an array that holds the y coordinates for the arc. 100 points 
x_arc = np.zeros(len(y_arc)) #x_arc is an array that holds the x coordinates for the arc
for i in range(0, len(y_arc)):
    x_arc[i] = math.sqrt((tabletop_view_distance/2)**2 - (y_arc[i] - tabletop_display_width/2)**2)
x_arc_size_half = int(len(x_arc)/2)
y_arc_size_half = int(len(y_arc)/2)
x_arc_mid = x_arc[x_arc_size_half]
y_arc_mid = y_arc[y_arc_size_half]
"""
#making the figures (graph)
tabletop_figure_top = go.Figure()

tabletop_figure_top.update_layout(title=dict(text='Coming Soon!', x=1, font=dict(color="red", size=48)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph

tabletop_figure_top.update_xaxes(range=[0, 0], zeroline=False)
tabletop_figure_top.update_yaxes(range=[0, 0])

"""
#making the head and hogel circle respectively
tabletop_figure_top.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=tabletop_head_xpos-HEAD_RADIUS,
            y0=tabletop_head_ypos-HEAD_RADIUS,
            x1=tabletop_head_xpos+HEAD_RADIUS,
            y1=tabletop_head_ypos+HEAD_RADIUS,
            line_color="Black",
            ),

        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=tabletop_hogel_xpos-tabletop_hogel_circle_radius,
            y0=tabletop_hogel_ypos-tabletop_hogel_circle_radius,
            x1=tabletop_hogel_xpos+tabletop_hogel_circle_radius,
            y1=tabletop_hogel_ypos+tabletop_hogel_circle_radius,
            line_color="Black",
            )
        ]
    )

#making the screen
tabletop_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0,
                    x1=0,
                    y1=tabletop_display_width,
                    line=dict(color="Black", width=3)
                )
            )

#top viewing angle line
tabletop_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=tabletop_display_width/2,
                    x1=-tabletop_view_distance,
                    y1=tabletop_view_distance*math.tan(tabletop_hor_view_angel) + tabletop_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

#bottom viewing angle line
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=tabletop_display_width/2,
                    x1=-tabletop_hogel_xpos,
                    y1=tabletop_view_distance*math.tan(-tabletop_hor_view_angel) + tabletop_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

tabletop_figure_top.add_trace(go.Scatter(x=-x_arc[1:], y=y_arc[1:], mode='lines')) #the arc between viewing angles
tabletop_figure_top.add_trace(go.Scatter(x=[-(x_arc_mid + tabletop_view_distance/16)], y=[y_arc_mid], text=["\u03B8"], mode="text")) #the theta next to the arc

#top hogel line
tabletop_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*tabletop_display_width,
                    x1=tabletop_hogel_xpos - tabletop_hogel_circle_radius/2,
                    y1=tabletop_hogel_ypos + math.sqrt(3) * tabletop_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )



#bottom hogel line
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*tabletop_display_width,
                    x1=tabletop_hogel_xpos - tabletop_hogel_circle_radius/2,
                    y1=tabletop_hogel_ypos - math.sqrt(3) * tabletop_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )

#left line in pixel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y0=tabletop_hogel_ypos + tabletop_hogel_circle_radius+ (1/16) * tabletop_hogel_circle_radius,
                    x1=tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y1=tabletop_hogel_ypos + tabletop_hogel_circle_radius + (1/8) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line in pixel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=2 * tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y0=tabletop_hogel_ypos + tabletop_hogel_circle_radius+ (1/16) * tabletop_hogel_circle_radius,
                    x1=2 * tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y1=tabletop_hogel_ypos + tabletop_hogel_circle_radius + (1/8) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting left and right line in pixel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y0=tabletop_hogel_ypos + tabletop_hogel_circle_radius + (1/8) * tabletop_hogel_circle_radius,
                    x1=2 * tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y1=tabletop_hogel_ypos + tabletop_hogel_circle_radius + (1/8) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of pixel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=1.5 * tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y0=tabletop_hogel_ypos + tabletop_hogel_circle_radius + (1/8) * tabletop_hogel_circle_radius,
                    x1=1.5 * tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius),
                    y1=tabletop_hogel_ypos + tabletop_hogel_circle_radius + (1/4) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#text for the pixel label
tabletop_figure_top.add_trace(go.Scatter(x=[1.5 * tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius)], y=[tabletop_hogel_ypos + 1.35 * tabletop_hogel_circle_radius], text=["Pixel Pitch"], mode="text"))



#left line sticking out of hogel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_hogel_xpos - tabletop_hogel_circle_radius,
                    y0=tabletop_hogel_ypos - tabletop_hogel_circle_radius,
                    x1=tabletop_hogel_xpos - tabletop_hogel_circle_radius,
                    y1=tabletop_hogel_ypos - tabletop_hogel_circle_radius - (1/4) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line sticking out of hogel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_hogel_xpos + tabletop_hogel_circle_radius,
                    y0=tabletop_hogel_ypos - tabletop_hogel_circle_radius,
                    x1=tabletop_hogel_xpos + tabletop_hogel_circle_radius,
                    y1=tabletop_hogel_ypos - tabletop_hogel_circle_radius - (1/4) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting the 2 lines of hogel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_hogel_xpos - tabletop_hogel_circle_radius,
                    y0=tabletop_hogel_ypos - tabletop_hogel_circle_radius - (1/4) * tabletop_hogel_circle_radius,
                    x1=tabletop_hogel_xpos + tabletop_hogel_circle_radius,
                    y1=tabletop_hogel_ypos - tabletop_hogel_circle_radius - (1/4) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of hogel label
tabletop_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_hogel_xpos,
                    y0=tabletop_hogel_ypos - tabletop_hogel_circle_radius - (1/4) * tabletop_hogel_circle_radius,
                    x1=tabletop_hogel_xpos,
                    y1=tabletop_hogel_ypos - tabletop_hogel_circle_radius - (1/4) * tabletop_hogel_circle_radius - (1/4) * tabletop_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )


#text for the hogel label
tabletop_figure_top.add_trace(go.Scatter(x=[tabletop_hogel_xpos], y=[tabletop_hogel_ypos - tabletop_hogel_circle_radius - (0.6) * tabletop_hogel_circle_radius], text=["Diameter of Hogel"], mode="text")) #the theta next to the arc

tabletop_figure_top.update_shapes(dict(xref='x', yref='y'))


#Drawing the lines for represent the pixels in the hogel circle

tabletop_num_pixel_lines = int(tabletop_hogel_circle_diameter / tabletop_pixel_radius_ratio)
tabletop_vertical_line_pos = tabletop_pixel_radius_ratio + (tabletop_hogel_xpos - tabletop_hogel_circle_radius) #far left of the circle + one "pixel"
tabletop_horizontal_line_pos = tabletop_pixel_radius_ratio + (tabletop_hogel_ypos - tabletop_hogel_circle_radius) #far bottom of the circle + one "pixel"


for i in range(0,tabletop_num_pixel_lines):
    tabletop_distance_from_center = abs(tabletop_hogel_xpos - tabletop_vertical_line_pos)
    tabletop_curr_line_top = tabletop_hogel_ypos + math.sqrt((tabletop_hogel_circle_radius)**2 - (tabletop_distance_from_center)**2)
    tabletop_curr_line_bottom = tabletop_hogel_ypos - math.sqrt((tabletop_hogel_circle_radius)**2 - (tabletop_distance_from_center)**2)
    draw_pixels(tabletop_figure_top, tabletop_vertical_line_pos, tabletop_vertical_line_pos, tabletop_curr_line_bottom, tabletop_curr_line_top)
    tabletop_vertical_line_pos = tabletop_vertical_line_pos + tabletop_pixel_radius_ratio

for i in range(0,tabletop_num_pixel_lines):
    tabletop_distance_from_center = abs(tabletop_hogel_ypos - tabletop_horizontal_line_pos)
    tabletop_curr_line_right = tabletop_hogel_xpos + math.sqrt((tabletop_hogel_circle_radius)**2 - (tabletop_distance_from_center)**2)
    tabletop_curr_line_left = tabletop_hogel_xpos - math.sqrt((tabletop_hogel_circle_radius)**2 - (tabletop_distance_from_center)**2)
    draw_pixels(tabletop_figure_top, tabletop_curr_line_left, tabletop_curr_line_right, tabletop_horizontal_line_pos, tabletop_horizontal_line_pos)
    tabletop_horizontal_line_pos = tabletop_horizontal_line_pos + tabletop_pixel_radius_ratio



"""
"""tabletop Side View"""


tabletop_figure_side = go.Figure()


tabletop_figure_side.update_layout(title=dict(text='', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
tabletop_figure_side.update_xaxes(range=[0, 0], zeroline=False)
tabletop_figure_side.update_yaxes(range=[0, 0])
"""
#drawing the head
tabletop_figure_side.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=tabletop_head_xpos-HEAD_RADIUS,
            y0=tabletop_head_ypos-HEAD_RADIUS,
            x1=tabletop_head_xpos+HEAD_RADIUS,
            y1=tabletop_head_ypos+HEAD_RADIUS,
            line_color="Black",
            )
        ]
    )

#drawing the body line
tabletop_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_head_xpos,
                    y0=tabletop_head_ypos - HEAD_RADIUS,
                    x1=tabletop_head_xpos,
                    y1=tabletop_head_ypos - HEAD_RADIUS - BODY_HEIGHT,
                    line=dict(color="Black", width=1)
                )
            )

#drawing the display line
tabletop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=-tabletop_display_height/2,
                    x1=0,
                    y1=tabletop_display_height/2,
                    line=dict(color="Black", width=3)
                )
            )

#Drawing view distance representation

tabletop_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=tabletop_head_xpos,
                    y0=tabletop_display_height/2 + 1.25 * HEAD_RADIUS,
                    x1=tabletop_head_xpos,
                    y1=tabletop_display_height/2 + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tabletop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=tabletop_display_height/2 + 1.25 * HEAD_RADIUS,
                    x1=0,
                    y1=tabletop_display_height/2 + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tabletop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=tabletop_head_xpos,
                    y0=tabletop_display_height/2 + 1.5 * HEAD_RADIUS,
                    x1=0,
                    y1=tabletop_display_height/2 + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tabletop_figure_side.add_shape(
                dict(
                    type="line",
                    x0=tabletop_head_xpos/2,
                    y0=tabletop_display_height/2 + 1.5 * HEAD_RADIUS,
                    x1=tabletop_head_xpos/2,
                    y1=tabletop_display_height/2 + 1.75 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

tabletop_figure_side.add_trace(go.Scatter(x=[tabletop_head_xpos/2], y=[tabletop_display_height/2 + 2 * HEAD_RADIUS], text=["View Distance"], mode="text")) #the theta next to the arc

"""

"""Home Cinema"""

#homecinema variables from excel file
homecinema_display_height = 810 #in mm
homecinema_display_width = 1440 #in mm
homecinema_view_distance = 2743.2   #in mm
homecinema_pixel_pitch = (47*(10**-3)) #in mm (so 27um)
homecinema_hogel_diameter = 0.8 
homecinema_lossless_depth = 25.06 #in mm
homecinema_view_angle = 61.9 #in degrees
homecinema_hor_view_angel = math.radians(30.97) #horizontal view angle in radians
homecinema_angular_resolution = 0.27
homecinema_hogel_circle_diameter = homecinema_view_distance * 0.75  #controls the size of the circle that represents one hogel
homecinema_hogel_circle_radius = homecinema_hogel_circle_diameter/2
homecinema_rad_times_pixpitch = homecinema_hogel_circle_diameter * homecinema_pixel_pitch #variable for calculating proper pixel pitch proportations
homecinema_pixel_radius_ratio = homecinema_rad_times_pixpitch / homecinema_hogel_diameter #pixel pitch proportional to circle diameter

#homecinema graph variables

homecinema_head_xpos = -homecinema_view_distance
homecinema_head_ypos = homecinema_display_width/2
homecinema_hogel_xpos = homecinema_view_distance
homecinema_hogel_ypos = homecinema_display_width/2
homecinema_axis_size = homecinema_view_distance * 1.5

#variables drawing the arc that goes in between the viewing angles
y_arc = np.linspace(homecinema_view_distance/2*math.tan(-homecinema_hor_view_angel) + homecinema_display_width/2, \
    homecinema_view_distance/2*math.tan(homecinema_hor_view_angel) + homecinema_display_width/2, endpoint=False) #y_arc is an array that holds the y coordinates for the arc. 100 points 
x_arc = np.zeros(len(y_arc)) #x_arc is an array that holds the x coordinates for the arc
for i in range(0, len(y_arc)):
    x_arc[i] = math.sqrt((homecinema_view_distance/2)**2 - (y_arc[i] - homecinema_display_width/2)**2)
x_arc_size_half = int(len(x_arc)/2)
y_arc_size_half = int(len(y_arc)/2)
x_arc_mid = x_arc[x_arc_size_half]
y_arc_mid = y_arc[y_arc_size_half]

#making the figures (graph)
homecinema_figure_top = go.Figure()
homecinema_figure_top.update_layout(title=dict(text='Top View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
homecinema_figure_top.update_xaxes(range=[-homecinema_axis_size, homecinema_axis_size], zeroline=False)
homecinema_figure_top.update_yaxes(range=[-homecinema_axis_size, homecinema_axis_size])


#making the head and hogel circle respectively
homecinema_figure_top.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=homecinema_head_xpos-HEAD_RADIUS,
            y0=homecinema_head_ypos-HEAD_RADIUS,
            x1=homecinema_head_xpos+HEAD_RADIUS,
            y1=homecinema_head_ypos+HEAD_RADIUS,
            line_color="Black",
            ),

        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=homecinema_hogel_xpos-homecinema_hogel_circle_radius,
            y0=homecinema_hogel_ypos-homecinema_hogel_circle_radius,
            x1=homecinema_hogel_xpos+homecinema_hogel_circle_radius,
            y1=homecinema_hogel_ypos+homecinema_hogel_circle_radius,
            line_color="Black",
            )
        ]
    )

#making the screen
homecinema_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0,
                    x1=0,
                    y1=homecinema_display_width,
                    line=dict(color="Black", width=3)
                )
            )

#top viewing angle line
homecinema_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=homecinema_display_width/2,
                    x1=-homecinema_view_distance,
                    y1=homecinema_view_distance*math.tan(homecinema_hor_view_angel) + homecinema_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

#bottom viewing angle line
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=homecinema_display_width/2,
                    x1=-homecinema_hogel_xpos,
                    y1=homecinema_view_distance*math.tan(-homecinema_hor_view_angel) + homecinema_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

homecinema_figure_top.add_trace(go.Scatter(x=-x_arc[1:], y=y_arc[1:], mode='lines')) #the arc between viewing angles
homecinema_figure_top.add_trace(go.Scatter(x=[-(x_arc_mid + homecinema_view_distance/16)], y=[y_arc_mid], text=["\u03B8"], mode="text")) #the theta next to the arc

#top hogel line
homecinema_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*homecinema_display_width,
                    x1=homecinema_hogel_xpos - homecinema_hogel_circle_radius/2,
                    y1=homecinema_hogel_ypos + math.sqrt(3) * homecinema_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )



#bottom hogel line
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*homecinema_display_width,
                    x1=homecinema_hogel_xpos - homecinema_hogel_circle_radius/2,
                    y1=homecinema_hogel_ypos - math.sqrt(3) * homecinema_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )

#left line in pixel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y0=homecinema_hogel_ypos + homecinema_hogel_circle_radius+ (1/16) * homecinema_hogel_circle_radius,
                    x1=homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y1=homecinema_hogel_ypos + homecinema_hogel_circle_radius + (1/8) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line in pixel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=2 * homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y0=homecinema_hogel_ypos + homecinema_hogel_circle_radius+ (1/16) * homecinema_hogel_circle_radius,
                    x1=2 * homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y1=homecinema_hogel_ypos + homecinema_hogel_circle_radius + (1/8) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting left and right line in pixel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y0=homecinema_hogel_ypos + homecinema_hogel_circle_radius + (1/8) * homecinema_hogel_circle_radius,
                    x1=2 * homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y1=homecinema_hogel_ypos + homecinema_hogel_circle_radius + (1/8) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of pixel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=1.5 * homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y0=homecinema_hogel_ypos + homecinema_hogel_circle_radius + (1/8) * homecinema_hogel_circle_radius,
                    x1=1.5 * homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius),
                    y1=homecinema_hogel_ypos + homecinema_hogel_circle_radius + (1/4) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#text for the pixel label
homecinema_figure_top.add_trace(go.Scatter(x=[1.5 * homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius)], y=[homecinema_hogel_ypos + 1.35 * homecinema_hogel_circle_radius], text=["Pixel Pitch"], mode="text"))



#left line sticking out of hogel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_hogel_xpos - homecinema_hogel_circle_radius,
                    y0=homecinema_hogel_ypos - homecinema_hogel_circle_radius,
                    x1=homecinema_hogel_xpos - homecinema_hogel_circle_radius,
                    y1=homecinema_hogel_ypos - homecinema_hogel_circle_radius - (1/4) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line sticking out of hogel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_hogel_xpos + homecinema_hogel_circle_radius,
                    y0=homecinema_hogel_ypos - homecinema_hogel_circle_radius,
                    x1=homecinema_hogel_xpos + homecinema_hogel_circle_radius,
                    y1=homecinema_hogel_ypos - homecinema_hogel_circle_radius - (1/4) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting the 2 lines of hogel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_hogel_xpos - homecinema_hogel_circle_radius,
                    y0=homecinema_hogel_ypos - homecinema_hogel_circle_radius - (1/4) * homecinema_hogel_circle_radius,
                    x1=homecinema_hogel_xpos + homecinema_hogel_circle_radius,
                    y1=homecinema_hogel_ypos - homecinema_hogel_circle_radius - (1/4) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of hogel label
homecinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_hogel_xpos,
                    y0=homecinema_hogel_ypos - homecinema_hogel_circle_radius - (1/4) * homecinema_hogel_circle_radius,
                    x1=homecinema_hogel_xpos,
                    y1=homecinema_hogel_ypos - homecinema_hogel_circle_radius - (1/4) * homecinema_hogel_circle_radius - (1/4) * homecinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )


#text for the hogel label
homecinema_figure_top.add_trace(go.Scatter(x=[homecinema_hogel_xpos], y=[homecinema_hogel_ypos - homecinema_hogel_circle_radius - (0.6) * homecinema_hogel_circle_radius], text=["Diameter of Hogel"], mode="text")) #the theta next to the arc

homecinema_figure_top.update_shapes(dict(xref='x', yref='y'))


#Drawing the lines for represent the pixels in the hogel circle

homecinema_num_pixel_lines = int(homecinema_hogel_circle_diameter / homecinema_pixel_radius_ratio)
homecinema_vertical_line_pos = homecinema_pixel_radius_ratio + (homecinema_hogel_xpos - homecinema_hogel_circle_radius) #far left of the circle + one "pixel"
homecinema_horizontal_line_pos = homecinema_pixel_radius_ratio + (homecinema_hogel_ypos - homecinema_hogel_circle_radius) #far bottom of the circle + one "pixel"


for i in range(0,homecinema_num_pixel_lines):
    homecinema_distance_from_center = abs(homecinema_hogel_xpos - homecinema_vertical_line_pos)
    homecinema_curr_line_top = homecinema_hogel_ypos + math.sqrt((homecinema_hogel_circle_radius)**2 - (homecinema_distance_from_center)**2)
    homecinema_curr_line_bottom = homecinema_hogel_ypos - math.sqrt((homecinema_hogel_circle_radius)**2 - (homecinema_distance_from_center)**2)
    draw_pixels(homecinema_figure_top, homecinema_vertical_line_pos, homecinema_vertical_line_pos, homecinema_curr_line_bottom, homecinema_curr_line_top)
    homecinema_vertical_line_pos = homecinema_vertical_line_pos + homecinema_pixel_radius_ratio

for i in range(0,homecinema_num_pixel_lines):
    homecinema_distance_from_center = abs(homecinema_hogel_ypos - homecinema_horizontal_line_pos)
    homecinema_curr_line_right = homecinema_hogel_xpos + math.sqrt((homecinema_hogel_circle_radius)**2 - (homecinema_distance_from_center)**2)
    homecinema_curr_line_left = homecinema_hogel_xpos - math.sqrt((homecinema_hogel_circle_radius)**2 - (homecinema_distance_from_center)**2)
    draw_pixels(homecinema_figure_top, homecinema_curr_line_left, homecinema_curr_line_right, homecinema_horizontal_line_pos, homecinema_horizontal_line_pos)
    homecinema_horizontal_line_pos = homecinema_horizontal_line_pos + homecinema_pixel_radius_ratio




"""homecinema Side View"""

homecinema_figure_side = go.Figure()
homecinema_figure_side.update_layout(title=dict(text='Side View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
homecinema_figure_side.update_xaxes(range=[-homecinema_axis_size, homecinema_axis_size], zeroline=False)
homecinema_figure_side.update_yaxes(range=[-homecinema_axis_size, homecinema_axis_size])

#drawing the head
homecinema_figure_side.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=homecinema_head_xpos-HEAD_RADIUS,
            y0=homecinema_head_ypos-HEAD_RADIUS,
            x1=homecinema_head_xpos+HEAD_RADIUS,
            y1=homecinema_head_ypos+HEAD_RADIUS,
            line_color="Black",
            )
        ]
    )

#drawing the body line
homecinema_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_head_xpos,
                    y0=homecinema_head_ypos - HEAD_RADIUS,
                    x1=homecinema_head_xpos,
                    y1=homecinema_head_ypos - HEAD_RADIUS - BODY_HEIGHT,
                    line=dict(color="Black", width=1)
                )
            )

#drawing the display line
homecinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=-homecinema_display_height/2,
                    x1=0,
                    y1=homecinema_display_height/2,
                    line=dict(color="Black", width=3)
                )
            )

#Drawing view distance representation

homecinema_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=homecinema_head_xpos,
                    y0=homecinema_head_ypos + 1.25 * HEAD_RADIUS,
                    x1=homecinema_head_xpos,
                    y1=homecinema_head_ypos + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

homecinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=homecinema_head_ypos + 1.25 * HEAD_RADIUS,
                    x1=0,
                    y1=homecinema_head_ypos + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

homecinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=homecinema_head_xpos,
                    y0=homecinema_head_ypos + 1.5 * HEAD_RADIUS,
                    x1=0,
                    y1=homecinema_head_ypos + 1.5 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

homecinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=homecinema_head_xpos/2,
                    y0=homecinema_head_ypos + 1.5 * HEAD_RADIUS,
                    x1=homecinema_head_xpos/2,
                    y1=homecinema_head_ypos + 1.75 * HEAD_RADIUS,
                    line=dict(color="Black", width=1)
                )
            )

homecinema_figure_side.add_trace(go.Scatter(x=[homecinema_head_xpos/2], y=[homecinema_display_height/2 + 2 * HEAD_RADIUS], text=["View Distance"], mode="text")) #the theta next to the arc





"""Cinema"""

#cinema variables from excel file
cinema_display_height = 12192 #in mm
cinema_display_width = 5151 #in mm
cinema_view_distance = 3658 #in mm
cinema_pixel_pitch = (50*(10**-3)) #in mm (so 27um)
cinema_hogel_diameter = 1.06 
cinema_lossless_depth = 17.53 #in mm
cinema_view_angle = 147.9 #in degrees
cinema_hor_view_angel = math.radians(73.94) #horizontal view angle in radians
cinema_angular_resolution = 0.14
cinema_hogel_circle_diameter = cinema_view_distance * 0.75  #controls the size of the circle that represents one hogel
cinema_hogel_circle_radius = cinema_hogel_circle_diameter/2
cinema_rad_times_pixpitch = cinema_hogel_circle_diameter * cinema_pixel_pitch #variable for calculating proper pixel pitch proportations
cinema_pixel_radius_ratio = cinema_rad_times_pixpitch / cinema_hogel_diameter #pixel pitch proportional to circle diameter

#cinema graph variables
cinema_head_xpos = -cinema_view_distance
cinema_head_ypos = cinema_display_width/2
cinema_hogel_xpos = cinema_view_distance
cinema_hogel_ypos = cinema_display_width/2
cinema_axis_size = cinema_display_height

#variables drawing the arc that goes in between the viewing angles
y_arc = np.linspace(cinema_view_distance/2*math.tan(-cinema_hor_view_angel) + cinema_display_width/2, \
    cinema_view_distance/2*math.tan(cinema_hor_view_angel) + cinema_display_width/2, endpoint=False) #y_arc is an array that holds the y coordinates for the arc. 100 points 
x_arc = np.zeros(len(y_arc)) #x_arc is an array that holds the x coordinates for the arc
for i in range(0, len(y_arc)):
    x_arc[i] = math.sqrt(abs((cinema_view_distance/2)**2 - (y_arc[i] - cinema_display_width/2)**2))

x_arc_size_half = int(len(x_arc)/2)
y_arc_size_half = int(len(y_arc)/2)
x_arc_mid = x_arc[x_arc_size_half]
y_arc_mid = y_arc[y_arc_size_half]

#making the figures (graph)
cinema_figure_top = go.Figure()
cinema_figure_top.update_layout(title=dict(text='Top View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
cinema_figure_top.update_xaxes(range=[-cinema_axis_size, cinema_axis_size], zeroline=False)
cinema_figure_top.update_yaxes(range=[-cinema_axis_size, cinema_axis_size])


#making the head and hogel circle respectively
cinema_figure_top.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=cinema_head_xpos-HEAD_RADIUS,
            y0=cinema_head_ypos-HEAD_RADIUS,
            x1=cinema_head_xpos+HEAD_RADIUS,
            y1=cinema_head_ypos+HEAD_RADIUS,
            line_color="Black",
            ),

        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=cinema_hogel_xpos-cinema_hogel_circle_radius,
            y0=cinema_hogel_ypos-cinema_hogel_circle_radius,
            x1=cinema_hogel_xpos+cinema_hogel_circle_radius,
            y1=cinema_hogel_ypos+cinema_hogel_circle_radius,
            line_color="Black",
            )
        ]
    )

#making the screen
cinema_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0,
                    x1=0,
                    y1=cinema_display_width,
                    line=dict(color="Black", width=3)
                )
            )

#top viewing angle line
cinema_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=cinema_display_width/2,
                    x1=-cinema_view_distance,
                    y1=cinema_view_distance*math.tan(cinema_hor_view_angel) + cinema_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

#bottom viewing angle line
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=cinema_display_width/2,
                    x1=-cinema_hogel_xpos,
                    y1=cinema_view_distance*math.tan(-cinema_hor_view_angel) + cinema_display_width/2,
                    line=dict(color="Black", width=1)
                )
            )

cinema_figure_top.add_trace(go.Scatter(x=-x_arc[18:33], y=y_arc[18:33], mode='lines')) #the arc between viewing angles
cinema_figure_top.add_trace(go.Scatter(x=[-(x_arc_mid + cinema_view_distance/16)], y=[y_arc_mid], text=["\u03B8"], mode="text")) #the theta next to the arc

#top hogel line
cinema_figure_top.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*cinema_display_width,
                    x1=cinema_hogel_xpos - cinema_hogel_circle_radius/2,
                    y1=cinema_hogel_ypos + math.sqrt(3) * cinema_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )



#bottom hogel line
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=0,
                    y0=0.75*cinema_display_width,
                    x1=cinema_hogel_xpos - cinema_hogel_circle_radius/2,
                    y1=cinema_hogel_ypos - math.sqrt(3) * cinema_hogel_circle_radius/2,
                    line=dict(color="Black", width=1)
                )
            )

#left line in pixel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y0=cinema_hogel_ypos + cinema_hogel_circle_radius+ (1/16) * cinema_hogel_circle_radius,
                    x1=cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y1=cinema_hogel_ypos + cinema_hogel_circle_radius + (1/8) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line in pixel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=2 * cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y0=cinema_hogel_ypos + cinema_hogel_circle_radius+ (1/16) * cinema_hogel_circle_radius,
                    x1=2 * cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y1=cinema_hogel_ypos + cinema_hogel_circle_radius + (1/8) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting left and right line in pixel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y0=cinema_hogel_ypos + cinema_hogel_circle_radius + (1/8) * cinema_hogel_circle_radius,
                    x1=2 * cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y1=cinema_hogel_ypos + cinema_hogel_circle_radius + (1/8) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of pixel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=1.5 * cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y0=cinema_hogel_ypos + cinema_hogel_circle_radius + (1/8) * cinema_hogel_circle_radius,
                    x1=1.5 * cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius),
                    y1=cinema_hogel_ypos + cinema_hogel_circle_radius + (1/4) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#text for the pixel label
cinema_figure_top.add_trace(go.Scatter(x=[1.5 * cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius)], y=[cinema_hogel_ypos + 1.35 * cinema_hogel_circle_radius], text=["Pixel Pitch"], mode="text"))



#left line sticking out of hogel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_hogel_xpos - cinema_hogel_circle_radius,
                    y0=cinema_hogel_ypos - cinema_hogel_circle_radius,
                    x1=cinema_hogel_xpos - cinema_hogel_circle_radius,
                    y1=cinema_hogel_ypos - cinema_hogel_circle_radius - (1/4) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#right line sticking out of hogel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_hogel_xpos + cinema_hogel_circle_radius,
                    y0=cinema_hogel_ypos - cinema_hogel_circle_radius,
                    x1=cinema_hogel_xpos + cinema_hogel_circle_radius,
                    y1=cinema_hogel_ypos - cinema_hogel_circle_radius - (1/4) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#connecting the 2 lines of hogel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_hogel_xpos - cinema_hogel_circle_radius,
                    y0=cinema_hogel_ypos - cinema_hogel_circle_radius - (1/4) * cinema_hogel_circle_radius,
                    x1=cinema_hogel_xpos + cinema_hogel_circle_radius,
                    y1=cinema_hogel_ypos - cinema_hogel_circle_radius - (1/4) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )

#line sticking out of hogel label
cinema_figure_top.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_hogel_xpos,
                    y0=cinema_hogel_ypos - cinema_hogel_circle_radius - (1/4) * cinema_hogel_circle_radius,
                    x1=cinema_hogel_xpos,
                    y1=cinema_hogel_ypos - cinema_hogel_circle_radius - (1/4) * cinema_hogel_circle_radius - (1/4) * cinema_hogel_circle_radius,
                    line=dict(color="Black", width=1)
                )
            )


#text for the hogel label
cinema_figure_top.add_trace(go.Scatter(x=[cinema_hogel_xpos], y=[cinema_hogel_ypos - cinema_hogel_circle_radius - (0.6) * cinema_hogel_circle_radius], text=["Diameter of Hogel"], mode="text")) #the theta next to the arc

cinema_figure_top.update_shapes(dict(xref='x', yref='y'))


#Drawing the lines for represent the pixels in the hogel circle

cinema_num_pixel_lines = int(cinema_hogel_circle_diameter / cinema_pixel_radius_ratio)
cinema_vertical_line_pos = cinema_pixel_radius_ratio + (cinema_hogel_xpos - cinema_hogel_circle_radius) #far left of the circle + one "pixel"
cinema_horizontal_line_pos = cinema_pixel_radius_ratio + (cinema_hogel_ypos - cinema_hogel_circle_radius) #far bottom of the circle + one "pixel"


for i in range(0,cinema_num_pixel_lines):
    cinema_distance_from_center = abs(cinema_hogel_xpos - cinema_vertical_line_pos)
    cinema_curr_line_top = cinema_hogel_ypos + math.sqrt((cinema_hogel_circle_radius)**2 - (cinema_distance_from_center)**2)
    cinema_curr_line_bottom = cinema_hogel_ypos - math.sqrt((cinema_hogel_circle_radius)**2 - (cinema_distance_from_center)**2)
    draw_pixels(cinema_figure_top, cinema_vertical_line_pos, cinema_vertical_line_pos, cinema_curr_line_bottom, cinema_curr_line_top)
    cinema_vertical_line_pos = cinema_vertical_line_pos + cinema_pixel_radius_ratio

for i in range(0,cinema_num_pixel_lines):
    cinema_distance_from_center = abs(cinema_hogel_ypos - cinema_horizontal_line_pos)
    cinema_curr_line_right = cinema_hogel_xpos + math.sqrt((cinema_hogel_circle_radius)**2 - (cinema_distance_from_center)**2)
    cinema_curr_line_left = cinema_hogel_xpos - math.sqrt((cinema_hogel_circle_radius)**2 - (cinema_distance_from_center)**2)
    draw_pixels(cinema_figure_top, cinema_curr_line_left, cinema_curr_line_right, cinema_horizontal_line_pos, cinema_horizontal_line_pos)
    cinema_horizontal_line_pos = cinema_horizontal_line_pos + cinema_pixel_radius_ratio




"""cinema Side View"""

cinema_figure_side = go.Figure()
cinema_figure_side.update_layout(title=dict(text='Side View', x=0.5, font=dict(color="Black", size=24)), plot_bgcolor='white', xaxis=dict(visible=False), yaxis=dict(visible=False), width=600, height=600, showlegend=False) #look of the graph
cinema_figure_side.update_xaxes(range=[-cinema_axis_size, cinema_axis_size], zeroline=False)
cinema_figure_side.update_yaxes(range=[-cinema_axis_size, cinema_axis_size])

#drawing the head
cinema_figure_side.update_layout(
        shapes=[
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=cinema_head_xpos-HEAD_RADIUS,
            y0=cinema_head_ypos-HEAD_RADIUS,
            x1=cinema_head_xpos+HEAD_RADIUS,
            y1=cinema_head_ypos+HEAD_RADIUS,
            line_color="Black",
            )
        ]
    )

#drawing the body line
cinema_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_head_xpos,
                    y0=cinema_head_ypos - HEAD_RADIUS,
                    x1=cinema_head_xpos,
                    y1=cinema_head_ypos - HEAD_RADIUS - BODY_HEIGHT,
                    line=dict(color="Black", width=1)
                )
            )

#drawing the display line
cinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=-cinema_display_height/2,
                    x1=0,
                    y1=cinema_display_height/2,
                    line=dict(color="Black", width=3)
                )
            )

#Drawing view distance representation
cinema_figure_side.add_shape(                     
                dict(
                    type="line",
                    x0=cinema_head_xpos,
                    y0=cinema_display_height/2 + 0.2 * cinema_display_height/2,
                    x1=cinema_head_xpos,
                    y1=cinema_display_height/2 + 0.3 * cinema_display_height/2,
                    line=dict(color="Black", width=1)
                )
            )

cinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=0,
                    y0=cinema_display_height/2 + 0.2 * cinema_display_height/2,
                    x1=0,
                    y1=cinema_display_height/2 + 0.3 * cinema_display_height/2,
                    line=dict(color="Black", width=1)
                )
            )

cinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=cinema_head_xpos,
                    y0=cinema_display_height/2 + 0.3 * cinema_display_height/2,
                    x1=0,
                    y1=cinema_display_height/2 + 0.3 * cinema_display_height/2,
                    line=dict(color="Black", width=1)
                )
            )

cinema_figure_side.add_shape(
                dict(
                    type="line",
                    x0=cinema_head_xpos/2,
                    y0=cinema_display_height/2 + 0.3 * cinema_display_height/2,
                    x1=cinema_head_xpos/2,
                    y1=cinema_display_height/2 + 0.4 * cinema_display_height/2,
                    line=dict(color="Black", width=1)
                )
            )

cinema_figure_side.add_trace(go.Scatter(x=[cinema_head_xpos/2], y=[cinema_display_height/2 + 0.5 * cinema_display_height/2], text=["View Distance"], mode="text")) #the theta next to the arc














"""Making the Application"""
app = dash.Dash(__name__)

lukes_images = (
        html.Div(
        className="app-header",
        children=[
        html.Div('Light Field Display Spatial/Angular Trade Analysis', className="app-header--title")
        ]
    ),
    html.Div(
        children=[
        dcc.Graph(
            id='top_view_figure',
            figure=tablet_figure_top,
            )
        ],
        style={ 'display': 'inline-block'}
    ),

    html.Div(
        children=[
        dcc.Graph(
            id='side_view_figure',
            figure=tablet_figure_side
            )
        ],
        style={ 'display': 'inline-block'}
    )
)

app.layout = html.Div(children=[
    *lukes_images,

    html.Div(children=[
        html.Table(

            id='variable-table',

            children =[
            html.Thead(
                children=[
                html.Tr(
                    children=[
                    html.Th(scope="col", children=["Symbol"]),
                    html.Th(scope="col", children=["Value"])
                    ]) #end Tr
                ]), #end Thead

            html.Tbody(
                children=[

                html.Tr(
                    children=[
                    html.Th(scope="row", children=["\u03B8"]),
                    html.Td(
                        id='view-angle-id',
                        children=["tablet_view_angle"]
                        )
                    ]),

                    html.Tr(
                    children=[
                    html.Th(scope="row", children=["Pixel Pitch (um)"]),
                    html.Td(
                        id='pixel-pitch-id',
                        children=[tablet_pixel_pitch]
                        )
                    ]),

                    html.Tr(
                    children=[
                    html.Th(scope="row", children=["Diameter of Hogel (mm)"]),
                    html.Td(
                        id='hogel-diameter-id',
                        children=[tablet_hogel_diameter]
                        )
                    ]),

                    html.Tr(
                    children=[
                    html.Th(scope="row", children=["View Distance (mm)"]),
                    html.Td(
                        id='view-distance-id',
                        children=[tablet_view_distance]
                        )
                    ]),

                    html.Tr(
                    children=[
                    html.Th(scope="row", children=["Lossless Projection Depth (mm)"]),
                    html.Td(
                        id='lossless-depth-id',
                        children=[tablet_lossless_depth]
                        )
                    ]),

                    html.Tr(
                    children=[
                    html.Th(scope="row", children=["Angular Resolution"]),
                    html.Td(
                        id='angular-resolution-id',
                        children=[tablet_angular_resolution]
                        )
                    ]),



                ]) #end Tbody
            ]), #end Table
        ],
        style={ 'display': 'inline-block'}

    ),

    
    html.Div(
        className="radio-elements",
        children=[
            dcc.RadioItems(
                id='form_buttons',
                inputClassName='input-class-name',
                options=[
                    {'label': 'Tablet', 'value': 'T' },
                    {'label': 'Desktop', 'value': 'D'},
                    {'label': 'TableTop', 'value': 'SF'},
                    {'label': 'HomeCinema', 'value': 'HC'},
                    {'label': 'Cinema', 'value': 'C'}
                ],
                value='T', #the radio button that is selected by default
            )
        ]
    ),
])

"""Controlling input and output"""

#Top View
@app.callback(
    Output(component_id='top_view_figure', component_property='figure'),
    [Input(component_id='form_buttons', component_property='value')]
)

def display_graph(button_value):
    if button_value=='T':
        figure=tablet_figure_top
        return figure
    elif button_value=='D':
        figure=desktop_figure_top
        return figure
    elif button_value=='SF':
        figure=tabletop_figure_top
        return figure
    elif button_value=='HC':
        figure=homecinema_figure_top
        return figure
    elif button_value=='C':
        figure=cinema_figure_top
        return figure
    else:
        figure=tablet_figure_top
        return figure

        return src 


#Side View
@app.callback(
    Output(component_id='side_view_figure', component_property='figure'),
    [Input(component_id='form_buttons', component_property='value')]
)

def display_graph(button_value):
    if button_value=='T':
        figure=tablet_figure_side
        return figure
    elif button_value=='D':
        figure=desktop_figure_side
        return figure
    elif button_value=='SF':
        figure=tabletop_figure_side
        return figure
    elif button_value=='HC':
        figure=homecinema_figure_side
        return figure
    elif button_value=='C':
        figure=cinema_figure_side
        return figure
    else:
        figure=tablet_figure_side
        return figure

        return src 


#View Angle in table
@app.callback(
    Output(component_id='view-angle-id', component_property='children'),
    [Input(component_id='form_buttons', component_property='value')]
)

def update_table(button_value):
    if button_value=='T':
        angle=tablet_view_angle
        return angle
    elif button_value=='D':
        angle=desktop_view_angle
        return angle
    elif button_value=='SF':
        angle=tabletop_view_angle
        return angle
    elif button_value=='HC':
        angle=homecinema_view_angle
        return angle
    elif button_value=='C':
        angle=homecinema_view_angle
        return angle
    else:
        angle=tablet_view_distance
        return angle

        return src 


#Pixel Pitch in table
@app.callback(
    Output(component_id='pixel-pitch-id', component_property='children'),
    [Input(component_id='form_buttons', component_property='value')]
)

def update_table(button_value):
    if button_value=='T':
        pixel_pitch=tablet_pixel_pitch*(10**3)
        return pixel_pitch
    elif button_value=='D':
        pixel_pitch=desktop_pixel_pitch*(10**3)
        return pixel_pitch
    elif button_value=='SF':
        pixel_pitch=tabletop_pixel_pitch*(10**3)
        return pixel_pitch
    elif button_value=='HC':
        pixel_pitch=homecinema_pixel_pitch*(10**3)
        return pixel_pitch
    elif button_value=='C':
        pixel_pitch=cinema_pixel_pitch*(10**3)
        return pixel_pitch
    else:
        pixel_pitch=tablet_pixel_pitch*(10**3)
        return pixel_pitch

        return src 


#Hogel Diameter in table
@app.callback(
    Output(component_id='hogel-diameter-id', component_property='children'),
    [Input(component_id='form_buttons', component_property='value')]
)

def update_table(button_value):
    if button_value=='T':
        hogel_diameter=tablet_hogel_diameter
        return hogel_diameter
    elif button_value=='D':
        hogel_diameter=desktop_hogel_diameter
        return hogel_diameter
    elif button_value=='SF':
        hogel_diameter=tabletop_hogel_diameter
        return hogel_diameter
    elif button_value=='HC':
        hogel_diameter=homecinema_hogel_diameter
        return hogel_diameter
    elif button_value=='C':
        hogel_diameter=cinema_hogel_diameter
        return hogel_diameter
    else:
        hogel_diameter=tablet_hogel_diameter
        return hogel_diameter

        return src 


#Tablet View Distance in table
@app.callback(
    Output(component_id='view-distance-id', component_property='children'),
    [Input(component_id='form_buttons', component_property='value')]
)

def update_table(button_value):
    if button_value=='T':
        view_distance=tablet_view_distance
        return view_distance
    elif button_value=='D':
        view_distance=desktop_view_distance
        return view_distance
    elif button_value=='SF':
        view_distance=tabletop_view_distance
        return view_distance
    elif button_value=='HC':
        view_distance=homecinema_view_distance
        return view_distance
    elif button_value=='C':
        view_distance=cinema_view_distance
        return view_distance
    else:
        view_distance=tablet_view_distance
        return view_distance

        return src     


#Lossless Depth in table
@app.callback(
    Output(component_id='lossless-depth-id', component_property='children'),
    [Input(component_id='form_buttons', component_property='value')]
)

def update_table(button_value):
    if button_value=='T':
        lossless_depth=tablet_lossless_depth
        return lossless_depth
    elif button_value=='D':
        lossless_depth=desktop_lossless_depth
        return lossless_depth
    elif button_value=='SF':
        lossless_depth=tabletop_lossless_depth
        return lossless_depth
    elif button_value=='HC':
        lossless_depth=homecinema_lossless_depth
        return lossless_depth
    elif button_value=='C':
        lossless_depth=cinema_lossless_depth
        return lossless_depth
    else:
        lossless_depth=tablet_lossless_depth
        return lossless_depth

        return src   

#Angular Resolution in table
@app.callback(
    Output(component_id='angular-resolution-id', component_property='children'),
    [Input(component_id='form_buttons', component_property='value')]
)

def update_table(button_value):
    if button_value=='T':
        angular_resolution=tablet_angular_resolution
        return angular_resolution
    elif button_value=='D':
        angular_resolution=desktop_angular_resolution
        return angular_resolution
    elif button_value=='SF':
        angular_resolution=tabletop_angular_resolution
        return angular_resolution
    elif button_value=='HC':
        angular_resolution=homecinema_angular_resolution
        return angular_resolution
    elif button_value=='C':
        angular_resolution=cinema_angular_resolution
        return angular_resolution
    else:
        angular_resolution=tablet_angular_resolution
        return angular_resolution

        return src            


if __name__ == '__main__':
    app.run_server(debug=True)
