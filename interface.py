# interface.py
import os
import pygame
import time

def animate_text_zoom(screen, base_text, position, start_size, target_size, duration=300, background=None, current_img=None, image_offset=0):
    """Animate overlay text zooming from a small size to target size."""
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(start_size + (target_size - start_size) * progress)
        font = pygame.font.SysFont(None, current_size)
        text_surface = font.render(base_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=position)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (image_offset, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def animate_logo_zoom(screen, logo, rect, base_size, target_size, duration=300, background=None, current_img=None):
    """Animate one logo zooming from base_size to target_size and back."""
    clock = pygame.time.Clock()
    center = rect.center
    # Expand
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(base_size + (target_size - base_size) * progress)
        scaled_img = pygame.transform.scale(logo, (current_size, current_size))
        new_rect = scaled_img.get_rect(center=center)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)
    # Contract back
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(target_size - (target_size - base_size) * progress)
        scaled_img = pygame.transform.scale(logo, (current_size, current_size))
        new_rect = scaled_img.get_rect(center=center)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def animate_logo_click(screen, logo, rect, base_size, target_size, duration=150, background=None, current_img=None, screen_size=(720, 720)):
    """Animate a logo click (pop effect): grow from base_size to target_size then shrink back."""
    clock = pygame.time.Clock()
    center = rect.center
    # Expand
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(base_size + (target_size - base_size) * progress)
        scaled_img = pygame.transform.scale(logo, (current_size, current_size))
        new_rect = scaled_img.get_rect(center=center)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (current_img.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)
    # Shrink back
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(target_size - (target_size - base_size) * progress)
        scaled_img = pygame.transform.scale(logo, (current_size, current_size))
        new_rect = scaled_img.get_rect(center=center)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (current_img.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))))
        screen.blit(scaled_img, new_rect)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def animate_both_logos_zoom(screen, single_logo, double_logo, single_rect, double_rect, base_size, target_size, duration=300, background=None, current_img=None):
    """Animate both logos zooming in together and then shrinking back."""
    clock = pygame.time.Clock()
    center_single = single_rect.center
    center_double = double_rect.center
    # Expand
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(base_size + (target_size - base_size) * progress)
        scaled_single = pygame.transform.scale(single_logo, (current_size, current_size))
        scaled_double = pygame.transform.scale(double_logo, (current_size, current_size))
        new_rect_single = scaled_single.get_rect(center=center_single)
        new_rect_double = scaled_double.get_rect(center=center_double)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_single, new_rect_single)
        screen.blit(scaled_double, new_rect_double)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)
    # Contract
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1.0)
        current_size = int(target_size - (target_size - base_size) * progress)
        scaled_single = pygame.transform.scale(single_logo, (current_size, current_size))
        scaled_double = pygame.transform.scale(double_logo, (current_size, current_size))
        new_rect_single = scaled_single.get_rect(center=center_single)
        new_rect_double = scaled_double.get_rect(center=center_double)
        if background:
            screen.blit(background, (0, 0))
        if current_img:
            screen.blit(current_img, (0, 0))
        screen.blit(scaled_single, new_rect_single)
        screen.blit(scaled_double, new_rect_double)
        pygame.display.flip()
        if progress >= 1.0:
            break
        clock.tick(60)

