from manim import *
import copy
import pandas as pd
import os
from pathlib import Path

SELECTED_PATH = 0

class AllCausalFunctions(Scene):
    def create_uber_diagram(self):
        # Create all boxes (questions in white, methods in blue)
        # Question boxes
        q1 = self.create_box("Have repeated observations of\nthe outcome over time?", WHITE)
        q2 = self.create_box("Have a control time series\ndata from a non-treated unit?", WHITE)
        q3 = self.create_box("More than a handful of obs\nbefore and after intervention?", WHITE)
        q4 = self.create_box("Treatment assignment\ndepends on a sharp cutoff?", WHITE)
        q5 = self.create_box("Have a third variable\nassociated with the outcome\nonly through the cause\nvariable?", WHITE)
        q6 = self.create_box("Have pre-intervention\ncovariates?", WHITE)
        
        # Method boxes (results)
        m1 = self.create_box("Interrupted time series\nsynthetic control", BLUE)
        m2 = self.create_box("difference-in-difference", BLUE)
        m3 = self.create_box("Interrupted time series w/o control\nSinge-group pre/post design", BLUE)
        m4 = self.create_box("Regression discontinuity", BLUE)
        m5 = self.create_box("Instrumental Variable", BLUE)
        m6 = self.create_box("Propensity score matching\nIPTW\ndoubly-robust estimation", BLUE)
        
        # Position boxes using next_to
        # Start with q1 as the leftmost element
        q1.to_edge(LEFT)
        
        # Position q2 to the right and slightly above q1
        q2.next_to(q1, RIGHT + UP, buff=2.0)
        
        # Position q3 to the right and above q2
        q3.next_to(q2, RIGHT + UP, buff=1.5)
        
        # Position q4 below and right of q1
        q4.next_to(q1, RIGHT + DOWN, buff=2.0)
        
        # Position q5 below q4
        q5.next_to(q4, DOWN, buff=1.5)
        
        # Position q6 to the right and below q5
        q6.next_to(q5, RIGHT + DOWN, buff=1.5)
        
        # Position method boxes (all aligned on the right side)
        m1.next_to(q3, RIGHT, buff=2.0)
        m2.next_to(m1, DOWN, buff=1.0).align_to(q2, UP)
        m3.next_to(m2, DOWN, buff=1.0).align_to(q1, UP)
        m4.next_to(m3, DOWN, buff=1.0).align_to(q4, UP)
        m5.next_to(m4, DOWN, buff=1.0).align_to(q5, UP)
        m6.next_to(m5, DOWN, buff=1.0).align_to(q6, UP)

        # Create arrows and labels
        arrows = []
        labels = []
        
        arrows_dict = {}
        # q1 to q2
        arrows_dict['q1_q2'] = self.create_arrow(q1, q2)
        arrows.append(arrows_dict['q1_q2'])
        labels.append(self.create_label("Yes", q1, q2, UP * 0.2))
        
        # q1 to q4
        arrows_dict['q1_q4'] = self.create_arrow(q1, q4)        
        arrows.append(arrows_dict['q1_q4'])
        labels.append(self.create_label("No", q1, q4, DOWN * 0.2))
        
        # q2 to q3
        arrows_dict['q2_q3'] = self.create_arrow(q2, q3)
        arrows.append(arrows_dict['q2_q3'])
        labels.append(self.create_label("Yes", q2, q3, UP * 0.2))
        
        # q2 to m3
        arrows_dict['q2_m3'] = self.create_arrow(q2, m3)
        arrows.append(arrows_dict['q2_m3'])
        labels.append(self.create_label("No", q2, m3, RIGHT * 0.2))
        
        # q3 to m1
        arrows_dict['q3_m1'] = self.create_arrow(q3, m1)
        arrows.append(arrows_dict['q3_m1'])
        labels.append(self.create_label("Yes", q3, m1, RIGHT * 0.2))
        
        # q3 to m2
        arrows_dict['q3_m2'] = self.create_arrow(q3, m2)
        arrows.append(arrows_dict['q3_m2'])
        labels.append(self.create_label("No", q3, m2, RIGHT * 0.2))
        
        # q4 to m4
        arrows_dict['q4_m4'] = self.create_arrow(q4, m4)
        arrows.append(arrows_dict['q4_m4'])
        labels.append(self.create_label("Yes", q4, m4, RIGHT * 0.2))
        
        # q4 to q5
        arrows_dict['q4_q5'] = self.create_arrow(q4, q5)
        arrows.append(arrows_dict['q4_q5'])
        labels.append(self.create_label("No", q4, q5, DOWN * 0.2))
        
        # q5 to m5
        arrows_dict['q5_m5'] = self.create_arrow(q5, m5)
        arrows.append(arrows_dict['q5_m5'])
        labels.append(self.create_label("Yes", q5, m5, RIGHT * 0.2))
        
        # q5 to q6
        arrows_dict['q5_q6'] = self.create_arrow(q5, q6)
        arrows.append(arrows_dict['q5_q6'])
        labels.append(self.create_label("No", q5, q6, DOWN * 0.2))
        
        # q6 to m6
        arrows_dict['q6_m6'] = self.create_arrow(q6, m6)
        arrows.append(arrows_dict['q6_m6'])
        labels.append(self.create_label("Yes", q6, m6, RIGHT * 0.2))

        # Create a group for all the boxes, arrows, and labels
        all_elements = [q1, q2, q3, q4, q5, q6, m1, m2, m3, m4, m5, m6]
        all_elements.extend(arrows)
        all_elements.extend(labels)
        self.entire_diagram = VGroup(*all_elements)
        self.entire_diagram.scale(0.4)
        self.entire_diagram.to_corner(UL)

        # # Render the entire diagram at once
        self.play(FadeIn(self.entire_diagram))

        # # Create highlights for each path
        # Highlight each path with different colors
        self.paths = [
            [q1, arrows_dict["q1_q2"], q2, arrows_dict["q2_q3"], q3, arrows_dict["q3_m1"], m1],  # Path to Interrupted time series synthetic control
            [q1, q2, q3, m1],  # Path to Interrupted time series synthetic control
            [q1, q2, q3, m2],  # Path to difference-in-difference
            [q1, q2, m3],      # Path to Interrupted time series w/o control
            [q1, q4, m4],      # Path to Regression discontinuity
            [q1, q4, q5, m5],  # Path to Instrumental Variable
            [q1, q4, q5, q6, m6]  # Path to Propensity score matching
        ]        

    def create_box(self, text, color=BLACK):
        """Create a rectangular box with text inside"""
        box = Rectangle(height=1.5, width=3, fill_opacity=0.1, color=BLACK)
        text_obj = Text(text, font_size=16, color=BLACK).move_to(box.get_center())
        # if color != BLACK:
        box.set_fill(color, opacity=0.2)
        text_obj.set_color(BLACK)

        return VGroup(box, text_obj)
    
    def create_arrow(self, start_obj, end_obj, offset=ORIGIN):
        """Create an arrow between two objects with an offset"""
        start = start_obj.get_center()
        end = end_obj.get_center()
        
        if abs(start[0] - end[0]) > abs(start[1] - end[1]):
            # Horizontal arrow
            if start[0] < end[0]:
                start_point = start_obj.get_edge_center(RIGHT)
                end_point = end_obj.get_edge_center(LEFT)
            else:
                start_point = start_obj.get_edge_center(LEFT)
                end_point = end_obj.get_edge_center(RIGHT)
        else:
            # Vertical arrow
            if start[1] < end[1]:
                start_point = start_obj.get_edge_center(UP)
                end_point = end_obj.get_edge_center(DOWN)
            else:
                start_point = start_obj.get_edge_center(DOWN)
                end_point = end_obj.get_edge_center(UP)
                
        return Arrow(start_point + offset, end_point + offset, buff=0.1, color=BLACK)
    
    def create_label(self, text, start_obj, end_obj, offset=ORIGIN):
        """Create a label for the arrow"""
        start = start_obj.get_center()
        end = end_obj.get_center()
        
        # Find midpoint based on direction
        if abs(start[0] - end[0]) > abs(start[1] - end[1]):
            # Horizontal arrow
            if start[0] < end[0]:
                start_point = start_obj.get_edge_center(RIGHT)
                end_point = end_obj.get_edge_center(LEFT)
            else:
                start_point = start_obj.get_edge_center(LEFT)
                end_point = end_obj.get_edge_center(RIGHT)
        else:
            # Vertical arrow
            if start[1] < end[1]:
                start_point = start_obj.get_edge_center(UP)
                end_point = end_obj.get_edge_center(DOWN)
            else:
                start_point = start_obj.get_edge_center(DOWN)
                end_point = end_obj.get_edge_center(UP)
                
        mid_point = (start_point + end_point) / 2 + offset
        label = Text(text, font_size=16, color=BLACK).move_to(mid_point)
        return label
    
    def highlight_path(self, path, color):
        """Highlight a specific path through the flowchart"""
        
        highlights = []
        
        for obj in path:
            highlight = obj[0].copy().set_fill(color, opacity=0.3).set_stroke(color, width=3)
            highlights.append(highlight)
        self.play(
            *[FadeIn(h) for h in highlights],
            run_time=1
        )
        # if fade_in:
        #     )
        # elif highlights:
        #     self.play(
        #         *[FadeOut(h) for h in highlights],
        #         run_time=1
        #     )
        # else:
        #     raise ValueError("No highlights to fade out.")
        return highlights

    def fadeout_path(self, path, all_elements):
        """Highlight a specific path through the flowchart"""
        
        if all_elements:

            # Fade out all elements except those in the selected path
            to_fade_out = []
            to_stay_in = []
            print(f'all_elements = {all_elements}')
            for element in all_elements:
                print(f'element = {element}')
                if element not in path or isinstance(element, Arrow):
                    to_fade_out.append(element)
                else:
                    to_stay_in.append(element)

            self.play(
                *[FadeOut(h) for h in to_fade_out],
                run_time=1
            )
        else:
            raise ValueError("No highlights to fade out.")
        return to_stay_in, to_fade_out

    def align_elements(self, path: list[VMobject]):
        # Calculate the horizontal position for the first element in the path
        leftmost_x = -config.frame_width / 2 + 2  # Start 1 unit from the left edge

        # Arrange the elements in the path horizontally
        # aux = path.copy()
        aux = copy.deepcopy(path)
        for i, obj in enumerate(aux):
            obj.scale(2)
            obj.move_to(ORIGIN)  # Move to origin first
            if i == 0:
                obj.move_to(np.array([leftmost_x, 0, 0]))  # Position the first element
                current_x = leftmost_x + 3  # Update current_x based on the width of the box
            else:
                obj.next_to(aux[i-1], RIGHT, buff=1)  # Position subsequent elements to the right
                current_x = obj.get_center()[0] + 3  # Update current_x        
        
        self.play(
            *[path[i].animate.move_to(obj.get_center()).scale(2) for i, obj in enumerate(aux)],
        )



