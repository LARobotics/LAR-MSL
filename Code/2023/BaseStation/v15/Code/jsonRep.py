import pygame
import json
import time
import consts

if __name__ == "__main__":
    pygame.init()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    with open('configs/decisionTree.json') as f:
        data = json.load(f)
    print(data)

    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('JSON Visualization')
    SMALLFONT = pygame.freetype.SysFont('segoeuiemoji', 5)

# Calculate the total width and height of the tree
def calculate_tree_size(node, dict_padding):
    if isinstance(node, dict):
        subtree_sizes = [calculate_tree_size(value, dict_padding) for value in node.values()]
        width = sum(size[0] for size in subtree_sizes) + dict_padding * (len(subtree_sizes) - 1)
        height = max(size[1] for size in subtree_sizes)
        return width, height
    elif isinstance(node, list):
        width = 100
        height = len(node) * 50
        return width, height

# Scale down the tree to fit the window
def scale_tree(node, scale_factor):
    if isinstance(node, dict):
        scaled_tree = {}
        for key, value in node.items():
            scaled_tree[key] = scale_tree(value, scale_factor)
        return scaled_tree
    elif isinstance(node, list):
        scaled_list = [item for item in node]
        return scaled_list
    
    
    
    

############################# HORIZONTALLY #################################

# # Function to recursively draw the JSON tree
# def draw_json_tree(node, x, y, scale_factor, x_scale_factor, y_scale_factor, x_dim, y_dim, dict_padding, parent_color, active_nodes, node_active, line_width, elements):
#     if isinstance(node, dict):
#         subtree_sizes = [calculate_tree_size(value, dict_padding) for value in node.values()]
#         total_width = sum(size[1] for size in subtree_sizes) + dict_padding * (len(subtree_sizes) - 1)
#         max_height = max(size[0] for size in subtree_sizes)

#         current_y = y - total_width * scale_factor * y_scale_factor / 2
            
#         for key, value in node.items():
#             subtree_width, subtree_height = calculate_tree_size(value, dict_padding)
#             endpoint_y = current_y + subtree_width * scale_factor * y_scale_factor / 2
#             endpoint_x = x + max_height * scale_factor + x_dim * scale_factor * x_scale_factor
            
#             if node_active and key in active_nodes:
#                 node_color = consts.COLORS["pink"]
#                 active = True
#             else:
#                 node_color = consts.COLORS["hover"]
#                 active = False

#             pygame.draw.line(consts.SCREEN, node_color, (x, y), (endpoint_x, endpoint_y), line_width)

#             # text, rect = consts.SCOREFONT.render(scoreString, (255, 255, 255))
#             # consts.SCOREFONT.render_to(consts.SCREEN, ((consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0])/2 + consts.FIELD_SIZE["wall"][0] - rect.width / 2, consts.YOFFSET + consts.FACTOR*4),str(scoreString), (255, 255, 255))
    
#             text_surface, text_rect = consts.SMALLFONT.render(key, node_color)
#             # text_rect = text_surface.get_rect(center=(endpoint_x, endpoint_y - 10 * scale_factor + 5*line_width))
#             consts.SMALLFONT.render_to(consts.SCREEN, (endpoint_x-(text_rect.width/2), endpoint_y - 10 * scale_factor + 5*line_width), str(key), node_color)
    
#             # consts.SCREEN.blit(text_surface, text_rect)

#             draw_json_tree(value, current_y + subtree_width * scale_factor * y_scale_factor / 2, x + max_height * scale_factor + x_dim * scale_factor, scale_factor, x_scale_factor, y_scale_factor, x_dim, y_dim, dict_padding, node_color, active_nodes, active, line_width, elements)
#             current_y += subtree_width * scale_factor * y_scale_factor + dict_padding * scale_factor

    # elif isinstance(node, list) and elements:
    #     current_x = x
    #     for item in node:
    #         node_color = consts.COLORS["hover"]
    #         if node_active:
    #             node_color = consts.COLORS["pink"]
                
    #         text_surface, text_rect = consts.SMALLFONT.render(str(item), node_color)
    #         consts.SMALLFONT.render_to(consts.SCREEN, (x-(text_rect.width/2), current_y + 50 * scale_factor), str(item), node_color)
            
    #         current_x += 30 * scale_factor