def show_pouring_and_loading(screen, pouring_img, loading_img, duration_sec, background=None):
    """Overlay pouring_img full screen and a spinning loading_img (720x720) drawn underneath."""
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    angle = 0
    screen_size = screen.get_size()
    screen_width, screen_height = screen_size
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        if elapsed >= duration_sec * 1000:
            break
        angle = (angle + 5) % 360
        rotated_loading = pygame.transform.rotate(loading_img, angle)
        rotated_rect = rotated_loading.get_rect(center=(screen_width // 2, screen_height // 2))
        if background:
            screen.blit(background, (0, 0))
        # Draw loading image first (under)
        screen.blit(rotated_loading, rotated_rect)
        # Then draw pouring image on top
        screen.blit(pouring_img, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def run_interface():
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    screen_size = screen.get_size()
    screen_width, screen_height = screen_size
    pygame.display.set_caption("Cocktail Swipe")

    # Load the static background image (tipsy.png)
    try:
        background = pygame.image.load("./tipsy.png")
        background = pygame.transform.scale(background, screen_size)
    except Exception as e:
        print("Error loading background image (tipsy.png):", e)
        background = None

    # Load main swipe images (drink logos)
    def get_images():
        imgs = []
        filenames = sorted([f for f in os.listdir("drink_logos") if f.lower().endswith('.png')])
        for f in filenames:
            path = os.path.join("drink_logos", f)
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (screen_size[0] // 1.5, screen_size[1] // 1.5))
                imgs.append((img, f))
            except Exception as e:
                print(f"Error loading {path}: {e}")
        return imgs

    images = get_images()
    if not images:
        print("No cocktail logos found in drink_logos")
        pygame.quit()
        return

    current_index = 0
    current_img, current_filename = images[current_index]

    def write_selection(filename):
        safe_name = os.path.splitext(filename)[0]
        with open("selected_cocktail.txt", "w") as f:
            f.write(safe_name)

    write_selection(current_filename)

    # Load extra logos and scale them to 75% of original (base size: 150x150)
    try:
        single_logo = pygame.image.load("single.png")
        single_logo = pygame.transform.scale(single_logo, (150, 150))
    except Exception as e:
        print("Error loading single.png:", e)
        single_logo = None
    try:
        double_logo = pygame.image.load("double.png")
        double_logo = pygame.transform.scale(double_logo, (150, 150))
    except Exception as e:
        print("Error loading double.png:", e)
        double_logo = None

    # Position extra logos: single on left, double on right, spaced more toward edges.
    margin = 50  # adjust as needed for spacing
    single_rect = pygame.Rect(margin, (screen_height - 150) // 2, 150, 150)
    double_rect = pygame.Rect(screen_width - margin - 150, (screen_height - 150) // 2, 150, 150)

    dragging = False
    drag_start_x = 0
    drag_offset = 0
    clock = pygame.time.Clock()

    normal_text_size = 72  
    text_position = (screen_width // 2, int(screen_height * 0.85))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                drag_start_x = event.pos[0]
            if event.type == pygame.MOUSEMOTION and dragging:
                current_x = event.pos[0]
                drag_offset = current_x - drag_start_x
            if event.type == pygame.MOUSEBUTTONUP and dragging:
                # If it's a click (minimal drag), check extra logos.
                if abs(drag_offset) < 10:
                    pos = event.pos
                    if single_rect.collidepoint(pos):
                        # Animate single logo click
                        if single_logo:
                            animate_logo_click(screen, single_logo, single_rect, base_size=150, target_size=220, duration=150, background=background, current_img=current_img, screen_size=screen_size)
                        # Write mode selection "single"
                        with open("selected_mode.txt", "w") as f:
                            f.write("single")
                        try:
                            pouring_img = pygame.image.load("pouring.png")
                            pouring_img = pygame.transform.scale(pouring_img, screen_size)
                        except Exception as e:
                            print("Error loading pouring.png:", e)
                            pouring_img = None
                        try:
                            loading_img = pygame.image.load("loading.png")
                            loading_img = pygame.transform.scale(loading_img, (720,720))
                        except Exception as e:
                            print("Error loading loading.png:", e)
                            loading_img = None
                        if pouring_img and loading_img:
                            show_pouring_and_loading(screen, pouring_img, loading_img, duration_sec=10, background=background)
                    elif double_rect.collidepoint(pos):
                        # Animate double logo click
                        if double_logo:
                            animate_logo_click(screen, double_logo, double_rect, base_size=150, target_size=220, duration=150, background=background, current_img=current_img, screen_size=screen_size)
                        # Write mode selection "double"
                        with open("selected_mode.txt", "w") as f:
                            f.write("double")
                        try:
                            pouring_img = pygame.image.load("pouring.png")
                            pouring_img = pygame.transform.scale(pouring_img, screen_size)
                        except Exception as e:
                            print("Error loading pouring.png:", e)
                            pouring_img = None
                        try:
                            loading_img = pygame.image.load("loading.png")
                            loading_img = pygame.transform.scale(loading_img, (720,720))
                        except Exception as e:
                            print("Error loading loading.png:", e)
                            loading_img = None
                        if pouring_img and loading_img:
                            show_pouring_and_loading(screen, pouring_img, loading_img, duration_sec=30, background=background)
                    dragging = False
                    drag_offset = 0
                    continue  # Skip further swipe handling.
                # Otherwise, it's a swipe.
                if abs(drag_offset) > screen_width / 2:
                    if drag_offset < 0:
                        target_offset = -screen_width
                        new_index = (current_index + 1) % len(images)
                    else:
                        target_offset = screen_width
                        new_index = (current_index - 1) % len(images)
                    start_offset = drag_offset
                    duration = 300
                    start_time = pygame.time.get_ticks()
                    while True:
                        elapsed = pygame.time.get_ticks() - start_time
                        progress = min(elapsed / duration, 1.0)
                        current_offset = start_offset + (target_offset - start_offset) * progress
                        if background:
                            screen.blit(background, (0, 0))
                        else:
                            screen.fill((0, 0, 0))
                        screen.blit(current_img, (current_img.get_rect(center=(screen_size[0] // 2 + current_offset, screen_size[1] // 2))))
                        if drag_offset < 0:
                            next_img, _ = images[(current_index + 1) % len(images)]
                            screen.blit(next_img, (current_img.get_rect(center=(screen_size[0] // 2 + current_offset + screen_width / 1.5, screen_size[1] // 2))))
                        else:
                            prev_img, _ = images[(current_index - 1) % len(images)]
                            screen.blit(prev_img, (current_img.get_rect(center=(screen_size[0] // 2 + current_offset - screen_width / 1.5, screen_size[1] // 2))))
                        # Draw overlay text at normal size.
                        font = pygame.font.SysFont(None, normal_text_size)
                        drink_name = os.path.splitext(current_filename)[0].replace('_', ' ').title()
                        text_surface = font.render(drink_name, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=text_position)
                        screen.blit(text_surface, text_rect)
                        # Draw extra logos at their current (base) size.
                        if single_logo:
                            screen.blit(single_logo, single_rect)
                        if double_logo:
                            screen.blit(double_logo, double_rect)
                        pygame.display.flip()
                        if progress >= 1.0:
                            break
                        clock.tick(60)
                    current_index = new_index
                    current_img, current_filename = images[current_index]
                    write_selection(current_filename)
                    # Animate both extra logos zooming together. NO STUDIP ANIMATION -tater
                    #if single_logo and double_logo:
                        #animate_both_logos_zoom(screen, single_logo, double_logo, single_rect, double_rect, base_size=150, target_size=175, duration=300, background=background, current_img=current_img)
                else:
                    # Animate snapping back if swipe is insufficient.
                    start_offset = drag_offset
                    duration = 300
                    start_time = pygame.time.get_ticks()
                    while True:
                        elapsed = pygame.time.get_ticks() - start_time
                        progress = min(elapsed / duration, 1.0)
                        current_offset = start_offset * (1 - progress)
                        if background:
                            screen.blit(background, (0, 0))
                        else:
                            screen.fill((0, 0, 0))
                        screen.blit(current_img, (current_img.get_rect(center=(screen_size[0] // 2 + current_offset, screen_size[1] // 2))))
                        font = pygame.font.SysFont(None, normal_text_size)
                        drink_name = os.path.splitext(current_filename)[0].replace('_', ' ').title()
                        text_surface = font.render(drink_name, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=text_position)
                        screen.blit(text_surface, text_rect)
                        # Draw extra logos.
                        if single_logo:
                            screen.blit(single_logo, single_rect)
                        if double_logo:
                            screen.blit(double_logo, double_rect)
                        pygame.display.flip()
                        if progress >= 1.0:
                            break
                        clock.tick(60)
                dragging = False
                drag_offset = 0

        # Main drawing (when not in special animation)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))
        if dragging:
            screen.blit(current_img, (current_img.get_rect(center=(screen_size[0] // 2 + drag_offset, screen_size[1] // 2))))
            if drag_offset < 0:
                next_img, _ = images[(current_index + 1) % len(images)]
                screen.blit(next_img, (current_img.get_rect(center=(screen_size[0] // 2 + drag_offset + screen_width / 1.5, screen_size[1] // 2))))
            elif drag_offset > 0:
                prev_img, _ = images[(current_index - 1) % len(images)]
                screen.blit(prev_img, (current_img.get_rect(center=(screen_size[0] // 2 + drag_offset - screen_width / 1.5, screen_size[1] // 2))))
        else:
            screen.blit(current_img, (current_img.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))))
        font = pygame.font.SysFont(None, normal_text_size)
        drink_name = os.path.splitext(current_filename)[0].replace('_', ' ').title()
        text_surface = font.render(drink_name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=text_position)
        screen.blit(text_surface, text_rect)
        # Draw extra logos at their base size.
        if single_logo:
            screen.blit(single_logo, single_rect)
        if double_logo:
            screen.blit(double_logo, double_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_interface()