class CausalInferenceFlowchart(AllCausalFunctions):
    def construct(self):
        self.camera.background_color = WHITE
        # Title
        title = Text("Causal Inference Method Selection", font_size=42, color=BLACK)
        title.to_edge(UP, buff=0.5)
        
        self.create_uber_diagram()

        # colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        highlight = self.highlight_path(self.paths[SELECTED_PATH], GREEN)
        self.wait(2)
        self.play(
            *[FadeOut(h) for h in highlight]
        )

        to_stay_in, to_fade_out = self.fadeout_path(self.paths[SELECTED_PATH], self.entire_diagram)

        self.align_elements(to_stay_in)

        self.play(
            *[FadeOut(h) for h in to_stay_in]
        )

class InterruptedTimeSeriesSyntheticControl(Scene):
    def construct(self):
        Text.set_default(color=BLACK)
        self.camera.background_color = WHITE

        # column_names = ['time', 'treated', 'control1', 'control2', 'control3', 'synthetic','intervention']

        # path = 'video_data/1_interrupted_time_series_synthetic_control/data.csv'
        path = os.path.join(os.getcwd(), 'uber_decision_tree_causal/video_data/1_interrupted_time_series_synthetic_control/data.csv')
        df = pd.read_csv(path)
        column_names = df.columns
        print(df.head())


        table = DecimalTable(
            # [["This", "is a"],
            # ["simple", "Table."]],
            df.head().values.tolist(),
            row_labels=[Text(str(c), color=BLACK) for c in range(df.head().shape[0])],
            # col_labels=[Text("C1"), Text("C2")],
            col_labels=[Text(c, color=BLACK) for c in column_names],
            top_left_entry=Star().scale(0.3),
            include_outer_lines=True,
            arrange_in_grid_config={"cell_alignment": RIGHT},
            line_config={"color": BLACK},
            element_to_mobject_config={"num_decimal_places": 2, "color": BLACK}).set_color(color=BLACK).scale(0.4)
        table.add(table.get_cell((2,2), color=RED))
        
        self.play(Write(table))

        col_labels = table.get_col_labels()

        vertices = column_names

        # Create a dictionary mapping vertices to their positions
        # (based on the column labels' positions)
        layout = {}
        for i, vertex in enumerate(vertices):
            # Get the center of each column label
            layout[vertex] = col_labels[i].get_center()        

        # Create edges between vertices
        edges = []        
        for idx, vertex in enumerate(vertices):
            if idx != 0:
                edges.append((vertices[idx-1], vertex))
        
        print({(v1, v2): {"stroke_color": BLACK} for v1, v2 in edges})
        # Create the graph with the custom layout
        graph = Graph(
            vertices, 
            edges, 
            layout=layout,
            vertex_config={"fill_color": RED},
            # edge_config={("v1", "v2"): {"stroke_color": BLACK}},
            # edge_config={(v1, v2): {"stroke_color": BLACK} for v1, v2 in edges},
            labels=True,
            label_fill_color=BLACK
        )
        
        # Add both objects to the scene
        # self.add(table)
        # self.add(graph)
        self.play(Write(graph))

        # DecimalTable.set_color(color=BLACK)
        # decimal_table = DecimalTable(
        #     [[1.23, 4.56], [7.89, 0.12]],
        #     row_labels=[Text("Row 1"), Text("Row 2")],
        #     col_labels=[Text("Column 1"), Text("Column 2")],
        #     element_to_mobject_config={"num_decimal_places": 2, "color": BLACK},
        #     top_left_entry=Star().scale(0.3),
        #     line_config={"color": BLACK},
        #     include_outer_lines=True
        # ).set_color(color=BLACK)
        # self.play(Write(decimal_table))