############################ VERTICALLY #################################

# Function to recursively draw the JSON tree
def draw_json_tree(node, x, y, scale_factor, x_scale_factor, y_scale_factor, x_dim, y_dim, dict_padding, parent_color, active_nodes, node_active, line_width, elements):
    if isinstance(node, dict):
        subtree_sizes = [calculate_tree_size(value, dict_padding) for value in node.values()]
        total_width = sum(size[0] for size in subtree_sizes) + dict_padding * (len(subtree_sizes) - 1)
        max_height = max(size[1] for size in subtree_sizes)

        current_x = x - total_width * scale_factor * x_scale_factor / 2
            
        for key, value in node.items():
            subtree_width, subtree_height = calculate_tree_size(value, dict_padding)
            endpoint_x = current_x + subtree_width * scale_factor * x_scale_factor / 2
            endpoint_y = y + max_height * scale_factor + y_dim * scale_factor * y_scale_factor
            
            if node_active and key in active_nodes:
                node_color = consts.COLORS["pink"]
                active = True
            else:
                node_color = consts.COLORS["hover"]
                active = False

            pygame.draw.line(consts.SCREEN, node_color, (x, y), (endpoint_x, endpoint_y), line_width)

            # text, rect = consts.SCOREFONT.render(scoreString, (255, 255, 255))
            # consts.SCOREFONT.render_to(consts.SCREEN, ((consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0])/2 + consts.FIELD_SIZE["wall"][0] - rect.width / 2, consts.YOFFSET + consts.FACTOR*4),str(scoreString), (255, 255, 255))
    
            text_surface, text_rect = consts.SSMALLFONT.render(key, node_color)
            # text_rect = text_surface.get_rect(center=(endpoint_x, endpoint_y - 10 * scale_factor + 5*line_width))
            consts.SSMALLFONT.render_to(consts.SCREEN, (endpoint_x-(text_rect.width/2), endpoint_y - 10 * scale_factor + 5*line_width), str(key), node_color)
    
            # consts.SCREEN.blit(text_surface, text_rect)

            draw_json_tree(value, current_x + subtree_width * scale_factor * x_scale_factor / 2, y + max_height * scale_factor + y_dim * scale_factor, scale_factor, x_scale_factor, y_scale_factor, x_dim, y_dim, dict_padding, node_color, active_nodes, active, line_width, elements)
            current_x += subtree_width * scale_factor * x_scale_factor + dict_padding * scale_factor

    elif isinstance(node, list) and elements:
        current_y = y
        for item in node:
            node_color = consts.COLORS["hover"]
            if node_active:
                node_color = consts.COLORS["pink"]
                
            text_surface, text_rect = consts.SSMALLFONT.render(str(item), node_color)
            consts.SSMALLFONT.render_to(consts.SCREEN, (x-(text_rect.width/2), current_y + 50 * scale_factor), str(item), node_color)
            
            current_y += 30 * scale_factor

def drawTree(json_dict, active_nodes, window_width, window_height, scale_factor_X, scale_factor_Y, X, Y, line, x_dim = 20, y_dim = -160, elements = True, name = "Player Decision Tree"):
    text_surf, text_rect = consts.SCOREFONT2.render(name, (255, 255, 255))
    consts.SCOREFONT2.render_to(consts.SCREEN, (X-(text_rect.width/2), Y - 50 * scale_factor_Y + 5*line), str(name), (255, 255, 255))
    
    tree_width, tree_height = calculate_tree_size(json_dict, 30)
    scale_factor = min(window_width / tree_width, window_height / tree_height, 1.0)
    scaled_tree = scale_tree(json_dict, scale_factor)
    draw_json_tree(scaled_tree, X, Y, scale_factor, scale_factor_X, scale_factor_Y, x_dim, y_dim, 30, consts.COLORS["white"], active_nodes, True, line, elements)


# Main game loop
if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(BLACK)
        active_nodes = []
        active_nodes = ["!Ball", "!CanShoot", "!CanGoal", "!CanPass", "knownBall", "free"]
        drawTree(data, active_nodes, 800, 600, 1, 1, 400, 50, 3, 0, 0)
        
        pygame.display.flip()
        time.sleep(1000)

    pygame.quit()
