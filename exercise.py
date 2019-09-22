from igraph import *
import numpy

g = Graph.Read_GraphML("exercise/networks/NREN.graphml", False)

summary(g)

# Exercise 8
print("\nNumber of vertices: %d" % len(g.vs))
print("Number of edges: %d" % len(g.es))
print("Radius: %d" % g.radius())
print("Diameter: %d" % g.diameter(False, False, "weight"))
# End exercise 8

# Exercise 10
for edge in g.es:
    buffer_delay = numpy.random.normal(2, math.sqrt(0.2))
    transmission_delay = numpy.random.normal(1, math.sqrt(0.15))
    propagation_delay = numpy.random.normal(50, math.sqrt(20))
    edge["delay"] = buffer_delay + transmission_delay + propagation_delay

g.write_graphml("delay_included_NREN.graphml")

shortest_path = g.get_shortest_paths(0, 1102, "delay")[0]
e2e_delay = 0
for i in range(len(shortest_path)-1):
    edge = g.es[g.get_eid(shortest_path[i], shortest_path[i+1])]
    e2e_delay += edge["delay"]

print("\nShortest path: " + str(shortest_path))
print("Number of hops: %d" % (len(shortest_path)-1))
print("End-to-end delay: %f" % e2e_delay)
# End exercise 10

# Exercise 11
layout = g.layout("large")

delays = []
for d in g.es["delay"]:
    delays.append(round(d, 2))

for edge in g.es:
    edge["edge_color"] = "black"

for i in range(len(shortest_path)-1):
    edge = g.es[g.get_eid(shortest_path[i], shortest_path[i+1])]
    edge["edge_color"] = "red"    # "highlight" the path in red
# End exercise 11

visual_style = {}
visual_style["vertex_shape"] = "circle"
visual_style["vertex_size"] = 10
visual_style["vertex_label"] = g.vs["asn"]
visual_style["layout"] = layout
visual_style["bbox"] = (2000,2000)
visual_style["margin"] = 10
visual_style["label_dist"] = 20
visual_style["edge_label"] = g.es["LinkSpeedRaw"]
visual_style["edge_color"] = g.es["edge_color"]

plot(g, "nren.pdf", **visual_style)