from manim import *

class TableGraphNetwork(Scene):
    def construct(self):
        # Create a table with headers
        table = Table(
            [["Data 1", "Data 2"], 
             ["Data 3", "Data 4"]],
            row_labels=[Text("R1"), Text("R2")],
            col_labels=[Text("C1"), Text("C2")],
            line_config={"color": BLACK}
        )
        
        # Get the column labels (headers)
        col_labels = table.get_col_labels()
        
        # Create vertices for the graph using the positions of column headers
        vertices = ["v1", "v2"]
        
        # Create a dictionary mapping vertices to their positions
        # (based on the column labels' positions)
        layout = {}
        for i, vertex in enumerate(vertices):
            # Get the center of each column label
            layout[vertex] = col_labels[i].get_center()
        
        # Create edges between vertices
        edges = [("v1", "v2")]
        
        # Create the graph with the custom layout
        graph = Graph(
            vertices, 
            edges, 
            layout=layout,
            vertex_config={"fill_color": RED},
            edge_config={("v1", "v2"): {"stroke_color": BLACK}},
            labels=True,
            label_fill_color=BLACK
        )
        
        # Add both objects to the scene
        self.add(table)
        self.add(graph)


# To run this animation:
# manim -pql causal_inference_animation.py CausalInferenceFlowchart